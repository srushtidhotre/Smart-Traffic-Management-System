import cv2
import streamlit as st
import pandas as pd
import numpy as np

from app.config import DEFAULT_VIDEO
from app.tracker import track_vehicles
from app.lane import PerspectiveLaneAnalyzer
from app.density import TrafficDensityAnalyzer
from app.signal_controller import AdaptiveSignalController
from app.analytics import TrafficAnalytics
from app.violations import TrafficViolationDetector


# ============================================================
# Page Configuration
# ============================================================

st.set_page_config(
    page_title="Smart Traffic Management",
    page_icon="🚦",
    layout="wide"
)

st.title("🚦 Smart Traffic Management System")

st.markdown(
    "**AI-powered traffic monitoring, vehicle tracking, "
    "lane analysis, congestion detection and traffic violation detection**"
)


# ============================================================
# Perspective Transformation
# ============================================================

PERSPECTIVE_SOURCE_POINTS = np.float32([
    [250, 180],
    [1050, 180],
    [1250, 700],
    [50, 700]
])

BIRD_VIEW_WIDTH = 900
BIRD_VIEW_HEIGHT = 600


def create_perspective_matrix(frame_width, frame_height):
    scale_x = frame_width / 1280
    scale_y = frame_height / 720

    source_points = PERSPECTIVE_SOURCE_POINTS.copy()

    source_points[:, 0] *= scale_x
    source_points[:, 1] *= scale_y

    destination_points = np.float32([
        [0, 0],
        [BIRD_VIEW_WIDTH, 0],
        [BIRD_VIEW_WIDTH, BIRD_VIEW_HEIGHT],
        [0, BIRD_VIEW_HEIGHT]
    ])

    matrix = cv2.getPerspectiveTransform(
        source_points,
        destination_points
    )

    return matrix, source_points


def transform_point(x, y, matrix):
    point = np.array(
        [[[x, y]]],
        dtype=np.float32
    )

    transformed = cv2.perspectiveTransform(
        point,
        matrix
    )

    return (
        int(transformed[0][0][0]),
        int(transformed[0][0][1])
    )


def create_bird_view(frame, matrix):
    return cv2.warpPerspective(
        frame,
        matrix,
        (
            BIRD_VIEW_WIDTH,
            BIRD_VIEW_HEIGHT
        )
    )


# ============================================================
# Perspective Lane Analysis
# ============================================================

def get_perspective_lane(x):
    lane_width = BIRD_VIEW_WIDTH / 3

    if x < lane_width:
        return 1

    if x < 2 * lane_width:
        return 2

    return 3


def create_perspective_lane_data(tracks, matrix):
    lane_data = {
        1: {
            "vehicle_count": 0,
            "density": "LOW"
        },
        2: {
            "vehicle_count": 0,
            "density": "LOW"
        },
        3: {
            "vehicle_count": 0,
            "density": "LOW"
        }
    }

    for track in tracks:

        x1, y1, x2, y2 = track["bbox"]

        center_x = int(
            (x1 + x2) / 2
        )

        center_y = int(
            (y1 + y2) / 2
        )

        transformed_x, transformed_y = (
            transform_point(
                center_x,
                center_y,
                matrix
            )
        )

        lane_number = get_perspective_lane(
            transformed_x
        )

        track["perspective_x"] = (
            transformed_x
        )

        track["perspective_y"] = (
            transformed_y
        )

        track["lane_number"] = (
            lane_number
        )

        if (
            0 <= transformed_x < BIRD_VIEW_WIDTH
            and
            0 <= transformed_y < BIRD_VIEW_HEIGHT
        ):
            lane_data[
                lane_number
            ][
                "vehicle_count"
            ] += 1

    for lane_number in range(1, 4):

        count = lane_data[
            lane_number
        ][
            "vehicle_count"
        ]

        if count <= 3:
            density = "LOW"

        elif count <= 7:
            density = "MEDIUM"

        else:
            density = "HIGH"

        lane_data[
            lane_number
        ][
            "density"
        ] = density

    return lane_data


# ============================================================
# Draw Perspective Region
# ============================================================

