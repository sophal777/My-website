from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

def run_browser(target_line_num):
    try:
        with open("vv.txt", "r", encoding="utf-8") as file:
            lines = file.readlines()
    except FileNotFoundError:
        print("[-] រកមិនឃើញឯកសារ accounts.txt ទេ។")
        return

    if not lines:
        print("[-] ឯកសារ Text គឺទទេ។")
        return

    print(f"[*] ឯកសាររបស់អ្នកមានសរុបចំនួន {len(lines)} បន្ទាត់។")

    # កំណត់យកបន្ទាត់ដែលបានបញ្ជូនចូល (ឧ. main(3) -> Index 2)
    idx = target_line_num - 1
    if 0 <= idx < len(lines):
        target_lines = [(idx, lines[idx])]
    else:
        print(f"[-] លេខបន្ទាត់ទី {target_line_num} មិនត្រឹមត្រូវ! (ត្រូវស្ថិតចន្លោះ 1 ដល់ {len(lines)})")
        return

    for idx, line in target_lines:
        line_str = line.strip()
        if not line_str:
            print(f"[-] បន្ទាត់ទី {idx+1} គឺទទេ។")
            return
        
        # អនុគមន៍សម្រាប់ទាញយកតម្លៃ Cookie ពីបន្ទាត់អត្ថបទ
        def extract_value(text, key):
            try:
                start_idx = text.find(key)
                if start_idx == -1:
                    return ""
                start_idx += len(key)
                end_idx = text.find("|", start_idx)
                if end_idx == -1:
                    return text[start_idx:].strip()
                return text[start_idx:end_idx].strip()
            except Exception:
                return ""

        c_user = extract_value(line_str, "c_user=")
        xs = extract_value(line_str, "xs=")
        datr = extract_value(line_str, "datr=")
        fr = extract_value(line_str, "fr=")

        if not c_user:
            print(f"[-] បន្ទាត់ទី {idx+1} រកមិនឃើញ c_user ទេ។")
            return

        print(f"[*] កំពុងបើក Browser សម្រាប់បន្ទាត់ទី {idx+1} (c_user: {c_user})")

        # កំណត់ជម្រើស Chrome Options
        options = Options()
        options.add_argument("--window-size=250,450")
        options.add_argument(
            "--user-agent=Mozilla/5.0 (Linux; Android 13; Pixel 7) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/131.0.0.0 Mobile Safari/537.36"
        )
        options.add_argument("--app=https://m.facebook.com/")
        options.add_argument("--disable-notifications")
        options.add_argument("--disable-extensions")
        options.add_argument("--window-position=0,20")

        driver = webdriver.Chrome(options=options)

        try:
            # ត្រូវបើក Domain គោលដៅមុនទើបអាចបញ្ចូល Cookie បាន
            driver.get("https://m.facebook.com/")
            time.sleep(2)

            cookies = [
                {"name": "c_user", "value": c_user, "domain": ".facebook.com", "path": "/"},
                {"name": "xs", "value": xs, "domain": ".facebook.com", "path": "/"},
                {"name": "datr", "value": datr, "domain": ".facebook.com", "path": "/"},
                {"name": "fr", "value": fr, "domain": ".facebook.com", "path": "/"},
            ]

            for cookie in cookies:
                if cookie["value"]:
                    try:
                        driver.add_cookie(cookie)
                    except Exception as e:
                        print(f"Error adding cookie {cookie['name']}: {e}")

            # Refresh ទំព័រដើម្បីให้ Cookie ដំណើរការចូល Account
            driver.refresh()
            
            # រង់ចាំមើលលទ្ធផល (អាចកែសម្រួលថើបតាមតម្រូវការ)
            time.sleep(10)

        except Exception as e:
            print(f"Error: {e}")
        finally:
            driver.quit()

# ឧទាហរណ៍នៃការហៅប្រើប្រាស់មុខងារ (ដំណើរការបន្ទាត់ទី 1)
if __name__ == "__main__":
    run_browser(1)
