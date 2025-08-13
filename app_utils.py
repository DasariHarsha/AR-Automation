from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time

def get_applications(driver):
    app_dropdown = driver.find_element(By.CSS_SELECTOR, 'div.col-3.form-group.form_item > select')
    app_options = app_dropdown.find_elements(By.TAG_NAME, 'option')
    app_names = [opt.text for opt in app_options if opt.get_attribute('value')]
    print(f"Applications found: {app_names}")
    return app_names

def set_entries_to_50(driver):
    try:
        dropdown_btn_xpath = '//*[@id="dropdownMenuButton"]'
        dropdown_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, dropdown_btn_xpath))
        )
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", dropdown_btn)
        time.sleep(1)
        dropdown_btn.click()
        # Wait for the dropdown menu popup to appear
        menu_xpath = '//*[@id="root"]/div[1]/div[2]/div[2]/div[1]/div[4]/div[2]/div[2]/div[13]/div/div[2]/div[1]/div/div'
        menu = WebDriverWait(driver, 5).until(
            EC.visibility_of_element_located((By.XPATH, menu_xpath))
        )
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
    except Exception as e:
        print(f"[ERROR] Could not set entries to 50: {e}")

def go_to_first_page(driver):
    try:
        while True:
            pagination = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div.pagination-center"))
            )
            page_spans = pagination.find_elements(By.TAG_NAME, "span")
            active_page_num = None
            for span in page_spans:
                classes = span.get_attribute("class") or ""
                if "active_page" in classes:
                    val = span.get_attribute("value")
                    if val and val.isdigit():
                        active_page_num = int(val)
                    break
            if active_page_num == 1:
                print("Reached first page.")
                break
            prev_btn = None
            for span in page_spans:
                role = span.get_attribute("role")
                if role == "button":
                    prev_btn = span
                    break
            if not prev_btn:
                print("Previous button not found, assuming first page.")
                break
            cls = prev_btn.get_attribute("class") or ""
            if "disabledCls" in cls:
                print("Previous button disabled, reached first page.")
                break
            print("Going back to first page...")
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", prev_btn)
            try:
                prev_btn.click()
            except:
                driver.execute_script("arguments[0].click();", prev_btn)
            time.sleep(2)
    except Exception:
        pass
