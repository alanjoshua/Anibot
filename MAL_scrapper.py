# THIS IS AM ABANDONED MODULE

# This module uses MAl to get information about anime, but I abandoned it because MAL is usually not immediately updated
# with information about the latest anime, and sometimes even seasons that have finished airing have some \
# episodes missing

from mal import AnimeSearch
from mal import Anime
import requests
from bs4 import BeautifulSoup


def getAllEpisodes(animeId):
    episodes = {}
    anime = Anime(animeId)
    url = anime.url
    newUrl = url + "/episode"

    page_response = requests.get(newUrl)
    master_page = BeautifulSoup(page_response.content, "html.parser")

    try:
        pages = master_page.find("div", class_='pagination ac').find_all('a')
    except:
        pages = []

    diffLinks = []
    for tag in pages:
        diffLinks.append(tag.get('href'))

    if len(diffLinks) == 0:
        diffLinks.append(newUrl)

    print(f"episode links: {diffLinks}")

    for link in diffLinks:
        page_response = requests.get(link)
        curr_page = BeautifulSoup(page_response.content, "html.parser")

        table = curr_page.find_all("table", class_='mt8 episode_list js-watch-episode-list ascend')[0]
        rows = table.find_all("tr", class_='episode-list-data')

        for row in rows:
            info = {}
            ep_num = int(row.find("td", class_='episode-number').text)

            info['episode_number'] = ep_num
            info['episode_name'] = row.find("td", class_='episode-title').find('a').text
            info['episode_aired'] = row.find("td", class_='episode-aired').text
            info['forum_link'] = row.find('td', class_='episode-forum ac nowrap').find('a').get('href')

            episodes[ep_num] = info
            print(f'Extracted episode {ep_num}...')

    return episodes


def getLatestEpisode(animeId):
    anime = Anime(animeId)
    url = anime.url
    newUrl = url + "/episode"

    page_response = requests.get(newUrl)
    master_page = BeautifulSoup(page_response.content, "html.parser")

    try:
        pages = master_page.find("div", class_='pagination ac').find_all('a')
    except:
        pages = []

    diffLinks = []
    for tag in pages:
        diffLinks.append(tag.get('href'))

    if len(diffLinks) == 0:
        diffLinks.append(newUrl)

    link = diffLinks[-1]  # Get last page of episodes

    page_response = requests.get(link)
    curr_page = BeautifulSoup(page_response.content, "html.parser")

    table = curr_page.find_all("table", class_='mt8 episode_list js-watch-episode-list ascend')
    if (table is None) or (len(table) == 0):
        print('Could not find episodes table')
        return None

    table = table[0]
    rows = table.find_all("tr", class_='episode-list-data')

    last_episode = rows[-1]  # Get last element
    info = {}
    ep_num = int(last_episode.find("td", class_='episode-number').text)

    info['episode_number'] = ep_num
    info['episode_name'] = last_episode.find("td", class_='episode-title').find('a').text
    info['episode_aired'] = last_episode.find("td", class_='episode-aired').text
    info['forum_link'] = last_episode.find('td', class_='episode-forum ac nowrap').find('a').get('href')

    print(f'Last episode num: {ep_num}')

    return info


def isEpisodeAvailable(malId, req_ep):
    if req_ep < 0:
        return False

    last_episode = getLatestEpisode(malId)
    if last_episode is None:
        return False

    return True if req_ep <= last_episode['episode_number'] else False


# def printAnime(anime):
#     print(f'Title: {anime.title_english}')
#     print(f'mal_id: {anime.mal_id}')
#     print(f"Status: {anime.status}")
#     print(f'Type: {anime.type}')
#     print(f'Aired: {anime.aired}')
#
#
# searchDefIndex = 0
# searchQuery = "Jujutsu Kaisen TV"
#
# search = AnimeSearch(searchQuery)  # Search for "cowboy bebop"
# anime = Anime(search.results[searchDefIndex].mal_id)
# printAnime(anime)
#
# for res in search.results:
#     print(f'{res.title} : {res.mal_id}')
#
# # last = getLatestEpisode(anime)
# print(isEpisodeAvailable(40748, 9))
# # print(last)