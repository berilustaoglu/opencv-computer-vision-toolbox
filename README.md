# 🛠️ Advanced Computer Vision & Image Processing Toolbox

A comprehensive, production-ready suite of desktop applications and utilities built using Python, **OpenCV**, **NumPy**, and **Matplotlib**. This toolbox encapsulates object-oriented (OOP) engineering solutions for image manipulation, data analytics, and digital forensics.

---

## 🧰 Modules Inside the Toolbox

### 1. Pro Color Palette Designer (`pro-color-palette-designer/`)
An interactive UI/UX tool that maps real-time hardware-level RGB trackbar inputs onto a dynamic rendering canvas, converting live bitstreams into web-ready Hexadecimal (`#RRGGBB`) color strings.

### 2. Smart Aspect-Ratio Resizer (`smart-image-resizer/`)
A mathematical scaling utility that resizes target images based on strict layout constraints (width-driven or height-driven) while preserving their native aspect ratios to protect against pixel stretching.

### 3. Image Forensic & Tamper Analyzer (`image-forensic-analyzer/`)
A pixel-by-pixel differential analyzer that computes localized absolute errors (`cv2.absdiff`) between two images. It programmatically generates binary masks and high-contrast red forensic heatmaps to pinpoint altered regions, calculating a precise similarity score down to 4 decimal places.

### 4. Image Intensity & Exposure Analyzer (`image-exposure-analyzer/`)
A high-fidelity data visualization tool that maps discrete RGB channels directly onto individual color-coded histogram curves, using grayscale luminance evaluations to programmatically diagnose `Underexposed` or `Overexposed` artifacts.

---

## 💻 Tech Stack & Dependencies
- **Language:** Python 3
- **Libraries:** OpenCV (`opencv-python`), NumPy (`numpy`), Matplotlib (`matplotlib`)

## 🛠️ Global Installation & Setup

1. Install all structural requirements in one command:
```bash
pip install opencv-python numpy matplotlib
```

2. Navigate into any project directory and spin up the desired utility:
```bash
cd pro-color-palette-designer
python designer.py
```
