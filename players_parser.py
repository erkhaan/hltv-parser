from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

# disable images
option = webdriver.ChromeOptions()
chrome_prefs = {}
option.experimental_options["prefs"] = chrome_prefs
chrome_prefs["profile.default_content_settings"] = {"images": 2}
chrome_prefs["profile.managed_default_content_settings"] = {"images": 2}
driver = webdriver.Chrome(options=option)

driver.get('https://www.hltv.org')
driver.implicitly_wait(5)
accept = driver.find_element(By.ID, 'CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll')
accept.send_keys(Keys.RETURN)
driver.implicitly_wait(0.5)

id_start = 7964
id_end = 7970
date_start = '2021-01-01'
date_end = '2021-12-31'

min_value = 30

player_match_links = {}

for id in range(id_start - 1, id_end):
    player_id = str(id + 1)
    is_empty = 0
    is_error = 0
    matches_links = []
    for offset in ['0', '100', '200']:
        link = 'https://www.hltv.org/results?content=highlights&' \
               + 'player=' \
               + player_id \
               + '&startDate=' \
               + date_start \
               + '&endDate=' \
               + date_end \
               + '&offset=' \
               + offset
        driver.get(link)
        try:
            driver.find_element(By.CLASS_NAME, 'error-body')
            is_error = 1
            break
        except NoSuchElementException:
            pass
        elemPag = driver.find_element(By.CLASS_NAME, 'pagination-data')
        text = elemPag.text
        a = [int(s) for s in text.split() if s.isdigit()]
        if a[2] < min_value:
            is_empty = 1
            break
        try:
            driver.find_elements(By.XPATH, "//*[contains(text(), 'My Button')]")
            elem = driver.find_element(By.CSS_SELECTOR, "div.results-all:not(.results-holder)")
            hrefs = elem.find_elements(By.CLASS_NAME, 'a-reset')
            for href in hrefs:
                matches_links.append(href.get_attribute('href'))
        except NoSuchElementException:
            pass
    if is_empty == 1 or is_error == 1:
        continue
    player_link = '/player/' + player_id + '/'
    player_name = driver.find_element(By.XPATH, '//a[contains(@href, "%s")]' % player_link).text
    player_match_links[player_name] = matches_links
    for name, links in player_match_links.items():
        print(name, links)
driver.close()
