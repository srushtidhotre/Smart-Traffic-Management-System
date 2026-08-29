import cv2
import numpy as np


class PerspectiveTransformer:
    """
    Converts a road image from camera perspective
    into a bird's-eye / top-down view.
    """

    def __init__(
        self,
        source_points,
        destination_width=900,
        destination_height=600
    ):

        self.source_points = np.float32(
            source_points
        )

        self.destination_width = (
            destination_width
        )

        self.destination_height = (
            destination_height
        )

        self.destination_points = np.float32([
            [0, 0],
            [destination_width, 0],
            [destination_width, destination_height],
            [0, destination_height]
        ])

        self.matrix = cv2.getPerspectiveTransform(
            self.source_points,
            self.destination_points
        )

    # ========================================================
    # TRANSFORM FRAME
    # ========================================================

    def transform_frame(self, frame):

        return cv2.warpPerspective(
            frame,
            self.matrix,
            (
                self.destination_width,
                self.destination_height
            )
        )

    # ========================================================
    # TRANSFORM POINT
    # ========================================================

    def transform_point(
        self,
        x,
        y
    ):

        point = np.float32([
            [[x, y]]
        ])

        transformed = cv2.perspectiveTransform(
            point,
            self.matrix
        )

        tx, ty = transformed[0][0]

        return int(tx), int(ty)