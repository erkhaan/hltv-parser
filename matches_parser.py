from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

# First to use
# This file gets match links of a player by ids and date

# Input data
# TODO: Should get as args
player_name = 'cadiaN'
player_id = '7964'
team_id = ['7175']
date_start = '2022-01-01'
date_end = '2022-12-31'

# Disable images
option = webdriver.ChromeOptions()
chrome_prefs = {}
option.experimental_options["prefs"] = chrome_prefs
chrome_prefs["profile.default_content_settings"] = {"images": 2}
chrome_prefs["profile.managed_default_content_settings"] = {"images": 2}
driver = webdriver.Chrome(options=option)

# TODO: - Move to method waitForAllowSelection, because of reuse
driver.get('https://www.hltv.org')
driver.implicitly_wait(5)
accept = driver.find_element(By.ID, 'CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll')
accept.send_keys(Keys.RETURN)
driver.implicitly_wait(0.5)

# TODO: Move to method collectLinks(teamID) -> matchLinks
match_links = []
for team in team_id:
    for offset in ['0', '100', '200']:
        link = ('https://www.hltv.org/results?offset='
                + offset
                + '&startDate='
                + date_start
                + '&endDate='
                + date_end
                + '&team='
                + team
                + '&content=highlights')
        # teamLink = 'https://www.hltv.org/results?content=highlights&'+'player='+playerID+'&startDate='+dateStart+'&endDate='+dateEnd+'&offset='+offset
        driver.get(link)
        try:
            driver.find_elements(By.XPATH, "//*[contains(text(), 'My Button')]")
            elem = driver.find_element(By.CSS_SELECTOR, "div.results-all:not(.results-holder)")
            hrefs = elem.find_elements(By.CLASS_NAME, 'a-reset')
            for href in hrefs:
                match_links.append(href.get_attribute('href'))
        except NoSuchElementException:
            pass
