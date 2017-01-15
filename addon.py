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



def cda_id_to_object(url='http://m.cda.pl/video/11557750e?wersja=720p'):
    response = urllib2.urlopen(url)
    html = response.read()
    title = re.search('<title>([^<]+)', html).group(1)
    player_data = re.search("player_data='([^']+)", html).group(1)
    player_data = json.loads(player_data)
    return {
        'title': "Kevinn",
        'poster_url': '',
        'video_url': '',
    }
    return {
        'title': title,
        'poster_url': player_data['video']['poster'],
        'video_url': player_data['video']['file'] + '.mp4',
    }




import urllib

def request_search(query):
    query = urllib.quote_plus(query)
    url_base = 'http://m.cda.pl/szukaj?q={}&gdzie=v&duration=dlugie&quality=all&s=best'
    url = url_base.format(query)
    logging.warn(url)
    response = urllib2.urlopen(url)
    html = response.read()
    titles = re.findall('<h2 class="title">([^<]+)', html)
    thumbs = re.findall('<img class="box-elem-img" src="([^"]+)', html)
    cda_ids = re.findall('<a class="link-box-elem" href="/video/([^"]+)', html)
    return zip(titles, thumbs, cda_ids)





if __query__.startswith('?cda-id='):
    # we gonna play movie
    pass
    logging.warn('plaing movie')
else:
    logging.warning(sys.argv)

    addon = xbmcaddon.Addon()
    addonname = addon.getAddonInfo('name')

    logging.warn('before modal')
    keyboard = xbmc.Keyboard('', 'Wpisz tytuł filmu', False)
    keyboard.doModal()
    logging.warn('after modal')
    user_input = keyboard.getText()
    if keyboard.isConfirmed() and user_input != '':
        search_results = request_search(user_input)
        logging.warn(search_results)

        kodi_search_res = []

        for title, thumb, cda_id in search_results:
            url = '{}?cda-id={}'.format(__url__, cda_id)
            list_item = xbmcgui.ListItem(label=title, thumbnailImage=thumb)
            list_item.setInfo('video', {})
            kodi_search_res.append((url, list_item, False))

        xbmcplugin.addDirectoryItems(__handle__, kodi_search_res)


    search_item = xbmcgui.ListItem(label='Search...')
    xbmcplugin.addDirectoryItem(handle=__handle__, url=__url__+ '?mode=search', listitem=search_item, isFolder=False, totalItems=1)


    xbmcplugin.addSortMethod(__handle__, xbmcplugin.SORT_METHOD_NONE)
    xbmcplugin.endOfDirectory(__handle__)


    #    line1 = "Hello World!"
#    line2 = "Nice to meet you %s" %(keyboard.getText())
#    line3 = "Welcome to Kodi!"
#
#    xbmcgui.Dialog().ok(addonname, line1, line2, line3) ###

