# 🪪 Smart ANPR & Access Control Security System

An advanced Automatic Number Plate Recognition (ANPR) and Smart Gate Access Controller built using Python, **OpenCV**, **NumPy**, and **Tesseract OCR**. This utility extracts vehicular identity markers and evaluates them against custom Access Control Lists (ACL) in real-time.

## 🚀 Key Innovation Upgrades
- **Access Control Layer (ACL):** Upgraded from a simple text scanner into an active security decision engine equipped with `Authorized` and `Blacklisted` plate telemetry logic.
- **SIEM Style Auditing Logs:** Automatically tracks and appends vehicle plate readings, millisecond-precise timestamps, and gate status reports into an immutable tracking file (`access_logs.txt`).
- **Adaptive Geometrical Approximation:** Leverages `cv2.approxPolyDP` polygonal bounding checks to isolate quadrilateral shapes matching standard plate aspect ratios under dynamic lighting conditions.
- **Fault-Tolerant Input Pipe:** Gracefully prevents thread termination when dealing with non-compliant text arrays or empty string frames.

## 💻 Tech Stack
- **Language:** Python 3
- **Frameworks:** OpenCV, Pytesseract (OCR Engine), NumPy, Imutils

## 🛠️ Installation & System Prerequisites

1. Ensure the Google Tesseract OCR engine binary is installed on your OS platform, then install the Python libraries:
```bash
pip install opencv-python pytesseract numpy imutils
```

2. Spin up the automated security gateway monitor:
```bash
python anpr_system.py
```
