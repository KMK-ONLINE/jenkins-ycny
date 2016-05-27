# -*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-
### BEGIN LICENSE
# This file is in the public domain
### END LICENSE

"""Code to add AppIndicator."""

from gi.repository import Gtk # pylint: disable=E0611
from gi.repository import GLib
from gi.repository import AppIndicator3 # pylint: disable=E0611

from jenkins_lib.helpers import get_media_file

import gettext
from gettext import gettext as _
gettext.textdomain('jenkins-ycny')

BUILDING_ABORTED = ['nobuilt.png', 'clock.png']
BUILDING_SUCCESS = ['blue.png', 'clock.png']
BUILDING_FAILURE = ['red.png', 'clock.png']

ABORTED = ['nobuilt.png']
SUCCESS = ['blue.png']
FAILURE = ['red.png']
JENKINS = ["jenkins.ico"]

class Indicator:
    def __init__(self, window):
        self.window = window

        self.indicator = AppIndicator3.Indicator.new('projectname', '', AppIndicator3.IndicatorCategory.APPLICATION_STATUS)
        self.indicator.set_status(AppIndicator3.IndicatorStatus.ACTIVE)

        self.icon_seqs = JENKINS
        #Uncomment and choose an icon for attention state. 
        #self.indicator.set_attention_icon("ICON-NAME")
        
        self.menu = Gtk.Menu()

        # Add items to Menu and connect signals.
        
        #Adding preferences button 
        #window represents the main Window object of your app
        self.preferences = Gtk.MenuItem("Preferences")
        self.preferences.connect("activate",window.on_mnu_preferences_activate)
        self.preferences.show()
        self.menu.append(self.preferences)

        # Show
        self.show = Gtk.MenuItem("Show")
        self.show.connect("activate",window.on_mnu_show_activate)
        self.show.show()
        self.menu.append(self.show)

        self.quit = Gtk.MenuItem("Quit")
        self.quit.connect("activate",window.on_mnu_close_activate)
        self.quit.show()
        self.menu.append(self.quit)

        # Add more items here                           

        self.menu.show()
        self.indicator.set_menu(self.menu)
        self.animate_frame = 0

        self.start()

    def start(self):
        self.animate_icon()
        GLib.timeout_add_seconds(1, self.animate_icon)

    def animate_icon(self):
        if self.animate_frame >= len(self.icon_seqs): self.animate_frame = 0

        icon_uri = get_media_file(self.icon_seqs[self.animate_frame])
        icon_path = icon_uri.replace("file:///", '')
        self.indicator.set_icon(icon_path)

        self.animate_frame += 1

        return True

    def update_display(self, latest_result, completed_result):
        if latest_result == 'BUILDING':
            if completed_result == 'SUCCESS':
                self.icon_seqs = BUILDING_SUCCESS
            elif completed_result == 'ABORTED':
                self.icon_seqs = BUILDING_ABORTED
            else:
                self.icon_seqs = BUILDING_FAILURE
        else:
            if latest_result == 'SUCCESS':
                self.icon_seqs = SUCCESS
            elif latest_result == 'ABORTED':
                self.icon_seqs = ABORTED
            else:
                self.icon_seqs = FAILURE

    def update_menu(self):
        pass
    
def new_application_indicator(window):
    return Indicator(window)    
