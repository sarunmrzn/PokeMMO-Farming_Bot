import os
import sys
import time
import pytesseract
import numpy as np
import win32gui, win32ui, win32con
import pygetwindow as gw
import cv2
import pyautogui

# ---------------- CONFIG ----------------
WINDOW_NAME = "РokеMMO"
region = (140, 175, 190, 15)  # Top left (140, 175) to bottom right (330, 190)
OCR_PSM = "--psm 7"

# ---------------- tesseract path ----------------
if getattr(sys, "frozen", False):
    base_path = sys._MEIPASS
else:
    base_path = os.path.dirname(__file__)

bundled_tess = os.path.join(base_path, "tesseract", "tesseract.exe")
if os.path.exists(bundled_tess):
    pytesseract.pytesseract.tesseract_cmd = bundled_tess

# Get window
all_windows = gw.getAllWindows()
print("Available window titles:")
for w in all_windows:
    if w.title.strip():
        print(f"  {w.title}")

windows = gw.getWindowsWithTitle(WINDOW_NAME)
if not windows:
    raise Exception(f"Window '{WINDOW_NAME}' not found!")

window = windows[0]
hwnd = getattr(window, "_hWnd", None)
if not hwnd or hwnd == 0:
    hwnd = win32gui.FindWindow(None, window.title)

window.activate()

def capture_window(hwnd, region=None):
    left, top, right, bottom = win32gui.GetClientRect(hwnd)
    left, top = win32gui.ClientToScreen(hwnd, (left, top))
    right, bottom = win32gui.ClientToScreen(hwnd, (right, bottom))
    w, h = right - left, bottom - top

    hwindc = win32gui.GetWindowDC(hwnd)
    srcdc = win32ui.CreateDCFromHandle(hwindc)
    memdc = srcdc.CreateCompatibleDC()
    bmp = win32ui.CreateBitmap()
    bmp.CreateCompatibleBitmap(srcdc, w, h)
    memdc.SelectObject(bmp)
    memdc.BitBlt((0, 0), (w, h), srcdc, (0, 0), win32con.SRCCOPY)

    signedIntsArray = bmp.GetBitmapBits(True)
    img = np.frombuffer(signedIntsArray, dtype=np.uint8)
    img.shape = (h, w, 4)

    srcdc.DeleteDC()
    memdc.DeleteDC()
    win32gui.ReleaseDC(hwnd, hwindc)
    win32gui.DeleteObject(bmp.GetHandle())

    img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)

    if region:
        x, y, rw, rh = region
        img = img[y:y+rh, x:x+rw]

    return img

def ocr_region_to_text(img_cv):
    if img_cv is None or img_cv.size == 0:
        return ""
    gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)
    text = pytesseract.image_to_string(thresh, config=OCR_PSM)
    return text.strip()

print("\n=== BATTLE DETECTION DEBUG MODE ===")
print(f"Capturing region: {region}")
print("Saving screenshots to: battle_debug_X.png")
print("Saving OCR text to: ocr_output.txt")
print("\nPress Ctrl+C to stop.\n")

frame_count = 0
try:
    while True:
        # Capture region
        img = capture_window(hwnd, region)
        
        # Run OCR
        text = ocr_region_to_text(img)
        
        # Save screenshot
        screenshot_name = f"battle_debug_{frame_count}.png"
        cv2.imwrite(screenshot_name, img)
        
        # Save OCR text
        with open("ocr_output.txt", "a") as f:
            f.write(f"\n--- Frame {frame_count} ---\n")
            f.write(text)
            f.write("\n")
        
        print(f"Frame {frame_count}: Saved {screenshot_name}")
        print(f"OCR Text: {repr(text)}\n")
        
        frame_count += 1
        time.sleep(0.5)  # Capture every 500ms
        
except KeyboardInterrupt:
    print("\n\nDebug stopped.")
    print(f"Captured {frame_count} frames")
    print("Check the generated battle_debug_*.png files and ocr_output.txt")
