# PokeMMO Legendary Encounter Automation

## Overview

This project automates the detection of Pokémon encounters in the PokeMMO game window using OCR (Optical Character Recognition). It triggers actions such as movement and keypresses based on detected Pokémon, and immediately stops all automation when a legendary Pokémon is found.

## Features

- **Automated Movement:** Moves the player left and right to trigger encounters.
- **Battle Detection:** Pauses movement and spams the 'E' key (while holding Ctrl) during battles.
- **Legendary Detection:** Stops all automation and brings the game window to the front when a legendary Pokémon is detected.
- **OCR Debugging:** Prints raw OCR output for troubleshooting.
- **Thread Synchronization:** Ensures both movement and OCR threads stop immediately when required.

## Requirements

- Windows OS
- Python 3.8+
- PokeMMO game client
- Pokémon ROM files (place in `Roms/` folder)
- Tesseract OCR (included in `tesseract/` folder)

## Installation

1. **Clone or Download the Project**
   Place all files in a folder, e.g. `C:\PokeMMO`.
2. **Install Dependencies**
   Open PowerShell in the project directory and run:
   ```powershell
   pip install -r requirements.txt
   ```
3. **ROMs and Tesseract**
   - Place your Pokémon ROM files in the `Roms/` folder.
   - Tesseract executables and DLLs are included in the `tesseract/` folder. No separate installation needed.

## Usage

1. **Start PokeMMO** and log in.
2. Rebind your keys `WASD` for movement and `E` for `A` key.
3. **Run the Automation Script**
   ```powershell
   python legend.py
   ```
4. **Stopping the Script**
   - Press `Z` in the game window to stop automation at any time.

## Troubleshooting

- **Window Not Found:** Ensure the game window title matches `РokеММO` (Cyrillic characters).
    add ```all_windows = gw.getAllWindows()
print("Available window titles:")
for w in all_windows:
    if w.title.strip():
        print(f"  {w.title}")```
  on line 35 to print all window titles, copy PokeMMO and replace the value on `WINDOW_NAME`, it might seem like its the same name but its different, copy and paste.
- **OCR Issues:** The script prints raw OCR output for debugging. Adjust the `region` variable in `legend.py` if detection is inaccurate.
- **Environment Issues:**
  - Clear Python cache if needed:
    ```powershell
    Remove-Item -Recurse -Force .\__pycache__
    ```
  - Reinstall dependencies if errors occur.

## Customization

- **Legendary List:** Edit the `LEGENDARIES` set in `legend.py` to add/remove legendary Pokémon.
- **Movement Region:** Adjust the `region` variable to match your game window layout.

## File Structure

- `legend.py` - Main automation script
- `ocr.py` - OCR logic (imported by main script)
- `window.py` - Window title debugging
- `requirements.txt` - Python dependencies
- `tesseract/` - Tesseract OCR executables and DLLs
- `Roms/` - Pokémon ROM files

## Disclaimer

This project is for educational purposes only. Use at your own risk. Automation in online games may violate terms of service.
Still has a few bugs, so dont panic, will fix them in next update.
