# 🚦 Smart Traffic Management System

An AI-powered Smart Traffic Management System that uses computer vision and intelligent traffic analytics to monitor vehicles, analyze traffic conditions, detect traffic violations, estimate congestion, and support adaptive traffic signal management.

---

## 📌 Project Overview

Traffic congestion and traffic violations are major challenges in modern transportation systems.

The **Smart Traffic Management System** provides an intelligent traffic monitoring solution using computer vision and machine learning techniques.

The system processes traffic video footage and performs:

- Vehicle detection
- Multi-object vehicle tracking
- Lane-wise traffic analysis
- Perspective transformation
- Vehicle speed estimation
- Traffic density estimation
- Queue length estimation
- Congestion scoring
- Adaptive traffic signal control
- Traffic violation detection
- Real-time dashboard visualization
- Traffic analytics and CSV report generation

The complete system is integrated into an interactive **Streamlit dashboard** for easy monitoring and analysis.

---

## 🎯 Objectives

The main objectives of this project are:

1. Detect vehicles from traffic video footage.
2. Track individual vehicles across multiple video frames.
3. Assign vehicles to their respective lanes.
4. Estimate vehicle speed.
5. Analyze traffic density for each lane.
6. Estimate the length of traffic queues.
7. Calculate an overall traffic congestion score.
8. Dynamically determine traffic signal priorities.
9. Detect traffic violations such as wrong-way movement and stopped vehicles.
10. Provide an interactive traffic monitoring dashboard.
11. Generate historical traffic analytics.
12. Provide downloadable traffic analysis and violation reports.

---

## 🏗️ System Architecture

The system follows the workflow below:

```text
                    Traffic Video
                         │
                         ▼
                Vehicle Detection
                         │
                         ▼
                   YOLO Model
                         │
                         ▼
                  ByteTrack
                Vehicle Tracking
                         │
            ┌────────────┼────────────┐
            │            │            │
            ▼            ▼            ▼
       Lane Analysis  Speed       Vehicle
                      Analysis     Positions
            │            │            │
            └────────────┼────────────┘
                         ▼
                Traffic Analytics
                         │
              ┌──────────┼──────────┐
              │          │          │
              ▼          ▼          ▼
           Density     Queue    Congestion
           Analysis   Estimation   Score
              │          │          │
              └──────────┼──────────┘
                         ▼
              Adaptive Signal Control
                         │
                         ▼
               Violation Detection
                         │
                         ▼
               Streamlit Dashboard
                         │
                         ▼
                Analytics & Reports
```

---

## 🧠 Technologies Used

| Technology | Purpose |
|------------|---------|
| Python | Core programming language |
| OpenCV | Computer vision and video processing |
| YOLO | Vehicle detection |
| Ultralytics | YOLO implementation |
| ByteTrack | Multi-object vehicle tracking |
| NumPy | Numerical operations |
| Pandas | Data processing and analytics |
| Streamlit | Interactive dashboard |
| Git | Version control |
| GitHub | Source code management |

---

## 📂 Project Structure

```text
Smart_Traffic_Detection/
│
├── app/
│   ├── __init__.py
│   ├── analytics.py
│   ├── config.py
│   ├── density.py
│   ├── lane.py
│   ├── signal_controller.py
│   ├── tracker.py
│   └── violations.py
│
├── models/
│   └── yolov8n.pt
│
├── notebooks/
│   ├── notebook_1.ipynb
│   ├── notebook_2.ipynb
│   ├── notebook_3.ipynb
│   ├── notebook_4.ipynb
│   ├── notebook_5.ipynb
│   ├── notebook_6.ipynb
│   ├── notebook_7.ipynb
│   ├── notebook_8.ipynb
│   └── notebook_9.ipynb
│
├── Results/
│   └── dashboard_analysis.csv
│
├── videos/
│   └── traffic video files
│
├── dashboard.py
├── requirements.txt
├── .gitignore
└── README.md
```

---

## ⚙️ Main System Components

### 1. Vehicle Detection

The system uses the YOLO object detection model to identify vehicles in each traffic video frame.

Detected vehicles are passed to the tracking system module for continuous monitoring.

---

### 2. Vehicle Tracking

ByteTrack is used for multi-object tracking.

A unique tracking ID is assigned to each detected vehicle.

Example:

```text
Vehicle → ID 1
Vehicle → ID 2
Vehicle → ID
```

