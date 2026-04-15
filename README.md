# PoseAssist 🧍‍♂️📸

A real-time human pose guidance system built with Python, MediaPipe, and OpenCV.  
Guides users to match target poses via live webcam feedback — like the AI camera mode in Meitu/SNOW/CapCut.

---

## Features

- 🦴 Real-time skeleton detection using MediaPipe Pose (Tasks API)
- 🎯 Pose matching against predefined templates with a live match score (0–100%)
- 📷 Camera framing guidance — "Move camera up", "Step back", "Center the subject"
- 💡 Joint-level feedback — "Bend your right elbow more"
- 📸 Auto-captures photo when pose match reaches 85%
- 🔄 Cycle through 4 pose templates with `N` key

---

## Pose Templates

| Template | Description |
|---|---|
| `standing_hand_on_hip` | Standing straight, right hand on hip |
| `arms_crossed` | Standing with arms crossed |
| `arms_raised` | Both arms raised to sides (T-pose) |
| `relaxed_standing` | Natural relaxed standing pose |

---

## Setup

### 1. Clone the repo
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
└── procedure.txt         # Full build documentation + real-world integrations
```

---

## Real-World Integration Examples

- **Social media apps** — Auto-shot feature like SNOW/Meitu
- **Fitness apps** — Exercise form correction (squat, plank, deadlift)
- **E-commerce** — Virtual try-on pose guidance
- **Healthcare** — Remote physiotherapy exercise tracking
- **Smart fitting rooms** — Body proportion measurement
- **Gaming** — Body-controlled input without a controller

See `procedure.txt` for detailed integration guides with AWS services.

---

## Tech Stack

- Python 3.10
- [MediaPipe](https://mediapipe.dev/) — Pose landmark detection (Tasks API)
- [OpenCV](https://opencv.org/) — Camera feed + drawing
- NumPy — Joint angle calculations

---

## How Pose Matching Works

Poses are matched using **joint angle constraints** (not pixel coordinates),  
making the system scale-invariant — works regardless of distance from camera.

```
angle = arccos( (BA · BC) / (|BA| × |BC|) )
```

Each template defines allowed angle ranges per joint.  
Score = fraction of constraints satisfied.
