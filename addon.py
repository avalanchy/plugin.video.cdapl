# encoding: utf8
import xbmcaddon
import xbmcgui


addon = xbmcaddon.Addon()
addonname = addon.getAddonInfo('name')

line1 = u"Hello Świat!"
line2 = "No to teraz to jest po polsku"
line3 = "Using Python"

xbmcgui.Dialog().ok(addonname, line1, line2, line3)
