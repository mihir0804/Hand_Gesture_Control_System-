import cv2
import time
import pyautogui
from gesture_v3 import config
from gesture_v3.perception.tracker import HandTracker
from gesture_v3.perception.smoothing import OneEuroFilter
from gesture_v3.intent.classifier import GestureClassifier
from gesture_v3.control.mouse_physics import PhysicsCursor
from gesture_v3.ui.hud import CinematicHUD

class SystemController:
    def __init__(self):
        self.running = True
        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        self.cap.set(cv2.CAP_PROP_FPS, config.TARGET_FPS)
        
        self.tracker = HandTracker()
        self.smoother = OneEuroFilter(time.time(), [0.5, 0.5], 
                                      min_cutoff=config.ONE_EURO_MIN_CUTOFF, 
                                      beta=config.ONE_EURO_BETA)
        self.classifier = GestureClassifier()
        self.cursor = PhysicsCursor()
        self.hud = CinematicHUD()
        
        self.start_time = time.time()
        self.prev_hand_x = 0
        self.prev_hand_y = 0
        
        # State Variables
        self.drag_active = False
        self.last_toggle_time = 0
        self.last_click_time = 0
        self.last_vol_y = 0
        self.last_scroll_y = 0

    def run(self):
        print(f"[{config.APP_NAME}] Initialized. Press 'Q' to Quit.")
        last_time = time.time()

        while self.running:
            current_time = time.time()
            dt = current_time - last_time
            last_time = current_time
            
            success, img = self.cap.read()
            if not success: continue

            img = cv2.flip(img, 1)
            img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            frame_timestamp_ms = (current_time - self.start_time) * 1000
            
            detection_result = self.tracker.process(img_rgb, frame_timestamp_ms)
            
            hand_landmarks = None
            state = "IDLE"
            confidence = 0.0
            
            if detection_result.hand_landmarks:
                hand_landmarks = detection_result.hand_landmarks[0]
                
                # Anchor: Index MCP (5)
                raw_point = hand_landmarks[5] 
                filtered_pos = self.smoother(current_time, [raw_point.x, raw_point.y])
                curr_x, curr_y = filtered_pos[0], filtered_pos[1]
                
                # Delta Calculation
                delta_x = curr_x - self.prev_hand_x
                delta_y = curr_y - self.prev_hand_y
                self.prev_hand_x = curr_x
                self.prev_hand_y = curr_y
                
                # Intent
                state, meta = self.classifier.process(hand_landmarks)
                confidence = meta.get("confidence", 0.0)
                
                # --- LOGIC & ACTIONS ---
                
                # 1. DRAG TOGGLE (FIST)
                if state == "FIST":
                    if (current_time - self.last_toggle_time) > config.DRAG_TOGGLE_COOLDOWN:
                        self.drag_active = not self.drag_active 
                        self.last_toggle_time = current_time
                        if self.drag_active: pyautogui.mouseDown() 
                        else: pyautogui.mouseUp()
                
                # 2. EXECUTE
                if self.drag_active:
                    state = "DRAG_ACTIVE"
                    self.cursor.update_relative(delta_x, delta_y, dt)
                else:
                    if state == "MOVE":
                        self.cursor.update_relative(delta_x, delta_y, dt)
                        
                    elif state == "CLICK_LEFT":
                        if (current_time - self.last_click_time) > config.CLICK_COOLDOWN:
                             pyautogui.click()
                             self.last_click_time = current_time
                             cv2.circle(img, (int(curr_x*config.WINDOW_WIDTH), int(curr_y*config.WINDOW_HEIGHT)), 50, config.COLOR_CLICK, 4)
                             
                    elif state == "CLICK_RIGHT":
                        if (current_time - self.last_click_time) > config.CLICK_COOLDOWN: 
                             pyautogui.rightClick()
                             self.last_click_time = current_time
                             
                    elif state == "SCROLL":
                        dy = curr_y - self.last_scroll_y
                        if abs(dy) > 0.005: 
                            pyautogui.scroll(int(-dy * config.SCROLL_SPEED * 100))
                        self.last_scroll_y = curr_y
                        
                    elif state == "VOLUME":
                        dy = self.last_vol_y - curr_y 
                        if abs(dy) > config.VOLUME_SENSITIVITY:
                            if dy > 0: pyautogui.press('volumeup')
                            else: pyautogui.press('volumedown')
                            self.last_vol_y = curr_y # Reset for steps
                            
                            # HUD Text override
                            cv2.putText(img, "VOL", (int(curr_x*config.WINDOW_WIDTH)+40, int(curr_y*config.WINDOW_HEIGHT)), 
                                        cv2.FONT_HERSHEY_PLAIN, 2, config.COLOR_VOLUME, 2)
                    
                    # Reset References if switching out of state
                    if state != "SCROLL": self.last_scroll_y = curr_y
                    if state != "VOLUME": self.last_vol_y = curr_y

                self.hud.draw(img, hand_landmarks, state, confidence)
                
            else:
                # Lost Hand
                if self.drag_active:
                    pyautogui.mouseUp()
                    self.drag_active = False
                self.classifier.process(None)
                self.hud.draw(img, None, "IDLE", 0.0)
            
            fps = 1/dt if dt > 0 else 0
            cv2.putText(img, f"J.A.R.V.I.S  |  FPS: {int(fps)}", (20, 30), cv2.FONT_HERSHEY_PLAIN, 1, (200, 255, 200), 1)
            cv2.imshow(config.APP_NAME, img)
            if cv2.waitKey(1) == ord('q'): self.running = False

        self.cap.release()
        cv2.destroyAllWindows()
