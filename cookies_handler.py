from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By


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
    driver.implicitly_wait(5)
    accept = driver.find_element(By.ID, 'CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll')
    accept.send_keys(Keys.RETURN)
    driver.implicitly_wait(0.5)


driver = get_driver()
apply_cookies(driver)