def draw_perspective_region(
    frame,
    source_points
):

    points = np.array(
        source_points,
        dtype=np.int32
    )

    overlay = frame.copy()

    cv2.fillPoly(
        overlay,
        [points],
        (255, 200, 0)
    )

    frame = cv2.addWeighted(
        overlay,
        0.12,
        frame,
        0.88,
        0
    )

    cv2.polylines(
        frame,
        [points],
        True,
        (0, 255, 255),
        3
    )

    x = int(
        source_points[0][0]
    )

    y = max(
        int(source_points[0][1] - 10),
        25
    )

    cv2.putText(
        frame,
        "Perspective ROI",
        (x, y),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (0, 255, 255),
        2
    )

    return frame


# ============================================================
# Draw Bird's-Eye View Lanes
# ============================================================

def draw_bird_view_lanes(
    bird_view,
    lane_data
):

    lane_width = BIRD_VIEW_WIDTH / 3

    for lane in range(1, 3):

        x = int(
            lane * lane_width
        )

        cv2.line(
            bird_view,
            (x, 0),
            (x, BIRD_VIEW_HEIGHT),
            (0, 255, 255),
            3
        )

    for lane_number in range(1, 4):

        x_start = int(
            (lane_number - 1)
            * lane_width
        )

        x_center = int(
            x_start + lane_width / 2
        )

        count = lane_data[
            lane_number
        ][
            "vehicle_count"
        ]

        density = lane_data[
            lane_number
        ][
            "density"
        ]

        cv2.putText(
            bird_view,
            f"LANE {lane_number}",
            (x_center - 70, 45),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (255, 255, 255),
            2
        )

        cv2.putText(
            bird_view,
            f"Vehicles: {count}",
            (x_center - 80, 75),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.55,
            (255, 255, 255),
            2
        )

        cv2.putText(
            bird_view,
            f"Density: {density}",
            (x_center - 80, 100),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.55,
            (255, 255, 255),
            2
        )

    return bird_view


# ============================================================
# Draw Bird's-Eye Vehicles
# ============================================================

def draw_bird_view_vehicles(
    bird_view,
    tracks
):

    for track in tracks:

        if "perspective_x" not in track:
            continue

        x = int(
            track["perspective_x"]
        )

        y = int(
            track["perspective_y"]
        )

        if not (
            0 <= x < BIRD_VIEW_WIDTH
            and
            0 <= y < BIRD_VIEW_HEIGHT
        ):
            continue

        track_id = track["track_id"]

        lane_number = track.get(
            "lane_number",
            0
        )

        cv2.circle(
            bird_view,
            (x, y),
            8,
            (0, 0, 255),
            -1
        )

        cv2.putText(
            bird_view,
            f"ID {track_id}",
            (x + 10, y),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.45,
            (255, 255, 255),
            2
        )

        cv2.putText(
            bird_view,
            f"L{lane_number}",
            (x + 10, y + 18),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.4,
            (255, 255, 0),
            1
        )

    return bird_view


# ============================================================
# Initialize System
# ============================================================

@st.cache_resource
def initialize_system():

    # Lane polygons for PerspectiveLaneAnalyzer
    lane_polygons = {

        1: [
            (0, 200),
            (400, 200),
            (450, 720),
            (0, 720)
        ],

        2: [
            (400, 200),
            (800, 200),
            (850, 720),
            (450, 720)
        ],

        3: [
            (800, 200),
            (1280, 200),
            (1280, 720),
            (850, 720)
        ]
    }

    lane_analyzer = PerspectiveLaneAnalyzer(
        lane_polygons
    )

    density_analyzer = TrafficDensityAnalyzer()

    analytics = TrafficAnalytics(
        fps=30,
        pixels_per_meter=10
    )

    signal_controller = AdaptiveSignalController(
        minimum_green=15,
        maximum_green=60,
        yellow_time=5,
        all_red_time=2
    )

    violation_detector = TrafficViolationDetector()

    return (
        lane_analyzer,
        density_analyzer,
        analytics,
        signal_controller,
        violation_detector
    )


(
    lane_analyzer,
    density_analyzer,
    analytics,
    signal_controller,
    violation_detector
) = initialize_system()


# ============================================================
# Sidebar Controls
# ============================================================

st.sidebar.header(
    "⚙️ System Controls"
)

max_frames = st.sidebar.slider(
    "Frames to Process",
    min_value=30,
    max_value=500,
    value=150,
    step=30
)

start_analysis = st.sidebar.button(
    "▶ Start Analysis"
)


# ============================================================
# Dashboard Placeholders
# ============================================================

video_placeholder = st.empty()
bird_view_placeholder = st.empty()
metrics_placeholder = st.empty()


# ============================================================
# Main Analysis
# ============================================================

