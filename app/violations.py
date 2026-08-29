# ============================================================
# Traffic Violation Detection
# ============================================================

class TrafficViolationDetector:

    def __init__(self):
        self.violations = []
        self.stop_frames = {}
        self.last_violation = {}

    # ========================================================
    # CLEAR PREVIOUS VIOLATIONS
    # ========================================================

    def clear_violations(self):
        self.violations.clear()
        self.stop_frames.clear()
        self.last_violation.clear()

    # ========================================================
    # WRONG-WAY DETECTION
    # ========================================================

    def detect_wrong_way(
        self,
        previous_position,
        current_position,
        expected_direction="forward"
    ):
        if previous_position is None:
            return False

        previous_x, previous_y = previous_position
        current_x, current_y = current_position

        movement_y = current_y - previous_y

        # Vehicle expected to move upward
        if expected_direction == "forward":
            return movement_y < -2

        # Vehicle expected to move downward
        if expected_direction == "backward":
            return movement_y > 2

        return False

    # ========================================================
    # STOPPED VEHICLE DETECTION
    # ========================================================

    def detect_stopped_vehicle(
        self,
        track_id,
        speed,
        frame_number,
        threshold=2.0,
        minimum_frames=30
    ):
        # Count consecutive low-speed frames
        if speed <= threshold:
            self.stop_frames[track_id] = (
                self.stop_frames.get(track_id, 0) + 1
            )
        else:
            self.stop_frames[track_id] = 0

        stopped_frames = self.stop_frames.get(
            track_id,
            0
        )

        return stopped_frames >= minimum_frames

    # ========================================================
    # RECORD VIOLATION
    # ========================================================

    def record_violation(
        self,
        track_id,
        violation_type,
        frame_number,
        description=""
    ):
        violation_key = (
            track_id,
            violation_type
        )

        # Prevent repeated records for the same vehicle
        last_frame = self.last_violation.get(
            violation_key,
            -9999
        )

        # Minimum gap between duplicate violations
        if frame_number - last_frame < 30:
            return

        violation = {
            "track_id": track_id,
            "type": violation_type,
            "frame": frame_number,
            "description": description
        }

        self.violations.append(
            violation
        )

        self.last_violation[
            violation_key
        ] = frame_number

    # ========================================================
    # GET ALL VIOLATIONS
    # ========================================================

    def get_violations(self):
        return self.violations

    # ========================================================
    # GET VIOLATION COUNT
    # ========================================================

    def get_violation_count(self):
        return len(
            self.violations
        )

    # ========================================================
    # GET VIOLATIONS BY TYPE
    # ========================================================

    def get_violations_by_type(
        self,
        violation_type
    ):
        return [
            violation
            for violation in self.violations
            if violation["type"] == violation_type
        ]