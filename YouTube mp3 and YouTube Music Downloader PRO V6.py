import os
import sys
import time
import glob
import shutil
import datetime
import socket

# --- CONFIGURATION & PATH SYNC ---
HEALER_DIR = os.path.dirname(os.path.abspath(__file__))
MAIN_SCRIPT_DIR = HEALER_DIR 
MAIN_SCRIPT_NAME = "YouTube mp3 and YouTube Music Downloader PRO V6.py"
MAIN_SCRIPT_PATH = os.path.join(MAIN_SCRIPT_DIR, MAIN_SCRIPT_NAME)

LOG_FILE_CSV = os.path.join(HEALER_DIR, "Music_Heal_Logs.csv")
CRASH_REPORT_DIR = os.path.join(MAIN_SCRIPT_DIR, "Music_Script_Error_Data")

APPDATA_DIR = os.getenv('APPDATA')
BACKUP_DIR = os.path.join(APPDATA_DIR, 'yt-dlp', 'Music_Script_Backup_Files')
LOCK_FILE = os.path.join(APPDATA_DIR, 'yt-dlp', 'session.lock')

# =========================================================================
# PUBLIC RECOVERY ENGINE CONFIGURATION 
# =========================================================================
ONLINE_MASTER_URL = "https://raw.githubusercontent.com/ParthiPatra/Youtube-Music-Downloader-Backbone/refs/heads/main/YouTube%20mp3%20and%20YouTube%20Music%20Downloader%20PRO%20V6.py"

os.system('') # Enable ANSI colors

def loading_animation(text, duration=2.0):
    chars = "|/-\\"
    end_time = time.time() + duration
    i = 0
    while time.time() < end_time:
        sys.stdout.write(f"\r\033[96m[{chars[i % len(chars)]}]\033[0m {text}...")
        sys.stdout.flush()
        time.sleep(0.1)
        i += 1
    sys.stdout.write(f"\r\033[92m[DONE]\033[0m {text}...          \n")

def is_connected():
    try:
        socket.create_connection(("8.8.8.8", 53), timeout=2)
        return True
    except OSError:
        return False

def write_heal_log(cause, action_taken, success, method):
    file_exists = os.path.isfile(LOG_FILE_CSV)
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE_CSV, 'a', encoding='utf-8') as f:
        if not file_exists: f.write("Date & Time,Crash Cause,Action Taken,Success,Heal Method\n")
        f.write(f'"{timestamp}","{cause}","{action_taken}","{success}","{method}"\n')

def get_latest_crash_log():
    if not os.path.exists(CRASH_REPORT_DIR): return None
    logs = glob.glob(os.path.join(CRASH_REPORT_DIR, 'Error_Crash_Handler_*.txt'))
    return max(logs, key=os.path.getctime) if logs else None

def analyze_crash():
    latest_log = get_latest_crash_log()
    cause = "Unknown Structural/Syntax Error"
    if latest_log:
        with open(latest_log, 'r', encoding='utf-8') as f:
            content = f.read()
            if "SyntaxError" in content or "IndentationError" in content: cause = "Corrupted Code Structure (Syntax)"
            elif "ModuleNotFoundError" in content: cause = "Missing Core Dependency"
            elif "PermissionError" in content: cause = "System Locked File (Permission Denied)"
            elif "FileNotFoundError" in content: cause = "Target System File Deleted or Missing"
            else: cause = "Runtime Execution Failure"
    return cause

def diagnose_backbone():
    PARENT_DIR = os.path.dirname(MAIN_SCRIPT_DIR)
    GRANDPARENT_DIR = os.path.dirname(PARENT_DIR)
    engine_folders = glob.glob(os.path.join(MAIN_SCRIPT_DIR, "Python v* file"))
    if not engine_folders: engine_folders = glob.glob(os.path.join(PARENT_DIR, "Python v* file"))
    if not engine_folders: engine_folders = glob.glob(os.path.join(GRANDPARENT_DIR, "Python v* file"))
    if not engine_folders: return False, "Complete Python Engine Missing"
    engine_path = engine_folders[0]
    missing = []
    if not glob.glob(os.path.join(engine_path, "*yt-dlp*.exe")): missing.append("yt-dlp.exe")
    if not glob.glob(os.path.join(engine_path, "*ffmpeg*.exe")): missing.append("ffmpeg.exe")
    if not os.path.exists(os.path.join(engine_path, "python.exe")): missing.append("python.exe")
    return (True, "Backbone Intact") if not missing else (False, f"Missing core binaries: {', '.join(missing)}")

