import cv2
import os
from datetime import datetime

import mediapipe as mp
from mediapipe.tasks import python as mp_python
from mediapipe.tasks.python import vision as mp_vision

from pose_templates import POSE_TEMPLATES
from pose_analyzer import extract_angles, match_pose
from camera_guidance import get_camera_guidance
from overlay_ui import draw_skeleton, draw_feedback

CAPTURE_DIR   = "captures"
MODEL_PATH    = "pose_landmarker.task"
SCORE_THRESHOLD = 0.85
CAPTURE_COOLDOWN = 60

os.makedirs(CAPTURE_DIR, exist_ok=True)


def build_landmarker():
    base_opts = mp_python.BaseOptions(model_asset_path=MODEL_PATH)
    opts = mp_vision.PoseLandmarkerOptions(
        base_options=base_opts,
        running_mode=mp_vision.RunningMode.VIDEO,
        num_poses=1,
        min_pose_detection_confidence=0.6,
        min_tracking_confidence=0.6,
    )
    return mp_vision.PoseLandmarker.create_from_options(opts)


def run():
    template_names = list(POSE_TEMPLATES.keys())
    template_idx = 0
    cooldown = 0

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("ERROR: Cannot open webcam.")
        return

    print("Human Pose Guidance System started.")
    print("Controls: Q = quit | N = next pose template")

    with build_landmarker() as landmarker:
        frame_idx = 0
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            frame = cv2.flip(frame, 1)
            h, w = frame.shape[:2]

            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb)
            timestamp_ms = int(frame_idx * (1000 / 30))
            result = landmarker.detect_for_video(mp_image, timestamp_ms)
            frame_idx += 1

            template_name = template_names[template_idx]
            template = POSE_TEMPLATES[template_name]

            pose_feedback = ["Stand in front of the camera"]
            camera_feedback = ["No person detected"]
            score = 0.0

            if result.pose_landmarks:
                lm = result.pose_landmarks[0]  # first detected person

                angles = extract_angles(lm, w, h)
                score, pose_feedback = match_pose(angles, template)
                camera_feedback = get_camera_guidance(lm, w, h)

                draw_skeleton(frame, lm)

                if score >= SCORE_THRESHOLD and cooldown == 0:
                    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
                    path = os.path.join(CAPTURE_DIR, f"{template_name}_{ts}.jpg")
                    cv2.imwrite(path, frame)
                    print(f"Auto-captured: {path}")
                    cooldown = CAPTURE_COOLDOWN

            if cooldown > 0:
                cooldown -= 1

            draw_feedback(frame, pose_feedback, camera_feedback, score, template["description"])
            cv2.imshow("Human Pose Guidance", frame)

            key = cv2.waitKey(1) & 0xFF
            if key == ord("q"):
                break
            elif key == ord("n"):
                template_idx = (template_idx + 1) % len(template_names)
                print(f"Switched to: {template_names[template_idx]}")

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    run()
