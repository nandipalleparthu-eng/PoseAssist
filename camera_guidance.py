NOSE          = 0
LEFT_SHOULDER = 11
RIGHT_SHOULDER= 12
LEFT_HIP      = 23
RIGHT_HIP     = 24


def get_camera_guidance(landmarks, frame_w, frame_h):
    """
    Analyze body framing and return camera adjustment suggestions.
    landmarks: list of NormalizedLandmark from MediaPipe Tasks API.
    """
    guidance = []

    nose       = landmarks[NOSE]
    l_shoulder = landmarks[LEFT_SHOULDER]
    r_shoulder = landmarks[RIGHT_SHOULDER]
    l_hip      = landmarks[LEFT_HIP]
    r_hip      = landmarks[RIGHT_HIP]

    body_cx = (l_shoulder.x + r_shoulder.x) / 2
    head_y  = nose.y - 0.08
    feet_y  = (l_hip.y + r_hip.y) / 2 + 0.35

    if body_cx < 0.35:
        guidance.append("Move camera RIGHT — subject is too far left")
    elif body_cx > 0.65:
        guidance.append("Move camera LEFT — subject is too far right")

    if head_y < 0.02:
        guidance.append("Move camera DOWN or step back — head is cut off")

    if nose.y > 0.55:
        guidance.append("Move camera UP — too much empty space above")

    if feet_y > 1.05:
        guidance.append("Step back or zoom out — feet may be cut off")

    if (feet_y - head_y) < 0.3:
        guidance.append("Move closer or zoom in — subject appears too small")

    if not guidance:
        guidance.append("Framing looks good!")

    return guidance
