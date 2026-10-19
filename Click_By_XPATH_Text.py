import time
from selenium.webdriver.common.by import By

def Find(driver, Name_ID):
    selectors = [
        (By.XPATH, f"//*[normalize-space(text())='{Name_ID}']"),
        (By.XPATH, f"//*[contains(normalize-space(text()),'{Name_ID}')]"),
        (By.CSS_SELECTOR, f'[aria-label="{Name_ID}"]'),
        (By.XPATH, f"//span[normalize-space(text())='{Name_ID}']"),
        (By.CSS_SELECTOR, f'span[aria-label="{Name_ID}"]')
    ]
    for by, selector in selectors:
        try:
            for element in driver.find_elements(by, selector):
                if element.is_displayed() and element.is_enabled():
                    return element
        except Exception:
            pass
    return None


def keys_By_XPATH_Text(driver, Name_ID, text, char=0.5):
    element = Find(driver, Name_ID)
    if element:
        time.sleep(2)
        element.click()
        for key in text:
            element.send_keys(key)
            time.sleep(char)
        print(f"Keys Success: {Name_ID}")
        return True
    print(f"Keys Failed: {Name_ID}")
    return False


def Click_By_XPATH_Text(driver, Name_ID):
    element = Find(driver, Name_ID)
    if element:
        time.sleep(2)
        element.click()
        time.sleep(2)
        print(f"Click Success: {Name_ID}")
        return True
    print(f"Click Failed: {Name_ID}")
    return False


def Search_By_XPATH_Text(driver, Name_ID):
    element = Find(driver, Name_ID)
    if element:
        print(f"Search Success: {Name_ID} | Tag: {element.tag_name} | Text: {element.text} | ARIA: {element.get_attribute('aria-label')}")
        return True
    print(f"Search Failed: {Name_ID}")
    return False
