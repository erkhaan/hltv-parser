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

min_matches = 50

player_match_links = {}


def get_link(player_id, date_start, date_end, offset):
    link = 'https://www.hltv.org/results?content=highlights&' \
           + 'player=' + player_id \
           + '&startDate=' + date_start \
           + '&endDate=' + date_end \
           + '&offset=' + offset
    return link


def is_enough_matches(driver, min_count):
    element_pagination = driver.find_element(By.CLASS_NAME, 'pagination-data')
    text = element_pagination.text
    pagination_data = [int(s) for s in text.split() if s.isdigit()]
    matches_count = pagination_data[2]
    if matches_count < min_count:
        return False
    else:
        return True


def parse_matches(driver, player_id):
    is_error = False
    matches_links = []
    for offset in ['0', '100', '200']:
        link = get_link(player_id, date_start,
                        date_end, offset)
        driver.get(link)
        try:
            driver.find_element(By.CLASS_NAME, 'error-body')
            is_error = True
            break
        except NoSuchElementException:
            pass
        if not is_enough_matches(driver, min_matches):
            is_error = True
            break
        try:
            driver.find_elements(By.XPATH, "//*[contains(text(), 'My Button')]")
            elem = driver.find_element(By.CSS_SELECTOR, "div.results-all:not(.results-holder)")
            hrefs = elem.find_elements(By.CLASS_NAME, 'a-reset')
            for href in hrefs:
                matches_links.append(href.get_attribute('href'))
        except NoSuchElementException:
            pass
    return matches_links, is_error


def get_player_name(driver, id):
    link = '/player/' + id + '/'
    name = driver.find_element(By.XPATH, '//a[contains(@href, "%s")]' % link).text
    return name


def print_links(player_match_links):
    for name, links in player_match_links.items():
        print(name, len(links))
        print(links)


def parse_players():
    for int_id in range(id_start - 1, id_end):
        player_id = str(int_id + 1)
        (matches_links, is_error) = parse_matches(driver, player_id)
        if is_error:
            continue
        name = get_player_name(driver, player_id)
        player_match_links[name] = matches_links


parse_players()
print_links(player_match_links)
