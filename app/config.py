from pathlib import Path

# ============================================================
# PROJECT ROOT
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

# ============================================================
# PROJECT DIRECTORIES
# ============================================================

DATASET_DIR = PROJECT_ROOT / "Dataset"
MODEL_DIR = PROJECT_ROOT / "Models"
RESULTS_DIR = PROJECT_ROOT / "Results"
ASSETS_DIR = PROJECT_ROOT / "assets"

# ============================================================
# DATASET PATHS
# ============================================================

VIDEO_DIR = DATASET_DIR / "videos"
IMAGE_DIR = DATASET_DIR / "images"

# ============================================================
# MODEL
# ============================================================

MODEL_PATH = MODEL_DIR / "yolo11n.pt"

# ============================================================
# DEFAULT INPUT / OUTPUT
# ============================================================

DEFAULT_VIDEO = VIDEO_DIR / "traffic.mp4"
OUTPUT_VIDEO = RESULTS_DIR / "smart_traffic_output.mp4"
REPORT_PATH = RESULTS_DIR / "traffic_report.csv"

# ============================================================
# YOLO SETTINGS
# ============================================================

CONFIDENCE_THRESHOLD = 0.40
IMAGE_SIZE = 640

# ============================================================
# VEHICLE CLASSES
# ============================================================

VEHICLE_CLASSES = [
    "car",
    "bus",
    "truck",
    "motorcycle"
]

# ============================================================
# TRACKING SETTINGS
# ============================================================

TRACKER = "bytetrack.yaml"

# ============================================================
# PROCESSING SETTINGS
# ============================================================

MAX_FRAMES = 300

# ============================================================
# CREATE REQUIRED DIRECTORIES
# ============================================================

RESULTS_DIR.mkdir(parents=True, exist_ok=True)

print("Smart Traffic Management configuration loaded.")

# ============================================================
# PERSPECTIVE TRANSFORMATION
# ============================================================

PERSPECTIVE_POINTS = [
    (250, 180),   # Top-left
    (1050, 180),  # Top-right
    (1250, 700),  # Bottom-right
    (50, 700)     # Bottom-left
]