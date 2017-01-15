#coding: utf8
import logging
import json
import re
import sys
import urllib2

import xbmc
import xbmcaddon
import xbmcgui
import xbmcplugin


# Get the plugin url in plugin:// notation.
__url__ = sys.argv[0]
# Get the plugin handle as an integer number.
__handle__ = int(sys.argv[1])
__query__ = sys.argv[2]


def get_cda_video_data(cda_id, quality):
    url = 'http://m.cda.pl/video/{}?wersja={}'
    url = url.format(cda_id, quality)
    response = urllib2.urlopen(url)
    html = response.read()
    title = re.search('<title>([^<]+)', html).group(1)
    player_data = re.search("player_data='([^']+)", html).group(1)
    player_data = json.loads(player_data)
    return {
        'title': title,
        'poster_url': player_data['video']['poster'],
        'video_url': player_data['video']['file'] + '.mp4',
    }



import urllib
from bs4 import BeautifulSoup

def request_search(query):
    query = urllib.quote_plus(query)
    url_base = 'http://m.cda.pl/szukaj?q={}&gdzie=v&duration=dlugie&quality=all&s=best'
    url = url_base.format(query)
    response = urllib2.urlopen(url)
    html = response.read()
    items = []
    bs = BeautifulSoup(html, 'lxml')
    results = bs.find_all('div', attrs={'class': 'box-elem'})
    for result in results:
        cda_id = result.find('a').attrs['href'].split('/')[-1]
        title = result.find('h2').text
        thumb = result.find('img').attrs['src']
        quality = result.find('span', attrs={'class': 'quality'})
        quality = quality.text if quality else ''
        duration = result.find('span', attrs={'class': 'timeElem'}).text
        h, m, s = duration.split(':')
        duration = int(h) * 3600 + int(m) * 60 + int(s)
        items.append((cda_id, title, thumb, quality, duration))
    return items


match = re.match('\?cda-id=(\w+)&quality=(\w*)', __query__)



if match:
    cda_id, quality = match.groups()
    obj = get_cda_video_data(cda_id, quality)

    # we gonna play movie
    player = xbmc.Player()
    player.play(obj['video_url'])
    sys.exit(0)


addon = xbmcaddon.Addon()
addonname = addon.getAddonInfo('name')

user_input = xbmcgui.Dialog().input('Wpisz tytuł filmu')
if user_input != '':
    search_results = request_search(user_input)

    kodi_search_res = []

    for cda_id, title, thumb, quality, duration in search_results:
        url = '{}?cda-id={}&quality={}'.format(__url__, cda_id, quality)
        list_item = xbmcgui.ListItem(label=title, thumbnailImage=thumb)
        list_item.setInfo('video', {'plot': 'bla bla bla', 'mediatype': 'movie', 'date': '01.01.2009'})
        list_item.setProperty("IsPlayable", "true")
        height = re.search('\d*', quality).group()
        list_item.addStreamInfo('video', {'codec': 'h264', 'aspect': 1.78, 'width': 1920, 'height': 1080, 'duration': duration})
        list_item.setArt({'icon': 'icon.png'})
        kodi_search_res.append((url, list_item, False))

    xbmcplugin.addDirectoryItems(__handle__, kodi_search_res)

search_item = xbmcgui.ListItem(label='Search...')
xbmcplugin.addDirectoryItem(handle=__handle__, url=__url__+ '?mode=search', listitem=search_item, isFolder=False, totalItems=1)


xbmcplugin.addSortMethod(__handle__, xbmcplugin.SORT_METHOD_NONE)
xbmcplugin.endOfDirectory(__handle__)
