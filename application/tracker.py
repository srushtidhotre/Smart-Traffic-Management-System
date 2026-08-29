from ultralytics import YOLO

from app.config import (MODEL_PATH,
                        CONFIDENCE_THRESHOLD,
                        IMAGE_SIZE,
                        VEHICLE_CLASSES,
                        TRACKER)


# ============================================================
# LOAD YOLO MODEL
# ============================================================

model = YOLO(str(MODEL_PATH))

# ============================================================
# TRACK VEHICLES
# ============================================================

def track_vehicles(frame):
    """
    Detect and track vehicles in a video frame.

    ByteTrack assigns a unique ID to vehicles and attempts
    to maintain that ID across consecutive frames.

    Parameters
    ----------
    frame : numpy.ndarray
        Input video frame.

    Returns
    -------
    tracks : list
        List containing tracked vehicle information.
    """

    results = model.track(source=frame,
                          persist=True,
                          tracker=TRACKER,
                          imgsz=IMAGE_SIZE,
                          conf=CONFIDENCE_THRESHOLD,
                          verbose=False
                          )

    tracks = []

    if not results:
        return tracks

    result = results[0]

    if result.boxes is None:
        return tracks

    boxes = result.boxes

    # Tracking IDs may not be available in every frame
    if boxes.id is None:
        return tracks

    track_ids = boxes.id.int().cpu().tolist()
    class_ids = boxes.cls.int().cpu().tolist()
    confidences = boxes.conf.cpu().tolist()
    coordinates = boxes.xyxy.int().cpu().tolist()

    for track_id, class_id, confidence, bbox in zip(track_ids,
                                                    class_ids,
                                                    confidences,
                                                    coordinates  ):

        class_name = model.names[class_id]

        # Keep only vehicles
        if class_name not in VEHICLE_CLASSES:
            continue

        x1, y1, x2, y2 = bbox

        tracks.append({
                        "track_id": int(track_id),
                        "class_id": int(class_id),
                        "class_name": class_name,
                        "confidence": float(confidence),
                        "bbox": (x1, y1, x2, y2)
                       })

    return tracks