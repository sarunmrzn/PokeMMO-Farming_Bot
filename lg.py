import os
import sys
import time
import pytesseract
import numpy as np
import win32gui, win32ui, win32con
import pygetwindow as gw
import cv2
import pyautogui
import keyboard
import threading
from difflib import SequenceMatcher

# ---------------- CONFIG ----------------
WINDOW_NAME = "PokeMМO"
region = (140, 175, 190, 15)  # Top left (140, 175) to bottom right (330, 190)
MOVE_DELAY = 0.5
E_PRESS_DELAY = 0.25
OCR_PSM = "--psm 7"

# Movement keys
MOVE_LEFT_KEY = "w"   # Change to "w" if needed
MOVE_RIGHT_KEY = "s"  # Change to "s" if needed
BATTLE_ESCAPE_KEY = "e"  # Change to "z" if needed
STOP_KEY = "z"  # Press this to stop the bot

# ---------------- tesseract path ----------------
if getattr(sys, "frozen", False):
    base_path = sys._MEIPASS
else:
    base_path = os.path.dirname(__file__)

bundled_tess = os.path.join(base_path, "tesseract", "tesseract.exe")
if os.path.exists(bundled_tess):
    pytesseract.pytesseract.tesseract_cmd = bundled_tess

# ---------------- load pokemon list ----------------
ALL_POKEMON = ["Bulbasaur", "Ivysaur", "Venusaur", "Charmander", "Charmeleon", "Charizard", "Sandshrew", "Spearow", "Rattata", "Psyduck", "Ekans", "Squirtle", "Wartortle", "Blastoise", "Caterpie", "Metapod", "Butterfree", "Weedle", "Kakuna", "Beedrill", "Pidgey", "Pidgeotto", "Pidgeot", "Raticate", "Fearow", "Arbok", "Pikachu", "Raichu", "Sandslash", "Nidoran♀", "Nidorina", "Nidoqueen", "Nidoran♂", "Nidorino", "Nidoking", "Clefairy", "Clefable", "Vulpix", "Ninetales", "Jigglypuff", "Wigglytuff", "Zubat", "Golbat", "Oddish", "Gloom", "Vileplume", "Paras", "Parasect", "Venonat", "Venomoth", "Diglett", "Dugtrio", "Meowth", "Persian", "Golduck", "Mankey", "Primeape", "Growlithe", "Arcanine", "Poliwag", "Poliwhirl", "Poliwrath", "Abra", "Kadabra", "Alakazam", "Machop", "Machoke", "Machamp", "Bellsprout", "Weepinbell", "Victreebel", "Tentacool", "Tentacruel", "Geodude", "Graveler", "Golem", "Ponyta", "Rapidash", "Slowpoke", "Slowbro", "Magnemite", "Magneton", "Farfetch'd", "Doduo", "Dodrio", "Seel", "Dewgong", "Grimer", "Muk", "Shellder", "Cloyster", "Gastly", "Haunter", "Gengar", "Onix", "Drowzee", "Hypno", "Krabby", "Kingler", "Voltorb", "Electrode", "Exeggcute", "Exeggutor", "Cubone", "Marowak", "Hitmonlee", "Hitmonchan", "Lickitung", "Koffing", "Weezing", "Rhyhorn", "Rhydon", "Chansey", "Tangela", "Kangaskhan", "Horsea", "Seadra", "Goldeen", "Seaking", "Staryu", "Starmie", "Mr. Mime", "Scyther", "Jynx", "Electabuzz", "Magmar", "Pinsir", "Tauros", "Magikarp", "Gyarados", "Lapras", "Ditto", "Eevee", "Vaporeon", "Jolteon", "Flareon", "Porygon", "Omanyte", "Omastar", "Kabuto", "Kabutops", "Aerodactyl", "Snorlax", "Dratini", "Dragonair", "Dragonite", "Chikorita", "Bayleef", "Meganium", "Cyndaquil", "Quilava", "Typhlosion", "Totodile", "Croconaw", "Feraligatr", "Sentret", "Furret", "Hoothoot", "Noctowl", "Ledyba", "Ledian", "Spinarak", "Ariados", "Crobat", "Chinchou", "Lanturn", "Pichu", "Cleffa", "Igglybuff", "Togepi", "Togetic", "Natu", "Xatu", "Mareep", "Flaaffy", "Ampharos", "Bellossom", "Marill", "Azumarill", "Sudowoodo", "Politoed", "Hoppip", "Skiploom", "Jumpluff", "Aipom", "Sunkern", "Sunflora", "Yanma", "Wooper", "Quagsire", "Espeon", "Umbreon", "Murkrow", "Slowking", "Misdreavus", "Unown", "Wobbuffet", "Girafarig", "Pineco", "Forretress", "Dunsparce", "Gligar", "Steelix", "Snubbull", "Granbull", "Qwilfish", "Scizor", "Shuckle", "Heracross", "Sneasel", "Teddiursa", "Ursaring", "Slugma", "Magcargo", "Swinub", "Piloswine", "Corsola", "Remoraid", "Octillery", "Delibird", "Mantine", "Skarmory", "Houndour", "Houndoom", "Kingdra", "Phanpy", "Donphan", "Porygon2", "Stantler", "Smeargle", "Tyrogue", "Hitmontop", "Smoochum", "Elekid", "Magby", "Miltank", "Blissey", "Pupitar", "Tyranitar", "Lugia", "Ho-Oh", "Treecko", "Grovyle", "Sceptile", "Torchic", "Combusken", "Blaziken", "Mudkip", "Marshtomp", "Swampert", "Poochyena", "Mightyena", "Zigzagoon", "Linoone", "Wurmple", "Silcoon", "Beautifly", "Cascoon", "Dustox", "Lotad", "Lombre", "Ludicolo", "Seedot", "Nuzleaf", "Shiftry", "Taillow", "Swellow", "Wingull", "Pelipper", "Ralts", "Kirlia", "Gardevoir", "Surskit", "Masquerain", "Shroomish", "Breloom", "Slakoth", "Vigoroth", "Slaking", "Nincada", "Ninjask", "Shedinja", "Whismur", "Loudred", "Exploud", "Makuhita", "Hariyama", "Azurill", "Nosepass", "Skitty", "Delcatty", "Sableye", "Mawile", "Aron", "Lairon", "Aggron", "Meditite", "Medicham", "Electrike", "Manectric", "Plusle", "Minun", "Volbeat", "Illumise", "Roselia", "Gulpin", "Swalot", "Carvanha", "Sharpedo", "Wailmer", "Wailord", "Numel", "Camerupt", "Torkoal", "Spoink", "Grumpig", "Spinda", "Trapinch", "Vibrava", "Flygon", "Cacnea", "Cacturne", "Swablu", "Altaria", "Zangoose", "Seviper", "Lunatone", "Solrock", "Barboach", "Whiscash", "Corphish", "Crawdaunt", "Baltoy", "Claydol", "Lileep", "Cradily", "Anorith", "Armaldo", "Feebas", "Milotic", "Castform", "Kecleon", "Shuppet", "Banette", "Duskull", "Dusclops", "Absol", "Latias", "Latios", "Snorunt", "Glalie", "Spheal", "Sealeo", "Walrein", "Clamperl", "Huntail", "Gorebyss", "Relicanth", "Luvdisc", "Bagon", "Shelgon", "Salamence", "Metagross", "Regirock", "Regice", "Registeel", "Kyogre", "Groudon", "Jirachi", "Deoxys", "Turtwig", "Grotle", "Torterra", "Chimchar", "Monferno", "Infernape", "Piplup", "Prinplup", "Empoleon", "Starly", "Staravia", "Staraptor", "Bidoof", "Bibarel", "Kricketot", "Kricketune", "Shinx", "Luxio", "Luxray", "Budew", "Roserade", "Cranidos", "Rampardos", "Shieldon", "Bastiodon", "Burmy", "Wormadam", "Mothim", "Combee", "Vespiquen", "Pachirisu", "Buizel", "Floatzel", "Cherubi", "Cherrim", "Shellos", "Gastrodon", "Ambipom", "Drifloon", "Drifblim", "Buneary", "Lopunny", "Mismagius", "Honchkrow", "Glameow", "Purugly", "Chingling", "Stunky", "Skuntank", "Bronzor", "Bronzong", "Chatot", "Spiritomb", "Gible", "Gabite", "Garchomp", "Munchlax", "Riolu", "Lucario", "Hippopotas", "Hippowdon", "Skorupi", "Drapion", "Croagunk", "Toxicroak", "Carnivine", "Finneon", "Lumineon", "Mantyke", "Snover", "Abomasnow", "Weavile", "Magnezone", "Lickilicky", "Rhyperior", "Tangrowth", "Electivire", "Magmortar", "Togekiss", "Yanmega", "Leafeon", "Glaceon", "Gliscor", "Mamoswine", "Porygon-Z", "Gallade", "Probopass", "Dusknoir", "Froslass", "Dialga", "Palkia", "Heatran", "Regigigas", "Cresselia", "Phione", "Manaphy", "Darkrai", "Victini", "Snivy", "Servine", "Serperior", "Tepig", "Pignite", "Emboar", "Oshawott", "Dewott", "Samurott", "Patrat", "Watchog", "Lillipup", "Herdier", "Stoutland", "Purrloin", "Liepard", "Pansage", "Simisage", "Pansear", "Simisear", "Panpour", "Simipour", "Munna", "Musharna", "Pidove", "Tranquill", "Unfezant", "Blitzle", "Zebstrika", "Roggenrola", "Boldore", "Gigalith", "Woobat", "Swoobat", "Drilbur", "Excadrill", "Audino", "Timburr", "Gurdurr", "Conkeldurr", "Tympole", "Palpitoad", "Seismitoad", "Throh", "Sawk", "Sewaddle", "Swadloon", "Leavanny", "Venipede", "Whirlipede", "Scolipede", "Cottonee", "Whimsicott", "Petilil", "Lilligant", "Basculin", "Sandile", "Krokorok", "Krookodile", "Darumaka", "Darmanitan", "Maractus", "Dwebble", "Crustle", "Scraggy", "Scrafty", "Sigilyph", "Yamask", "Cofagrigus", "Tirtouga", "Carracosta", "Archen", "Archeops", "Trubbish", "Garbodor", "Zorua", "Zoroark", "Minccino", "Cinccino", "Gothita", "Gothorita", "Gothitelle", "Solosis", "Duosion", "Reuniclus", "Ducklett", "Swanna", "Vanillite", "Vanillish", "Vanilluxe", "Deerling", "Sawsbuck", "Emolga", "Karrablast", "Escavalier", "Foongus", "Amoonguss", "Frillish", "Jellicent", "Alomomola", "Joltik", "Galvantula", "Ferroseed", "Ferrothorn", "Klink", "Klang", "Klinklang", "Tynamo", "Eelektrik", "Eelektross", "Elgyem", "Beheeyem", "Litwick", "Lampent", "Chandelure", "Axew", "Fraxure", "Haxorus", "Cubchoo", "Beartic", "Cryogonal", "Shelmet", "Accelgor", "Stunfisk", "Mienfoo", "Mienshao", "Druddigon", "Golett", "Golurk", "Pawniard", "Bisharp", "Bouffalant", "Rufflet", "Braviary", "Vullaby", "Mandibuzz", "Heatmor", "Durant", "Deino", "Zweilous", "Hydreigon", "Larvesta", "Volcarona", "Tornadus", "Thundurus", "Landorus", "Reshiram", "Zekrom", "Kyurem", "Meloetta", "Genesect", "Pangoro", "Sliggoo", "Goodra", "Diancie", "Hoopa", "Volcanion", "Gimmighoul", "Gholdengo", "Jigglyputt"]
LEGENDARIES = {"Articuno","Zapdos","Moltres","Raikou","Entei","Suicune"}
ALL_POKEMON_LOWER = [p.lower() for p in ALL_POKEMON]
LEGENDARIES_LOWER = {p.lower() for p in LEGENDARIES}

