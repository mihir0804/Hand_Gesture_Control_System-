"""
Centralized configuration.
"""
import pyautogui

# --- SYSTEM ---
APP_NAME = "J.A.R.V.I.S Gesture Interface"
WINDOW_WIDTH, WINDOW_HEIGHT = pyautogui.size()
TARGET_FPS = 60

# --- PERCEPTION (OneEuroFilter) ---
ONE_EURO_MIN_CUTOFF = 0.5   
ONE_EURO_BETA = 4.0         
ONE_EURO_D_CUTOFF = 1.0     

# --- GESTURE CONFIG ---
GESTURE_CONFIDENCE_THRESHOLD = 0.8  
CONFIDENCE_DECAY = 0.2             
CONFIDENCE_GROWTH = 0.15           

# Thresholds
PINCH_THRESHOLD_NORM = 0.06
CLICK_COOLDOWN = 0.4

# Scroll
SCROLL_SPEED = 20
SCROLL_DEADZONE = 0.05

# Volume Control (NEW)
VOLUME_SENSITIVITY = 0.02       
COLOR_VOLUME = (128, 0, 128)    # Purple (BGR)

# Drag (Toggle)
DRAG_TOGGLE_COOLDOWN = 1.0 
COLOR_DRAG_ACTIVE = (0, 255, 0) # Green

# --- RELATIVE PHYSICS (AIR MOUSE) ---
DEAD_ZONE = 0.002        
BASE_SENSITIVITY = 3.0   
ACCELERATION_FACTOR = 20.0 
MAX_SENSITIVITY = 12.0   
DELTA_SMOOTHING = 0.6    

# --- UI COLORS (BGR) ---
COLOR_IDLE = (255, 255, 0)      # Cyan
COLOR_MOVE = (255, 255, 255)    # White
COLOR_CLICK = (0, 0, 255)       # Red
COLOR_RIGHT_CLICK = (255, 0, 0) # Blue
COLOR_SCROLL = (255, 0, 255)    # Magenta
COLOR_TEXT = (255, 255, 255)

# --- SAFETY ---
FAILSAFE_FPS = 15