def test_script_health(script_path):
    if not os.path.exists(script_path): return False
    try:
        with open(script_path, 'r', encoding='utf-8') as f: source = f.read()
        compile(source, script_path, 'exec')
        return True
    except: return False

# ==========================================
# ADVANCED OFFLINE HEALING (SUCCESS-PRIORITY)
# ==========================================
def heal_from_offline_vault():
    if not os.path.exists(BACKUP_DIR):
        return False
    
    all_backups = glob.glob(os.path.join(BACKUP_DIR, '*\\*.py'))
    if not all_backups:
        return False
        
    success_backups = []
    standard_backups = []
    
    # Sort into Priority and Standard lists based on folder name
    for backup in all_backups:
        folder_name = os.path.basename(os.path.dirname(backup))
        if folder_name.endswith("- Success Run"):
            success_backups.append(backup)
        else:
            standard_backups.append(backup)
            
    # Sort both lists individually by newest creation time first
    success_backups.sort(key=os.path.getctime, reverse=True)
    standard_backups.sort(key=os.path.getctime, reverse=True)
    
    # Combine them (Success runs are ALWAYS checked and restored first)
    prioritized_backups = success_backups + standard_backups
    
    print(f"    > Found {len(prioritized_backups)} offline snapshots in the Vault ({len(success_backups)} Priority Success Runs). Validating...")
    
    for backup in prioritized_backups:
        if test_script_health(backup):
            try:
                shutil.copy2(backup, MAIN_SCRIPT_PATH)
                folder_used = os.path.basename(os.path.dirname(backup))
                if folder_used.endswith("- Success Run"):
                    print(f"    > \033[92mValidated and applied pristine Priority Snapshot: {folder_used}\033[0m")
                else:
                    print(f"    > \033[92mValidated and applied pristine snapshot: {folder_used}\033[0m")
                return True
            except:
                continue
    return False

def heal_from_online_source():
    if not is_connected():
        print("    \033[91m[!] Online Support Failed: No active internet connection detected.\033[0m")
        return False
    print("    > Contacting Online Public Master Repository Vault...")
    temp_file = os.path.join(HEALER_DIR, "temp_online_script.py")
    curl_cmd = f'curl -s -L -o "{temp_file}" "{ONLINE_MASTER_URL}"'
    ps_cmd = f'powershell -Command "Invoke-WebRequest -Uri \'{ONLINE_MASTER_URL}\' -OutFile \'{temp_file}\'"'
    os.system(curl_cmd)
    if not os.path.exists(temp_file) or os.path.getsize(temp_file) == 0: os.system(ps_cmd)
    if not os.path.exists(temp_file) or os.path.getsize(temp_file) == 0:
        print("    \033[91m[!] Failed to connect to the cloud master file stream.\033[0m")
        return False
    print("    > Download complete. Running sandbox code compilation checks...")
    if test_script_health(temp_file):
        try:
            shutil.copy2(temp_file, MAIN_SCRIPT_PATH)
            if not os.path.exists(BACKUP_DIR): os.makedirs(BACKUP_DIR)
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            online_backup_folder = os.path.join(BACKUP_DIR, f"{timestamp} - Online_Backup_File")
            os.makedirs(online_backup_folder, exist_ok=True)
            shutil.copy2(temp_file, os.path.join(online_backup_folder, MAIN_SCRIPT_NAME))
            
            existing_vault_folders = sorted(glob.glob(os.path.join(BACKUP_DIR, "*")), key=os.path.getctime, reverse=True)
            if len(existing_vault_folders) > 10:
                for old_folder in existing_vault_folders[10:]:
                    try: shutil.rmtree(old_folder)
                    except: pass
            
            os.remove(temp_file)
            print("    > \033[92mSuccess: Compiled and applied pristine public master snapshot.\033[0m")
            print(f"    > \033[94m[VAULT UPDATED] Cloud copy saved locally as: {timestamp} - Online_Backup_File\033[0m")
            return True
        except: pass
    if os.path.exists(temp_file): os.remove(temp_file)
    return False

def purge_ghost_files():
    if os.path.exists(LOCK_FILE):
        try: os.remove(LOCK_FILE)
        except: pass
    pycache_dir = os.path.join(MAIN_SCRIPT_DIR, "__pycache__")
    if os.path.exists(pycache_dir):
        try: shutil.rmtree(pycache_dir)
        except: pass

