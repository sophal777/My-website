import subprocess
import time
import json
import uiautomator2 as u2

ADB_PATH = r"C:\platform-tools\adb.exe"
SURFSHARK = "com.surfshark.vpnclient.android"
FACEBOOK = "com.facebook.katana"
TARGET_CITY = "Los Angeles"


def connect_device():
    # ស្វែងរក Device ដំបូងគេ រួចភ្ជាប់តាមរយៈ uiautomator2
    try:
        res = subprocess.run(f'"{ADB_PATH}" devices', shell=True, capture_output=True, text=True).stdout
        lines = res.strip().splitlines()[1:]
        device_id = None
        for line in lines:
            if "\tdevice" in line:
                device_id = line.split()[0]
                break
        
        if not device_id:
            print("[-] No device found!")
            return None

        device = u2.connect(device_id)
        print(f"[+] Connected to: {device_id} (uiautomator2)")
        return device
    except Exception as e:
        print(f"[Error] Failed to connect: {e}")
        return None


def click_safe(device, text_pht, timeout=15):
    # ចុចលើ Element ដោយសុវត្ថិភាព និងទប់ទល់ពេល UI Dump គាំង
    end_time = time.time() + timeout
    text_lower = text_pht.lower()
    xpath = f'//*[translate(@text, "ABCDEFGHIJKLMNOPQRSTUVWXYZ", "abcdefghijklmnopqrstuvwxyz")="{text_lower}" or translate(@content-desc, "ABCDEFGHIJKLMNOPQRSTUVWXYZ", "abcdefghijklmnopqrstuvwxyz")="{text_lower}"]'

    while time.time() < end_time:
        try:
            if device(text=text_pht).exists:
                time.sleep(0.5)
                device(text=text_pht).click()
                return True

            if device.xpath(xpath).exists:
                time.sleep(0.5)
                device.xpath(xpath).click()
                return True
        except Exception:
            time.sleep(1)

        time.sleep(0.4)
    return False


def get_device_city(device):
    # ឆែកមើល IP និងទីក្រុងជាក់ស្ដែងលើទូរសព្ទតាមរយៈ curl
    try:
        cmd_ip = device.shell("curl -s --max-time 10 https://api.ipify.org").output.strip()
        if not cmd_ip or " " in cmd_ip or len(cmd_ip) > 45:
            return "Unknown"

        cmd_city = device.shell(f"curl -s --max-time 10 http://ip-api.com/json/{cmd_ip}?fields=status,city").output.strip()
        data = json.loads(cmd_city)
        if data.get("status") == "success":
            return data.get("city", "Unknown")
    except Exception as e:
        print(f"[-] Geolocation check error: {e}")
    return "Unknown"


def ensure_vpn_connected(device, max_retries=5):
    # ភ្ជាប់ និងផ្ទៀងផ្ទាត់ VPN ប្រសិនបើខុស នឹងបិទ App រួចបើកភ្ជាប់ម្ដងទៀត
    for attempt in range(1, max_retries + 1):
        print(f"\n[*] [Attempt {attempt}/{max_retries}] Launching Surfshark to connect VPN...")
        
        # បើកកម្មវិធី Surfshark
        device.app_start(SURFSHARK)
        time.sleep(3)
        
        # ចុច Connect ឬ Quick Connect
        if not click_safe(device, "Connect", timeout=8):
            click_safe(device, "Quick Connect", timeout=5)

        print("[*] Waiting for VPN connection to establish (12s)...")
        time.sleep(17)

        # ឆែកទីក្រុងជាក់ស្ដែងលើទូរសព្ទ
        current_city = get_device_city(device)
        print(f"[+] Detected city on device: {current_city}")

        # លក្ខខណ្ឌផ្ទៀងផ្ទាត់ទីក្រុង
        if current_city == TARGET_CITY:
            print(f"[✓] Correct city matched: {TARGET_CITY}!")
            return True
        else:
            print(f"[!] Incorrect city (Got: {current_city}). Force stopping app and retrying...")
            # បង្ខំបិទ App ទាំងស្រុងដើម្បី Reset
            device.app_stop(SURFSHARK)
            time.sleep(2)

    print(f"\n[-] Reached maximum retries ({max_retries}). Failed to get {TARGET_CITY}.")
    return False


# --- ចាប់ផ្ដើមដំណើរការស្គ្រីប ---
device = connect_device()
if device:
    try:
        device.reset_uiautomator()
        time.sleep(2)
    except Exception:
        pass

    # ១. ត្រួតពិនិត្យទីក្រុងបច្ចុប្បន្នលើ Device ជាមុនសិន
    initial_city = get_device_city(device)
    print(f"[*] Initial city detected on device: {initial_city}")

    # ២. ពិនិត្យលក្ខខណ្ឌទីក្រុង
    if initial_city == "Los Angeles":
        print("[+] Device is already in Los Angeles. Launching Facebook...")
        device.app_start(FACEBOOK)
        time.sleep(4)
        
        # ដាក់កូដដំណើរការលើ Facebook របស់អ្នកនៅទីនេះ

    elif initial_city == "Phnom Penh" or initial_city != "Los Angeles":
        print(f"[!] Current city is '{initial_city}'. Launching Surfshark to switch VPN...")
        
        # ដំណើរការភ្ជាប់ VPN រហូតដល់បាន Los Angeles
        is_vpn_valid = ensure_vpn_connected(device, max_retries=5)

        if is_vpn_valid:
            print("[+] VPN connected successfully to Los Angeles! Opening Facebook...")
            device.app_start(FACEBOOK)
            time.sleep(4)
            
            # ដាក់កូដដំណើរការលើ Facebook របស់អ្នកនៅទីនេះ
        else:
            print("[-] VPN connection failed. Aborting Facebook launch.")
