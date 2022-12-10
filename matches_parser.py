from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import browser_setup as bs

# First to use
# This file gets match links of a player by ids and date

# Input data
# TODO: Should get as args
player_name = 'cadiaN'
player_id = '7964'
team_id = ['7175']
date_start = '2022-09-01'
date_end = '2022-12-31'

# Browser
driver = bs.driver

def get_link(offset, date_start, date_end, team):
    link = ('https://www.hltv.org/results?offset='
            + offset
            + '&startDate='
            + date_start
            + '&endDate='
            + date_end
            + '&team='
            + team
            + '&content=highlights')
    return link


# TODO: Move to method collectLinks(teamID) -> matchLinks
match_links = []
for team in team_id:
    for offset in ['0', '100', '200']:
        link = get_link(offset,
                        date_start,
                        date_end,
                        team)
        driver.get(link)
        try:
            driver.find_elements(By.XPATH, "//*[contains(text(), 'My Button')]")
            elem = driver.find_element(By.CSS_SELECTOR, "div.results-all:not(.results-holder)")
            hrefs = elem.find_elements(By.CLASS_NAME, 'a-reset')
            for href in hrefs:
                match_links.append(href.get_attribute('href'))
        except NoSuchElementException:
            pass
