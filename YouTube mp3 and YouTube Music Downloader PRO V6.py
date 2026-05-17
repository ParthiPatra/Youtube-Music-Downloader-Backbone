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
    
    # User-Requested Folder Structure
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
    
    # RELOCATED PATH: Smart locator for the healer script (Deep Sweep)
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
        subprocess.Popen(['start', 'cmd', '/c', sys.executable, healer_path, "AUTO_TRIGGER"], shell=True)
    else:
        print("\n[WARNING] 'Music_Crash_Healer.py' not found. Cannot auto-heal.")
        
    input("\nPress Enter to safely close this window...")

# Bind the global crash handler
sys.excepthook = lambda t, v, tb: trigger_crash_report(t, v, tb)

# ==========================================
# CORE NETWORK HELPERS
# ==========================================
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
# DYNAMIC BACKBONE CONNECTION ENGINE (SMART PATH UPDATED)
# ==========================================
PARENT_DIR = os.path.dirname(SCRIPT_DIR)
GRANDPARENT_DIR = os.path.dirname(PARENT_DIR)

PRIVATE_ENGINE_PATH = None

# Strategy 1: Instant Handshake. If the Watchdog launched this, sys.executable is already correct.
EXEC_DIR = os.path.dirname(sys.executable)
if os.path.exists(os.path.join(EXEC_DIR, "python.exe")) and os.path.exists(os.path.join(EXEC_DIR, "ffmpeg.exe")):
    PRIVATE_ENGINE_PATH = EXEC_DIR

# Strategy 2: Deep Sweep Search. Searches up to 2 levels out for the Holy Trinity of files.
if not PRIVATE_ENGINE_PATH:
    for search_dir in [SCRIPT_DIR, PARENT_DIR, GRANDPARENT_DIR]:
        if PRIVATE_ENGINE_PATH: break
        for root, dirs, files in os.walk(search_dir):
            if "Setup_and_Update_Logs" in root:
                continue
            files_lower = [f.lower() for f in files]
            # Ensure it is OUR specific environment by checking for multiple core files
            if "python.exe" in files_lower and "ffmpeg.exe" in files_lower:
                PRIVATE_ENGINE_PATH = root
                break

if not PRIVATE_ENGINE_PATH:
    print("\n\033[91m[CRITICAL ERROR] Core Engine Backbone NOT FOUND!\033[0m")
    print("The private environment is completely missing from this folder.")
    print(">>> Please manually start 'Setup_and_Update.bat' to download the missing files.")
    input("\nPress Enter to exit...")
    sys.exit(1)

PRIVATE_PYTHON = os.path.join(PRIVATE_ENGINE_PATH, "python.exe")

# --- SMART NAMING LOCATOR ---
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

# 1. Enforce Execution via Private Python Bubble
if os.path.normpath(sys.executable) != os.path.normpath(PRIVATE_PYTHON):
    if not os.path.exists(PRIVATE_PYTHON):
        print("\n\033[91m[CRITICAL ERROR] python.exe is missing from the engine folder.\033[0m")
        print(">>> Please start 'Setup_and_Update.bat' file for diagnosis.")
        input("\nPress Enter to exit...")
        sys.exit(1)
    subprocess.run([PRIVATE_PYTHON, __file__] + sys.argv[1:])
    sys.exit(0)

# ==========================================
# INITIALIZATION & CONFIGURATION
# ==========================================
SCRIPT_VERSION = 6.0

APPDATA_DIR = os.getenv('APPDATA')
CONFIG_DIR = os.path.join(APPDATA_DIR, 'yt-dlp')
CONFIG_FILE = os.path.join(CONFIG_DIR, 'music_config.txt')
STATE_FILE = os.path.join(CONFIG_DIR, 'music_usage_state.json')
BACKUP_DIR = os.path.join(CONFIG_DIR, 'Music_Script_Backup_Files') 
LOCK_FILE = os.path.join(CONFIG_DIR, 'session.lock')

