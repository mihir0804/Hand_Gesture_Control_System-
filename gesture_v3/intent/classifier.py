import time
import math
from gesture_v3 import config

class GestureClassifier:
    def __init__(self):
        self.state = "IDLE"
        self.pinch_confidence = 0.0
        self.last_update = time.time()
        self.prev_wrist = None
        
    def process(self, landmarks):
        if not landmarks:
            self.state = "IDLE"
            self.pinch_confidence = 0.0
            return self.state, {}

        # 1. Pinch Detection
        thumb = landmarks[4]
        index = landmarks[8]
        middle = landmarks[12]
        
        dist_click = math.hypot(thumb.x - index.x, thumb.y - index.y)
        dist_right = math.hypot(thumb.x - middle.x, thumb.y - middle.y)
        
        # 2. Stability Check
        wrist = landmarks[0]
        curr_time = time.time()
        dt = curr_time - self.last_update
        self.last_update = curr_time
        
        velocity = 0.0
        if self.prev_wrist:
            dx = wrist.x - self.prev_wrist.x
            dy = wrist.y - self.prev_wrist.y
            if dt > 0: velocity = math.hypot(dx, dy) / dt 
        self.prev_wrist = wrist
        is_stable = velocity < 2.0 

        # 3. Confidence Logic
        if dist_click < config.PINCH_THRESHOLD_NORM and is_stable:
             self.pinch_confidence += config.CONFIDENCE_GROWTH
        elif dist_right < config.PINCH_THRESHOLD_NORM and is_stable:
             self.pinch_confidence += config.CONFIDENCE_GROWTH
        else:
             self.pinch_confidence -= config.CONFIDENCE_DECAY
        self.pinch_confidence = max(0.0, min(1.0, self.pinch_confidence))

        # 4. Finger States
        fingers_up = [False] * 5
        # Index(8) to Pinky(20) - Compare Tip Y to Pip Y
        for i, tip_idx in enumerate([8, 12, 16, 20]):
            pip_idx = tip_idx - 2
            fingers_up[i+1] = landmarks[tip_idx].y < landmarks[pip_idx].y 
            
        # Thumb(4) - Compare to Index MCP(5)
        thumb_tip = landmarks[4]
        index_mcp = landmarks[5]
        dist_thumb_out = math.hypot(thumb_tip.x - index_mcp.x, thumb_tip.y - index_mcp.y)
        fingers_up[0] = dist_thumb_out > 0.05
        
        # 5. Gesture Definitions
        is_fist = not any(fingers_up[1:])
        is_palm = all(fingers_up)
        is_peace = fingers_up[1] and fingers_up[2] and not fingers_up[3] and not fingers_up[4] 
        
        # [NEW] VOLUME GESTURE (Shaka): Thumb & Pinky UP, others DOWN
        is_volume = fingers_up[0] and fingers_up[4] and not any(fingers_up[1:4])
        
        # 6. State Machine Priority
        if dist_click < config.PINCH_THRESHOLD_NORM:
            self.state = "CLICK_LEFT"
            self.pinch_confidence = 1.0 
        elif dist_right < config.PINCH_THRESHOLD_NORM:
            self.state = "CLICK_RIGHT"
        elif is_volume:
            self.state = "VOLUME"
        elif is_peace:
            self.state = "SCROLL"
        elif is_fist:
            self.state = "FIST"
        elif is_palm:
            self.state = "MOVE"
        else:
            self.state = "IDLE" 

        return self.state, {"confidence": self.pinch_confidence}
