#!/usr/bin/env python
# coding: latin-1

"""
Displays VPN connection status in the System bar and lets user connect / disconnect from vpn

To automatically start this script, please check the link below
https://askubuntu.com/questions/48321/how-do-i-start-applications-automatically-on-login
"""

import os
import signal
import subprocess

import gi

gi.require_version('Gtk', '3.0')
from gi.repository import AppIndicator3 as appindicator
from gi.repository import Gtk as gtk
from gi.repository import Notify as notify
from gi.repository import GLib as glib


class Widget:
    APPINDICATOR_ID = 'ubuntu_widget_status'
    BASE_DIR = os.path.dirname(os.path.realpath(__file__))
    ICON_ON = os.path.join(BASE_DIR, "on.svg")
    ICON_OFF = os.path.join(BASE_DIR, "off.svg")
    CONNECTED_STRING = "Connected to "
    CONNECT_CMD = ["expressvpn", "connect", "smart"]
    DISCONNECT_CMD = ["expressvpn", "disconnect"]
    UPDATE_FREQUENCY = 30

    def __init__(self):
        self.indicator = None
        self.connection_status = 0
        self.timer = None

    def build_menu(self):
        menu = gtk.Menu()
        item_status = gtk.MenuItem('Connect')
        item_status.connect('activate', self.connect)
        menu.append(item_status)
        item_status = gtk.MenuItem('Disconnect')
        item_status.connect('activate', self.disconnect)
        menu.append(item_status)
        item_status = gtk.MenuItem('Update Connection Status')
        item_status.connect('activate', self.get_status)
        menu.append(item_status)
        item_quit = gtk.MenuItem('Quit')
        item_quit.connect('activate', self.quit)
        menu.append(item_quit)
        menu.show_all()
        return menu

    def main(self):
        self.indicator = appindicator.Indicator.new(self.APPINDICATOR_ID, self.ICON_OFF,
                                                    appindicator.IndicatorCategory.SYSTEM_SERVICES)
        self.indicator.set_status(appindicator.IndicatorStatus.ACTIVE)
        self.indicator.set_menu(self.build_menu())

        # This sets the handler for “INT” signal processing
        #- the one issued by the OS when “Ctrl+C” is typed.
        #The handler we assign to it is the “default” handler, which,
        #in case of the interrupt signal, is to stop execution.
        signal.signal(signal.SIGINT, signal.SIG_DFL)  #listen to quit signal

        notify.init(self.APPINDICATOR_ID)
        self.update()
        glib.timeout_add_seconds(self.UPDATE_FREQUENCY, self.update)
        gtk.main()


    def quit(self, source):
        if self.timer:
            self.timer.cancel()
        notify.uninit()
        gtk.main_quit()

    def connect(self, _):
        notify.Notification.new("<b>Connection Status</b>", "Connecting..", None).show()
        ret = subprocess.call(self.CONNECT_CMD)
        if ret:
            notify.Notification.new("<b>Connection Status</b>",
                                    "Error trying connect. Please check next connection update to verify the status.",
                                    None).show()
        self.update()

    def disconnect(self, _):
        notify.Notification.new("<b>Connection Status</b>", "Disconnecting..", None).show()
        ret = subprocess.call(self.DISCONNECT_CMD)
        if ret:
            notify.Notification.new("<b>Connection Status</b>",
                                    "Error trying to disconnect. Please check next connection update to verify the status.",
                                    None).show()
        self.update()


    def get_status(self, _):
        notify.Notification.new("<b>Connection Status</b>", self._update_status(), None).show()


    def update(self):
        current_status = self.connection_status
        status = self._update_status()
        if current_status != self.connection_status:
            notify.Notification.new("<b>Connection Status</b>", status, None).show()
        return True


    def _update_status(self):
        status = self.get_connection_status()
        if self.CONNECTED_STRING == status[0:len(self.CONNECTED_STRING)]:
            self.connection_status = 1
            self.indicator.set_icon(self.ICON_ON)
        else:
            self.connection_status = 0
            self.indicator.set_icon(self.ICON_OFF)
        return status

    def get_connection_status(self):
        return subprocess.check_output(["expressvpn", "status"])


if __name__ == "__main__":
    w = Widget()
    w.main()
