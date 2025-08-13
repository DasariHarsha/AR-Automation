import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
def login(driver, username, password,url):
    driver.get(url)
    time.sleep(2)
    driver.find_element(By.CSS_SELECTOR, '#standard-basic-username').send_keys(username)
    driver.find_element(By.CSS_SELECTOR, '#standard-basic-password').send_keys(password)
    driver.find_element(By.XPATH, '//button[contains(text(), "Login")]').click()
    # time.sleep(3)

def click_create_assessment(driver):
    # driver.find_element(By.CSS_SELECTOR, '#root > div.App > div.main_container > div.sidebar_main > div.sidebar_wrapper > div.sidebar_nav > div:nth-child(7) > div').click()
    # time.sleep(5)
    try:
        # Wait for loader/spinner to disappear
        WebDriverWait(driver, 2000).until(
            EC.invisibility_of_element_located((By.CLASS_NAME, "loader"))
        )

        # Wait for the target menu item to be clickable
        menu_item = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '#root > div.App > div.main_container > div.sidebar_main > div.sidebar_wrapper > div.sidebar_nav > div:nth-child(7) > div'))
        )

        # Scroll into view and click
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", menu_item)
        menu_item.click()

    except Exception as e:
        print(f"[ERROR] Failed to click 'Create Assessment' menu item: {e}")
    

def click_review_assessment(driver):
    # driver.find_element(By.CSS_SELECTOR, '#Review\\ Assessment').click()
    # time.sleep(2)
    try:
        # Wait for loader to disappear (if it exists)
        WebDriverWait(driver, 2000).until(
            EC.invisibility_of_element_located((By.CLASS_NAME, "loader"))
        )

        # Wait for the button to be clickable
        button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '#Review\\ Assessment'))
        )

        # Scroll into view and click
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", button)
        button.click()
        # time.sleep(2)

    except Exception as e:
        print(f"[ERROR] Failed to click 'Review Assessment' button: {e}")

def select_report_from_dropdown(driver, report_name):
    # report_dropdown = driver.find_element(By.CSS_SELECTOR, '#root > div.App > div.main_container > div.right-container > div.white_bg > div.full-width-table-wrapper > div:nth-child(1) > div > div > div > div.col-lg-3.col-md-3 > div > div > div.review_assessment__value-container.css-hlgwow > div.review_assessment__input-container.css-19bb58m')
    # report_dropdown.click()
    # time.sleep(2)
    # report_options = driver.find_elements(By.XPATH, '//div[contains(@class, "review_assessment__option")]')
    # for option in report_options:
    #     if report_name in option.text:
    #         driver.execute_script("arguments[0].scrollIntoView(true);", option)
    #         time.sleep(2)
    #         try:
    #             option.click()
    #         except Exception:
    #             driver.execute_script("arguments[0].click();", option)
    #         break
    # time.sleep(10)
    try:
        # Wait until loader disappears (if present)
        WebDriverWait(driver, 2000).until(
            EC.invisibility_of_element_located((By.CLASS_NAME, "loader"))
        )

        # Wait for the dropdown to be clickable and click it
        dropdown = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 
                '#root > div.App > div.main_container > div.right-container > div.white_bg > div.full-width-table-wrapper > div:nth-child(1) > div > div > div > div.col-lg-3.col-md-3 > div > div > div.review_assessment__value-container.css-hlgwow > div.review_assessment__input-container.css-19bb58m'))
        )
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", dropdown)
        dropdown.click()

        # Wait for report options to appear
        report_options = WebDriverWait(driver, 20).until(
            EC.presence_of_all_elements_located((By.XPATH, '//div[contains(@class, "review_assessment__option")]'))
        )

        # Find and click the matching report option
        for option in report_options:
            if report_name in option.text:
                driver.execute_script("arguments[0].scrollIntoView(true);", option)
                WebDriverWait(driver, 5).until(EC.element_to_be_clickable(option))
                try:
                    option.click()
                except Exception:
                    driver.execute_script("arguments[0].click();", option)
                break

        # Optional: Wait for the page to load or update after selection
        WebDriverWait(driver, 2000).until(
            EC.invisibility_of_element_located((By.CLASS_NAME, "loader"))
        )

    except Exception as e:
        print(f"[ERROR] Failed to select report '{report_name}' from dropdown: {e}")

    time.sleep(2)


def click_assessment_questionnaire(driver):
    driver.find_element(By.CSS_SELECTOR, '#Assessment\\ Questionnaire').click()
    WebDriverWait(driver, 2000).until(
            EC.invisibility_of_element_located((By.CLASS_NAME, "loader"))
        )
