# coding: latin-1


import os

import json
from urllib2 import Request, urlopen, URLError

from gi.repository import AppIndicator3 as appindicator
from gi.repository import Gtk as gtk
from gi.repository import Notify as notify
import signal


APPINDICATOR_ID = 'ubuntu_widget_status'
ICON_ON = os.path.abspath("on.svg")
ICON_OFF = os.path.abspath("off.svg")
global_indicator = None

def fetch_joke():
    request = Request('http://api.icndb.com/jokes/random?limitTo=[nerdy]')
    response = urlopen(request)
    joke = json.loads(response.read())['value']['joke']
    return joke

def build_menu():
    menu = gtk.Menu()
    item_joke = gtk.MenuItem('Joke')
    item_joke.connect('activate', joke)
    menu.append(item_joke)
    item_quit = gtk.MenuItem('Quit')
    item_quit.connect('activate', quit)
    menu.append(item_quit)
    menu.show_all()
    return menu


def main():
    indicator = appindicator.Indicator.new(APPINDICATOR_ID, gtk.STOCK_INFO, appindicator.IndicatorCategory.SYSTEM_SERVICES)
    indicator = appindicator.Indicator.new(APPINDICATOR_ID, ICON_ON, appindicator.IndicatorCategory.SYSTEM_SERVICES)
    indicator.set_status(appindicator.IndicatorStatus.ACTIVE)
    indicator.set_menu(build_menu())
    global_indicator = indicator
    global_indicator.set_icon(ICON_OFF)
    #This sets the handler for “INT” signal processing 
    #- the one issued by the OS when “Ctrl+C” is typed. 
    #The handler we assign to it is the “default” handler, which, 
    #in case of the interrupt signal, is to stop execution.
    signal.signal(signal.SIGINT, signal.SIG_DFL) #listen to quit signal
    notify.init(APPINDICATOR_ID)
    gtk.main()

 
def quit(source):
    notify.uninit()
    gtk.main_quit()

def joke(_):
    global_indicator.set_icon(ICON_OFF)
    notify.Notification.new("<b>Joke</b>", fetch_joke(), None).show()


if __name__ == "__main__":
    main()
