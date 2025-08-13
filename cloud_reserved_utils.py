import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def cloud_reserved_workflow(driver, option):
    # Cloud dropdown
    cloud_dropdown_xpath = '//*[@id="CatchCloud"]/div/div/div[1]'
    try:
        cloud_dropdown = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, cloud_dropdown_xpath))
        )
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", cloud_dropdown)
        time.sleep(0.5)
        try:
            cloud_dropdown.click()
        except Exception:
            driver.execute_script("arguments[0].click();", cloud_dropdown)
    except Exception as e:
        print(f"[ERROR] Could not click cloud dropdown for application '{option.text}': {e}")
        return
    # Wait for dropdown options to appear
    aws_option_xpath = "//div[contains(@class, 'css-11unzgr') and text()='Amazon Web Services']"
    try:
        aws_option = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, aws_option_xpath))
        )
        aws_option.click()
    except Exception as e:
        try:
            input_xpath = "//div[@id='CatchCloud']//input[@type='text']"
            input_elem = WebDriverWait(driver, 5).until(
                EC.visibility_of_element_located((By.XPATH, input_xpath))
            )
            input_elem.clear()
            input_elem.send_keys('Amazon Web Services')
            time.sleep(0.2)
            from selenium.webdriver.common.keys import Keys
            input_elem.send_keys(Keys.ENTER)
            time.sleep(0.5)
        except Exception as e2:
            print(f"[ERROR] Could not type/select 'Amazon Web Services' for application '{option.text}': {e2}")
            return
    # time.sleep(1)
    WebDriverWait(driver, 2000).until(
            EC.invisibility_of_element_located((By.CLASS_NAME, "loader"))
        )
    # Reserved Instance checkbox
    reserved_checkbox_xpath = '//*[@id="showReserved"]'
    try:
        reserved_checkbox = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, reserved_checkbox_xpath))
        )
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", reserved_checkbox)
        time.sleep(0.2)
        if reserved_checkbox.is_selected():
            try:
                reserved_checkbox.click()
            except Exception:
                driver.execute_script("arguments[0].click();", reserved_checkbox)
            # time.sleep(0.5)
        if not reserved_checkbox.is_selected():
            try:
                reserved_checkbox.click()
            except Exception:
                driver.execute_script("arguments[0].click();", reserved_checkbox)
            time.sleep(0.5)
    except Exception as e:
        print(f"[ERROR] Could not select Reserved Instance checkbox for application '{option.text}': {e}")
        return
    # No Upfront radio
    no_upfront_radio_xpath = '//*[@id="root"]/div[1]/div[2]/div[2]/div[1]/div[4]/div[2]/div[2]/div[2]/div[1]/div[4]/div[2]/div[4]/div/div[2]/div/div/div[1]/label/input'
    try:
        no_upfront_radio = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, no_upfront_radio_xpath))
        )
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", no_upfront_radio)
        # time.sleep(0.3)
        try:
            no_upfront_radio.click()
        except Exception:
            driver.execute_script("arguments[0].click();", no_upfront_radio)
        time.sleep(0.5)
    except Exception as e:
        try:
            radios = driver.find_elements(By.XPATH, '//div[contains(@class, "cmdb-event-modal-container")]//input[@type="radio"]')
            found = False
            for idx, radio in enumerate(radios):
                value = radio.get_attribute('value')
                if value and value.strip().lower() == 'no upfront':
                    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", radio)
                    # time.sleep(0.2)
                    try:
                        radio.click()
                    except Exception:
                        driver.execute_script("arguments[0].click();", radio)
                    # time.sleep(0.5)
                    found = True
                    # print(f"[INFO] Selected 'No Upfront' radio for application '{option.text}' by value.")
                    break
            if not found:
                print(f"[ERROR] 'No Upfront' radio not found by value for application '{option.text}'")
                return
        except Exception as e2:
            print(f"[DEBUG] Could not list/select radio buttons: {e2}")
            return
    # Save button
    save_btn_xpath = '//*[@id="root"]/div[1]/div[2]/div[2]/div[1]/div[4]/div[2]/div[2]/div[2]/div[1]/div[4]/div[2]/div[4]/div/div[3]/button[2]'
    save_btn = None
    try:
        save_btn = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, save_btn_xpath))
        )
    except Exception:
        try:
            modal = driver.find_element(By.XPATH, '//div[contains(@class, "cmdb-event-modal-container")]')
            buttons = modal.find_elements(By.TAG_NAME, 'button')
            for btn in buttons:
                if btn.text.strip().lower() == 'save':
                    save_btn = btn
                    break
        except Exception as e2:
            print(f"[ERROR] Could not find Save button by text: {e2}")
    if save_btn is not None:
        try:
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", save_btn)
            # time.sleep(0.5)
            try:
                save_btn.click()
                time.sleep(0.3)
            except Exception:
                try:
                    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", save_btn)
                    save_btn.send_keys(" ")
                    time.sleep(0.1)
                    save_btn.click()
                    time.sleep(0.2)
                except Exception:
                    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", save_btn)
                    driver.execute_script("arguments[0].click();", save_btn)
            # time.sleep(2)
        except Exception as e:
            print(f"[ERROR] Could not click Save button for application '{option.text}': {e}")
            return
    else:
        print(f"[ERROR] Save button not found for application '{option.text}'")
        return
