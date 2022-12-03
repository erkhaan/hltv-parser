from selenium.webdriver.common.by import By
import matches_parser as mp
import os

player = mp.player_name

# Parse clip links
clip_links = []
clutch_only = False

def is_clutch(text):
    keywords = ['1vs2', '1vs3', '1vs4', '1vs5', 'clutch']
    for word in keywords:
        if word in text:
            return True
    return False

for link in mp.match_links:
    mp.driver.get(link)
    highlight_boxes = mp.driver.find_elements(By.CLASS_NAME,
                                              'highlight.padding.standard-box')
    for box in highlight_boxes:
        clip = box.get_attribute('data-highlight-embed')
        is_player = player in box.text
        if clutch_only:
            if is_player & is_clutch(box.text):
                clip_links.append(clip)
        else:
            if is_player:
                clip_links.append(clip)

# Clean links from params
clean_links = []
for link in clip_links:
    clean_links.append(link
                       .replace('embed?clip=', '')
                       .replace('&autoplay=true&parent=www.hltv.org', ''))
# Create dir if not exists
directory = './data/'
if not os.path.exists(directory):
    os.makedirs(directory)

# Add result to text file
if clutch_only:
    filename = './data/clutches_' + player + '.txt'
else:
    filename = './data/highlights_' + player + '.txt'

with open(filename, 'w', newline='') as myfile:
    for link in clean_links:
        print(link, file=myfile)
