# -*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-
### BEGIN LICENSE
# This file is in the public domain
### END LICENSE

from locale import gettext as _

from gi.repository import Gtk # pylint: disable=E0611
import logging
logger = logging.getLogger('jenkins')

from jenkins_lib import Window
from jenkins_ycny.AboutJenkinsDialog import AboutJenkinsDialog
from jenkins_ycny.PreferencesJenkinsDialog import PreferencesJenkinsDialog
from jenkins_ycny.scheduler import JenkinsScheduler


# See jenkins_lib.Window.py for more details about how this class works
class JenkinsWindow(Window):
    __gtype_name__ = "JenkinsWindow"
    
    def finish_initializing(self, builder): # pylint: disable=E1002
        """Set up the main window"""
        super(JenkinsWindow, self).finish_initializing(builder)

        self.AboutDialog = AboutJenkinsDialog
        self.PreferencesDialog = PreferencesJenkinsDialog

        # Code for other initialization actions should be added here.
		self.scheduler = JenkinsScheduler(self)

		self.scheduler.register_display(self)
		self.scheduler.register_display(self.indicator)

		self.scheduler.start()

		self.connect('delete-event', self.hide_window)

	def on_mnu_show_activate(self, widget):
		self.show()

	def hide_window(self, widget, event):
    	self.hide()
    	return True
  
	def update_display(self, latest_result, completed_result):
		pass
