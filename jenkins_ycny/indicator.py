# -*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-
### BEGIN LICENSE
# This file is in the public domain
### END LICENSE

"""Code to add AppIndicator."""

from gi.repository import Gtk # pylint: disable=E0611
from gi.repository import GLib
from gi.repository import AppIndicator3 # pylint: disable=E0611
from gi.repository import Notify

from jenkins_lib.helpers import get_media_file

import gettext
from gettext import gettext as _
gettext.textdomain('jenkins-ycny')

BUILDING_ABORTED = ['clock.png', 'nobuilt.png']
BUILDING_SUCCESS = ['clock.png', 'blue.png']
BUILDING_FAILURE = ['clock.png', 'red.png']

ABORTED = ['nobuilt.png']
SUCCESS = ['blue.png']
FAILURE = ['red.png']

JENKINS = ["jenkins.ico"]
ERROR = ['warning.png']

APPINDICATOR_ID = 'jenkins_ycny'

class Status(object):
    def __init__(self, name):
        self.name = name
        self._state = None
        self._last_state = None
        self._menu_item = None

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, new_state):
        self._last_state = self._state
        self._state = new_state

        if self._last_state != self._state:
            self.on_changes()

    def on_changes(self):
        message = None
        if self._state == 'ERROR':
            message = 'Error!'
            self.set_image( ERROR[0] )            
        elif self._state == 'BUILDING':
            self.set_image( BUILDING_FAILURE[0] )            
        elif self._state == 'SUCCESS':
            self.set_image( SUCCESS[0] )
        elif self._state == 'ABORTED':
            message = 'Build Aborted'
            self.set_image( ABORTED[0] )
        else:
            message = 'Build Failure'
            self.set_image( FAILURE[0] )

        if message:
            Notify.Notification.new("<b>Jenkins</b>", self.name + ' ' + message, None).show()

    @property
    def menu_item(self):
        if self._menu_item: return self._menu_item

        self._menu_item = Gtk.ImageMenuItem(self.name)

        mnu_job = self._menu_item

        self.set_image( JENKINS[0] )
        
        mnu_job.show()

        return self._menu_item

    def set_image(self, filename):
        if not self._menu_item: return

        icon_uri = get_media_file(filename)
        icon_path = icon_uri.replace("file:///", '')
        
        img = Gtk.Image()
        img.set_from_file(icon_path)

        mnu_job = self.menu_item
        mnu_job.set_image(img)
        mnu_job.set_always_show_image(True)

        return img 


class Indicator(object):
    def __init__(self, window):
        self.window = window

        Notify.init(APPINDICATOR_ID)

        self.indicator = AppIndicator3.Indicator.new(APPINDICATOR_ID, '', AppIndicator3.IndicatorCategory.APPLICATION_STATUS)
        self.indicator.set_status(AppIndicator3.IndicatorStatus.ACTIVE)

        self.icon_seqs = JENKINS
        #Uncomment and choose an icon for attention state. 
        #self.indicator.set_attention_icon("ICON-NAME")
        
        self.init_menus()
        self.last_state = None

        self.master_job = None
        self.slave_jobs = dict()
        self.parse_settings()

        self.animate_frame = 0

        self.start()

    def shutdown(self):
        Notify.uninit()

    def init_menus(self):
        window = self.window

        self.menu = Gtk.Menu()

        # Separator
        mnu_separator = Gtk.SeparatorMenuItem()
        mnu_separator.show()
        self.menu.append(mnu_separator)

        #Adding preferences button 
        #window represents the main Window object of your app
        mnu_preferences = Gtk.MenuItem("Preferences")
        mnu_preferences.connect("activate",window.on_mnu_preferences_activate)
        mnu_preferences.show()
        self.menu.append(mnu_preferences)

        # Show
        mnu_show = Gtk.MenuItem("Show")
        mnu_show.connect("activate",window.on_mnu_show_activate)
        mnu_show.show()
        self.menu.append(mnu_show)

        mnu_separator = Gtk.SeparatorMenuItem()
        mnu_separator.show()
        self.menu.append(mnu_separator)

        mnu_quit = Gtk.MenuItem("Quit")
        mnu_quit.connect("activate",window.on_mnu_close_activate)
        mnu_quit.show()
        self.menu.append(mnu_quit)

        # Add more items here                           

        self.menu.show()
        self.indicator.set_menu(self.menu)

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

    def update_display(self, obj):        
        self.update_master_icon( *obj.m_result )

        self.master_job.state = obj.m_result[0]

        for name in obj.s_results:            
            self.slave_jobs[name].state = obj.s_results[name][0]

    def update_master_icon(self, latest_result, completed_result):
        current_state = (latest_result, completed_result)
        if current_state == self.last_state: return

        message = None
        if latest_result == 'ERROR':
            self.icon_seqs = ERROR
            message = 'Error!'
        elif latest_result == 'BUILDING':
            message = 'Building...'
            if completed_result == 'SUCCESS':
                self.icon_seqs = BUILDING_SUCCESS
            elif completed_result == 'ABORTED':
                self.icon_seqs = BUILDING_ABORTED
            else:
                self.icon_seqs = BUILDING_FAILURE
        else:
            if latest_result == 'SUCCESS':
                message = 'Build Success'
                self.icon_seqs = SUCCESS
            elif latest_result == 'ABORTED':
                message = 'Build Aborted'
                self.icon_seqs = ABORTED
            else:
                message = 'Build Failure'
                self.icon_seqs = FAILURE

        if message:
            Notify.Notification.new("<b>Jenkins</b>", message, None).show()

        self.last_state = current_state
    
    def parse_settings(self):
        for mnu in self.menu.get_children():
            if type(mnu) == Gtk.SeparatorMenuItem: break
            self.menu.remove( mnu )

        status_m_job = Status(self.window.settings.get_string('master-job'))
        
        self.master_job = status_m_job
        self.menu.insert(status_m_job.menu_item, 0)

        for name in self.window.settings.get_string('slave-jobs').split(','):
            name = name.strip()

            status_s_job = Status(name)
            
            self.slave_jobs[name] = status_s_job

            self.menu.insert(status_s_job.menu_item, len(self.slave_jobs))

def new_application_indicator(window):
    return Indicator(window)    
