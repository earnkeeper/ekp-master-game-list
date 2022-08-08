
from pprint import pprint
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from fake_useragent import UserAgent
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

driver = webdriver.Remote(
    command_executor='http://127.0.0.1:4444/wd/hub',
    desired_capabilities=DesiredCapabilities.CHROME
)

driver.get("https://twitter.com/earnkeeper")

WebDriverWait(driver, 10).until(
    EC.presence_of_element_located(
        (By.XPATH, "//a[contains(@href, '/earnkeeper/followers')]"))
)

element = driver.find_element(By.XPATH, "//a[contains(@href, '/earnkeeper/header_photo')]")

element = element.find_element(By.TAG_NAME, "img")

element = driver.find_element(
    By.XPATH, "//a[contains(@href, '/earnkeeper/followers')]"
)

element = element.find_element(By.CSS_SELECTOR, 'span > span')
followers = int(element.text.replace(",", ""))

