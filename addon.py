import sys
from urlparse import parse_qsl
import xbmcgui
import xbmcplugin



# Get the plugin url in plugin:// notation.
__url__ = sys.argv[0]
# Get the plugin handle as an integer number.
__handle__ = int(sys.argv[1])

import json
import re
import urllib2



def url_to_object(url='http://m.cda.pl/video/11557750e?wersja=720p'):
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


obj = url_to_object()

url = '{0}?action=play&video={1}'.format(__url__, obj['video_url'])

list_item = xbmcgui.ListItem(
    label=obj['title'],
    thumbnailImage=obj['poster_url'],
)
list_item.setInfo('video', {})
list_item.setProperty('IsPlayable', 'true')


list_item = xbmcgui.ListItem(
    label=obj['title'],
    thumbnailImage=obj['poster_url'],
)

listing = []
listing.append((obj['video_url'], list_item, False))

xbmcplugin.addDirectoryItems(__handle__, listing, len(listing))

xbmcplugin.addSortMethod(__handle__, xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE)
xbmcplugin.endOfDirectory(__handle__)



import xbmcaddon

import xbmc

addon       = xbmcaddon.Addon()
addonname   = addon.getAddonInfo('name')

keyboard = xbmc.Keyboard("", "Type your name", False)
keyboard.doModal()
if keyboard.isConfirmed() and keyboard.getText() != "":
    line1 = "Hello World!"
    line2 = "Nice to meet you %s" %(keyboard.getText())
    line3 = "Welcome to Kodi!"

    xbmcgui.Dialog().ok(addonname, line1, line2, line3) ###