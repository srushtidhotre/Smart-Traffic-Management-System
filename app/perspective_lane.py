import cv2
import numpy as np


class PerspectiveLaneAnalyzer:

    def __init__(
        self,
        transformer,
        lane_polygons
    ):

        self.transformer = (
            transformer
        )

        self.lane_polygons = (
            lane_polygons
        )


    # ========================================================
    # GET LANE
    # ========================================================

    def get_lane(
        self,
        x,
        y
    ):

        # Transform original point
        # into bird's-eye coordinates

        transformed_x, transformed_y = (
            self.transformer.transform_point(
                x,
                y
            )
        )


        point = (
            transformed_x,
            transformed_y
        )


        # Check each polygon

        for lane_number, polygon in (
            self.lane_polygons.items()
        ):

            polygon_array = np.array(
                polygon,
                dtype=np.int32
            )


            inside = cv2.pointPolygonTest(
                polygon_array,
                point,
                False
            )


            if inside >= 0:

                return lane_number


        return 0


    # ========================================================
    # ANALYZE
    # ========================================================

    def analyze(
        self,
        tracks
    ):

        lane_data = {}


        for lane_number in (
            self.lane_polygons
        ):

            lane_data[
                lane_number
            ] = {

                "vehicle_count": 0,

                "vehicle_ids": [],

                "density": "LOW"

            }


        # ====================================================
        # PROCESS VEHICLES
        # ====================================================

        for track in tracks:

            x1, y1, x2, y2 = (
                track["bbox"]
            )


            center_x = int(
                (x1 + x2) / 2
            )

            center_y = int(
                (y1 + y2) / 2
            )


            lane = self.get_lane(
                center_x,
                center_y
            )


            if lane == 0:

                continue


            track[
                "lane"
            ] = lane


            lane_data[
                lane
            ][
                "vehicle_count"
            ] += 1


            lane_data[
                lane
            ][
                "vehicle_ids"
            ].append(
                track[
                    "track_id"
                ]
            )


        # ====================================================
        # DENSITY CLASSIFICATION
        # ====================================================

        for lane_number in (
            lane_data
        ):

            count = lane_data[
                lane_number
            ][
                "vehicle_count"
            ]


            if count >= 10:

                lane_data[
                    lane_number
                ][
                    "density"
                ] = "HIGH"


            elif count >= 5:

                lane_data[
                    lane_number
                ][
                    "density"
                ] = "MEDIUM"


            else:

                lane_data[
                    lane_number
                ][
                    "density"
                ] = "LOW"


        return lane_data