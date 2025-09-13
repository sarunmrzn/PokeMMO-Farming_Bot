import pytesseract
import numpy as np
import win32gui, win32ui, win32con
import pygetwindow as gw
import cv2

# Tell pytesseract where tesseract.exe is
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Game window name
WINDOW_NAME = "РokеММO"

# Find the game window
windows = gw.getWindowsWithTitle(WINDOW_NAME)
if not windows:
    raise Exception(f"Window '{WINDOW_NAME}' not found!")
window = windows[0]

# Get HWND handle
hwnd = win32gui.FindWindow(None, WINDOW_NAME)

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

# Define region relative to client area
region = (250, 160, 400, 20)

# List of Pokémon to match
pokemon_list = ["Growlithe", "Psyduck"]

# Capture region from game window
screenshot_cv = capture_window(hwnd, region)
cv2.imwrite("current_region.png", screenshot_cv)  # optional for debugging

# OCR the captured region
ocr_result = pytesseract.image_to_string(screenshot_cv).strip().split()
if ocr_result:
    text = ocr_result[0]
else:
    text = ""
print("OCR text:", text)

# Direct match from list (case-insensitive)
matched = None
for name in pokemon_list:
    if text.lower() == name.lower():
        matched = name
        break

if matched:
    print(f"✅ Matched Pokémon: {matched}")
else:
    print(f"❌ Not matched, detected text: {text}")
    print("Bringing game window to front...")
    window.activate()
