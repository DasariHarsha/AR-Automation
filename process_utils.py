from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from app_utils import set_entries_to_50, go_to_first_page

def process_applications(driver, app_names, filtered):
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
    for app in app_names:
        app_dropdown = driver.find_element(By.CSS_SELECTOR, 'div.col-3.form-group.form_item > select')
        Select(app_dropdown).select_by_visible_text(app)
        WebDriverWait(driver, 2000).until(
                        EC.invisibility_of_element_located((By.CLASS_NAME, "loader")))
        set_entries_to_50(driver)
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
                    platform_migration_cell = tds[7] if len(tds) > 7 else None
                    platform_migration_strategy = platform_migration_cell.text.strip() if platform_migration_cell else ""
                    if not row.empty:
                        excel_r_strategy = str(row.iloc[0]['R-Strategy']).strip()
                        if platform_migration_strategy.lower() == excel_r_strategy.lower():
                            summary['updated'].append(hostname)
                            app_summary[app]['updated'].append(hostname)
                            if excel_r_strategy.lower() == 'rehost':
                                summary['rehost'].append(hostname)
                                app_summary[app]['rehost'].append(hostname)
                            elif excel_r_strategy.lower() == 'replatform' or excel_r_strategy.lower() == 're-platform':
                                summary['replatform'].append(hostname)
                                app_summary[app]['replatform'].append(hostname)
                            elif excel_r_strategy.lower() == 'retire':
                                summary['retire'].append(hostname)
                                app_summary[app]['retire'].append(hostname)
                        else:
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
                                if option.text.strip() == excel_r_strategy:
                                    if option.is_enabled():
                                        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", option)
                                        select.select_by_visible_text(option.text)
                                        option_found = True
                                    else:
                                        print(f"R-Strategy option '{option.text}' is disabled for hostname {hostname}")
                                    break
                            if option_found:
                                summary['updated'].append(hostname)
                                app_summary[app]['updated'].append(hostname)
                                if excel_r_strategy.lower() == 'rehost':
                                    summary['rehost'].append(hostname)
                                    app_summary[app]['rehost'].append(hostname)
                                elif excel_r_strategy.lower() == 'replatform' or excel_r_strategy.lower() == 're-platform':
                                    summary['replatform'].append(hostname)
                                    app_summary[app]['replatform'].append(hostname)
                                elif excel_r_strategy.lower() == 'retire':
                                    summary['retire'].append(hostname)
                                    app_summary[app]['retire'].append(hostname)
                            else:
                                summary['not_updated'].append(hostname)
                                app_summary[app]['not_updated'].append(hostname)
                                print(f"R-Strategy '{excel_r_strategy}' not found or not enabled for hostname {hostname}. Available options: {[o.text for o in select.options]}")
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
                except Exception:
                    summary['error_hostnames'].append(hostname)
                    app_summary[app]['error_hostnames'].append(hostname)
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
            except Exception:
                break
        go_to_first_page(driver)
    return summary, app_summary
