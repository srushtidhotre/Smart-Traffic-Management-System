from collections import defaultdict

class VehicleCounter:
    """
    Vehicle counting system based on tracking IDs.

    The counter maintains vehicle identities across frames
    and records vehicles that cross a predefined counting line.
    """

    def __init__(self, line_position=0.60):

        # Position of counting line as a percentage
        # of the frame height.
        #
        # Example:
        # 0.60 = 60% down the frame

        self.line_position = line_position

        # IDs of all vehicles observed
        self.seen_ids = set()

        # IDs that have already crossed the line
        self.counted_ids = set()

        # Vehicle type associated with each tracking ID
        self.vehicle_types = {}

        # Previous center position of each vehicle
        self.previous_positions = {}

        # Total crossing count
        self.total_count = 0

        # Count by vehicle type
        self.type_counts = defaultdict(int)

    # ========================================================
    # UPDATE COUNTER
    # ========================================================

    def update(self, tracks, frame_height):
        """
        Update vehicle counts using current tracking results.

        Parameters
        ----------
        tracks : list
            Tracking results from tracker.py.

        frame_height : int
            Height of current video frame.

        Returns
        -------
        count_data : dict
            Current counting statistics.
        """

        line_y = int(frame_height * self.line_position)

        for track in tracks:
            track_id = track["track_id"]
            vehicle_type = track["class_name"]
            x1, y1, x2, y2 = track["bbox"]

            # ------------------------------------------------
            # Calculate vehicle center
            # ------------------------------------------------

            center_x = int((x1 + x2) / 2)
            center_y = int((y1 + y2) / 2)

            current_position = (center_x, center_y)

            # ------------------------------------------------
            # Register vehicle
            # ------------------------------------------------

            self.seen_ids.add(track_id)
            self.vehicle_types[track_id] = vehicle_type

            # ------------------------------------------------
            # Check whether vehicle crossed counting line
            # ------------------------------------------------

            if track_id in self.previous_positions:

                previous_x, previous_y = (self.previous_positions[track_id])

                # Vehicle moving downward across line
                crossed_downward = (previous_y < line_y
                                    and 
                                    center_y >= line_y)

                # Vehicle moving upward across line
                crossed_upward = (previous_y > line_y
                                  and 
                                  center_y <= line_y)

                crossed_line = (crossed_downward or crossed_upward)

                if (crossed_line
                    and 
                    track_id not in self.counted_ids):
                    self.counted_ids.add(track_id)
                    self.total_count += 1
                    self.type_counts[vehicle_type] += 1

            # ------------------------------------------------
            # Store current position
            # ------------------------------------------------

            self.previous_positions[track_id] = current_position

        # ====================================================
        # RETURN STATISTICS
        # ====================================================

        return {
            "current_vehicles": len(tracks),
            "unique_vehicles": len(self.seen_ids),
            "counted_vehicles": self.total_count,
            "car_count": self.type_counts["car"],
            "bus_count": self.type_counts["bus"],
            "truck_count": self.type_counts["truck"],
            "motorcycle_count": (self.type_counts["motorcycle"]),
            "line_y": line_y
        }