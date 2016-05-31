# -*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-
# ## BEGIN LICENSE
# This file is in the public domain
# ## END LICENSE

# from locale import gettext as _

from gi.repository import Gtk  # pylint: disable=E0611
from gi.repository import GLib
from gi.repository import Gdk

from jenkins_lib import Window
from jenkins_ycny.AboutJenkinsDialog import AboutJenkinsDialog
from jenkins_ycny.PreferencesJenkinsDialog import PreferencesJenkinsDialog
from jenkins_ycny.scheduler import JenkinsScheduler
from jenkins_lib.helpers import get_media_file

from git import Repo
import logging

logger = logging.getLogger('jenkins')


def extract_pair_users(user_id):
    if user_id.startswith('pair+'):
        users = user_id.split('+')[1:]
    else:
        users = [user_id]
    return users


class GitSuspect(object):
    def __init__(self, window):
        self.window = window

    def parse_settings(self):
        self.proj_dir = self.window.settings.get_string('project-dir')
        self.repo = None
        try:
            self.repo = Repo(self.proj_dir)
            logger.debug(self.repo)
        except Exception as e:
            logger.exception(e)

    def current_user(self):
        if not self.repo:
            return (None, None)

        user_email = self.repo.config_reader().get_value('user', 'email')
        user_name = self.repo.config_reader().get_value('user', 'name')
        user_id = user_email.split('@', 1)[0]
        return (user_id, user_email, user_name)


class SplashScreen(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Your Country Needs You")

        icon_uri = get_media_file('jenkins.ico')
        icon_path = icon_uri.replace("file:///", '')
        self.set_icon_from_file(icon_path)

        icon_uri = get_media_file('YourCountryNeedsYou.jpg')
        icon_path = icon_uri.replace("file:///", '')

        img = Gtk.Image()
        img.set_from_file(icon_path)

        self.add(img)

        self.modify_bg(Gtk.StateType.NORMAL, Gdk.color_parse('#E6DCAD'))

    def show(self):
        self.resize(1024, 768)
        self.set_position(Gtk.WindowPosition.CENTER)
        self.show_all()
        self.present()
        self.grab_focus()

        # GLib.timeout_add_seconds(5, self.close_splash)

    def close_splash(self):
        self.destroy()
        return False


def your_country_needs_you():
    sp = SplashScreen()
    sp.show()
    return sp


# See jenkins_lib.Window.py for more details about how this class works
class JenkinsWindow(Window):
    __gtype_name__ = "JenkinsWindow"

    def finish_initializing(self, builder):  # pylint: disable=E1002
        """Set up the main window"""
        super(JenkinsWindow, self).finish_initializing(builder)

        self.job_states = dict()

        self.AboutDialog = AboutJenkinsDialog
        self.PreferencesDialog = PreferencesJenkinsDialog

        # Init Git
        self.suspect = GitSuspect(self)

        # Code for other initialization actions should be added here.
        self.scheduler = JenkinsScheduler(self)

        self.scheduler.register_display(self)
        self.scheduler.register_display(self.indicator)

        self.connect('delete-event', self.hide_window)

        self.settings_dirty = True
        self.apply_settings()

    def on_mnu_splash_activate(self, widget, data=None):
        your_country_needs_you()

    def on_mnu_show_activate(self, widget):
        self.show()

    def hide_window(self, widget, event):
        self.hide()
        return True

    def culprits_failed_job(self, job):

        try:
            st = job.lastBuild.result

            if self.job_states.get(job.name) != st:
                self.job_states[job.name] = st
                if st not in ('BUILDING', 'SUCCESS', 'ERROR'):
                    return job.lastBuild.culprits
        except Exception as e:
            logger.exception(e)

        return []

    def update_display(self, obj):
        culprits = []

        culprits += self.culprits_failed_job(obj.m_job)

        for name in obj.s_jobs:
            culprits += self.culprits_failed_job(obj.s_jobs[name])

        users = []
        for culprit in culprits:
            users += extract_pair_users(culprit)

        ours = extract_pair_users(self.suspect.current_user()[0])

        logger.debug(self.job_states)
        logger.debug(users)
        logger.debug(ours)
        logger.debug(self.suspect.current_user())

        if set(ours) & set(users):
            your_country_needs_you()

    def on_preferences_dialog_destroyed(self, widget, data=None):
        self.apply_settings()
        Window.on_preferences_dialog_destroyed(self, widget, data)

    def on_preferences_changed(self, settings, key, data=None):
        self.settings_dirty = True
        Window.on_preferences_changed(self, settings, key, data)

    def apply_settings(self):
        if self.settings_dirty:
            self.suspect.parse_settings()
            self.indicator.parse_settings()
            self.scheduler.parse_settings()
            self.scheduler.start()
            self.settings_dirty = False