def run_healer(is_auto=False):
    print("\033[96m========================================================\033[0m")
    print("\033[96m           NEXT-GEN OFFLINE & ONLINE EMERGENCY HEALER   \033[0m")
    print("\033[96m========================================================\033[0m")
    if is_auto:
        print("\n\033[93m[AUTO-MODE] Healer was triggered dynamically by a script crash.\033[0m")
        print(" > Purging ghost locks and corrupted memory caches...")
        purge_ghost_files()
    else:
        print("\n\033[93m[MANUAL OVERRIDE] User directly initiated the Emergency Healer.\033[0m")
        loading_animation("Initializing Deep Scan & Memory Allocation", 2.0)
        purge_ghost_files()
        loading_animation("Purging ghost locks and corrupted caches", 1.5)
    print("\n\033[93m[STEP 1] Diagnosing External Environment...\033[0m")
    if not is_auto: loading_animation("Verifying Core Engine Backbone Integrity", 2.0)
    backbone_ok, backbone_msg = diagnose_backbone()
    if not backbone_ok:
        print(f"\n\033[91m[CRITICAL] Backbone Error: {backbone_msg}\033[0m")
        print("\033[93mThe script code is likely fine, but your media tools are missing.\033[0m")
        print(">> FIX: Please run 'Setup.bat' to re-download the missing components.")
        input("\nPress Enter to exit the Healer...")
        return
    print(" > \033[92mEnvironment Verified: All core engines are active.\033[0m")
    if is_auto:
        print("\n\033[93m[STEP 2] Analyzing Crash Reports...\033[0m")
        cause = analyze_crash()
        print(f" > Identified Cause: \033[95m{cause}\033[0m")
    else: cause = "Manual Scan Requested"
    print("\n\033[93m[STEP 3] Testing Main Script Structural Health...\033[0m")
    if not is_auto: loading_animation("Compiling Main Script Syntax & Code Validation", 3.0)
    if test_script_health(MAIN_SCRIPT_PATH):
        if not is_auto:
            print("\n\033[92m========================================================================================\033[0m")
            print("\033[92mYour 'YouTube mp3 and YouTube Music Downloader PRO V6' is totally fine and healthy. no issues found.\033[0m")
            print("\033[92m========================================================================================\033[0m")
        else:
            print("\n\033[92m[HEALTHY] The main music script is structurally intact.\033[0m")
            print("No code healing is required.")
        input("\nPress Enter to exit...")
        return
    print("\n\033[91m[!] CODE DAMAGE DETECTED. Initiating Recovery Protocols...\033[0m")
    time.sleep(1)
    method_used, heal_success = "None", False
    print("\n--> Accessing [OFFLINE VAULT RECOVERY]...")
    if heal_from_offline_vault():
        print("    \033[92m[SUCCESS] Restored from local validated backup.\033[0m")
        method_used, heal_success = "Offline Vault Backup", True
    else:
        print("    \033[91m[FAILED] No valid local backups found in the vault.\033[0m")
        print("\n--> Accessing [ONLINE RECOVERY Vault]...")
        if heal_from_online_source():
            print("    \033[92m[SUCCESS] Restored from Cloud Master Repository.\033[0m")
            method_used, heal_success = "Public Cloud Support", True
        else:
            print("    \033[91m[FAILED] Cloud recovery unavailable or connection dropped.\033[0m")
    if heal_success:
        print("\nVerifying applied repairs...")
        if test_script_health(MAIN_SCRIPT_PATH):
            print("\n\033[92m========================================================\033[0m")
            print("\033[92m[SUCCESS] The script has been completely healed!\033[0m")
            print("\033[92m========================================================\033[0m")
            write_heal_log(cause, "Overwrote corrupted file with pristine code", "Yes", method_used)
        else:
            print("\n\033[91m[CRITICAL] Repair applied, but structural damage persists.\033[0m")
            write_heal_log(cause, "Applied repair, but test failed", "No", method_used)
    else:
        print("\n\033[91m[FATAL] ALL RECOVERY SYSTEMS FAILED. Manual script replacement required.\033[0m")
        write_heal_log(cause, "Failed to find valid code source locally or online", "No", method_used)
    print("\nLogs have been updated in: Music_Heal_Logs.csv")
    input("\nPress Enter to exit the Healer module...")

if __name__ == "__main__":
    run_healer(len(sys.argv) > 1 and sys.argv[1].upper() == "AUTO_TRIGGER")
