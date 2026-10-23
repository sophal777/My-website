import subprocess
import re
import time
import uiautomator2 as u2
import random
import string

ADB_PATH = r"C:\platform-tools\adb.exe"
package = "com.facebook.katana"


# --- ១. កូដភ្ជាប់ Device (ប្រើ u2.connect) ---
def connect_device():
    """ស្វែងរក Device ដំបូងគេ រួចភ្ជាប់តាមរយៈ uiautomator2"""
    try:
        res = subprocess.run(f'"{ADB_PATH}" devices', shell=True, capture_output=True, text=True).stdout
        lines = res.strip().splitlines()[1:]
        device_id = None
        for line in lines:
            if "\tdevice" in line:
                device_id = line.split()[0]
                break
        
        if not device_id:
            print("[-] រកមិនឃើញ Device ទេ!")
            return None

        # ភ្ជាប់ uiautomator2 ទៅកាន់ Serial នោះ
        device = u2.connect(device_id)
        print(f"[+] ភ្ជាប់ជោគជ័យទៅកាន់: {device_id} (uiautomator2)")
        return device
    except Exception as e:
        print(f"[Error] មិនអាចភ្ជាប់ Device បានទេ: {e}")
        return None

# --- ២. កូដបង្ហាញ Text ទាំងអស់លើអេក្រង់ ---
def show_all_text(device):
    """ស្រង់យក Text និង Description ទាំងអស់ដែលកំពុងបង្ហាញ"""
    try:
        xml = device.dump_hierarchy()
        texts = re.findall(r'(?:text|content-desc)="([^"]+)"', xml)
        unique_texts = list(dict.fromkeys([t.strip() for t in texts if t.strip()]))
        
        print("\n--- [បញ្ជី Text លើអេក្រង់] ---")
        for i, t in enumerate(unique_texts, 1):
            print(f"{i}. {t}")
        print("-----------------------------\n")
        return unique_texts
    except Exception as e:
        print(f"[Error] {e}")
        return []


def send_keys_with_delay(device, text: str, delay: float = 0.1):
    """ផ្ញើអក្សរម្ដងមួយៗទៅកាន់ device ដោយមាន delay"""
    try:
        # បម្លែងទៅជា String ជាស្វ័យប្រវត្តិកុំឱ្យ Error ពេលបញ្ជូនលេខ
        text = str(text)
        for char in text:
            device.send_keys(char)
            time.sleep(delay)
    except Exception as e:
        print(f"Error sending keys: {e}")

def click_text_and_xpath(device, text_pht, timeout=30):
    end_time = time.time() + timeout
    text_lower = text_pht.lower()
    xpath = f'//*[translate(@text, "ABCDEFGHIJKLMNOPQRSTUVWXYZ", "abcdefghijklmnopqrstuvwxyz")="{text_lower}" or translate(@content-desc, "ABCDEFGHIJKLMNOPQRSTUVWXYZ", "abcdefghijklmnopqrstuvwxyz")="{text_lower}"]'

    while time.time() < end_time:
        try:
            if device(text=text_pht).exists:
                time.sleep(1)
                device(text=text_pht).click()
                return True

            if device.xpath(xpath).exists:
                time.sleep(1)
                device.xpath(xpath).click()
                return True
        except Exception:
            pass

        time.sleep(0.2)

    return False

def If_you_have_it_click(device, text_pht, timeout=6):
    end_time = time.time() + timeout
    text_lower = text_pht.lower()
    xpath = f'//*[translate(@text, "ABCDEFGHIJKLMNOPQRSTUVWXYZ", "abcdefghijklmnopqrstuvwxyz")="{text_lower}" or translate(@content-desc, "ABCDEFGHIJKLMNOPQRSTUVWXYZ", "abcdefghijklmnopqrstuvwxyz")="{text_lower}"]'

    while time.time() < end_time:
        try:
            if device(text=text_pht).exists:
                time.sleep(1)
                device(text=text_pht).click()
                return True

            if device.xpath(xpath).exists:
                time.sleep(1)
                device.xpath(xpath).click()
                return True
        except Exception:
            pass

        time.sleep(0.2)

    return False


    
