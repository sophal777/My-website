# 1. Import Libraries
import subprocess
import re
import time
import uiautomator2 as u2
import random
import string
import json
import os
from Gmail_IMAP_Code_FB import Gmail_IMAP_Code_FB
# 2. Configuration

FACEBOOK = 'com.facebook.katana'
ADB_PATH = r'C:\platform-tools\adb.exe'
SURFSHARK = 'com.surfshark.vpnclient.android'
vpn_Los_Angeles = 'Los Angeles'


def connect_device():
   try:
      result = subprocess.run(
         [ADB_PATH, 'devices'], capture_output=True, text=True, timeout=10, check=True
      )
      device_ids = [
         line.split()[0]
         for line in result.stdout.splitlines()[1:]
         if len(line.split()) >= 2 and line.split()[1] == 'device'
      ]

      if not device_ids:
         print('[-] No connected device found!')
         return None

      device_id = device_ids[0]
      device = u2.connect(device_id)
      print(f'[+] Connected: {device_id} (uiautomator2)')
      return device

   except Exception as e:
      print(f'[Error] Connect device failed: {e}')
      return None


def get_device_city(device):
   try:
      cmd_ip = device.shell('curl -s --max-time 6 https://api.ipify.org').output.strip()
      if not cmd_ip or ' ' in cmd_ip or len(cmd_ip) > 45:
         return 'Unknown'

      cmd_city = device.shell(
         f"curl -s --max-time 6 'http://ip-api.com/json/{cmd_ip}?fields=status,city'"
      ).output.strip()
      data = json.loads(cmd_city)

      if data.get('status') == 'success':
         return data.get('city') or 'Unknown'

   except Exception as e:
      print(f'[-] Geolocation check error: {e}')

   return 'Unknown'


def is_vpn_active(device):
   try:
      res = device.shell('ip route').output
      return 'tun' in res
   except Exception:
      return False


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


def send_keys_with_delay(device, text, delay=0.08):
   try:
      for char in str(text):
         device.send_keys(char)
         time.sleep(delay)
   except Exception as e:
      print(f'[Error] Send keys failed: {e}')


def If_you_have_it_click(device, text_pht, timeout=5):
   return click_text_and_xpath(device, text_pht, timeout)


def check_text(device, text_pht, timeout=30):
   end_time = time.time() + timeout
   text_lower = text_pht.lower()
   xpath = f'//*[@text="{text_pht}" or @content-desc="{text_pht}" or translate(@text, "ABCDEFGHIJKLMNOPQRSTUVWXYZ", "abcdefghijklmnopqrstuvwxyz")="{text_lower}" or translate(@content-desc, "ABCDEFGHIJKLMNOPQRSTUVWXYZ", "abcdefghijklmnopqrstuvwxyz")="{text_lower}"]'

   while time.time() < end_time:
      try:
         if device(text=text_pht).exists or device(description=text_pht).exists:
            return True

         if device.xpath(xpath).exists:
            return True

      except Exception:
         pass

      time.sleep(0.2)

   return False


def check_city():

   city = get_device_city(device)
   print(f'[*] Current Device City: {city}')

   attempts = 5
   vpn_ready = False

   while attempts > 0:
      if city == 'Los Angeles':
         vpn_ready = True
         print('[+] Successfully verified location: Los Angeles')
         break
      device.app_start(SURFSHARK)
      time.sleep(2)
      click_text_and_xpath(device, 'Connect', timeout=10)
      print(f'[*] Attempt remaining: {attempts} | Reconnecting Surfshark...')

      deadline = time.time() + 20
      while time.time() < deadline:
         if is_vpn_active(device):
            print('[+] VPN interface (tun0) detected!')
            time.sleep(3)
            break
         time.sleep(1)

      city = get_device_city(device)
      print(f'[*] Detected City: {city}')

      if city == vpn_Los_Angeles:
         vpn_ready = True
         print('[+] Successfully connected to Los Angeles!')
         break

      attempts -= 1

   if vpn_ready:
      print('[+] Preparing Facebook...')

   else:
      print("[-] Failed: Could not get 'Los Angeles' after 5 attempts. Exiting...")


