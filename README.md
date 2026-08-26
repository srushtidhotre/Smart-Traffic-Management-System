# 🚦 Smart Traffic Management System

An AI-powered Smart Traffic Management System that uses computer vision and machine learning techniques to monitor traffic, detect and track vehicles, analyze lanes, estimate congestion, detect traffic violations, and support adaptive traffic signal management.

---

## 📌 Project Overview

Traffic congestion and traffic violations are major challenges in modern transportation systems.

This project provides an intelligent traffic monitoring solution using:

- YOLO for vehicle detection
- ByteTrack for multi-object tracking
- Perspective Transformation for bird's-eye traffic analysis
- Lane-wise vehicle analysis
- Traffic density estimation
- Vehicle speed estimation
- Queue length estimation
- Congestion scoring
- Adaptive traffic signal control
- Traffic violation detection
- Streamlit-based interactive dashboard

The system processes traffic videos and generates real-time analytics through an interactive dashboard.

---

## 🎯 Objectives

The main objectives of this project are:

1. Detect vehicles from traffic video footage.
2. Track individual vehicles across video frames.
3. Identify vehicles according to their lanes.
4. Estimate vehicle speed.
5. Analyze traffic density.
6. Estimate traffic queue length.
7. Calculate traffic congestion.
8. Dynamically determine traffic signal priorities.
9. Detect traffic violations.
10. Provide an interactive traffic monitoring dashboard.
11. Generate downloadable traffic analysis reports.

---

## 🏗️ System Architecture

The overall system follows this workflow:

```text
Traffic Video
      │
      ▼
Vehicle Detection
      │
      ▼
YOLO + ByteTrack
      │
      ▼
Vehicle Tracking
      │
      ├───────────────┐
      │               │
      ▼               ▼
Lane Analysis     Speed Analysis
      │               │
      └───────┬───────┘
              ▼
       Traffic Analytics
              │
       ┌──────┼───────────┐
       │      │           │
       ▼      ▼           ▼
    Density  Queue    Congestion
       │      │           │
       └──────┼───────────┘
              ▼
    Adaptive Signal Control
              │
              ▼
     Traffic Violation
         Detection
              │
              ▼
     Streamlit Dashboard
              │
              ▼
       Reports & Analytics
