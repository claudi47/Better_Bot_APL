import time

import requests  # for the first tests we'll use requests because it's simple
from bs4 import BeautifulSoup  # web scraping module(bs4) with class(BeautifulSoup)
from selenium import webdriver  # necessary for web dynamic pages
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

url = 'https://sports.bwin.it/it/sports/calcio-4'
url_list = {
    'serie_A': '/scommesse/italia-20/serie-a-102846',
    'champions_league': '/scommesse/europa-7/champions-league-0:3',
    'europa_league': '/scommesse/europa-7/uefa-europa-league-0:5',
    'premier_league': '/scommesse/inghilterra-14/premier-league-102841',
    'la_liga': '/scommesse/spagna-28/laliga-102829',
    'bundesliga': '/scommesse/germania-17/bundesliga-102842',
    'ligue_1': '/scommesse/francia-16/ligue-1-102843',
    'serie_B': '/scommesse/italia-20/serie-b-102848'
}
# headers = {
#     'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
#                   'Chrome/96.0.4664.45 Safari/537.36'
# }
# page = requests.get(url, headers=headers)  # the second param is needed to bypass anti-bot security
# if not page.ok:
#     print(page.reason)
#     exit(-1)
# content = page.content
#
# # from this point we'll use BeautifulSoup
# # https://www.crummy.com/software/BeautifulSoup/bs4/doc/#installing-a-parser
# parser_var = BeautifulSoup(content, 'lxml')
# body = parser_var.find('body')
# print(body)
# # .scroll-adapter.scroll-adapter--large-arrows ul > li:nth-of-type(1)
# selector = parser_var.select('.scroll-adapter.scroll-adapter--large-arrows ul > li:nth-of-type(1)')
# print(selector)

# another approach because we noticed that bwin's page is dynamic, so requests-BeautifulSoup are not effective
# this second approach requires the usage of Selenium library and an external driver (downloaded from the website of
# Selenium docs). We put the exe of this driver in the same directory of the project
serv = Service('../chromedriver.exe')
# the successive two lines are useful to set the window size where the bot will take the infos
# in fact, in bwin site, smaller window means less information on the screen
chrome_opts = webdriver.ChromeOptions()
chrome_opts.add_argument('window-size=1920,1080')
#  chrome_opts.add_argument('headless')
driver = webdriver.Chrome(service=serv, options=chrome_opts)
try:
    # if an element is not found, the driver will wait at most 3 seconds
    driver.implicitly_wait(3)
    driver.get(url + url_list['champions_league'])
    #  time.sleep(2)  # time necessary to load the page
    #  web_element = driver.find_element(By.CSS_SELECTOR, '.grid')

    # This method waits that the element is present in the web page
    web_element = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.grid')))
    #  print(web_element.text)
    ms_event_groups = WebDriverWait(driver, 5).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.grid > ms-event-group')))
    #  print(ms_event_groups.text)
    for ms_event_group in ms_event_groups:
        header = ms_event_group.find_element(By.CSS_SELECTOR, 'ms-event-group > .header-wrapper')
        day = header.find_element(By.CSS_SELECTOR, 'ms-event-group .date-group')
        print(day.get_property('textContent').upper())

        ms_events = ms_event_group.find_elements(By.CSS_SELECTOR, 'ms-event-group > ms-event')
        for ms_event in ms_events:
            team1 = ms_event.find_element(By.CSS_SELECTOR,
                                          '.grid-event-detail > .grid-event-name  .participants-pair-game > div:nth-of-type(1)')
            team2 = ms_event.find_element(By.CSS_SELECTOR,
                                          '.grid-event-detail > .grid-event-name  .participants-pair-game > div:nth-of-type(2)')
            #  '.grid-event-detail > .grid-event-name > ms-inline-tooltip > div > div:nth-of-type(1) > .participant-container > .participant'
            #  content-message fullscreen-promo-banner djsignup / ui-icon theme-ex ng-star-inserted

            print(team1.get_property('textContent') + " - " + team2.get_property('textContent'))
    driver.quit()
except Exception as e:
    print(e)
    driver.quit()
