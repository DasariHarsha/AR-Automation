from selenium import webdriver
from selenium.webdriver.chrome.service import Service

def start_driver(chromedriver_path):
    service = Service(chromedriver_path)
    driver = webdriver.Chrome(service=service)
    return driver
