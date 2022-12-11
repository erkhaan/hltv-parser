from selenium.webdriver.common.by import By
import players_parser as pp
import os


def clips_links_from(match_links, name):
    clips_links = []
    for link in match_links:
        driver.get(link)
        clip_boxes = driver.find_elements(By.CLASS_NAME,
                                          'highlight.padding.standard-box')
        for box in clip_boxes:
            if name in box.text:
                clip_link = box.get_attribute('data-highlight-embed')
                clips_links.append(clip_link)
    return clips_links


def clean_links_for(clip_links):
    clean_links = []
    for link in clip_links:
        clean_link = link \
            .replace('embed?clip=', '') \
            .replace('&autoplay=true&parent=www.hltv.org', '')
        clean_links.append(clean_link)
    return clean_links


def save_links(name, links):
    if len(links) == 0:
        return
    directory = './data/players_parser/'
    manage_directory(directory)
    filename = directory + 'highlights_' + name + '.txt'
    write_file(filename, links)


def manage_directory(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)


def write_file(filename, links):
    with open(filename, 'w', newline='') as myfile:
        for link in links:
            print(link, file=myfile)


def print_info_for(count, name, links):
    print(count, '\t', name, '\t', len(links))


def parse_player_clip_links():
    count = 1
    for name, matches in pp.player_match_links.items():
        clip_links = clips_links_from(matches, name)
        links = clean_links_for(clip_links)
        save_links(name, links)
        print_info_for(count, name, links)
        count += 1


driver = pp.driver
parse_player_clip_links()
driver.close()
