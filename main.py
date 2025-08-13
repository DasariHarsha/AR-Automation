# from excel_utils import read_excel_and_filter
# from credentials_utils import read_credentials
from driver_utils import start_driver
from navigation_utils import login, click_create_assessment, click_review_assessment, select_report_from_dropdown, click_assessment_questionnaire
from app_utils import get_applications
from process_utils import process_applications
from after_r_strategy_utils import after_r_strategy
from summary_utils import print_summary, print_summary_for_RecommendationSelection
from InstanceType_process_utils import select_application_and_cloud
# import getpass
import datetime


def run_automation_with_inputs(username, password, report_name, filtered, region, url, skip_rstrategy,skip_instance):
    chromedriver_path = 'chromedriver.exe'
    driver = start_driver(chromedriver_path)
    start_time = datetime.datetime.now()
    try:
        summary = None
        app_summary = None
        summary1 = None
        app_summary1 = None
        login(driver, username, password, url)
        click_create_assessment(driver)
        click_review_assessment(driver)
        select_report_from_dropdown(driver, report_name)
        click_assessment_questionnaire(driver)
        app_names = get_applications(driver)
        if(skip_rstrategy=='No'):
            summary, app_summary = process_applications(driver, app_names, filtered)
        else:
            pass
        if(skip_instance=='No'):
            after_r_strategy(driver)
            summary1, app_summary1 = select_application_and_cloud(driver, region, filtered)
        else:
            pass

    finally:
        driver.quit()
    end_time = datetime.datetime.now()
    if summary is not None and app_summary is not None:
        print_summary(summary, app_summary, start_time, end_time, report_name)
    else:
        print("Rstrategy is Skipped")
    if summary1 is not None and app_summary1 is not None:
        print_summary_for_RecommendationSelection(summary1, app_summary1, start_time, end_time, report_name)
    else:
        print("Instance selection is skipped")
    
 