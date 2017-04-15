# coding: latin-1


import os
import signal
import subprocess
import threading

from gi.repository import AppIndicator3 as appindicator
from gi.repository import Gtk as gtk
from gi.repository import Notify as notify


class Widget:
    APPINDICATOR_ID = 'ubuntu_widget_status'
    ICON_ON = os.path.abspath("on.svg")
    ICON_OFF = os.path.abspath("off.svg")
    CONNECTED_STRING = "Connected to "

    def __init__(self):
        self.indicator = None
        self.connection_status = 0
        self.timer = None

    def build_menu(self):
        menu = gtk.Menu()
        item_status = gtk.MenuItem('Force Status Update')
        item_status.connect('activate', self.set_status)
        menu.append(item_status)
        item_quit = gtk.MenuItem('Quit')
        item_quit.connect('activate', self.quit)
        menu.append(item_quit)
        menu.show_all()
        return menu

    def main(self):
        self.indicator = appindicator.Indicator.new(self.APPINDICATOR_ID, gtk.STOCK_INFO, appindicator.IndicatorCategory.SYSTEM_SERVICES)
        self.indicator = appindicator.Indicator.new(self.APPINDICATOR_ID, self.ICON_OFF, appindicator.IndicatorCategory.SYSTEM_SERVICES)
        self.indicator.set_status(appindicator.IndicatorStatus.ACTIVE)
        self.indicator.set_menu(self.build_menu())
        #This sets the handler for “INT” signal processing
        #- the one issued by the OS when “Ctrl+C” is typed.
        #The handler we assign to it is the “default” handler, which,
        #in case of the interrupt signal, is to stop execution.
        signal.signal(signal.SIGINT, signal.SIG_DFL) #listen to quit signal
        notify.init(self.APPINDICATOR_ID)
        self.set_status(None)
        #self.timer = threading.Timer(5.0, self.set_status(None))
        #self.timer.start()
        gtk.main()

    def quit(self, source):
        self.timer.cancel()
        notify.uninit()
        gtk.main_quit()

    def set_status(self,_):
        print("setting status...")
        status = self.get_connection_status()
        if self.CONNECTED_STRING == status[0:len(self.CONNECTED_STRING)]:
            self.connection_status = 1
            self.indicator.set_icon(self.ICON_ON)
        else:
            self.connection_status = 0
            self.indicator.set_icon(self.ICON_OFF)
        notify.Notification.new("<b>Connection Status</b>", status, None).show()

    def get_connection_status(self):
        return subprocess.check_output(["expressvpn", "status"])

if __name__ == "__main__":
    w = Widget()
    w.main()
