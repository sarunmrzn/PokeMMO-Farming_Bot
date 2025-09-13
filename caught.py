import cv2
import pyautogui
import numpy as np
import time

time.sleep(3)  # switch to game

# Region coordinates
region = (200, 100, 400, 100)
screenshot = pyautogui.screenshot(region=region)

# Convert to OpenCV format
screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

# Load pokeball template
template = cv2.imread("pokeball.jpg", cv2.IMREAD_COLOR)

# Match template
result = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)
min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

if max_val >= 0.8:  # confidence threshold
    print("Already caught!")
else:
    print("Nothing detected.")