This allows the system to monitor individual vehicles as they move through the traffic scene.

---

### 3. Perspective Transformation

Perspective transformation is used to convert the original traffic scene into a bird's-eye view.

This provides a better representation of vehicle positions and lane distribution.

The transformed view helps with:

- Lane analysis
- Vehicle positioning
- Traffic density analysis
- Queue estimation
- Traffic visualization

---

### 4. Lane Analysis

The system divides the traffic region into three lanes and determines the lane of each detected vehicle using its transformed position.

For each lane, the system calculates:

- Vehicle count
- Traffic density
- Signal priority
- Green signal duration

Example:

```text
Lane 1 → 8 Vehicles → HIGH Density
Lane 2 → 4 Vehicles → MEDIUM Density
Lane 3 → 2 Vehicles → LOW Density
```

---

### 5. Speed Estimation

The system analyzes vehicle movement between consecutive frames to estimate vehicle speed.

The calculated speed is displayed on the dashboard as:

```text
Average Speed: XX.X km/h
```

---

### 6. Queue Estimation

The system estimates the number of vehicles forming traffic queues.

Queue length is used as one of the parameters for evaluating traffic conditions and congestion.

---

### 7. Traffic Density Analysis

Traffic density is calculated using the number of vehicles detected within the analyzed traffic lanes.

The system categorizes density into:

```text
LOW
MEDIUM
HIGH
```

This provides a simple indication of the current traffic condition.

---

### 8. Congestion Detection

The system calculates a congestion score using traffic parameters including:

- Number of detected vehicles
- Number of queued vehicles
- Average vehicle speed

The dashboard displays the resulting congestion score.

Example:

```text
Congestion: 72.5 / 100
```

A higher congestion score indicates heavier traffic conditions.

---

### 9. Adaptive Traffic Signal Control

The system analyzes traffic conditions in each lane and determines signal priorities.

The adaptive signal controller considers lane traffic conditions and generates signal timing information.

Example:

```text
Lane 1
Vehicles: 8
Density: HIGH
Green Time: 40 sec
Priority: HIGH
```

This provides an intelligent approach to allocating green signal time based on traffic conditions.

---

### 10. Traffic Violation Detection

The system currently detects traffic violations including:

- Wrong-way movement
- Stopped vehicles

When a violation is detected, the corresponding vehicle is highlighted in the video.

Violation records include information such as:

- Vehicle ID
- Violation type
- Frame number
- Description

---

## 🖥️ Streamlit Dashboard

The complete system is integrated into an interactive Streamlit dashboard which provides real-time traffic monitoring.

The dashboard displays the following features.

### Live Traffic Monitoring

The dashboard displays:

- Detected vehicles
- Vehicle tracking IDs
- Vehicle type
- Lane number
- Estimated speed
- Traffic violations

### Traffic Metrics

The dashboard displays:

```text
🚗 Vehicles
🏎️ Average Speed
🚧 Queue Length
🚨 Violations
```

It also provides traffic congestion information.

### Perspective-Aware Lane Analysis

The dashboard provides lane-wise information including:

- Vehicle count
- Density
- Green signal time
- Signal priority

### Bird's-Eye Traffic View

The perspective-transformed traffic view displays:

- Lane boundaries
- Vehicle positions
- Vehicle IDs
- Lane assignments

This provides an easier way to understand vehicle distribution across lanes.

### Historical Traffic Analytics

After video processing, the system generates historical analytics including:

- Vehicle count
- Average speed
- Congestion score
- Traffic violations

These values are displayed using interactive charts.

### Traffic Violation History

Detected violations are displayed in a dedicated table.

The dashboard also provides violation statistics and allows the violation report to be downloaded as a CSV file.

### Lane Performance Summary

The dashboard provides a summary of lane performance using:

- Average vehicles per lane
- Peak vehicles per lane

This helps compare traffic conditions between lanes.

---

## 📊 Generated Results

The system generates traffic analysis data in CSV format.

The analysis includes:

```text
Frame
Vehicles
Average Speed
Queued Vehicles
Congestion Score
Violations
Priority Lane
Lane 1 Vehicles
Lane 2 Vehicles
Lane 3 Vehicles
Density Score
Traffic
```

The main analysis output is stored in:

```text
Results/dashboard_analysis.csv
```

---

## 🚀 Installation