# ---------------- window setup ----------------
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

def find_pokemon_in_text(text):
    if not text:
        return None
    t = text.lower()
    best = None
    best_score = 0
    best_len = 0
    
    # First try exact substring matching
    for idx, name in enumerate(ALL_POKEMON_LOWER):
        if name in t:
            if len(name) > best_len:
                best = ALL_POKEMON[idx]
                best_score = 1.0
                best_len = len(name)
    
    # If no exact match, try fuzzy matching (for OCR errors)
    if not best:
        for idx, name in enumerate(ALL_POKEMON_LOWER):
            # Split text by whitespace and special chars to get words
            words = [w for w in t.replace('.', ' ').replace('$', ' ').split() if len(w) > 2]
            for word in words:
                ratio = SequenceMatcher(None, name, word).ratio()
                # If match is > 75% similar, consider it a match
                if ratio > 0.75 and (best is None or len(name) > best_len):
                    best = ALL_POKEMON[idx]
                    best_score = ratio
                    best_len = len(name)
    
    if best:
        print(f"[MATCH] Found '{best}' (score: {best_score:.2f}) in text: {repr(text)}")
    return best

# ---------------- threading flags ----------------
battle_detected = threading.Event()
legendary_found = threading.Event()
stop_flag = threading.Event()

# ---------------- worker threads ----------------
def movement_worker():
    while not stop_flag.is_set():
        if battle_detected.is_set():
            # Wait for battle to end, but also check the stop flag
            while battle_detected.is_set() and not stop_flag.is_set():
                time.sleep(0.1)
            continue
        
        # Move left
        pyautogui.keyDown(MOVE_LEFT_KEY)
        # Wait for MOVE_DELAY, but this can be interrupted by the stop_flag
        # The wait() function returns True if the event was set
        if stop_flag.wait(MOVE_DELAY):
            pyautogui.keyUp(MOVE_LEFT_KEY)
            break # Exit the loop immediately
        pyautogui.keyUp(MOVE_LEFT_KEY)

        # Check the stop flag again before starting the next action
        if stop_flag.is_set():
            break

        # Move right
        pyautogui.keyDown(MOVE_RIGHT_KEY)
        # Wait for MOVE_DELAY, can be interrupted by the stop_flag
        if stop_flag.wait(MOVE_DELAY):
            pyautogui.keyUp(MOVE_RIGHT_KEY)
            break # Exit the loop immediately
        pyautogui.keyUp(MOVE_RIGHT_KEY)

