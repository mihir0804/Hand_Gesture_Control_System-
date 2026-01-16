# Project J.A.R.V.I.S: Advanced Gesture Interface System (V3)

**A Physics-Based Human-Computer Interaction Framework**

## Executive Summary

Project J.A.R.V.I.S is a high-fidelity software solution designed to replace traditional computer mouse input with touchless hand gestures. Unlike conventional gesture recognition scripts that map hand coordinates directly to screen pixels—often resulting in jittery and fatiguing user experiences—this system implements a custom physics engine. By simulating mass, momentum, and friction, the cursor behaves like a physical object, ensuring smooth, organic, and precise control.

Built upon Python, MediaPipe, and OpenCV, this project demonstrates advanced implementation of signal processing (OneEuro filtering), state machine logic for intent prediction, and modular software architecture.

## Technical Highlights

### 1. Physics-Driven Cursor Control
The core innovation of this system is its decoupling of raw hand data from cursor position. Hand movements act as a force applied to a virtual mass (the cursor), which is then governed by friction and inertia. This naturally filters out high-frequency noise and hand tremors without the lag associated with simple moving averages.

### 2. Probabilistic Intent Engine
To address the "Midas Touch" problem (where every movement is interpreted as an action), the system employs a confidence-based state machine. Gestures such as "Left Click" are only triggered when the geometric relationship between the thumb and index finger meets a specific confidence threshold over a set duration (dwell time).

### 3. Adaptive Signal Smoothing
Input data from the webcam is processed through a OneEuro Filter. This adaptive algorithm dynamically adjusts its cutoff frequency based on speed:
* **Low Velocity:** High smoothing to eliminate jitter for precision work.
* **High Velocity:** Low smoothing to minimize latency for rapid traversal.

### 4. Holographic Heads-Up Display (HUD)
A non-intrusive visualization layer draws real-time diagnostics directly onto the video feed. This includes gesture confidence metrics, system state indicators, and motion trails, providing immediate feedback to the user regarding how the system is interpreting their intent.

## System Architecture

The codebase follows a modular design pattern to ensure scalability and separation of concerns:

* **`core/`**: Manages the primary system loop and application lifecycle.
* **`perception/`**: Handles computer vision tasks, including MediaPipe integration and raw coordinate extraction.
* **`intent/`**: Contains the state machine logic for distinguishing specific gestures (e.g., pinching vs. resting).
* **`control/`**: The physics engine responsible for calculating velocity, acceleration, and final cursor coordinates.
* **`ui/`**: Manages the rendering of the diagnostic overlay and visual feedback.

## Installation and Setup

### Prerequisites
* **Python:** Version 3.8 or higher.
* **Hardware:** Standard USB Webcam or integrated camera.

### Dependency Installation
Execute the following command to install the necessary libraries:

```bash
pip install -r requirements.txt
