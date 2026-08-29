import math
from collections import defaultdict

class TrafficAnalytics:
    """
    Advanced traffic analytics module.

    Calculates:
    - Vehicle speed
    - Traffic flow
    - Queue length
    - Congestion score
    """

    def __init__(self,
                 fps=30,
                 pixels_per_meter=10 ):

        self.fps = fps
        self.pixels_per_meter = pixels_per_meter

        # Store previous vehicle positions
        self.previous_positions = {}

        # Count vehicles passing through lanes
        self.lane_flow = defaultdict(set)

    # ========================================================
    # SPEED ESTIMATION
    # ========================================================

    def calculate_speed(self,
                        track_id,
                        center_x,
                        center_y ):
        """
        Estimate vehicle speed using movement
        between consecutive frames.

        NOTE:
        This is an approximate speed unless the camera
        is calibrated with real-world measurements.
        """

        current_position = (center_x, center_y)

        if track_id not in self.previous_positions:
            self.previous_positions[track_id] = current_position
            return 0.0

        previous_x, previous_y = (self.previous_positions[track_id])

        # Pixel displacement
        pixel_distance = math.sqrt(
                                    (center_x - previous_x) ** 2
                                    +
                                    (center_y - previous_y) ** 2 )

        # Convert pixels → meters
        distance_meters = (pixel_distance/self.pixels_per_meter)

        # Time between frames
        time_seconds = ( 1 / self.fps)

        if time_seconds <= 0:
            return 0.0

        # m/s → km/h
        speed_kmh = (distance_meters/time_seconds * 3.6 )

        self.previous_positions[track_id] = current_position

        return round(speed_kmh, 2)

    # ========================================================
    # TRAFFIC FLOW
    # ========================================================

    def calculate_flow(self, tracks):
        """
        Calculate approximate traffic flow.

        Flow = number of unique vehicles
        observed during the analysis period.
        """

        for track in tracks:
            track_id = track["track_id"]
            lane = track.get("lane", 0)
            self.lane_flow[lane].add(track_id)

        flow = {}

        for lane, vehicle_ids in (self.lane_flow.items()):
            flow[lane] = len(vehicle_ids)

        return flow

    # ========================================================
    # QUEUE ESTIMATION
    # ========================================================

    def estimate_queue(self,
                       tracks,
                       speed_threshold=8 ):
        """
        Estimate queue length using slowly moving
        or stationary vehicles.

        Vehicles below speed_threshold are treated
        as part of a potential queue.
        """

        queue = defaultdict(int)

        for track in tracks:
            lane = track.get("lane", 0)
            speed = track.get("speed", 0)

            if speed <= speed_threshold:
                queue[lane] += 1

        return dict(queue)

    # ========================================================
    # CONGESTION SCORE
    # ========================================================

    @staticmethod
    def calculate_congestion_score(vehicle_count,
                                   queue_count,
                                   average_speed,
                                   max_vehicles=20 ):
        """
        Calculate a combined congestion score.

        Score:
        0   → Free flowing
        100 → Severe congestion
        """

        # ---------------------------------------------
        # Vehicle density component
        # ---------------------------------------------

        vehicle_component = min(vehicle_count/max_vehicles, 1.0) * 40

        # ---------------------------------------------
        # Queue component
        # ---------------------------------------------

        queue_component = min(queue_count/max_vehicles, 1.0) * 35

        # ---------------------------------------------
        # Speed component
        # ---------------------------------------------

        speed_component = max(0,
                              25-min(average_speed,25))

        score = (vehicle_component 
                 + queue_component
                 + speed_component)

        return round(min(score, 100), 2)

    # ========================================================
    # CONGESTION LEVEL
    # ========================================================

    @staticmethod
    def get_congestion_level(score):

        if score >= 75:
            return "SEVERE"

        elif score >= 50:
            return "HIGH"

        elif score >= 25:
            return "MEDIUM"

        else:
            return "LOW"