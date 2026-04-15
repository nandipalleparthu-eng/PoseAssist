import numpy as np

# MediaPipe Pose landmark indices (same as before, just constants now)
NOSE           = 0
LEFT_SHOULDER  = 11
RIGHT_SHOULDER = 12
LEFT_ELBOW     = 13
RIGHT_ELBOW    = 14
LEFT_WRIST     = 15
RIGHT_WRIST    = 16
LEFT_HIP       = 23
RIGHT_HIP      = 24


def get_angle(a, b, c):
    """Compute angle at joint b given three 2D points a, b, c."""
    a, b, c = np.array(a), np.array(b), np.array(c)
    ba = a - b
    bc = c - b
    cosine = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc) + 1e-6)
    return np.degrees(np.arccos(np.clip(cosine, -1.0, 1.0)))


def extract_angles(landmarks, w, h):
    """Extract key joint angles from MediaPipe Tasks API landmarks (list of NormalizedLandmark)."""
    def pt(idx):
        lm = landmarks[idx]
        return [lm.x * w, lm.y * h]

    angles = {
        "right_elbow_angle": get_angle(
            pt(RIGHT_SHOULDER), pt(RIGHT_ELBOW), pt(RIGHT_WRIST)
        ),
        "left_elbow_angle": get_angle(
            pt(LEFT_SHOULDER), pt(LEFT_ELBOW), pt(LEFT_WRIST)
        ),
        "shoulder_level": abs(
            landmarks[LEFT_SHOULDER].y - landmarks[RIGHT_SHOULDER].y
        ) < 0.05,
    }
    return angles


def match_pose(current_angles, template):
    """
    Returns (match_score 0-1, list of feedback strings).
    match_score = fraction of constraints satisfied.
    """
    constraints = template["key_joints"]
    passed = 0
    total = len(constraints)
    feedback = []

    for key, rule in constraints.items():
        val = current_angles.get(key)
        if val is None:
            total -= 1
            continue

        if isinstance(rule, tuple):
            lo, hi = rule
            if lo <= val <= hi:
                passed += 1
            else:
                direction = "more" if val < lo else "less"
                joint_name = key.replace("_angle", "").replace("_", " ")
                feedback.append(f"Bend your {joint_name} {direction} (currently {val:.0f}°)")
        elif isinstance(rule, bool):
            if val == rule:
                passed += 1
            else:
                feedback.append("Level your shoulders — one side is higher than the other")

    score = passed / total if total > 0 else 0.0
    return round(score, 2), feedback
