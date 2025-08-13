import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def set_entries_to_50(driver):
    """
    Sets the entries dropdown to 50 on the current page.
    """
    dropdown_btn_xpath = '//*[@id="dropdownMenuButton"]'
    try:
        dropdown_btns = driver.find_elements(By.XPATH, dropdown_btn_xpath)
        if len(dropdown_btns) == 6:
            dropdown_btn = dropdown_btns[3]  # 4th dropdown (0-based index)
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", dropdown_btn)
            time.sleep(1)
            dropdown_btn.click()
            # Wait for the dropdown menu to appear near the 4th dropdown
            menu_xpath = "//div[contains(@class, 'dropdown-menu') and contains(@class, 'show')]"
            menus = driver.find_elements(By.XPATH, menu_xpath)
            # Find the menu that is displayed and closest to the 4th dropdown
            menu = None
            for m in menus:
                if m.is_displayed():
                    menu = m
                    break
            if not menu:
                print("[ERROR] No visible dropdown menu found after clicking 4th dropdown.")
                return
            # Find the '50' entry in the menu
            option_50 = None
            options = menu.find_elements(By.XPATH, ".//div[contains(@class, 'dropdown-item') and text()='50']")
            for opt in options:
                if opt.text.strip() == '50':
                    option_50 = opt
                    break
            if option_50:
                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", option_50)
                time.sleep(0.2)
                option_50.click()
                time.sleep(1)
            else:
                print("[ERROR] '50' entry not found in entries dropdown.")
        else:
            print(f"[ERROR] Dropdowns found are not equal to 6, found {len(dropdown_btns)}.")
            return
    except Exception as e:
        print(f"[ERROR] Could not set entries to 50: {e}")
