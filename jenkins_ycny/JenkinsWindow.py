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


from git import Repo
class GitSuspect(object):
    def __init__(self, window):
        self.window = window

    def parse_settings(self):
        self.proj_dir = self.window.settings.get_string('project-dir')
        self.repo = Repo(self.proj_dir)

    def current_user(self):
        user_email = self.repo.config_reader().get_value('user', 'email')
        user_name = self.repo.config_reader().get_value('user', 'name')        
        return (user_email, user_name)

# See jenkins_lib.Window.py for more details about how this class works
class JenkinsWindow(Window):
    __gtype_name__ = "JenkinsWindow"
    
    def finish_initializing(self, builder): # pylint: disable=E1002
        """Set up the main window"""
        super(JenkinsWindow, self).finish_initializing(builder)

        self.job_states = dict()

        self.AboutDialog = AboutJenkinsDialog
        self.PreferencesDialog = PreferencesJenkinsDialog

        # Init Git
        self.suspect = GitSuspect(self)
        self.suspect.parse_settings()

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
  
  	def culprits_failed_job(self, job):
  		st = job.lastBuild.result

  		if self.job_states.get(job.name) != st:
			self.job_states[job.name] = st
			if st not in ('BUILDING', 'SUCCESS'):
				return job.lastBuild.culprits

		return []

	def update_display(self, obj):
		culprits = []

		culprits += self.culprits_failed_job( obj.m_job )

		for name in obj.s_jobs:
			culprits += self.culprits_failed_job( obj.s_jobs[name] )

		print self.job_states
		print culprits
		print self.suspect.current_user()

	def on_preferences_changed(self, settings, key, data=None):
		Window.on_preferences_changed(self, settings, key, data)