def generate_random_name():
   first_names = ['Sophea', 'Dara', 'Veasna', 'Borey', 'Chann', 'Kosal', 'Vannak', 'Serey']
   last_names = ['Heng', 'Chan', 'Keo', 'Sok', 'Chea', 'Meas', 'Lim', 'Ros']
   return random.choice(first_names), random.choice(last_names)


def generate_random_phone():
   prefixes = ['012', '015', '016', '098', '088', '097']
   suffix = ''.join(random.choices(string.digits, k=6))
   return f'+855{random.choice(prefixes)}{suffix}'


def generate_random_password(length=12):
   chars = string.ascii_letters + string.digits + '@#$'
   return ''.join(random.choices(chars, k=length))


def FB1(device):

   check_city()

   device.app_clear(FACEBOOK)
   device.app_start(FACEBOOK)
   first_name, last_name = generate_random_name()
   random_gender = random.choice(['Female', 'Male'])
   random_phone = generate_random_phone()
   random_password = generate_random_password(12)

   click_text_and_xpath(device, 'Create new account') or click_text_and_xpath(
      device, 'Get started'
   )
   If_you_have_it_click(device, 'Get started') or If_you_have_it_click(
      device, 'Create new account'
   )
   If_you_have_it_click(device, 'ALLOW')

   click_text_and_xpath(device, 'First name')
   send_keys_with_delay(device, first_name)
   click_text_and_xpath(device, 'Last name')
   send_keys_with_delay(device, last_name)
   click_text_and_xpath(device, 'Next')
   click_text_and_xpath(device, 'Next')
   click_text_and_xpath(device, 'Next')

   # បំពេញអាយុ
   age = random.randint(18, 30)
   If_you_have_it_click(device, 'Age')
   send_keys_with_delay(device, str(age))
   click_text_and_xpath(device, 'Next')
   If_you_have_it_click(device, 'OK')

   # ជ្រើសរើសភេទតាមតម្លៃចៃដន្យតែមួយ
   click_text_and_xpath(device, random_gender)
   click_text_and_xpath(device, 'Next')

   # ១. បំពេញលេខទូរសព្ទ

   random_phone = generate_random_phone()
   click_text_and_xpath(device, 'Mobile number')
   send_keys_with_delay(device, random_phone)
   click_text_and_xpath(device, 'Next')
   time.sleep(4)


def FB2(device):

   # Use a while loop to keep retrying if the number is flagged/invalid
   while check_text(device, "What's your mobile number?", timeout=5):
      new_phone = generate_random_phone()
      click_text_and_xpath(device, 'Mobile number')
      device.clear_text()  # លុបលេខចាស់ចេញ
      send_keys_with_delay(device, new_phone)
      click_text_and_xpath(device, 'Next')
      time.sleep(4)  # Give it a moment to process the new number

   # Once it moves past the mobile screen, check what screen appeared next
   if check_text(device, 'Create a password', timeout=5):
      random_password = generate_random_password(12)
      click_text_and_xpath(device, 'Password')
      send_keys_with_delay(device, random_password)
      click_text_and_xpath(device, 'Next')
      time.sleep(4)

   elif check_text(device, 'Password', timeout=5):
      New__password = generate_random_password(12)
      click_text_and_xpath(device, 'Password')
      device.clear_text()
      send_keys_with_delay(device, New__password)
      click_text_and_xpath(device, 'Next')