if not os.path.exists(CONFIG_DIR):
    try:
        os.makedirs(CONFIG_DIR)
    except Exception as e:
        print(f"[CRITICAL ERROR] Could not create config folder in AppData: {e}")
        input("Press Enter to exit...")
        sys.exit(1)

def remove_lock():
    if os.path.exists(LOCK_FILE):
        try: os.remove(LOCK_FILE)
        except: pass

atexit.register(remove_lock)

# ==========================================
# NEW EVENT-DRIVEN BACKUP SYSTEM
# ==========================================
def execute_backup(suffix=""):
    if not os.path.exists(BACKUP_DIR):
        os.makedirs(BACKUP_DIR, exist_ok=True)
        
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    folder_name = f"{timestamp}{suffix}"
    current_backup_folder = os.path.join(BACKUP_DIR, folder_name)
    os.makedirs(current_backup_folder, exist_ok=True)
    try:
        shutil.copy2(__file__, os.path.join(current_backup_folder, os.path.basename(__file__)))
    except Exception:
        pass

# ==========================================
# CORE SCRIPT LOGIC
# ==========================================
def load_state():
    default_state = {
        "usage_count": 0, "cooldown_until": 0.0, "daily_video_count": 0, 
        "last_activity_timestamp": 0, "last_health_check": 0, "engine_health": True,
        "last_daily_backup": 0, "last_success_backup": 0
    }
    if os.path.exists(STATE_FILE):
        try:
            with open(STATE_FILE, 'r') as f:
                data = json.load(f)
                for k, v in default_state.items():
                    if k not in data: data[k] = v
                return data
        except:
            pass
    return default_state

def save_state(state):
    with open(STATE_FILE, 'w') as f:
        json.dump(state, f)

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
        with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
            saved_path = f.read().strip()
        if os.path.exists(saved_path):
            return saved_path
        else:
            print(f"\n[WARNING] Saved download folder is missing: {saved_path}")

    while True:
        print("\nDownload folder missing or not set.")
        new_path = input("Please paste the full path to your desired Music folder: ").strip()
        new_path = new_path.strip('"').strip("'")
        
        if new_path:
            if not os.path.exists(new_path):
                print(f"Folder does not exist. Creating: {new_path}")
                try:
                    os.makedirs(new_path)
                except Exception as e:
                    print(f"Error creating folder: {e}. Please try a different path.")
                    continue
            
            with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
                f.write(new_path)
            return new_path

def get_next_serial(log_file):
    if not os.path.exists(log_file):
        return 1
    with open(log_file, 'r', encoding='utf-8') as f:
        count = sum(1 for line in f if line.strip() and line.strip()[0].isdigit())
        return count + 1

def format_size(size_bytes):
    if size_bytes == 0: return "N/A"
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0
    return "N/A"

def get_latest_file_size(folder, extension=".mp3"):
    try:
        files = [os.path.join(folder, f) for f in os.listdir(folder) if f.endswith(extension)]
        if not files: return "N/A"
        latest_file = max(files, key=os.path.getctime)
        return format_size(os.path.getsize(latest_file))
    except:
        return "N/A"

