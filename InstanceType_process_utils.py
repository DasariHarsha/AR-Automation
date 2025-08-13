import time
from selenium.webdriver.common.by import By

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from cloud_reserved_utils import cloud_reserved_workflow
from entries_utils import set_entries_to_50
from pagination_utils import go_to_first_page
def select_application_and_cloud(driver: WebDriver, region, filtered):
    """
    Iterates over each application in the application dropdown and selects 'Amazon Web Services' in the cloud dropdown for each.
    """
    # Application dropdown
    app_dropdown_xpath = '//*[@id="root"]/div[1]/div[2]/div[2]/div[1]/div[4]/div[2]/div[2]/div[1]/div[1]/div[2]/div[1]/select'
    app_dropdown = driver.find_element(By.XPATH, app_dropdown_xpath)
    select = Select(app_dropdown)
    app_options = [o for o in select.options if o.get_attribute('value')]
    # region and filtered are now passed as arguments from main.py

    summary = {
        'updated': [],
        'not_updated': [],
        'error_hostnames': [],
        'applications': [o.text for o in app_options],
    }
    app_summary = {app.text: {
        'updated': [],
        'not_updated': [],
        'error_hostnames': []
    } for app in app_options}

    for option in app_options:
        select.select_by_visible_text(option.text)
        WebDriverWait(driver, 2000).until(
            EC.invisibility_of_element_located((By.CLASS_NAME, "loader"))
        )
        cloud_reserved_workflow(driver, option)
        set_entries_to_50(driver)

        while True:
            rows_xpath = '//*[@id="root"]/div[1]/div[2]/div[2]/div[1]/div[4]/div[2]/div[2]/div[2]/div[1]/div[4]/div[2]/div[1]/div/table/tbody/tr'
            rows = driver.find_elements(By.XPATH, rows_xpath)
            if not rows:
                print("[ERROR] No rows found in the instance table.")
                break
            for row in rows:
                try:
                    hostname_cell = row.find_element(By.XPATH, './td[1]')
                    hostname = hostname_cell.text.strip()
                    excel_row = filtered[filtered['HostName'] == hostname]
                    if excel_row.empty:
                        print(f"[WARN] Hostname '{hostname}' not found in Excel.")
                        summary['not_updated'].append(hostname)
                        app_summary[option.text]['not_updated'].append(hostname)
                        continue
                    instance_type = str(excel_row.iloc[0]['InstanceType']).strip()
                    region_input_xpath = './td[6]//div[contains(@class, "review_assessment__input-container")]//input'
                    region_input = row.find_element(By.XPATH, region_input_xpath)
                    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", region_input)
                    time.sleep(0.2)
                    region_input.clear()
                    region_input.send_keys(region)
                    time.sleep(0.2)
                    from selenium.webdriver.common.keys import Keys
                    region_input.send_keys(Keys.ENTER)
                    WebDriverWait(driver, 2000).until(
                        EC.invisibility_of_element_located((By.CLASS_NAME, "loader")))
                    instance_type_input_xpath = './td[8]//div[contains(@class, "review_assessment__input-container")]//input'
                    try:
                        instance_type_input = row.find_element(By.XPATH, instance_type_input_xpath)
                        instance_type_input.clear()
                        instance_type_input.send_keys(instance_type)
                        time.sleep(0.7)
                        from selenium.webdriver.common.keys import Keys
                        instance_type_input.send_keys(Keys.ENTER)
                    except Exception as e:
                        print(f"[ERROR] Could not set instance type for hostname '{hostname}': {e}")
                    WebDriverWait(driver, 2000).until(
                        EC.invisibility_of_element_located((By.CLASS_NAME, "loader")))
                    try:
                        radio_btns = row.find_elements(By.XPATH, './/input[@id="pricingRadio"]')
                        radio_selected = False
                        if len(radio_btns) >= 2:
                            radio_btn = radio_btns[1]
                            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", radio_btn)
                            time.sleep(0.2)
                            if not radio_btn.is_selected():
                                radio_btn.click()
                            radio_selected = True
                        elif len(radio_btns) == 1:
                            radio_btn = radio_btns[0]
                            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", radio_btn)
                            time.sleep(0.2)
                            if not radio_btn.is_selected():
                                radio_btn.click()
                            radio_selected = True
                        else:
                            print(f"[ERROR] No radio buttons found for hostname '{hostname}'.")
                        if radio_selected:
                            summary['updated'].append(hostname)
                            app_summary[option.text]['updated'].append(hostname)
                        else:
                            summary['not_updated'].append(hostname)
                            app_summary[option.text]['not_updated'].append(hostname)
                    except Exception as e:
                        print(f"[ERROR] Could not select 3yrs plan radio button for hostname '{hostname}': {e}")
                        summary['not_updated'].append(hostname)
                        app_summary[option.text]['not_updated'].append(hostname)
                except Exception as e:
                    print(f"[ERROR] Could not process row for hostname: {e}")
                    summary['error_hostnames'].append(hostname)
                    app_summary[option.text]['error_hostnames'].append(hostname)

            try:
                WebDriverWait(driver, 2000).until(
                    EC.invisibility_of_element_located((By.CLASS_NAME, "loader")))
                save_btn_xpath = '//*[@id="root"]/div[1]/div[2]/div[2]/div[1]/div[4]/div[2]/div[2]/div[2]/div[2]/span[2]/button'
                save_btn = driver.find_element(By.XPATH, save_btn_xpath)
                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", save_btn)
                time.sleep(1)
                if save_btn.is_enabled() and save_btn.get_attribute('disabled') is None:
                    try:
                        save_btn.click()
                    except Exception as click_e:
                        driver.execute_script("arguments[0].click();", save_btn)
                        print("[INFO] Clicked 'Save all selections' button using JS.")
                else:
                    print("[INFO] 'Save all selections' button is disabled, skipping click.")
            except Exception as e:
                print(f"[ERROR] Could not click 'Save all selections' button: {e}")
            WebDriverWait(driver, 2000).until(
                EC.invisibility_of_element_located((By.CLASS_NAME, "loader")))

            try:
                pagination_elements = WebDriverWait(driver, 10).until(
                    EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.pagination-center"))
                )
                if len(pagination_elements) == 6:
                    target_pagination = pagination_elements[3]
                    page_spans = target_pagination.find_elements(By.TAG_NAME, "span")
                    active_page_num = None
                    last_page_num = None
                    last_page_idx = None
                    for i, span in enumerate(page_spans):
                        val = span.get_attribute("value")
                        if val and val.isdigit():
                            val_int = int(val)
                            if last_page_num is None or val_int > last_page_num:
                                last_page_num = val_int
                                last_page_idx = i
                            if "active_page" in (span.get_attribute("class") or ""):
                                active_page_num = val_int
                    if active_page_num is None or last_page_num is None:
                        print("Could not determine page numbers.")
                        break
                    if active_page_num >= last_page_num:
                        print(f"Already on last page: {active_page_num}.")
                        break
                    next_btn = None
                    if last_page_idx is not None and last_page_idx + 1 < len(page_spans):
                        next_btn = page_spans[last_page_idx + 1]
                    if next_btn and "disabledCls" not in (next_btn.get_attribute("class") or ""):
                        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", next_btn)
                        time.sleep(1)
                        try:
                            next_btn.click()
                        except:
                            driver.execute_script("arguments[0].click();", next_btn)
                        time.sleep(3)
                    else:
                        print("Next button is disabled or not found.")
                        break
                else:
                    print("Less than 6 pagination containers found and cannot navigate to next page.")
                    break
            except Exception as e:
                print(f"[ERROR] Pagination failed: {e}")
                break
        go_to_first_page(driver)
    return summary, app_summary