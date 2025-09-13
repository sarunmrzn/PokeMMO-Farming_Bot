import pyautogui
import time

print("Move your mouse to the top-left corner of the area you want to capture.")
time.sleep(5)  # gives you 5 seconds to position your mouse

x, y = pyautogui.position()
print(f"Top-left corner coordinates: x={x}, y={y}")