def FB3(device):

   if check_text(device, "Agree to Facebook's terms and policies", timeout=5):
      click_text_and_xpath(device, 'I agree')
      time.sleep(30)
   if check_text(device, 'I didn’t get the code', timeout=5):
      click_text_and_xpath(device, 'I didn’t get the code')
      If_you_have_it_click(device, 'Confirm by email')

      file_path = 'gmail_accounts.txt'
      with open(file_path, 'r', encoding='utf-8') as f:
         lines = f.readlines()
      current_email = lines.pop(0).strip() if lines else None
      with open(file_path, 'w', encoding='utf-8') as f:
         f.writelines(lines)

      if current_email:
         click_text_and_xpath(device, 'Email')
         send_keys_with_delay(device, current_email)
         click_text_and_xpath(device, 'Next')
         time.sleep(4)

         while True:
            if check_text(device, 'Confirmation code', timeout=5):
               print('OK')
               time.sleep(10)

               Email_email = current_email
               print('Email ត្រឹមត្រូវ:', Email_email)
               gmail = Email_email
               code_otp = Gmail_IMAP_Code_FB(gmail)

               click_text_and_xpath(device, 'Confirmation code')
               send_keys_with_delay(device, code_otp)
               click_text_and_xpath(device, 'Next')

               break
            elif check_text(device, 'Enter an email', timeout=5):
               print('Email rejected - Trying next email...')

               with open(file_path, 'r', encoding='utf-8') as f:
                  lines = f.readlines()

               current_email = lines.pop(0).strip() if lines else None

               with open(file_path, 'w', encoding='utf-8') as f:
                  f.writelines(lines)

               if current_email:
                  click_text_and_xpath(device, 'Email')
                  device.clear_text()
                  send_keys_with_delay(device, current_email)
                  click_text_and_xpath(device, 'Next')
                  time.sleep(6)
               else:
                  print('អស់ Email ក្នុង File ហើយ!')
                  break
      else:
         print('គ្មាន Email នៅក្នុង File ទេ!')

   elif check_text(device, "Agree to Facebook's terms and policies", timeout=5):
      device.app_start(SURFSHARK)
      time.sleep(2)
      device.app_stop(SURFSHARK)
      time.sleep(2)
      device.app_start(FACEBOOK)
      time.sleep(2)
      click_text_and_xpath(device, 'I agree')
      time.sleep(3)

      click_text_and_xpath(device, 'I didn’t get the code')
      If_you_have_it_click(device, 'Confirm by email')
      check_city()

      device.app_start(FACEBOOK)

      file_path = 'gmail_accounts.txt'
      with open(file_path, 'r', encoding='utf-8') as f:
         lines = f.readlines()
      current_email = lines.pop(0).strip() if lines else None
      with open(file_path, 'w', encoding='utf-8') as f:
         f.writelines(lines)

      if current_email:
         click_text_and_xpath(device, 'Email')
         send_keys_with_delay(device, current_email)
         click_text_and_xpath(device, 'Next')
         time.sleep(4)

         while True:
            if check_text(device, 'Confirmation code', timeout=5):
               print('OK')
               time.sleep(10)

               Email_email = current_email
               print('Email ត្រឹមត្រូវ:', Email_email)
               gmail = Email_email
               code_otp = Gmail_IMAP_Code_FB(gmail)

               click_text_and_xpath(device, 'Confirmation code')
               send_keys_with_delay(device, code_otp)
               click_text_and_xpath(device, 'Next')

               break
            elif check_text(device, 'Enter an email', timeout=5):
               print('Email rejected - Trying next email...')

               with open(file_path, 'r', encoding='utf-8') as f:
                  lines = f.readlines()

               current_email = lines.pop(0).strip() if lines else None

               with open(file_path, 'w', encoding='utf-8') as f:
                  f.writelines(lines)

               if current_email:
                  click_text_and_xpath(device, 'Email')
                  device.clear_text()
                  send_keys_with_delay(device, current_email)
                  click_text_and_xpath(device, 'Next')
                  time.sleep(6)
               else:
                  print('អស់ Email ក្នុង File ហើយ!')
                  break
      else:
         print('គ្មាន Email នៅក្នុង File ទេ!')


device = connect_device()


if device:
   FB1(device)  # បង្កើតដំបូងរហូតដល់លេខទូរសព្ទ
   FB2(device)  # លក្ខខណ្ឌលេខទូរសព្ទនិង gmail
   FB3(device)  # ផ្ទៀងផ្ទាត់លេខ OTP
