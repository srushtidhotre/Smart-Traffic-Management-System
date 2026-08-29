import cv2


class PerspectiveLaneAnalyzer:

    def __init__(
        self,
        lane_polygons
    ):

        self.lane_polygons = (
            lane_polygons
        )


    # ========================================================
    # FIND LANE
    # ========================================================

    def get_lane(
        self,
        x,
        y
    ):

        point = (
            int(x),
            int(y)
        )


        for lane_number, polygon in (
            self.lane_polygons.items()
        ):

            polygon_array = (
                __import__("numpy")
                .array(
                    polygon,
                    dtype="int32"
                )
            )


            result = cv2.pointPolygonTest(
                polygon_array,
                point,
                False
            )


            if result >= 0:

                return lane_number


        return 0


    # ========================================================
    # ANALYZE TRACKS
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


            track["lane"] = lane


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
        # DENSITY
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

                density = "HIGH"

            elif count >= 5:

                density = "MEDIUM"

            else:

                density = "LOW"


            lane_data[
                lane_number
            ][
                "density"
            ] = density


        return lane_data

# Backward compatibility
LaneAnalyzer = PerspectiveLaneAnalyzer