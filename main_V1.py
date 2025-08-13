
#Slects R-strategy without comparing the platform migration strategy



import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import time
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
 
 
def go_to_first_page(driver):
    """Navigate back to first page by clicking the previous button until at page 1."""
    try:
        while True:
            pagination = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div.pagination-center"))
            )
            page_spans = pagination.find_elements(By.TAG_NAME, "span")
 
            # Find active page number
            active_page_num = None
            for span in page_spans:
                classes = span.get_attribute("class") or ""
                if "active_page" in classes:
                    val = span.get_attribute("value")
                    if val and val.isdigit():
                        active_page_num = int(val)
                    break
 
            if active_page_num == 1:
                # Already at first page, stop
                print("Reached first page.")
                break
 
            # Find previous button (first span with role="button")
            prev_btn = None
            for span in page_spans:
                role = span.get_attribute("role")
                if role == "button":
                    prev_btn = span
                    break
 
            if not prev_btn:
                print("Previous button not found, assuming first page.")
                break
 
            # Check if previous button is disabled by class
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
 
    except Exception as e:
        # print(f"Error going back to first page: {e}")
        pass
 
def update_r_strategy():
    # Read Excel file
    df = pd.read_excel('Files/Cop.xlsx')
    business_functions = input("Enter business functions to filter (comma separated): ").split(",")
    business_functions = [b.strip() for b in business_functions]
    filtered = df[df['BusinessFunction'].isin(business_functions)]
 
    # Read credentials from file
    cred_path = 'c:\\Projects\\Python workspace\\AR Automation\\credentials.txt'
    username = password = None
    with open(cred_path, 'r') as f:
        for line in f:
            if line.startswith('username='):
                username = line.strip().split('=', 1)[1]
            elif line.startswith('password='):
                password = line.strip().split('=', 1)[1]
    if not username or not password:
        raise ValueError('Username or password not found in credentials.txt')
 
    report_name = "ASSMNT_TRUI_TPOT_REPORT"
    service = Service("C:\\Projects\\Python workspace\\AR Automation\\chromedriver.exe")
    driver = webdriver.Chrome(service=service)
    driver.get('https://cm-us-est-prod-01.cmigrate.com/login?realm=Truist')
    time.sleep(2)
 
    # Login
    driver.find_element(By.CSS_SELECTOR, '#standard-basic-username').send_keys(username)
    driver.find_element(By.CSS_SELECTOR, '#standard-basic-password').send_keys(password)
    driver.find_element(By.XPATH, '//button[contains(text(), "Login")]').click()
    time.sleep(3)
 
    # Click Create Assessment
    driver.find_element(By.CSS_SELECTOR, '#root > div.App > div.main_container > div.sidebar_main > div.sidebar_wrapper > div.sidebar_nav > div:nth-child(7) > div').click()
    time.sleep(2)
 
    # Click Review Assessment
    driver.find_element(By.CSS_SELECTOR, '#Review\\ Assessment').click()
    time.sleep(2)
 
    # Select report from dropdown
    report_dropdown = driver.find_element(By.CSS_SELECTOR, '#root > div.App > div.main_container > div.right-container > div.white_bg > div.full-width-table-wrapper > div:nth-child(1) > div > div > div > div.col-lg-3.col-md-3 > div > div > div.review_assessment__value-container.css-hlgwow > div.review_assessment__input-container.css-19bb58m')
    report_dropdown.click()
    time.sleep(2)
    report_options = driver.find_elements(By.XPATH, '//div[contains(@class, "review_assessment__option")]')
    for option in report_options:
        if report_name in option.text:
            driver.execute_script("arguments[0].scrollIntoView(true);", option)
            time.sleep(2)
            try:
                option.click()
            except Exception:
                driver.execute_script("arguments[0].click();", option)
            break
    time.sleep(10)
 
    # Click Assessment Questionnaire
    driver.find_element(By.CSS_SELECTOR, '#Assessment\\ Questionnaire').click()
    time.sleep(10)
 
    # Get all applications from the dropdown
    app_dropdown = driver.find_element(By.CSS_SELECTOR, 'div.col-3.form-group.form_item > select')
    app_options = app_dropdown.find_elements(By.TAG_NAME, 'option')
    app_names = [opt.text for opt in app_options if opt.get_attribute('value')]
    print(f"Applications found: {app_names}")
 
    # --- Summary tracking variables ---
    summary = {
        'updated': [],
        'not_updated': [],
        'error_hostnames': [],
        'applications': app_names,
        'rehost': [],
        'replatform': []
    }
    app_summary = {app: {
        'updated': [],
        'not_updated': [],
        'error_hostnames': [],
        'rehost': [],
        'replatform': []
    } for app in app_names}
 
    # Loop through each application
    for app in app_names:
        app_dropdown = driver.find_element(By.CSS_SELECTOR, 'div.col-3.form-group.form_item > select')
        Select(app_dropdown).select_by_visible_text(app)
        time.sleep(4)
 
        try:
            entries_dropdown = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, '#dropdownMenuButton'))
            )
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", entries_dropdown)
            try:
                entries_dropdown.click()
            except Exception:
                driver.execute_script("arguments[0].click();", entries_dropdown)
 
            dropdown_items = WebDriverWait(driver, 5).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".dropdown-menu .dropdown-item"))
            )
            chosen = None
            for item in dropdown_items:
                if '50' in item.text:
                    chosen = item
                    break
            if not chosen:
                numeric_values = []
                for item in dropdown_items:
                    try:
                        numeric_values.append((int(''.join(filter(str.isdigit, item.text))), item))
                    except:
                        continue
                if numeric_values:
                    chosen = max(numeric_values, key=lambda x: x[0])[1]
            if chosen:
                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", chosen)
                ActionChains(driver).move_to_element(chosen).click().perform()
                time.sleep(2)
        except Exception as e:
            # print(f"Could not reliably set 50 entries for app {app}: {e}")
            pass
        last_active_page = 0
        while True:
            rows = driver.find_elements(By.CSS_SELECTOR, 'table > tbody > tr')
            for row_elem in rows:
                hostname = "<unknown>"
                try:
                    tds = row_elem.find_elements(By.TAG_NAME, 'td')
                    if len(tds) < 4:
                        continue
                    hostname_cell = tds[3]
                    hostname = hostname_cell.text.strip()
                    row = filtered[filtered['HostName'] == hostname]
                    if not row.empty:
                        r_strategy = row.iloc[0]['R-Strategy']
                        try:
                            WebDriverWait(driver, 10).until(
                                EC.invisibility_of_element_located((By.CSS_SELECTOR, 'div.loader'))
                            )
                        except Exception:
                            pass
                        edit_btn = row_elem.find_element(By.CSS_SELECTOR, 'td:nth-child(11) > div > span > img')
                        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", edit_btn)
                        try:
                            edit_btn.click()
                        except Exception:
                            driver.execute_script("arguments[0].click();", edit_btn)
                        time.sleep(1)
 
                        select_elem = row_elem.find_element(By.CSS_SELECTOR, 'td:nth-child(9) > div > select')
                        select = Select(select_elem)
                        option_found = False
                        for option in select.options:
                            if option.text.strip() == str(r_strategy).strip():
                                if option.is_enabled():
                                    select.select_by_visible_text(option.text)
                                    option_found = True
                                else:
                                    print(f"R-Strategy option '{option.text}' is disabled for hostname {hostname}")
                                break
                        if option_found:
                            summary['updated'].append(hostname)
                            app_summary[app]['updated'].append(hostname)
                            if str(r_strategy).strip().lower() == 'rehost':
                                summary['rehost'].append(hostname)
                                app_summary[app]['rehost'].append(hostname)
                            elif str(r_strategy).strip().lower() == 're-platform':
                                summary['replatform'].append(hostname)
                                app_summary[app]['replatform'].append(hostname)
                        else:
                            summary['not_updated'].append(hostname)
                            app_summary[app]['not_updated'].append(hostname)
                            print(f"R-Strategy '{r_strategy}' not found or not enabled for hostname {hostname}. Available options: {[o.text for o in select.options]}")
 
                        comments_elem = row_elem.find_element(By.CSS_SELECTOR, 'td:nth-child(10) > textarea')
                        if comments_elem.is_enabled() and comments_elem.is_displayed():
                            comments_elem.clear()
                            comments_elem.send_keys(' ')
                        else:
                            print(f"Comments textarea is not interactable for hostname {hostname}")
 
                        save_btn = row_elem.find_element(By.CSS_SELECTOR, 'td:nth-child(11) > div > span:nth-child(1) > img')
                        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", save_btn)
                        try:
                            save_btn.click()
                        except Exception:
                            driver.execute_script("arguments[0].click();", save_btn)
                        time.sleep(1)
                    else:
                        summary['not_updated'].append(hostname)
                        app_summary[app]['not_updated'].append(hostname)
                except Exception as e:
                    summary['error_hostnames'].append(hostname)
                    app_summary[app]['error_hostnames'].append(hostname)
                    #print(f"Error processing row for hostname {hostname}: {e}")
                    pass
 
            try:
                pagination = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "div.pagination-center"))
                )
                page_spans = pagination.find_elements(By.TAG_NAME, "span")
 
                active_page_num = None
                for span in page_spans:
                    classes = span.get_attribute("class") or ""
                    if "active_page" in classes:
                        active_page_num = int(span.get_attribute("value"))
                        break
 
                if active_page_num is None:
                    print("Could not determine active page number, assuming page 1")
                    active_page_num = 1
 
                next_btn = None
                spans_with_role = [s for s in page_spans if s.get_attribute("role") == "button"]
 
                active_index = None
                for i, span in enumerate(spans_with_role):
                    if "active_page" in (span.get_attribute("class") or ""):
                        active_index = i
                        break
 
                if active_index is not None and active_index + 1 < len(spans_with_role):
                    candidate = spans_with_role[active_index + 1]
                    candidate_class = candidate.get_attribute("class") or ""
                    if "disabledCls" not in candidate_class:
                        next_btn = candidate
 
                if not next_btn:
                    print("Next button disabled or not found, reached last page")
                    break
 
                if active_page_num <= last_active_page:
                    print(f"Active page number did not increase ({active_page_num} <= {last_active_page}), stopping pagination")
                    break
 
                last_active_page = active_page_num
 
                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", next_btn)
                try:
                    next_btn.click()
                except:
                    driver.execute_script("arguments[0].click();", next_btn)
                time.sleep(4)
 
            except Exception as e:
                # print(f"Next button not found or not clickable: {e}")
                break
        go_to_first_page(driver)
    driver.quit()
 
    # --- Print overall summary ---
    print("\n--- Overall Automation Summary ---")
    print(f"Total applications processed: {len(summary['applications'])}")
    print(f"Total hostnames with R-Strategy updated: {len(summary['updated'])}")
    print(f"Total hostnames not updated: {len(summary['not_updated'])}")
    print(f"Hostnames not updated: {summary['not_updated']}")
    print(f"Total error hostnames: {len(summary['error_hostnames'])}")
    print(f"Total Rehost: {len(summary['rehost'])}")
    print(f"Total Replatform: {len(summary['replatform'])}")
 
    # --- Print application-wise summary ---
    print("\n--- Application-wise Summary ---")
    for app in app_names:
        print(f"\nApplication: {app}")
        print(f"  Hostnames with R-Strategy updated: {len(app_summary[app]['updated'])}")
        print(f"  Hostnames not updated: {len(app_summary[app]['not_updated'])}")
        print(f"  Not updated hostnames: {app_summary[app]['not_updated']}")
        print(f"  Error hostnames: {len(app_summary[app]['error_hostnames'])}")
        print(f"  Rehost: {len(app_summary[app]['rehost'])}")
        print(f"  Replatform: {len(app_summary[app]['replatform'])}")
 
 
if __name__ == "__main__":
    update_r_strategy()
 