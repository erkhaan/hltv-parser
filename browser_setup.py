from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def get_driver():
    option = webdriver.ChromeOptions()
    chrome_prefs = {}
    option.experimental_options["prefs"] = chrome_prefs
    chrome_prefs["profile.default_content_settings"] = {"images": 2}
    chrome_prefs["profile.managed_default_content_settings"] = {"images": 2}
    driver = webdriver.Chrome(options=option)
    return driver


def apply_cookies(driver):
    driver.get('https://www.hltv.org')
    element_id = 'CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll'
    accept = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.ID, element_id))
    )
    accept.send_keys(Keys.RETURN)
    driver.implicitly_wait(0.5)


driver = get_driver()
apply_cookies(driver)
