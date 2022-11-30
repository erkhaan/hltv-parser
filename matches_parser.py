from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import csv
import os

# First to use
# This file gets match links of a player by ids and date
# Returns csv file with links into ./data

# Input data
# TODO: Should get as args
playerName = 'cadiaN'
playerID = '7964'
teamID = ['7175']
dateStart = '2022-01-01'
dateEnd = '2022-12-31'

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
matchLinks = []
for team in teamID:
    for offset in ['0', '100', '200']:
        teamLink = ('https://www.hltv.org/results?offset='
                    + offset
                    + '&startDate='
                    + dateStart
                    + '&endDate='
                    + dateEnd
                    + '&team='
                    + team
                    + '&content=highlights')
        # teamLink = 'https://www.hltv.org/results?content=highlights&'+'player='+playerID+'&startDate='+dateStart+'&endDate='+dateEnd+'&offset='+offset
        driver.get(teamLink)
        try:
            driver.find_elements(By.XPATH, "//*[contains(text(), 'My Button')]")
            elem = driver.find_element(By.CSS_SELECTOR, "div.results-all:not(.results-holder)")
            hrefs = elem.find_elements(By.CLASS_NAME, 'a-reset')
            for href in hrefs:
                matchLinks.append(href.get_attribute('href'))
        except NoSuchElementException:
            pass

# Create dir if not exists
directory = './data/'
if not os.path.exists(directory):
    os.makedirs(directory)

file_path = ('./data/matches_'
             + playerName
             + '.csv')

# Overwrites if file exist
with open(file_path, 'w', newline='') as myfile:
    wr = csv.writer(myfile)
    wr.writerow(['links'])
    for link in matchLinks:
        wr.writerow([link])

# After file is created, parse highlights
