from selenium.webdriver.common.by import By
import matches_parser as mp
import os

player = mp.player_name

# Parse clip links
clip_links = []
for link in mp.match_links:
    mp.driver.get(link)
    highlight_boxes = mp.driver.find_elements(By.CLASS_NAME,
                                              'highlight.padding.standard-box')
    for box in highlight_boxes:
        # Required highlights
        # if (playerName in i.text and ('ACE' in i.text or '1vs5' in i.text or '1vs4' in i.text or '1vs3' in i.text or '4' in i.text or 'quick' in i.text)):
        if player in box.text:
            clip_links.append(box.get_attribute('data-highlight-embed'))

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
filename = './data/highlights_' + player + '.txt'
with open(filename, 'w', newline='') as myfile:
    for link in clean_links:
        print(link, file=myfile)