def ocr_worker():
    while not stop_flag.is_set():
        img = capture_window(hwnd, region)
        text = ocr_region_to_text(img)
        
        # Check for Shiny
        if "shiny" in text.lower():
            print("SHINY FOUND:", text)
            stop_flag.set()  # This stops both threads
            try:
                window.activate()
                time.sleep(0.1)
            except Exception:
                pass
            break
        
        matched = find_pokemon_in_text(text)
        if matched:
            print("Detected:", matched)
            if matched.lower() in LEGENDARIES_LOWER:
                print("LEGENDARY FOUND:", matched)
                stop_flag.set()  # This stops both threads
                try:
                    window.activate()
                    time.sleep(0.1)
                except Exception:
                    pass
                break
            else:
                battle_detected.set()
                # Instead of pressing Ctrl+E, repeatedly click at the desired
                # coordinates until the battle ends or stop is requested.
                while not stop_flag.is_set():
                    pyautogui.click(420, 450)
                    time.sleep(E_PRESS_DELAY)
                    img2 = capture_window(hwnd, region)
                    text2 = ocr_region_to_text(img2)

                    new_match = find_pokemon_in_text(text2)
                    if not new_match:
                        print("Battle ended. Resuming movement.")
                        battle_detected.clear()
                        break
        else:
            time.sleep(0.1)

print(f"Automation started. Press {STOP_KEY.upper()} to stop.")

t1 = threading.Thread(target=movement_worker, daemon=True)
t2 = threading.Thread(target=ocr_worker, daemon=True)

t1.start()
t2.start()

try:
    while not stop_flag.is_set():
        if keyboard.is_pressed(STOP_KEY):
            print("Stop key pressed.")
            stop_flag.set()
        time.sleep(0.1)
except KeyboardInterrupt:
    stop_flag.set()

print("Automation stopped.")
