import cv2

# MediaPipe Pose connections (pairs of landmark indices)
POSE_CONNECTIONS = [
    (11, 12), (11, 13), (13, 15), (12, 14), (14, 16),
    (11, 23), (12, 24), (23, 24), (23, 25), (24, 26),
    (25, 27), (26, 28), (0, 11),  (0, 12),
]


def draw_skeleton(frame, landmarks):
    """Draw pose landmarks and connections on frame."""
    h, w = frame.shape[:2]
    pts = [(int(lm.x * w), int(lm.y * h)) for lm in landmarks]

    for a, b in POSE_CONNECTIONS:
        if landmarks[a].visibility > 0.4 and landmarks[b].visibility > 0.4:
            cv2.line(frame, pts[a], pts[b], (0, 200, 255), 2)

    for i, (x, y) in enumerate(pts):
        if landmarks[i].visibility > 0.4:
            cv2.circle(frame, (x, y), 4, (0, 255, 0), -1)


def draw_feedback(frame, pose_feedback, camera_feedback, score, target_name):
    """Draw all UI overlays: title, score bar, pose tips, camera tips."""
    h, w = frame.shape[:2]

    overlay = frame.copy()
    cv2.rectangle(overlay, (0, 0), (360, h), (0, 0, 0), -1)
    cv2.addWeighted(overlay, 0.45, frame, 0.55, 0, frame)

    y = 30
    cv2.putText(frame, f"Target: {target_name}", (10, y),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)
    y += 35

    bar_w = int(320 * score)
    color = (0, 255, 0) if score >= 0.8 else (0, 165, 255) if score >= 0.5 else (0, 0, 255)
    cv2.rectangle(frame, (10, y), (330, y + 18), (60, 60, 60), -1)
    cv2.rectangle(frame, (10, y), (10 + bar_w, y + 18), color, -1)
    cv2.putText(frame, f"Match: {int(score * 100)}%", (10, y + 14),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
    y += 35

    cv2.putText(frame, "POSE TIPS:", (10, y),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 1)
    y += 22
    for tip in (pose_feedback[:4] if pose_feedback else ["Pose looks great!"]):
        cv2.putText(frame, f"  {tip}", (10, y),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.42, (200, 200, 200), 1)
        y += 20

    y += 10
    cv2.putText(frame, "CAMERA TIPS:", (10, y),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 200, 255), 1)
    y += 22
    for tip in camera_feedback[:4]:
        cv2.putText(frame, f"  {tip}", (10, y),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.42, (200, 200, 200), 1)
        y += 20

    if score >= 0.85:
        cv2.putText(frame, "PERFECT POSE - CAPTURING!", (w // 2 - 160, h - 20),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 2)

    cv2.putText(frame, "Q=quit  N=next pose", (w - 220, h - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.45, (150, 150, 150), 1)