def update_tracker(music_folder, status, title, artist, duration, platform, link, file_size, error_cause="None"):
    tracker_folder = os.path.join(music_folder, "Youtube Music Tracker Data")
    if not os.path.exists(tracker_folder):
        os.makedirs(tracker_folder)
        
    tracker_file = os.path.join(tracker_folder, "Download_Tracker.txt")
    serial_no = get_next_serial(tracker_file)
    date_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
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
    with open(LOCK_FILE, 'w') as f: f.write("active") 
    state = load_state()
    
    while True:
        clear_screen()
        
        now_dt = datetime.datetime.now()
        active_reset_dt = now_dt.replace(hour=4, minute=0, second=0, microsecond=0)
        if now_dt < active_reset_dt:
            active_reset_dt -= datetime.timedelta(days=1)
            
        # 1. NEW DAILY BACKUP TRIGGER
        if state.get("last_daily_backup", 0) < active_reset_dt.timestamp():
            execute_backup()
            state["last_daily_backup"] = time.time()
            save_state(state)
            
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
                print("Your private environment is incomplete.")
                print("\033[93m>>> Please manually start 'Setup_and_Update.bat' to download the missing files.\033[0m")
                input("\nPress Enter to exit...")
                sys.exit(1)

            corrupted_files = []
            
            print(" > Verifying yt-dlp core...")
            try:
                res_yt = subprocess.run([YTDLP_EXE, '--version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, creationflags=0x08000000)
                if res_yt.returncode != 0 or not res_yt.stdout.strip()[:4].isdigit(): 
                    corrupted_files.append("yt-dlp.exe")
            except Exception:
                corrupted_files.append("yt-dlp.exe")

            print(" > Verifying FFmpeg media suite...")
            try:
                res_ff = subprocess.run([FFMPEG_EXE, '-version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, creationflags=0x08000000)
                if res_ff.returncode != 0 or "ffmpeg version" not in res_ff.stdout.lower():
                    corrupted_files.append("ffmpeg.exe")
            except Exception:
                corrupted_files.append("ffmpeg.exe")

            if corrupted_files:
                print(f"\n\033[91m[CRITICAL ERROR] Files are Corrupted:\033[0m {', '.join(corrupted_files)}")
                print("\033[93m>>> Please start setup file for diagnosis.\033[0m")
                input("\nPress Enter to exit...")
                sys.exit(1)

            print("\n\033[92m[SUCCESS] All private backbone resources are located and connected.\033[0m")
            state["engine_health"] = True
            state["last_health_check"] = time.time()
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
        print("║" + "(PRO EDITION) - VERSION 6".center(70) + "║")
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

        current_time = time.time()
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
        print("(You can separate links with commas or just spaces)")
        
        raw_input_str = input("\nPaste Links Here: ").strip()
        if not raw_input_str:
            continue

        wait_for_network()

        parsed_links = raw_input_str.replace(',', ' ').split()
        unique_links = []
        for l in parsed_links:
            clean_link = l.strip()
            if clean_link and clean_link not in unique_links:
                unique_links.append(clean_link)
        
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
                cmd_scan = [
                    YTDLP_EXE,
                    '-J', 
                    '--flat-playlist',
                    '--no-warnings',
                    '--extractor-args', 'youtube:client=android,ios',
                    link
                ]
                
                res = subprocess.run(cmd_scan, capture_output=True, text=True, encoding='utf-8', errors='ignore', creationflags=0x08000000)
                
                if res.returncode != 0:
                    error_msg = res.stderr.strip() if res.stderr else "Unknown scan error"
                    raise Exception(error_msg)
                    
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
                        if not entry_link.startswith('http'):
                            entry_link = f"https://www.youtube.com/watch?v={entry_link}"
                        
                        videos_info.append({
                            'link': entry_link,
                            'title': title,
                            'artist': artist,
                            'duration': duration_str,
                            'platform': platform,
                            'playlist_folder': playlist_title 
                        })
                else:
                    title = info.get('title', 'Unknown Title')
                    artist = info.get('artist') or info.get('uploader') or 'N/A'
                    duration_sec = info.get('duration', 0)
                    duration_str = str(datetime.timedelta(seconds=duration_sec)) if duration_sec else 'N/A'
                    
                    videos_info.append({
                        'link': link,
                        'title': title,
                        'artist': artist,
                        'duration': duration_str,
                        'platform': platform,
                        'playlist_folder': None
                    })
            
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
                now_dt_check = datetime.datetime.now()
                next_reset_dt = now_dt_check.replace(hour=4, minute=0, second=0, microsecond=0)
                if now_dt_check >= next_reset_dt: next_reset_dt += datetime.timedelta(days=1)
                state["cooldown_until"] = next_reset_dt.timestamp()
                state["last_activity_timestamp"] = time.time()
                save_state(state)
                time.sleep(4)
                continue 
            else:
                print(f"\n\033[91m[WARNING] You are gonna hit full daily quota!\033[0m")
                print(f"You scanned {valid_count} valid tracks (including playlists), but only {allowed_slots} slot(s) remain today.")
                print("Only the following track(s) will proceed:")
                for i in range(allowed_slots):
                    print(f"  {i+1}. {videos_info[i]['title']}")
                
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
        for idx, v in enumerate(videos_info):
             print(f"[{idx+1}] {v['title']}\n    Source: {v['platform']} | Artist: {v['artist']}")
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
                YTDLP_EXE, 
                '-x', 
                '--audio-format', 'mp3', 
                '--audio-quality', '0', 
                '--embed-thumbnail', 
                '--embed-metadata', 
                '--parse-metadata', 'playlist_index:%(track_number)s',
                '--extractor-args', 'youtube:client=android,ios',
                '--ffmpeg-location', PRIVATE_ENGINE_PATH, 
                '--no-warnings',
                '-o', save_path,
                v['link']
            ]
            
            success = False
            error_reason = "None"
            
            for attempt in range(1, 4):
                wait_for_network()
                try:
                    if attempt > 1:
                        print(f"-> Retry Attempt {attempt}/3...")
                        
                    result = subprocess.run(cmd, check=True, capture_output=True, text=True, encoding='utf-8', errors='ignore', creationflags=0x08000000)
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
                update_tracker(
                    music_folder=music_folder, status="SUCCESS", title=v['title'], 
                    artist=v['artist'], duration=v['duration'], platform=v['platform'], 
                    link=v['link'], file_size=file_size, error_cause="None"
                )
                print(f"SUCCESS: Logged to Tracker. Final Size: {file_size}")
            else:
                print(f"\n[CRITICAL] Failed 3 times. Bypassing track: {v['title']}")
                update_tracker(
                    music_folder=music_folder, status="ERROR", title=v['title'], 
                    artist=v['artist'], duration=v['duration'], platform=v['platform'], 
                    link=v['link'], file_size="N/A", error_cause=error_reason
                )

        print("\n" + "="*70)
        print("ALL TASKS COMPLETE! Tracker data has been updated.")
        
        # 2. NEW SUCCESS RUN BACKUP TRIGGER
        if successful_downloads > 0 and state.get("last_success_backup", 0) < active_reset_dt.timestamp():
            execute_backup(" - Success Run")
            state["last_success_backup"] = time.time()
            print("\n\033[92m[SYSTEM] 'Success Run' Snapshot safely archived to vault.\033[0m")
        
        state["usage_count"] = state.get("usage_count", 0) + 1
        state["daily_video_count"] = state.get("daily_video_count", 0) + successful_downloads
        state["last_activity_timestamp"] = time.time()
        
        if state["usage_count"] >= 10:
            state["cooldown_until"] = time.time() + (5 * 3600)
            state["usage_count"] = 0 
            print("\n[LIMITER] 10 continuous uses reached! 5-Hour sleep timer activated.")
        elif successful_downloads >= 5:
            state["cooldown_until"] = time.time() + 300 
            print("\n[LIMITER] 5 valid tracks successfully processed! 5-Minute sleep timer activated.")
        elif successful_downloads == 4:
            state["cooldown_until"] = time.time() + 150 
            print("\n[LIMITER] 4 valid tracks successfully processed! 2.5-Minute sleep timer activated.")
        elif successful_downloads == 3:
            state["cooldown_until"] = time.time() + 60  
            print("\n[LIMITER] 3 valid tracks successfully processed! 1-Minute sleep timer activated.")
        elif successful_downloads in [1, 2]:
            state["cooldown_until"] = time.time() + 10 
            print(f"\n[LIMITER] {successful_downloads} valid track(s) successfully processed! 10-Second sleep timer activated.")
            
        save_state(state)
        
        input("Press Enter to download more music...")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        remove_lock()
        print("\n\n\033[93m[!] Process terminated by user.\033[0m")
        sys.exit(0)
