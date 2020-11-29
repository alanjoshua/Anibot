import requests
from bs4 import BeautifulSoup
from selenium import webdriver


options = webdriver.ChromeOptions()
options.add_argument("--disable-extensions")
options.add_argument("--disable-gpu")
options.add_argument("--headless")

BASE_URL = 'https://gogoanime.so/'  # Change this if this link to gogoanime goes down


def validateName(name):
    if len(name.split()) > 0:
        name = str(name).lower()
        newName = str(name).replace(' ', '-')
        newName = newName.replace(":", '-')
        newName = newName.replace("--", '-')
    return newName


# Uses selenium to get last Episode
def getLastEpisode(anime, base_url=BASE_URL):
    anime = validateName(anime)
    print(anime)
    newUrl = base_url + "category/" + anime

    # driver = webdriver.Chrome(options=options, executable_path=r'C:\Program Files\chromedriver.exe')
    driver = webdriver.Chrome(options=options)
    driver.get(newUrl)

    try:
        episodes_list = driver.find_element_by_css_selector("ul[id='episode_related']")
        lastEpisode = episodes_list.find_element_by_css_selector("a")
        lastEpisode_num = int(lastEpisode.find_element_by_class_name("name").text.split()[1])
        lastEpisode_num_part_link = lastEpisode.get_attribute("href")
        lastEpisode_link = lastEpisode_num_part_link
    except:
        driver.close()
        return None

    driver.quit()
    return {"num": lastEpisode_num, "link": lastEpisode_link}


def getEpisode(anime, re_ep, base_url=BASE_URL):
    anime = validateName(anime)
    episodeUrl = base_url + anime + '-episode-' + str(re_ep)
    page_response = requests.get(episodeUrl)
    master_page = BeautifulSoup(page_response.content, "html.parser")

    try:
        master_page.find('h1', class_='entry-title').text
        print('episode not found')
        return None
    except:
        return episodeUrl


def search(anime, base_url=BASE_URL):
    anime = validateName(anime)
    searchUrl = base_url + '/search.html?keyword='+anime

    page_response = requests.get(searchUrl)
    page = BeautifulSoup(page_response.content, "html.parser")

    items = page.find('div', class_='last_episodes').findAll('li')
    res = []

    for item in items:
        info = {}
        info['name'] = item.find('p', class_='name').find('a').text
        info['link'] = base_url + item.find('p', class_='name').find('a').get('href')
        info['released'] = item.find('p', class_='released').text.strip()
        res.append(info)

    return res