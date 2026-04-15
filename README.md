# PoseAssist 🧍‍♂️📸

A real-time human pose guidance system built with Python, MediaPipe, and OpenCV.  
Guides users to match target poses via live webcam feedback — like the AI camera mode in Meitu/SNOW/CapCut.

---
# PoseAssist 🧍‍♂️📸

> Real-time AI pose guidance system — like the smart camera mode in Meitu, SNOW, and CapCut, built with Python.

![Python](https://img.shields.io/badge/Python-3.10-blue?logo=python)
![MediaPipe](https://img.shields.io/badge/MediaPipe-0.10-green?logo=google)
![OpenCV](https://img.shields.io/badge/OpenCV-4.8-red?logo=opencv)
![License](https://img.shields.io/badge/License-Apache2.0-yellow)

---

## What It Does

PoseAssist opens your webcam and guides you to match a target pose in real time.

- Detects your full body skeleton using **MediaPipe Pose (Tasks API)**
- Compares your pose against a predefined template using **joint angle math**
- Shows a live **match score (0–100%)** as a progress bar
- Gives **joint-level tips** — *"Bend your right elbow more"*
- Gives **camera framing tips** — *"Move camera up", "Step back"*
- **Auto-captures** a photo the moment your pose hits 85% match

---

## Demo

```
┌─────────────────────────────────────────────────────┐
│ Target: Standing, right hand on hip                 │
│ Match: ████████████░░░░  72%                        │
│                                                     │
│ POSE TIPS:                                          │
│   Bend your right elbow more (currently 142°)       │
│                                                     │
│ CAMERA TIPS:                                        │
│   Move camera UP — too much empty space above       │
│                                          Q=quit N=next│
└─────────────────────────────────────────────────────┘
```

---

## Pose Templates

| # | Template | Description |
|---|---|---|
| 1 | `standing_hand_on_hip` | Standing straight, right hand on hip |
| 2 | `arms_crossed` | Standing with arms crossed over chest |
| 3 | `arms_raised` | Both arms raised to sides (T-pose) |
| 4 | `relaxed_standing` | Natural relaxed standing, arms at sides |

---

## Setup

### 1. Clone
```bash
git clone https://github.com/nandipalleparthu-eng/PoseAssist.git
cd PoseAssist
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Download the MediaPipe model
```bash
python download_model.py
```

### 4. Run
```bash
python main.py
```

---

## Controls

| Key | Action |
|---|---|
| `N` | Switch to next pose template |
| `Q` | Quit |

Auto-captured photos are saved to the `captures/` folder.

---

## How Pose Matching Works

Poses are matched using **joint angle constraints**, not pixel coordinates.  
This makes the system **scale-invariant** — works at any distance from the camera.

```
angle = arccos( (BA · BC) / (|BA| × |BC|) )
```

Each template defines allowed angle ranges per joint.  
**Score = fraction of constraints satisfied.**

Example constraint for `standing_hand_on_hip`:
```python
"right_elbow_angle": (70, 110),   # elbow must be 70°–110°
"left_elbow_angle":  (150, 180),  # left arm must be straight
"shoulder_level":    True,        # shoulders must be level
```

---

## Project Structure

```
PoseAssist/
├── main.py               # Entry point — webcam loop + auto-capture
├── pose_templates.py     # Predefined pose angle constraints
├── pose_analyzer.py      # Joint angle math + pose matching engine
├── camera_guidance.py    # Framing analysis + camera suggestions
├── overlay_ui.py         # Skeleton + score bar + tips overlay
├── download_model.py     # Downloads MediaPipe .task model file
├── requirements.txt      # Python dependencies
└── procedure.txt         # Full build documentation + integrations
```

---

## Tech Stack

| Tool | Purpose |
|---|---|
| [MediaPipe](https://mediapipe.dev/) | Pose landmark detection (33 keypoints, Tasks API) |
| [OpenCV](https://opencv.org/) | Webcam feed, drawing, image saving |
| [NumPy](https://numpy.org/) | Vector math for joint angle calculations |
| Python 3.10 | Core language |

---

## Real-World Integration Examples

| Industry | Use Case |
|---|---|
| 📱 Social Media Apps | Auto-shot like SNOW / Meitu / CapCut |
| 🏋️ Fitness Apps | Exercise form correction (squat, plank, deadlift) |
| 🛍️ E-Commerce | Virtual try-on pose guidance |
| 🏥 Healthcare | Remote physiotherapy exercise tracking |
| 🪞 Smart Fitting Rooms | Body proportion measurement |
| 🎮 Gaming | Body-controlled input without a controller |
| 🎤 Presentation Coaching | Posture and body language feedback |

> See `procedure.txt` for detailed AWS integration guides for each use case.

---

## License

Licensed under the [Apache 2.0 License](LICENSE).

