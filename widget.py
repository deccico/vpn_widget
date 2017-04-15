# coding: latin-1

from gi.repository import Gtk as gtk
from gi.repository import AppIndicator3 as appindicator
import signal


APPINDICATOR_ID = 'vpn_status'

def build_menu():
    menu = gtk.Menu()
    item_quit = gtk.MenuItem('Quit')
    item_quit.connect('activate', quit)
    menu.append(item_quit)
    menu.show_all()
    return menu


def main():
    indicator = appindicator.Indicator.new(APPINDICATOR_ID, gtk.STOCK_INFO, appindicator.IndicatorCategory.SYSTEM_SERVICES)
    indicator.set_status(appindicator.IndicatorStatus.ACTIVE)
    indicator.set_menu(build_menu())

    #This sets the handler for “INT” signal processing 
    #- the one issued by the OS when “Ctrl+C” is typed. 
    #The handler we assign to it is the “default” handler, which, 
    #in case of the interrupt signal, is to stop execution.
    signal.signal(signal.SIGINT, signal.SIG_DFL) #listen to quit signal
    gtk.main()

 
def quit(source):
    gtk.main_quit()


if __name__ == "__main__":
    main()
