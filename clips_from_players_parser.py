from selenium.webdriver.common.by import By
import players_parser as pp
import os


def get_highlight_links(matches, name):
    highlight_links = []
    for link in matches:
        driver.get(link)
        highlight_boxes = driver.find_elements(By.CLASS_NAME, 'highlight.padding.standard-box')
        for box in highlight_boxes:
            if name in box.text:
                highlight_links.append(box.get_attribute('data-highlight-embed'))
    return highlight_links


def get_cleaned_links(highlight_links):
    cleaned_links = []
    for link in highlight_links:
        cleaned_links.append(link.replace('embed?clip=', '').replace('&autoplay=true&parent=www.hltv.org', ''))
    return cleaned_links


def manage_directory(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)


def save_links_in_file(name, links):
    directory = './data/players_parser/'
    manage_directory(directory)
    filename = directory + 'highlights_' + name + '.txt'
    with open(filename, 'w', newline='') as myfile:
        for link in links:
            print(link, file=myfile)


def print_info(count, name, links):
    print(count, '\t', name, '\t', len(links))


def parse_player_clip_links():
    count = 1
    for name, matches in pp.player_match_links.items():
        highlight_links = get_highlight_links(matches, name)
        links = get_cleaned_links(highlight_links)
        save_links_in_file(name, links)
        print_info(count, name, links)
        count += 1


driver = pp.driver
parse_player_clip_links()
driver.close()
