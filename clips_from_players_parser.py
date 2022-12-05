from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import pandas as pd
import players_parser as pp
import os

driver = pp.driver
k = 1
for name, links in pp.player_match_links.items():
    match_list = links
    # print(len(matchList))
    player_name = name

    hlLink = []
    for link in match_list:
        driver.get(link)
        highlightBoxes = driver.find_elements(By.CLASS_NAME, 'highlight.padding.standard-box')
        for i in highlightBoxes:
            if player_name in i.text:
                hlLink.append(i.get_attribute('data-highlight-embed'))
    cleanLink = []

    for link in hlLink:
        cleanLink.append(link.replace('embed?clip=', '').replace('&autoplay=true&parent=www.hltv.org', ''))
    directory = './data/players_parser/'
    if not os.path.exists(directory):
        os.makedirs(directory)

    filename = directory + 'highlights_' + player_name + '.txt'
    with open(filename, 'w', newline='') as myfile:
        for link in cleanLink:
            print(link, file=myfile)
    print(k, '\t', player_name, '\t', len(hlLink))
    k += 1
driver.close()