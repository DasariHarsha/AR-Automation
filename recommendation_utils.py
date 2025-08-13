import time
from selenium.webdriver.common.by import By

from selenium.webdriver.remote.webdriver import WebDriver
# from InstanceType_process_utils import select_application_and_cloud
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def click_recommendation_and_selection_tab(driver: WebDriver):
    """
    Clicks on the 'Recommendations & Selections' tab and waits for 2 seconds.
    """
    
    tab_xpath = '//*[@id="Recommendations & Selections"]'
    tab = driver.find_element(By.XPATH, tab_xpath)
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", tab)
    time.sleep(0.5)
    driver.execute_script("arguments[0].click();", tab)
    WebDriverWait(driver, 2000).until(
            EC.invisibility_of_element_located((By.CLASS_NAME, "loader"))
        )
    # time.sleep(2)

def click_next_button(driver: WebDriver):
    """
    Clicks the 'Next' button on the Recommendations & Selections tab.
    """
    next_btn_xpath = '//*[@id="root"]/div[1]/div[2]/div[2]/div[1]/div[4]/div[2]/div[2]/div[2]/div[2]/div/div/div/div[3]/span/button'
    next_btn = driver.find_element(By.XPATH, next_btn_xpath)
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", next_btn)
    time.sleep(0.5)
    driver.execute_script("arguments[0].click();", next_btn)
    # time.sleep(5)
    WebDriverWait(driver, 2000).until(
            EC.invisibility_of_element_located((By.CLASS_NAME, "loader"))
        )

def handle_recommendation_and_selection(driver: WebDriver):
    """
    Handles the process of clicking the Recommendations & Selections tab and then the Next button.
    """
    click_recommendation_and_selection_tab(driver)
    click_next_button(driver)
    # After recommendations, process instance type selection for each application
    # select_application_and_cloud(driver)
