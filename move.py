import pyautogui
import time
import keyboard  # new import

time.sleep(3)

while True:
    if keyboard.is_pressed("z"):  # escape sezuence
        break

    # Press A (left)
    pyautogui.keyDown("a")
    time.sleep(1)
    pyautogui.keyUp("a")

    if keyboard.is_pressed("z"): break

    # Press D (right)
    pyautogui.keyDown("d")
    time.sleep(1)
    pyautogui.keyUp("d")

    if keyboard.is_pressed("z"): break

