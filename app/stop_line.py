import cv2


class StopLineDetector:

    def __init__(self, y_position=400):
        self.y_position = y_position

    # Check whether vehicle crossed stop line
    def crossed_line(
        self,
        previous_y,
        current_y
    ):

        if previous_y is None:
            return False

        return (
            previous_y < self.y_position
            and current_y >= self.y_position
        )

    # Draw stop line
    def draw_line(self, frame):

        height, width = frame.shape[:2]

        cv2.line(
            frame,
            (0, self.y_position),
            (width, self.y_position),
            (0, 0, 255),
            3
        )

        cv2.putText(
            frame,
            "STOP LINE",
            (20, self.y_position - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 0, 255),
            2
        )

        return frame