import mediapipe as mp
import os
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

class HandTracker:
    def __init__(self, model_path="hand_landmarker.task"):
        # Handle path resolution
        if not os.path.exists(model_path):
             # Fallback for running from different dirs
             if os.path.exists("../" + model_path):
                 model_path = "../" + model_path
             elif os.path.exists("Control_pc_using_Hand-Gesture-main/" + model_path):
                 model_path = "Control_pc_using_Hand-Gesture-main/" + model_path
        
        base_options = python.BaseOptions(model_asset_path=model_path)
        options = vision.HandLandmarkerOptions(
            base_options=base_options,
            running_mode=vision.RunningMode.VIDEO,
            num_hands=2,
            min_hand_detection_confidence=0.5,
            min_hand_presence_confidence=0.5,
            min_tracking_confidence=0.5
        )
        self.landmarker = vision.HandLandmarker.create_from_options(options)

    def process(self, image_rgb, timestamp_ms):
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=image_rgb)
        return self.landmarker.detect_for_video(mp_image, int(timestamp_ms))
