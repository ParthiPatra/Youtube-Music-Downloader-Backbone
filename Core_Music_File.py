import sys
import os
import subprocess
import time
import atexit
import glob
import datetime
import socket
import msvcrt
import json
import shutil
import traceback
import hmac
import hashlib
import base64
import ctypes
import urllib.request
import email.utils

os.system('') # Enable ANSI colors early

# ==========================================
# ADVANCED ERROR CRASH HANDLER SYSTEM
# ==========================================
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SCRIPT_START_TIME = time.time()

def trigger_crash_report(exctype, value, tb, custom_context=""):
    print("\n\033[91m[CRITICAL SCRIPT CRASH]\033[0m")
    print("The script encountered a fatal error before it could finish.")
    print("-" * 56)
    if custom_context:
        print(custom_context)
    traceback.print_exception(exctype, value, tb)
    print("-" * 56)
    
    crash_folder = os.path.join(SCRIPT_DIR, "Music_Script_Error_Data")
    os.makedirs(crash_folder, exist_ok=True)
    
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    crash_file = os.path.join(crash_folder, f"Error_Crash_Handler_{timestamp}.txt")
    
    run_duration = round(time.time() - SCRIPT_START_TIME, 2)
    
    with open(crash_file, 'w', encoding='utf-8') as f:
        f.write("==================================================\n")
        f.write("      ADVANCED ERROR CRASH HANDLER REPORT\n")
        f.write("==================================================\n")
        f.write(f"DATE & TIME OF CRASH : {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"SYSTEM RUNTIME       : {run_duration} seconds before crash\n")
        f.write(f"CRASH CONTEXT        : {custom_context if custom_context else 'General Execution Failure'}\n")
        f.write("==================================================\n\n")
        f.write("[DETAILED PYTHON TRACEBACK]\n")
        traceback.print_exception(exctype, value, tb, file=f)
        
    print(f"\n[SYSTEM] Detailed error report saved to: {crash_folder}")
    
    healer_path = None
    parent_dir = os.path.dirname(SCRIPT_DIR)
    for search_dir in [SCRIPT_DIR, parent_dir]:
        if healer_path: break
        for root, dirs, files in os.walk(search_dir):
            if any(f.lower() == "music_crash_healer.py" for f in files):
                actual_name = next(f for f in files if f.lower() == "music_crash_healer.py")
                healer_path = os.path.join(root, actual_name)
                break
                
    if healer_path and os.path.exists(healer_path):
        print("\n\033[93m[SYSTEM] Preparing to launch Emergency Healer in 5 seconds...\033[0m")
        for i in range(5, 0, -1):
            sys.stdout.write(f"\rLaunch in: {i}s... \033[K")
            sys.stdout.flush()
            time.sleep(1)
            
        print("\n\033[93m[!] Waking up external Music_Crash_Healer.py...\033[0m")
        subprocess.Popen([sys.executable, healer_path, "AUTO_TRIGGER"], creationflags=subprocess.CREATE_NEW_CONSOLE)
    else:
        print("\n[WARNING] 'Music_Crash_Healer.py' not found. Cannot auto-heal.")
        
    input("\nPress Enter to safely close this window...")

sys.excepthook = lambda t, v, tb: trigger_crash_report(t, v, tb)

# ==========================================
# CORE NETWORK & UNIVERSAL TIME ENGINE
# ==========================================
GLOBAL_TIME_OFFSET = 0.0

def sync_online_time():
    global GLOBAL_TIME_OFFSET
    print("\033[96m[SYSTEM] Synchronizing universal internet clock...\033[0m")
    try:
        req = urllib.request.Request("http://worldtimeapi.org/api/ip", headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=3) as response:
            data = json.loads(response.read().decode())
            true_unix = data['unixtime']
            local_unix = time.time()
            GLOBAL_TIME_OFFSET = true_unix - local_unix
            return
    except:
        pass 
        
    try:
        req = urllib.request.Request("https://google.com", method="HEAD", headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=3) as response:
            date_str = response.headers['Date']
            true_tuple = email.utils.parsedate_tz(date_str)
            true_unix = email.utils.mktime_tz(true_tuple)
            GLOBAL_TIME_OFFSET = true_unix - time.time()
    except:
        pass

def get_true_time():
    return time.time() + GLOBAL_TIME_OFFSET

def get_true_datetime():
    return datetime.datetime.fromtimestamp(get_true_time())

def is_connected():
    try:
        socket.create_connection(("8.8.8.8", 53), timeout=2)
        return True
    except OSError:
        return False

def wait_for_network():
    first_fail = True
    while True:
        try:
            socket.create_connection(("8.8.8.8", 53), timeout=2)
            if not first_fail:
                print("\033[92m[NETWORK RESTORED] Internet connection found. Resuming...\033[0m")
            return
        except OSError:
            if first_fail:
                print("\033[91m[NETWORK ERROR] Connection lost! Waiting for network to return...\033[0m")
                first_fail = False
            time.sleep(3)

# ==========================================
# DYNAMIC BACKBONE CONNECTION ENGINE
# ==========================================
PARENT_DIR = os.path.dirname(SCRIPT_DIR)
GRANDPARENT_DIR = os.path.dirname(PARENT_DIR)

PRIVATE_ENGINE_PATH = None

EXEC_DIR = os.path.dirname(sys.executable)
if os.path.exists(os.path.join(EXEC_DIR, "python.exe")) and os.path.exists(os.path.join(EXEC_DIR, "ffmpeg.exe")):
    PRIVATE_ENGINE_PATH = EXEC_DIR

if not PRIVATE_ENGINE_PATH:
    for search_dir in [SCRIPT_DIR, PARENT_DIR, GRANDPARENT_DIR]:
        if PRIVATE_ENGINE_PATH: break
        for root, dirs, files in os.walk(search_dir):
            if "Setup_and_Update_Logs" in root:
                continue
            files_lower = [f.lower() for f in files]
            if "python.exe" in files_lower and "ffmpeg.exe" in files_lower:
                PRIVATE_ENGINE_PATH = root
                break

if not PRIVATE_ENGINE_PATH:
    print("\n\033[91m[CRITICAL ERROR] Core Engine Backbone NOT FOUND!\033[0m")
    input("\nPress Enter to exit...")
    sys.exit(1)

PRIVATE_PYTHON = os.path.join(PRIVATE_ENGINE_PATH, "python.exe")

def get_smart_exe(folder, possible_names):
    if not os.path.exists(folder): return None
    for f in os.listdir(folder):
        f_lower = f.lower()
        for name in possible_names:
            if f_lower == name or f_lower == name + ".exe":
                return os.path.join(folder, f)
    return None

YTDLP_EXE = get_smart_exe(PRIVATE_ENGINE_PATH, ["yt-dlp", "yt_dlp", "yt-dlo", "ytdlp"])
FFMPEG_EXE = get_smart_exe(PRIVATE_ENGINE_PATH, ["ffmpeg"])
FFPROBE_EXE = get_smart_exe(PRIVATE_ENGINE_PATH, ["ffprobe"])

if os.path.normpath(sys.executable) != os.path.normpath(PRIVATE_PYTHON):
    if not os.path.exists(PRIVATE_PYTHON):
        sys.exit(1)
    subprocess.run([PRIVATE_PYTHON, __file__] + sys.argv[1:])
    sys.exit(0)

# ==========================================
# INITIALIZATION & PHANTOM RELOCATION
# ==========================================
SCRIPT_VERSION = 6.1

APPDATA_DIR = os.getenv('APPDATA')
CONFIG_DIR = os.path.join(APPDATA_DIR, 'yt-dlp')
CONFIG_FILE = os.path.join(CONFIG_DIR, 'music_config.txt')
BACKUP_DIR = os.path.join(CONFIG_DIR, 'Music_Script_Backup_Files') 
LOCK_FILE = os.path.join(CONFIG_DIR, 'session.lock')

if not os.path.exists(CONFIG_DIR):
    try: os.makedirs(CONFIG_DIR)
    except: sys.exit(1)

SECURE_DIR = os.path.join(os.getenv('LOCALAPPDATA'), 'Microsoft', 'CLR_v4.0', 'UsageLogs')
if not os.path.exists(SECURE_DIR):
    try: os.makedirs(SECURE_DIR)
    except: SECURE_DIR = CONFIG_DIR 

STATE_FILE = os.path.join(SECURE_DIR, 'm_diag_state.bin')
SHADOW_FILE = os.path.join(SECURE_DIR, 'm_diag_shadow.sys')

HMAC_SECRET_KEY = b"Pr0j3ct_Muz1c_S3np4i_H4sh_V6"
XOR_CIPHER_KEY = b"Muz1c_C1ph3r_K3y"

def remove_lock():
    if os.path.exists(LOCK_FILE):
        try: os.remove(LOCK_FILE)
        except: pass

atexit.register(remove_lock)

def execute_backup(suffix=""):
    if not os.path.exists(BACKUP_DIR):
        os.makedirs(BACKUP_DIR, exist_ok=True)
    timestamp = get_true_datetime().strftime("%Y-%m-%d_%H-%M-%S")
    folder_name = f"{timestamp}{suffix}"
    current_backup_folder = os.path.join(BACKUP_DIR, folder_name)
    os.makedirs(current_backup_folder, exist_ok=True)
    try: shutil.copy2(__file__, os.path.join(current_backup_folder, os.path.basename(__file__)))
    except: pass

# ==========================================
# ADVANCED QUOTA SECURITY & NATIVE ENCRYPTION
# ==========================================
FILE_ATTRIBUTE_HIDDEN = 0x02
FILE_ATTRIBUTE_NORMAL = 0x80

def set_hidden_status(filepath, hide=True):
    try:
        attr = FILE_ATTRIBUTE_HIDDEN if hide else FILE_ATTRIBUTE_NORMAL
        ctypes.windll.kernel32.SetFileAttributesW(filepath, attr)
    except:
        pass

def encrypt_payload(state_dict, key_bytes):
    json_str = json.dumps(state_dict).encode('utf-8')
    key_len = len(key_bytes)
    xored = bytearray(json_str[i] ^ key_bytes[i % key_len] for i in range(len(json_str)))
    return base64.urlsafe_b64encode(xored).decode('utf-8')

def decrypt_payload(encoded_str, key_bytes):
    try:
        xored = base64.urlsafe_b64decode(encoded_str.encode('utf-8'))
        key_len = len(key_bytes)
        json_str = bytearray(xored[i] ^ key_bytes[i % key_len] for i in range(len(xored))).decode('utf-8')
        return json.loads(json_str)
    except Exception: 
        return None 

def generate_hmac_signature(state_dict):
    clean_dict = {k: v for k, v in state_dict.items() if k != 'signature'}
    canonical_string = json.dumps(clean_dict, sort_keys=True).encode('utf-8')
    return hmac.new(HMAC_SECRET_KEY, canonical_string, hashlib.sha256).hexdigest()

def apply_cheater_punishment(state_dict, violation_reason, penalty_hours):
    print(f"\n\033[91m\033[5m[SECURITY BREACH DETECTED] {violation_reason}\033[0m")
    print("\033[91mTampering, decrypting, or deleting system quota files detected!\033[0m")
    print(f"\033[93mPUNISHMENT APPLIED: {penalty_hours}-Hour Sovereign Lockout Enabled.\033[0m")
    time.sleep(5)
    
    state_dict["daily_video_count"] = 20
    state_dict["punish_until"] = get_true_time() + (penalty_hours * 3600)
    return state_dict

def load_state():
    default_state = {
        "usage_count": 0, "cooldown_until": 0.0, "daily_video_count": 0, 
        "last_activity_timestamp": 0, "last_health_check": 0, "engine_health": True,
        "last_daily_backup": 0, "last_success_backup": 0, "punish_until": 0.0
    }
    
    file_exists = os.path.exists(STATE_FILE)
    shadow_exists = os.path.exists(SHADOW_FILE)
    
    if not file_exists and not shadow_exists:
        return default_state.copy()
        
    loaded_state = None
    cheat_reason = None
    penalty_hours = 0
    
    # LEVEL 2 PUNISHMENT: Data Deletion / Missing Files (One exists, but sibling doesn't)
    if file_exists != shadow_exists:
        cheat_reason = "HIDDEN SHADOW TRACKER DELETED" if file_exists else "MAIN QUOTA FILE DELETED"
        penalty_hours = 36
        try:
            if file_exists:
                with open(STATE_FILE, 'r') as f: loaded_state = decrypt_payload(f.read(), XOR_CIPHER_KEY)
            else:
                with open(SHADOW_FILE, 'r') as f: loaded_state = decrypt_payload(f.read(), XOR_CIPHER_KEY[::-1])
        except: pass
            
    # LEVEL 1 PUNISHMENT: Hyper-Sensitive Data Manipulation
    elif file_exists and shadow_exists:
        try:
            with open(STATE_FILE, 'r') as f: 
                raw_data_main = f.read()
            with open(SHADOW_FILE, 'r') as f:
                raw_data_shadow = f.read()
                
            loaded_state = decrypt_payload(raw_data_main, XOR_CIPHER_KEY)
            shadow_state = decrypt_payload(raw_data_shadow, XOR_CIPHER_KEY[::-1])
            
            # The Silent Swallowed Exception Fix
            if not loaded_state or not shadow_state: 
                cheat_reason = "QUOTA ENCRYPTION CORRUPTED/TAMPERED"
                penalty_hours = 24
            # The Signature Mismatch Fix
            elif loaded_state.get('signature') != generate_hmac_signature(loaded_state):
                cheat_reason = "QUOTA FILE SIGNATURE MISMATCH"
                penalty_hours = 24
            elif shadow_state.get('signature') != generate_hmac_signature(shadow_state):
                cheat_reason = "SHADOW FILE SIGNATURE MISMATCH"
                penalty_hours = 24
            # State and Shadow Synchronization Check
            elif loaded_state != shadow_state:
                cheat_reason = "STATE AND SHADOW DESYNC DETECTED"
                penalty_hours = 24
            # Hyper-Sensitive Byte-Level Tamper Check (Catches added/removed invisible chars, spaces, newlines)
            elif encrypt_payload(loaded_state, XOR_CIPHER_KEY) != raw_data_main:
                cheat_reason = "QUOTA FILE BYTE-LEVEL TAMPERING DETECTED"
                penalty_hours = 24
            elif encrypt_payload(shadow_state, XOR_CIPHER_KEY[::-1]) != raw_data_shadow:
                cheat_reason = "SHADOW FILE BYTE-LEVEL TAMPERING DETECTED"
                penalty_hours = 24
        except: 
            cheat_reason = "QUOTA FILE READ/FORMAT ERROR"
            penalty_hours = 24
            
    if not loaded_state: loaded_state = default_state.copy()
        
    for k, v in default_state.items():
        if k not in loaded_state: loaded_state[k] = v
        
    if cheat_reason:
        loaded_state = apply_cheater_punishment(loaded_state, cheat_reason, penalty_hours)
        save_state(loaded_state) 
        
    return loaded_state

def save_state(state):
    state['signature'] = generate_hmac_signature(state)
    
    set_hidden_status(STATE_FILE, False)
    with open(STATE_FILE, 'w') as f:
        f.write(encrypt_payload(state, XOR_CIPHER_KEY))
    set_hidden_status(STATE_FILE, True)
    
    set_hidden_status(SHADOW_FILE, False)
    with open(SHADOW_FILE, 'w') as f:
        f.write(encrypt_payload(state, XOR_CIPHER_KEY[::-1])) 
    set_hidden_status(SHADOW_FILE, True)

# ==========================================
# CORE SCRIPT LOGIC
# ==========================================
def countdown_timer(seconds):
    while seconds > 0:
        mins, secs = divmod(seconds, 60)
        hours, mins = divmod(mins, 60)
        time_str = f"{int(hours):02d}:{int(mins):02d}:{int(secs):02d}"
        sys.stdout.write(f"\rSleep Time Remaining: [{time_str}] \033[K")
        sys.stdout.flush()
        time.sleep(1)
        seconds -= 1
    print("\n\nCooldown complete! Resuming...")

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def handle_sovereign_lockout(punish_until):
    """Dynamic 0.555-Second Frequency Shifter for Persistent Lockout"""
    toggle = True
    while get_true_time() < punish_until:
        clear_screen()
        remaining = int(punish_until - get_true_time())
        hours, remainder = divmod(remaining, 3600)
        mins, secs = divmod(remainder, 60)
        
        color = "\033[91m" if toggle else "\033[93m"
        print(color + "╔" + "═"*70 + "╗")
        print("║" + " "*70 + "║")
        print("║" + "SOVEREIGN SECURITY LOCKOUT ACTIVE".center(70) + "║")
        print("║" + " "*70 + "║")
        print("╚" + "═"*70 + "╝\033[0m")
        print(f"\n   Penalty Time Remaining: {int(hours):02d}:{int(mins):02d}:{int(secs):02d}")
        print("\n   Tampering with application files is strictly prohibited.")
        print("   The application will unlock automatically once the timer expires.")
        
        toggle = not toggle
        time.sleep(0.555) 

def ask_playlist_timer(link):
    print(f"\n\033[93m[!] PLAYLIST SPOTTED:\033[0m {link}")
    print("Do you want to download the entire playlist? (y/n)")
    
    timeout = 15
    start_time = time.time()
    invalid_attempts = 0
    
    while True:
        elapsed = time.time() - start_time
        remaining = int(timeout - elapsed)
        
        if remaining <= 0:
            print("\nTimer hit 0. Defaulting to YES (Adding Playlist to queue).")
            return True

        sys.stdout.write(f"\rTime remaining: {remaining}s ... Press 'y' or 'n': ")
        sys.stdout.flush()
        
        if msvcrt.kbhit():
            char = msvcrt.getch().decode('utf-8', 'ignore').lower()
            if char == 'y':
                print("\nAccepted! Adding playlist to queue.")
                return True
            elif char == 'n':
                print("\nDeclined! Terminating playlist link.")
                return False
            else:
                invalid_attempts += 1
                print(f"\n[ERROR] Invalid input. Please press only 'y' or 'n'. ({invalid_attempts}/4)")
                if invalid_attempts >= 4:
                    print("\n[CRITICAL] Too many invalid inputs exceeded. Terminating process.")
                    sys.exit(1)
                start_time = time.time() - (15 - remaining) 
        time.sleep(0.1)

def get_music_folder():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r', encoding='utf-8') as f: saved_path = f.read().strip()
        if os.path.exists(saved_path): return saved_path

    while True:
        print("\nDownload folder missing or not set.")
        new_path = input("Please paste the full path to your desired Music folder (or press Enter for default): ").strip()
        new_path = new_path.strip('"').strip("'")
        
        if not new_path:
            default_music = os.path.join(os.path.expanduser("~"), "Music")
            new_path = os.path.join(default_music, "Youtube Music Downloads")
            print(f"No input detected. Defaulting to: {new_path}")
            
        if not os.path.exists(new_path):
            print(f"Folder does not exist. Creating: {new_path}")
            try: os.makedirs(new_path)
            except: continue
            
        with open(CONFIG_FILE, 'w', encoding='utf-8') as f: f.write(new_path)
        return new_path

def get_next_serial(log_file):
    if not os.path.exists(log_file): return 1
    with open(log_file, 'r', encoding='utf-8') as f:
        count = sum(1 for line in f if line.strip() and line.strip()[0].isdigit())
        return count + 1

def format_size(size_bytes):
    if size_bytes == 0: return "N/A"
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0: return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0
    return "N/A"

def get_latest_file_size(folder, extension=".mp3"):
    try:
        files = [os.path.join(folder, f) for f in os.listdir(folder) if f.endswith(extension)]
        if not files: return "N/A"
        latest_file = max(files, key=os.path.getctime)
        return format_size(os.path.getsize(latest_file))
    except: return "N/A"

def update_tracker(music_folder, status, title, artist, duration, platform, link, file_size, error_cause="None"):
    tracker_folder = os.path.join(music_folder, "Youtube Music Tracker Data")
    if not os.path.exists(tracker_folder): os.makedirs(tracker_folder)
        
    tracker_file = os.path.join(tracker_folder, "Download_Tracker.txt")
    serial_no = get_next_serial(tracker_file)
    date_str = get_true_datetime().strftime("%Y-%m-%d %H:%M:%S")
    
    if not os.path.exists(tracker_file) or os.path.getsize(tracker_file) == 0:
        with open(tracker_file, 'w', encoding='utf-8') as f:
            f.write(f"{'S.No':<5} | {'Date & Time':<20} | {'Status':<8} | {'Platform':<15} | {'File Size':<10} | {'Length':<8} | {'Artist':<20} | {'Title':<45} | {'Error Cause'} \n")
            f.write("="*160 + "\n")
            
    with open(tracker_file, 'a', encoding='utf-8') as f:
        clean_artist = (artist[:17] + '...') if len(artist) > 20 else artist
        clean_title = (title[:42] + '...') if len(title) > 45 else title
        clean_error = (error_cause[:30] + '...') if len(error_cause) > 30 else error_cause
        
        row = f"{serial_no:<5} | {date_str:<20} | {status:<8} | {platform:<15} | {file_size:<10} | {duration:<8} | {clean_artist:<20} | {clean_title:<45} | {clean_error}\n"
        link_row = f"      | Link: {link}\n"
        f.write(row)
        f.write(link_row)
        f.write("-" * 160 + "\n")

def main():
    sync_online_time() 
    with open(LOCK_FILE, 'w') as f: f.write("active") 
    state = load_state()
    
    while True:
        # 1. Enforce True Non-Volatile Persistent Lockout (Top Priority)
        punish_until = state.get("punish_until", 0)
        if get_true_time() < punish_until:
            handle_sovereign_lockout(punish_until)
            # Once timer clears, remove punishment lock
            state["punish_until"] = 0
            save_state(state)
            continue # Restart loop to re-evaluate state

        clear_screen()
        
        now_dt = get_true_datetime()
        active_reset_dt = now_dt.replace(hour=4, minute=0, second=0, microsecond=0)
        if now_dt < active_reset_dt: active_reset_dt -= datetime.timedelta(days=1)
            
        if state.get("last_daily_backup", 0) < active_reset_dt.timestamp():
            execute_backup()
            state["last_daily_backup"] = get_true_time()
            save_state(state)
            
        # Standard 4:00 AM Reset Logic (Only runs if NOT punished)
        if state.get("last_activity_timestamp", 0) < active_reset_dt.timestamp():
            state["daily_video_count"] = 0
            state["usage_count"] = 0 
            save_state(state)
            
        if state.get("last_health_check", 0) < active_reset_dt.timestamp():
            clear_screen()
            print("\n" + "═"*70)
            print(" [SYSTEM] Initializing Master Backbone Health Check... Please wait.")
            print("═"*70)
            print(f" Target Engine : {os.path.basename(PRIVATE_ENGINE_PATH)}")
            time.sleep(1)

            missing_files = []
            if not YTDLP_EXE: missing_files.append("yt-dlp.exe")
            if not FFMPEG_EXE: missing_files.append("ffmpeg.exe")
            if not FFPROBE_EXE: missing_files.append("ffprobe.exe")

            if missing_files:
                print(f"\n\033[91m[CRITICAL ERROR] Missing Required Files:\033[0m {', '.join(missing_files)}")
                input("\nPress Enter to exit...")
                sys.exit(1)

            corrupted_files = []
            print(" > Verifying yt-dlp core...")
            try:
                res_yt = subprocess.run([YTDLP_EXE, '--version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, creationflags=0x08000000)
                if res_yt.returncode != 0 or not res_yt.stdout.strip()[:4].isdigit(): corrupted_files.append("yt-dlp.exe")
            except: corrupted_files.append("yt-dlp.exe")

            print(" > Verifying FFmpeg media suite...")
            try:
                res_ff = subprocess.run([FFMPEG_EXE, '-version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, creationflags=0x08000000)
                if res_ff.returncode != 0 or "ffmpeg version" not in res_ff.stdout.lower(): corrupted_files.append("ffmpeg.exe")
            except: corrupted_files.append("ffmpeg.exe")

            if corrupted_files:
                print(f"\n\033[91m[CRITICAL ERROR] Files are Corrupted:\033[0m {', '.join(corrupted_files)}")
                input("\nPress Enter to exit...")
                sys.exit(1)

            print("\n\033[92m[SUCCESS] All private backbone resources are located and connected.\033[0m")
            state["engine_health"] = True
            state["last_health_check"] = get_true_time()
            save_state(state)
            time.sleep(2)
            clear_screen()
            
        network_status = "\033[92mNetwork Connected\033[0m" if is_connected() else "\033[91mNetwork connection error\033[0m"
        current_quota = state.get('daily_video_count', 0)
        
        engine_state = "\033[92mHealthy\033[0m" if state.get("engine_health", True) else "\033[91mDamaged\033[0m"
        recovery_state = "\033[92mCloud Ready\033[0m" if is_connected() else "\033[93mLocal Offline\033[0m"
        
        print("\033[96m╔" + "═"*70 + "╗")
        print("║" + " "*70 + "║")
        print("║" + "YOUTUBE SMART MUSIC & PLAYLIST DOWNLOADER".center(70) + "║")
        print("║" + "(PRO EDITION) - VERSION 6.1".center(70) + "║")
        print("║" + " "*70 + "║")
        print("╠" + "═"*70 + "╣")
        print("║" + "By: Perk-Senpai & Google Gemini | Date Created: 15/05/2026".center(70) + "║")
        print("╚" + "═"*70 + "╝\033[0m")
        print(f" Status: {network_status}  |  \033[95mDaily Music Quota: {current_quota}/20\033[0m")
        print(f" Engine: {engine_state}  |  Recovery: {recovery_state}\n")
        
        if 15 <= current_quota < 20:
            left = 20 - current_quota
            print(f"\033[91m\033[5m !! WARNING: YOU ONLY HAVE {left} MUSIC DOWNLOADS LEFT TODAY !! \033[0m\n")
        elif current_quota >= 20:
            print(f"\033[91m\033[5m !! WARNING: YOUR DAILY QUOTA IS FULLY REACHED !! Wait for 4:00 AM reset.\033[0m\n")

        current_time = get_true_time()
        cooldown_end = state.get("cooldown_until", 0)
        
        if current_time < cooldown_end:
            remaining = int(cooldown_end - current_time)
            print("[LIMITER] Script is currently resting to prevent YouTube IP bans.")
            print("No other tasks or link pasting are available until the timer finishes.")
            countdown_timer(remaining)
            state["cooldown_until"] = 0
            save_state(state)
            continue 
            
        music_folder = get_music_folder()
        print(f"\nSaving to: \033[93m{music_folder}\033[0m")
        print("\nPaste up to 5 YouTube/YouTube Music links.")
        raw_input_str = input("\nPaste Links Here: ").strip()
        if not raw_input_str: continue

        wait_for_network()

        parsed_links = raw_input_str.replace(',', ' ').split()
        unique_links = []
        for l in parsed_links:
            clean_link = l.strip()
            if clean_link and clean_link not in unique_links: unique_links.append(clean_link)
        
        links = unique_links
        if len(links) > 5:
            print("\n[WARNING] More than 5 links detected. Only the first 5 will be processed.")
            links = links[:5]

        active_links = []
        for link in links:
            if "list=" in link:
                wants_playlist = ask_playlist_timer(link)
                if not wants_playlist:
                    update_tracker(music_folder, "SKIPPED", "N/A", "N/A", "N/A", "Playlist", link, "N/A", "User declined playlist")
                    continue
            active_links.append(link)

        if not active_links:
            input("\nNo links remaining to process. Press Enter to restart.")
            continue

        print(f"\nScanning {len(active_links)} link(s)... Please wait.")
        videos_info = []
        
        for idx, link in enumerate(active_links):
            wait_for_network()
            try:
                cmd_scan = [ YTDLP_EXE, '-J', '--flat-playlist', '--no-warnings', '--extractor-args', 'youtube:client=android,ios', link ]
                res = subprocess.run(cmd_scan, capture_output=True, text=True, encoding='utf-8', errors='ignore', creationflags=0x08000000)
                if res.returncode != 0: raise Exception(res.stderr.strip() if res.stderr else "Unknown scan error")
                info = json.loads(res.stdout)
                platform = "YouTube Music" if "music.youtube" in link.lower() else "YouTube"
                
                if 'entries' in info:
                    playlist_title = info.get('title', 'Unknown Playlist')
                    print(f"[{idx+1}] PLAYLIST DETECTED: {playlist_title} ({len(list(info.get('entries', [])))} tracks)")
                    for entry in info['entries']:
                        if not entry: continue
                        title = entry.get('title', 'Unknown Title')
                        artist = entry.get('uploader') or 'N/A'
                        duration_sec = entry.get('duration', 0)
                        duration_str = str(datetime.timedelta(seconds=duration_sec)) if duration_sec else 'N/A'
                        entry_link = entry.get('url') or entry.get('id')
                        if not entry_link.startswith('http'): entry_link = f"https://www.youtube.com/watch?v={entry_link}"
                        videos_info.append({'link': entry_link, 'title': title, 'artist': artist, 'duration': duration_str, 'platform': platform, 'playlist_folder': playlist_title })
                else:
                    title = info.get('title', 'Unknown Title')
                    artist = info.get('artist') or info.get('uploader') or 'N/A'
                    duration_sec = info.get('duration', 0)
                    duration_str = str(datetime.timedelta(seconds=duration_sec)) if duration_sec else 'N/A'
                    videos_info.append({'link': link, 'title': title, 'artist': artist, 'duration': duration_str, 'platform': platform, 'playlist_folder': None})
            except Exception as e:
                print(f"[{idx+1}] FAILED TO SCAN: {link}")
                update_tracker(music_folder, "ERROR", "N/A", "N/A", "N/A", "Unknown", link, "N/A", "Scan Failed")

        if not videos_info:
            input("\nNo valid tracks to download. Press Enter to restart.")
            continue
            
        valid_count = len(videos_info)

        if current_quota + valid_count > 20:
            allowed_slots = max(0, 20 - current_quota)
            if allowed_slots == 0:
                print(f"\n[LIMITER] Daily music quota exceeds! (Max 20/day).")
                print("A sleep timer will now activate. Please wait until 4:00 AM to reset the day quota.")
                now_dt_check = get_true_datetime()
                next_reset_dt = now_dt_check.replace(hour=4, minute=0, second=0, microsecond=0)
                if now_dt_check >= next_reset_dt: next_reset_dt += datetime.timedelta(days=1)
                state["cooldown_until"] = next_reset_dt.timestamp()
                state["last_activity_timestamp"] = get_true_time()
                save_state(state)
                time.sleep(4)
                continue 
            else:
                print(f"\n\033[91m[WARNING] You are gonna hit full daily quota!\033[0m")
                print(f"You scanned {valid_count} valid tracks, but only {allowed_slots} slot(s) remain today.")
                for i in range(allowed_slots): print(f"  {i+1}. {videos_info[i]['title']}")
                print("")
                for i in range(10, 0, -1):
                    sys.stdout.write(f"\rProceeding in {i} seconds... \033[K")
                    sys.stdout.flush()
                    time.sleep(1)
                print("\n")
                videos_info = videos_info[:allowed_slots]
                valid_count = allowed_slots
                
        print("\n" + "="*70)
        print("                   QUEUE SUMMARY")
        print("="*70)
        for idx, v in enumerate(videos_info): print(f"[{idx+1}] {v['title']}\n    Source: {v['platform']} | Artist: {v['artist']}")
        print("="*70)

        input("\nPress Enter to begin downloading the queue...")
        successful_downloads = 0

        for idx, v in enumerate(videos_info):
            print("\n" + "="*70)
            print(f"Processing ({idx+1}/{len(videos_info)}): {v['title']}")
            
            if v['playlist_folder']:
                save_path = os.path.join(music_folder, v['playlist_folder'], '%(title)s.%(ext)s')
                target_folder = os.path.join(music_folder, v['playlist_folder'])
            else:
                save_path = os.path.join(music_folder, '%(title)s.%(ext)s')
                target_folder = music_folder
            
            cmd = [
                YTDLP_EXE, '-x', '--audio-format', 'mp3', '--audio-quality', '0', 
                '--embed-thumbnail', '--embed-metadata', '--parse-metadata', 'playlist_index:%(track_number)s',
                '--extractor-args', 'youtube:client=android,ios', '--ffmpeg-location', PRIVATE_ENGINE_PATH, 
                '--no-warnings', '-o', save_path, v['link']
            ]
            success = False
            error_reason = "None"
            
            for attempt in range(1, 4):
                wait_for_network()
                try:
                    if attempt > 1: print(f"-> Retry Attempt {attempt}/3...")
                    subprocess.run(cmd, check=True, capture_output=True, text=True, encoding='utf-8', errors='ignore', creationflags=0x08000000)
                    success = True
                    break 
                except subprocess.CalledProcessError as e:
                    error_out = e.stderr.strip() if e.stderr else str(e)
                    error_reason = "Unknown Error"
                    for line in error_out.split('\n'):
                        if "ERROR:" in line:
                            error_reason = line.split("ERROR:")[-1].strip()
                            break
                    print(f"\033[91m[ERROR] Attempt {attempt} failed: {error_reason}\033[0m")
                    time.sleep(2)
            
            if success:
                successful_downloads += 1
                file_size = get_latest_file_size(target_folder)
                update_tracker(music_folder, "SUCCESS", v['title'], v['artist'], v['duration'], v['platform'], v['link'], file_size, "None")
                print(f"SUCCESS: Logged to Tracker. Final Size: {file_size}")
            else:
                print(f"\n[CRITICAL] Failed 3 times. Bypassing track: {v['title']}")
                update_tracker(music_folder, "ERROR", v['title'], v['artist'], v['duration'], v['platform'], v['link'], "N/A", error_reason)

        print("\n" + "="*70)
        print("ALL TASKS COMPLETE! Tracker data has been updated.")
        
        force_success_backup = False
        if successful_downloads > 0:
            if not os.path.exists(BACKUP_DIR): force_success_backup = True
            else:
                has_success = any(f.endswith("- Success Run") for f in os.listdir(BACKUP_DIR) if os.path.isdir(os.path.join(BACKUP_DIR, f)))
                if not has_success: force_success_backup = True

        if successful_downloads > 0 and (force_success_backup or state.get("last_success_backup", 0) < active_reset_dt.timestamp()):
            execute_backup(" - Success Run")
            state["last_success_backup"] = get_true_time()
            print("\n\033[92m[SYSTEM] 'Success Run' Snapshot safely archived to vault.\033[0m")
        
        state["usage_count"] = state.get("usage_count", 0) + 1
        state["daily_video_count"] = state.get("daily_video_count", 0) + successful_downloads
        state["last_activity_timestamp"] = get_true_time()
        
        if state["usage_count"] >= 10:
            state["cooldown_until"] = get_true_time() + (5 * 3600)
            state["usage_count"] = 0 
            print("\n[LIMITER] 10 continuous uses reached! 5-Hour sleep timer activated.")
        elif successful_downloads >= 5:
            state["cooldown_until"] = get_true_time() + 300 
            print("\n[LIMITER] 5 valid tracks successfully processed! 5-Minute sleep timer activated.")
        elif successful_downloads == 4:
            state["cooldown_until"] = get_true_time() + 150 
            print("\n[LIMITER] 4 valid tracks successfully processed! 2.5-Minute sleep timer activated.")
        elif successful_downloads == 3:
            state["cooldown_until"] = get_true_time() + 60  
            print("\n[LIMITER] 3 valid tracks successfully processed! 1-Minute sleep timer activated.")
        elif successful_downloads in [1, 2]:
            state["cooldown_until"] = get_true_time() + 10 
            print(f"\n[LIMITER] {successful_downloads} valid track(s) successfully processed! 10-Second sleep timer activated.")
            
        save_state(state)
        input("Press Enter to download more music...")

if __name__ == "__main__":
    try: main()
    except KeyboardInterrupt:
        remove_lock()
        print("\n\n\033[93m[!] Process terminated by user.\033[0m")
        sys.exit(0)
