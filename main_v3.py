"""
Project J.A.R.V.I.S (Gesture Interface V3)
Entry Point.
"""
import sys
import os

# Ensure proper import resolution for the gesture_v3 package
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from gesture_v3.core.system import SystemController

if __name__ == "__main__":
    app = SystemController()
    app.run()
