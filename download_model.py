"""Run this once after cloning to download the MediaPipe pose model."""
import urllib.request
import os

MODEL_URL = (
    "https://storage.googleapis.com/mediapipe-models/"
    "pose_landmarker/pose_landmarker_lite/float16/latest/pose_landmarker_lite.task"
)
MODEL_PATH = "pose_landmarker.task"

if os.path.exists(MODEL_PATH):
    print(f"Model already exists: {MODEL_PATH}")
else:
    print("Downloading MediaPipe pose model...")
    urllib.request.urlretrieve(MODEL_URL, MODEL_PATH)
    print(f"Downloaded: {MODEL_PATH}")