### 1. Clone the Repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
```

Navigate to the project directory:

```bash
cd Smart_Traffic_Detection
```

---

### 2. Create a Virtual Environment

```bash
python -m venv .venv
```

---

### 3. Activate the Virtual Environment

For Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

If PowerShell execution policy prevents activation, use:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
```

Then activate the environment:

```powershell
.venv\Scripts\Activate.ps1
```

---

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## ▶️ Running the Application

Start the Streamlit dashboard using:

```bash
streamlit run dashboard.py
```

The application will be available at:

```text
http://localhost:8501
```

---

## 🎮 How to Use

1. Activate the virtual environment.
2. Start the Streamlit application.
3. Open the dashboard in your browser.
4. Select the number of frames to process.
5. Click **▶ Start Analysis**.
6. The configured traffic video will be loaded.
7. Vehicles will be detected and tracked.
8. Lane analysis and traffic analytics will be performed.
9. Traffic violations will be detected.
10. Results will be displayed on the dashboard.
11. After processing, traffic analysis can be downloaded as a CSV file.

---

## 📈 Dashboard Workflow

```text
Start Application
       │
       ▼
Load Traffic Video
       │
       ▼
Detect Vehicles
       │
       ▼
Track Vehicles
       │
       ▼
Analyze Lanes
       │
       ▼
Calculate Speed
       │
       ▼
Estimate Queue
       │
       ▼
Calculate Density
       │
       ▼
Calculate Congestion
       │
       ▼
Adaptive Signal Decision
       │
       ▼
Detect Violations
       │
       ▼
Display Dashboard
       │
       ▼
Generate Reports
```

---

## 🔍 Traffic Violation Output

Normal vehicle:

```text
ID 12 | car | L2 | 32.4 km/h
```

Stopped vehicle:

```text
ID 12 | car | L2 | 0.0 km/h | STOPPED
```

Wrong-way vehicle:

```text
ID 7 | car | L1 | 25.4 km/h | WRONG WAY
```

When a violation is detected, the vehicle is highlighted on the video.
Violations can also be exported using the dashboard's download option.
---

## 📥 Output Files

The application generates traffic analysis results in the `Results` directory.

Example:

```text
Results/
│
└── dashboard_analysis.csv
```

The dashboard also provides downloadable reports:

```text
traffic_analysis.csv
traffic_violations.csv
```

---

## 🧪 Testing

The system has been tested using traffic video input.

The following components were successfully verified:

- Vehicle detection
- Vehicle tracking
- Lane assignment
- Perspective transformation
- Bird's-eye view generation
- Speed estimation
- Queue estimation
- Traffic density analysis
- Congestion analysis
- Adaptive signal control
- Traffic violation detection
- Streamlit dashboard
- CSV result generation

---

## 🔐 GitHub and Security

The project uses Git and GitHub for version control.

The following files and directories should not be committed:

```text
.venv/
__pycache__/
*.pyc
.ipynb_checkpoints/
.env
```

These are handled through the `.gitignore` file.

Large datasets, unnecessary generated files, and sensitive credentials should also be excluded from the repository.

---

## 🔮 Future Enhancements

The system can be further enhanced with:

- Real-time CCTV camera integration
- Automatic Number Plate Recognition (ANPR)
- Red-light violation detection
- Additional traffic violation detection
- Emergency vehicle detection
- Automatic accident and incident detection
- Real-time cloud monitoring
- IoT integration
- Edge-device deployment
- Intelligent route optimization
- Reinforcement-learning-based traffic signal optimization
- Real-time alerts and notifications
- Advanced Predictive traffic analytics
- Support for multiple traffic intersections

---

## 🎓 Academic Applications

This project demonstrates the practical application of:

- Computer Vision
- Machine Learning
- Object Detection
- Multi-Object Tracking
- Data Analytics
- Intelligent Transportation Systems
- Traffic Management
- Real-Time Dashboard Development

It can be used as an academic project to demonstrate the integration of AI, computer vision, and data analytics into a real-world transportation problem.

---

## 👩‍💻 Project Author

### Srushti Dhotre

**Bachelor of Engineering – Artificial Intelligence & Data Science**

---

## ⭐ Acknowledgement

This project was developed as an academic project focused on applying artificial intelligence, computer vision, and intelligent traffic management techniques to real-world transportation challenges.

---

## 📜 License

This project is intended for educational and academic purposes.
