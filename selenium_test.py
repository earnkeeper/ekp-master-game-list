
from pprint import pprint
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from fake_useragent import UserAgent
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

# options = Options()

# options.add_argument('--headless')
# options.add_argument("--incognito")
# options.add_argument("--nogpu")
# options.add_argument("--disable-gpu")
# options.add_argument("--window-size=1280,1280")
# options.add_argument("--no-sandbox")
# options.add_argument("--enable-javascript")
# options.add_experimental_option("excludeSwitches", ["enable-automation"])
# options.add_experimental_option('useAutomationExtension', False)
# options.add_argument('--disable-blink-features=AutomationControlled')

# ua = UserAgent()
# userAgent = ua.random

# print(userAgent)

# driver = webdriver.Chrome(options=options)
# driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
# driver.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": userAgent})

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
print(element.get_attribute("src"))

element = driver.find_element(
    By.XPATH, "//a[contains(@href, '/earnkeeper/followers')]"
)

element = element.find_element(By.CSS_SELECTOR, 'span > span')
followers = int(element.text.replace(",", ""))
print(followers)