device = connect_device()
if device:


    show_all_text(device)
    device.app_start(package)

    click_text_and_xpath(device, "Create new account") or click_text_and_xpath(device, "Get started")



    If_you_have_it_click(device, "Get started")


    If_you_have_it_click(device, "Allow")



    click_text_and_xpath(device, "First name")
    device.send_keys("ah")
    click_text_and_xpath(device, "Last name")
    device.send_keys("da")

    click_text_and_xpath(device, "Next")
    click_text_and_xpath(device, "Next")
    click_text_and_xpath(device, "Next")

    click_text_and_xpath(device, "Age")
    age = random.randint(18, 30)

    device.send_keys(str(age))
    click_text_and_xpath(device, "Next")

    click_text_and_xpath(device, "OK")

    click_text_and_xpath(device, "Female")
    
    click_text_and_xpath(device, "Male")
    click_text_and_xpath(device, "Next")

    click_text_and_xpath(device, "Mobile number")
    device.send_keys("098764746")

    click_text_and_xpath(device, "Next")

    click_text_and_xpath(device, "Password")
    device.send_keys("A:KJSLKAHS")

    click_text_and_xpath(device, "Next")

    click_text_and_xpath(device, "I agree")

    click_text_and_xpath(device, "I didn’t get the code")

    click_text_and_xpath(device, "Confirm by email")
#######################################################################
    click_text_and_xpath(device, "Get started")
    click_text_and_xpath(device, "Create new account")
    click_text_and_xpath(device, "First name")
    click_text_and_xpath(device, "Last name")
    click_text_and_xpath(device, "Next")
    click_text_and_xpath(device, "Mobile number")
    click_text_and_xpath(device, "Password")
    click_text_and_xpath(device, "Age")
    click_text_and_xpath(device, "OK")
    click_text_and_xpath(device, "Female")
    click_text_and_xpath(device, "Male")
    click_text_and_xpath(device, "Back")
    click_text_and_xpath(device, "Cancel")
    click_text_and_xpath(device, "Continue")
    click_text_and_xpath(device, "Confirm")
    click_text_and_xpath(device, "Submit")
    click_text_and_xpath(device, "Done")
    click_text_and_xpath(device, "Save")
    click_text_and_xpath(device, "Edit")
    click_text_and_xpath(device, "Delete")
    click_text_and_xpath(device, "Close")
    click_text_and_xpath(device, "Skip")
    click_text_and_xpath(device, "Retry")
    click_text_and_xpath(device, "Search")
    click_text_and_xpath(device, "Next")
    click_text_and_xpath(device, "Previous")
    click_text_and_xpath(device, "Allow")
    click_text_and_xpath(device, "Deny")
    click_text_and_xpath(device, "Yes")
    click_text_and_xpath(device, "No")
    click_text_and_xpath(device, "OK")
    click_text_and_xpath(device, "Log in")
    click_text_and_xpath(device, "Log out")
    click_text_and_xpath(device, "Sign in")
    click_text_and_xpath(device, "Sign up")
    click_text_and_xpath(device, "Create account")
    click_text_and_xpath(device, "Forgot password?")
    click_text_and_xpath(device, "Verify")
    click_text_and_xpath(device, "Resend code")
    click_text_and_xpath(device, "Send code")
    click_text_and_xpath(device, "Try again")
    click_text_and_xpath(device, "Settings")
    click_text_and_xpath(device, "Help")
    click_text_and_xpath(device, "Help Center")
    click_text_and_xpath(device, "More")
    click_text_and_xpath(device, "Refresh")
    click_text_and_xpath(device, "Open")
    click_text_and_xpath(device, "Add")
    click_text_and_xpath(device, "Remove")
    click_text_and_xpath(device, "Select")
    click_text_and_xpath(device, "Select all")
    click_text_and_xpath(device, "Copy")
    click_text_and_xpath(device, "Paste")
    click_text_and_xpath(device, "Share")
    click_text_and_xpath(device, "Update")
    click_text_and_xpath(device, "Install")
    click_text_and_xpath(device, "Uninstall")
    click_text_and_xpath(device, "Enable")
    click_text_and_xpath(device, "Disable")
    click_text_and_xpath(device, "Allow access")
    click_text_and_xpath(device, "Not now")
    click_text_and_xpath(device, "Maybe later")
    click_text_and_xpath(device, "I agree")
    click_text_and_xpath(device, "I disagree")
    click_text_and_xpath(device, "Didn't get the code?")
    click_text_and_xpath(device, "didn’t get the code")
    click_text_and_xpath(device, "Confirm by email")
    click_text_and_xpath(device, "Send code")
    click_text_and_xpath(device, "Resend code")
    click_text_and_xpath(device, "Try another way")
    click_text_and_xpath(device, "Use another method")
    click_text_and_xpath(device, "Continue")
    click_text_and_xpath(device, "Cancel")
    click_text_and_xpath(device, "Back")
    click_text_and_xpath(device, "Enter code")
    click_text_and_xpath(device, "Enter confirmation code")
    click_text_and_xpath(device, "Check your email")
    click_text_and_xpath(device, "Check your messages")
    click_text_and_xpath(device, "Verify your email")
    click_text_and_xpath(device, "Confirm your identity")
    click_text_and_xpath(device, "Two-factor authentication")
    click_text_and_xpath(device, "2-Step Verification")
    click_text_and_xpath(device, "Try again")
