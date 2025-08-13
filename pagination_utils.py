from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time

def go_to_first_page(driver):
    """Navigate back to first page by clicking the previous button until at page 1."""
    try:
        pagination_elements = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.pagination-center"))
        )

        if len(pagination_elements) == 6:
            target_pagination = pagination_elements[3]
        else:
            print("Less than 6 pagination elements found so cannot navigate to first page.")
            return

        while True:
            page_spans = target_pagination.find_elements(By.TAG_NAME, "span")

            # Detect active page number
            active_page_num = None
            first_page_idx = None
            for i, span in enumerate(page_spans):
                val = span.get_attribute("value")
                cls = span.get_attribute("class") or ""
                if val and val.isdigit():
                    if first_page_idx is None:
                        first_page_idx = i
                    if "active_page" in cls:
                        active_page_num = int(val)
                        break

            if active_page_num == 1:
                print("[INFO] Reached first page.")
                break

            # Previous button is expected just before the first page number span
            prev_btn = None
            if first_page_idx is not None and first_page_idx > 0:
                prev_btn = page_spans[first_page_idx - 1]

            if not prev_btn:
                print("[WARN] Previous button not found.")
                break

            prev_class = prev_btn.get_attribute("class") or ""
            if "disabledCls" in prev_class:
                print("[INFO] Previous button is disabled. Already at first page.")
                break

            print("[INFO] Clicking Previous button...")
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", prev_btn)
            try:
                prev_btn.click()
            except:
                driver.execute_script("arguments[0].click();", prev_btn)
            time.sleep(1.5)

    except Exception as e:
        print(f"[ERROR] Failed to go to first page: {e}")