from ultralytics import YOLO

from app.config import (MODEL_PATH,
                        CONFIDENCE_THRESHOLD,
                        IMAGE_SIZE,
                        VEHICLE_CLASSES)

# ============================================================
# LOAD YOLO MODEL
# ============================================================

model = YOLO(str(MODEL_PATH))

# ============================================================
# VEHICLE DETECTION FUNCTION
# ============================================================

def detect_vehicles(frame):
    """
    Detect vehicles in a single video frame.

    Parameters
    ----------
    frame : numpy.ndarray
        Input video frame.

    Returns
    -------
    detections : list
        List containing detected vehicle information.
    """

    results = model(frame,
                    imgsz=IMAGE_SIZE,
                    conf=CONFIDENCE_THRESHOLD,
                    verbose=False)

    detections = []

    for result in results:

        if result.boxes is None:
            continue

        for box in result.boxes:

            # Bounding box coordinates
            x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())

            # Confidence
            confidence = float(box.conf[0])

            # Class ID
            class_id = int(box.cls[0])

            # Class name
            class_name = model.names[class_id]

            # Keep only vehicles
            if class_name not in VEHICLE_CLASSES:
                continue

            detection = {"class_id": class_id,
                         "class_name": class_name,
                         "confidence": confidence,
                         "bbox": (x1, y1, x2, y2)
                         }

            detections.append(detection)

    return detections