if start_analysis:

    violation_detector.clear_violations()

    cap = cv2.VideoCapture(
        str(DEFAULT_VIDEO)
    )

    if not cap.isOpened():

        st.error(
            f"Could not open video: {DEFAULT_VIDEO}"
        )

        st.stop()

    video_width = int(
        cap.get(
            cv2.CAP_PROP_FRAME_WIDTH
        )
    )

    video_height = int(
        cap.get(
            cv2.CAP_PROP_FRAME_HEIGHT
        )
    )

    video_fps = cap.get(
        cv2.CAP_PROP_FPS
    )

    if video_fps <= 0:
        video_fps = 30

    st.sidebar.success(
        "Video loaded successfully"
    )

    st.sidebar.write(
        f"Resolution: "
        f"**{video_width} × {video_height}**"
    )

    st.sidebar.write(
        f"FPS: **{video_fps:.1f}**"
    )

    perspective_matrix, source_points = (
        create_perspective_matrix(
            video_width,
            video_height
        )
    )

    progress = st.progress(0)

    records = []
    frame_number = 0
    previous_positions = {}

    while frame_number < max_frames:

        ret, frame = cap.read()

        if not ret:
            break

        frame_number += 1

        # Vehicle detection and tracking
        tracks = track_vehicles(
            frame
        )

        # Speed calculation
        speed_values = []

        for track in tracks:

            x1, y1, x2, y2 = track["bbox"]

            center_x = int(
                (x1 + x2) / 2
            )

            center_y = int(
                (y1 + y2) / 2
            )

            speed = analytics.calculate_speed(
                track["track_id"],
                center_x,
                center_y
            )

            track["speed"] = speed

            speed_values.append(
                speed
            )

        if speed_values:

            average_speed = (
                sum(speed_values)
                / len(speed_values)
            )

        else:

            average_speed = 0

        # Perspective lane analysis
        lane_data = create_perspective_lane_data(
            tracks,
            perspective_matrix
        )

        # Use the project's lane analyzer too
        detected_lane_data = lane_analyzer.analyze(
            tracks
        )

        # Traffic density
        density = density_analyzer.analyze(
            lane_data
        )

        # Queue estimation
        queue = analytics.estimate_queue(
            tracks
        )

        total_queue = sum(
            queue.values()
        )

        # Congestion score
        congestion_score = (
            analytics.calculate_congestion_score(
                len(tracks),
                total_queue,
                average_speed
            )
        )

        # Adaptive signal control
        signal_result = signal_controller.decide(
            lane_data
        )

        signal_plan = signal_result[
            "signal_plan"
        ]

        priority_lane = signal_result[
            "priority_lane"
        ]

        # ====================================================
        # Traffic Violation Detection
        # ====================================================

        for track in tracks:

            x1, y1, x2, y2 = track["bbox"]

            track_id = track["track_id"]

            speed = track.get(
                "speed",
                0
            )

            lane_number = track.get(
                "lane_number",
                0
            )

            center_x = int(
                (x1 + x2) / 2
            )

            center_y = int(
                (y1 + y2) / 2
            )

            current_position = (
                center_x,
                center_y
            )

            previous_position = (
                previous_positions.get(
                    track_id
                )
            )

            # Wrong-way detection
            wrong_way = (
                violation_detector.detect_wrong_way(
                    previous_position,
                    current_position,
                    expected_direction="forward"
                )
            )

            if wrong_way:

                violation_detector.record_violation(
                    track_id,
                    "Wrong Way",
                    frame_number,
                    "Vehicle moving against expected direction"
                )

            # Stopped vehicle detection
            stopped = (
                violation_detector.detect_stopped_vehicle(
                    track_id,
                    speed,
                    frame_number
                )
            )

            if stopped:

                violation_detector.record_violation(
                    track_id,
                    "Stopped Vehicle",
                    frame_number,
                    "Vehicle stationary for extended duration"
                )

            previous_positions[
                track_id
            ] = current_position

            track["wrong_way"] = wrong_way
            track["stopped"] = stopped

        # ====================================================
        # Draw Perspective ROI
        # ====================================================

        frame = draw_perspective_region(
            frame,
            source_points
        )

        # ====================================================
        # Draw Vehicles
        # ====================================================

        for track in tracks:

            x1, y1, x2, y2 = track["bbox"]

            track_id = track["track_id"]

            vehicle_type = track.get(
                "class_name",
                "vehicle"
            )

            lane_number = track.get(
                "lane_number",
                0
            )

            speed = track.get(
                "speed",
                0
            )

            wrong_way = track.get(
                "wrong_way",
                False
            )

            stopped = track.get(
                "stopped",
                False
            )

            if wrong_way or stopped:

                box_color = (
                    0,
                    0,
                    255
                )

            else:

                box_color = (
                    0,
                    255,
                    0
                )

            cv2.rectangle(
                frame,
                (x1, y1),
                (x2, y2),
                box_color,
                2
            )

            label = (
                f"ID {track_id} | "
                f"{vehicle_type} | "
                f"L{lane_number} | "
                f"{speed:.1f} km/h"
            )

            if wrong_way:

                label += " | WRONG WAY"

            elif stopped:

                label += " | STOPPED"

            cv2.putText(
                frame,
                label,
                (
                    x1,
                    max(
                        y1 - 8,
                        20
                    )
                ),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                box_color,
                2
            )

        # ====================================================
        # Traffic Information Panel
        # ====================================================

        total_violations = len(
            violation_detector.get_violations()
        )

        cv2.rectangle(
            frame,
            (10, 10),
            (390, 155),
            (0, 0, 0),
            -1
        )

        cv2.putText(
            frame,
            f"Vehicles: {len(tracks)}",
            (20, 35),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.65,
            (255, 255, 255),
            2
        )

        cv2.putText(
            frame,
            f"Avg Speed: {average_speed:.1f} km/h",
            (20, 65),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.65,
            (255, 255, 255),
            2
        )

        cv2.putText(
            frame,
            f"Congestion: {congestion_score:.1f}/100",
            (20, 95),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.65,
            (255, 255, 255),
            2
        )

        cv2.putText(
            frame,
            f"Violations: {total_violations}",
            (20, 125),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.65,
            (0, 0, 255),
            2
        )

        # ====================================================
        # Bird's-Eye View
        # ====================================================

        bird_view = create_bird_view(
            frame,
            perspective_matrix
        )

        bird_view = draw_bird_view_lanes(
            bird_view,
            lane_data
        )

        bird_view = draw_bird_view_vehicles(
            bird_view,
            tracks
        )

        cv2.putText(
            bird_view,
            "BIRD'S-EYE TRAFFIC VIEW",
            (20, 575),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.75,
            (255, 255, 255),
            2
        )

        # ====================================================
        # Display
        # ====================================================

        frame_rgb = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2RGB
        )

        bird_view_rgb = cv2.cvtColor(
            bird_view,
            cv2.COLOR_BGR2RGB
        )

        video_placeholder.image(
            frame_rgb,
            channels="RGB",
            use_container_width=True
        )

        bird_view_placeholder.image(
            bird_view_rgb,
            channels="RGB",
            use_container_width=True
        )

        # ====================================================
        # Live Metrics
        # ====================================================

        with metrics_placeholder.container():

            col1, col2, col3, col4 = (
                st.columns(4)
            )

            with col1:

                st.metric(
                    "🚗 Vehicles",
                    len(tracks)
                )

            with col2:

                st.metric(
                    "🏎️ Avg Speed",
                    f"{average_speed:.1f} km/h"
                )

            with col3:

                st.metric(
                    "🚧 Queue",
                    total_queue
                )

            with col4:

                st.metric(
                    "🚨 Violations",
                    total_violations
                )

            st.divider()

            st.subheader(
                "🛣️ Lane Analysis"
            )

            lane_cols = st.columns(3)

            for index, lane_number in enumerate(
                range(1, 4)
            ):

                lane = lane_data[
                    lane_number
                ]

                signal = signal_plan.get(
                    lane_number,
                    {
                        "green_time": 0,
                        "priority": False
                    }
                )

                with lane_cols[index]:

                    st.markdown(
                        f"### Lane {lane_number}"
                    )

                    st.metric(
                        "Vehicles",
                        lane[
                            "vehicle_count"
                        ]
                    )

                    st.write(
                        f"Density: "
                        f"**{lane['density']}**"
                    )

                    st.write(
                        f"Green Time: "
                        f"**{signal.get('green_time', 0)} sec**"
                    )

        # ====================================================
        # Save Analytics
        # ====================================================

        records.append({
            "Frame": frame_number,
            "Vehicles": len(tracks),
            "Average Speed": round(
                average_speed,
                2
            ),
            "Queued Vehicles": total_queue,
            "Congestion Score": round(
                congestion_score,
                2
            ),
            "Violations": total_violations,
            "Priority Lane": priority_lane,
            "Lane 1 Vehicles": lane_data[1][
                "vehicle_count"
            ],
            "Lane 2 Vehicles": lane_data[2][
                "vehicle_count"
            ],
            "Lane 3 Vehicles": lane_data[3][
                "vehicle_count"
            ]
        })

        progress.progress(
            min(
                frame_number / max_frames,
                1.0
            )
        )

    cap.release()

    progress.progress(1.0)

    # ========================================================
    # Final Results
    # ========================================================

    if records:

        df = pd.DataFrame(
            records
        )

        df.to_csv(
            "Results/dashboard_analysis.csv",
            index=False
        )

        st.divider()

        st.subheader(
            "📈 Traffic Analytics"
        )

        st.line_chart(
            df.set_index("Frame")[
                [
                    "Vehicles",
                    "Average Speed",
                    "Congestion Score",
                    "Violations"
                ]
            ]
        )

        st.subheader(
            "📋 Traffic Summary"
        )

        st.dataframe(
            df.tail(20),
            use_container_width=True
        )

        st.subheader(
            "📊 Overall Statistics"
        )

        col1, col2, col3, col4 = (
            st.columns(4)
        )

        with col1:

            st.metric(
                "Total Frames",
                len(df)
            )

        with col2:

            st.metric(
                "Peak Vehicles",
                int(
                    df["Vehicles"].max()
                )
            )

        with col3:

            st.metric(
                "Avg Recorded Speed",
                f"{df['Average Speed'].mean():.1f} km/h"
            )

        with col4:

            st.metric(
                "Total Violations",
                int(
                    df["Violations"].max()
                )
            )

        # ====================================================
        # Violation History
        # ====================================================

        st.subheader(
            "🚨 Traffic Violation History"
        )

        violations = (
            violation_detector.get_violations()
        )

        if violations:

            violation_df = pd.DataFrame(
                violations
            )

            st.dataframe(
                violation_df,
                use_container_width=True,
                hide_index=True
            )

            violation_counts = (
                violation_df[
                    "type"
                ]
                .value_counts()
                .reset_index()
            )

            violation_counts.columns = [
                "Violation",
                "Count"
            ]

            st.subheader(
                "📊 Violation Statistics"
            )

            st.bar_chart(
                violation_counts.set_index(
                    "Violation"
                )
            )

            violation_csv = (
                violation_df.to_csv(
                    index=False
                )
            )

            st.download_button(
                "⬇️ Download Violation Report",
                violation_csv,
                "traffic_violations.csv",
                "text/csv"
            )

        else:

            st.success(
                "✅ No traffic violations detected."
            )

        # ====================================================
        # Lane Performance
        # ====================================================

        st.subheader(
            "🛣️ Lane Performance Summary"
        )

        lane_summary = pd.DataFrame({
            "Lane": [
                "Lane 1",
                "Lane 2",
                "Lane 3"
            ],
            "Average Vehicles": [
                df["Lane 1 Vehicles"].mean(),
                df["Lane 2 Vehicles"].mean(),
                df["Lane 3 Vehicles"].mean()
            ],
            "Peak Vehicles": [
                df["Lane 1 Vehicles"].max(),
                df["Lane 2 Vehicles"].max(),
                df["Lane 3 Vehicles"].max()
            ]
        })

        lane_summary[
            "Average Vehicles"
        ] = lane_summary[
            "Average Vehicles"
        ].round(2)

        st.dataframe(
            lane_summary,
            use_container_width=True,
            hide_index=True
        )

        # ====================================================
        # Export Results
        # ====================================================

        st.subheader(
            "📥 Export Results"
        )

        csv_data = df.to_csv(
            index=False
        )

        st.download_button(
            "⬇️ Download Traffic Analysis CSV",
            csv_data,
            "traffic_analysis.csv",
            "text/csv"
        )

        st.success(
            "✅ Traffic analysis completed successfully."
        )

    else:

        st.warning(
            "No traffic data was generated."
        )

else:

    st.info(
        "Select the number of frames and click "
        "**▶ Start Analysis** to begin."
    )


# ============================================================
# Footer
# ============================================================

st.divider()

st.caption(
    "Smart Traffic Management System | "
    "YOLO + Vehicle Tracking + Perspective Transformation + "
    "Traffic Analytics + Adaptive Signal Control + "
    "Violation Detection"
)