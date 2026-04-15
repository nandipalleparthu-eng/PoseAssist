"""
Predefined pose templates stored as normalized landmark index ratios.
Each template defines key joint angle constraints.
"""

POSE_TEMPLATES = {
    "standing_hand_on_hip": {
        "description": "Standing straight, right hand on hip",
        "instructions": "Stand straight, place your right hand on your hip, face the camera",
        "key_joints": {
            "right_elbow_angle": (70, 110),   # (min, max) degrees
            "left_elbow_angle": (150, 180),
            "shoulder_level": True,            # shoulders should be level
        }
    },
    "arms_crossed": {
        "description": "Standing with arms crossed",
        "instructions": "Cross your arms over your chest, stand straight",
        "key_joints": {
            "right_elbow_angle": (40, 80),
            "left_elbow_angle": (40, 80),
            "shoulder_level": True,
        }
    },
    "arms_raised": {
        "description": "Both arms raised to sides (T-pose style)",
        "instructions": "Raise both arms out to your sides at shoulder height",
        "key_joints": {
            "right_elbow_angle": (160, 180),
            "left_elbow_angle": (160, 180),
            "shoulder_level": True,
        }
    },
    "relaxed_standing": {
        "description": "Natural relaxed standing pose",
        "instructions": "Stand naturally with arms at your sides, relax your shoulders",
        "key_joints": {
            "right_elbow_angle": (150, 180),
            "left_elbow_angle": (150, 180),
            "shoulder_level": True,
        }
    },
}
