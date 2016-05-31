# -*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-
# ## BEGIN LICENSE
# This file is in the public domain
# ## END LICENSE

# This is your preferences dialog.
#
# Define your preferences in
# data/glib-2.0/schemas/net.launchpad.jenkins.gschema.xml
# See http://developer.gnome.org/gio/stable/GSettings.html for more info.

from gi.repository import Gio  # pylint: disable=E0611
# from locale import gettext as _
from jenkins_lib.PreferencesDialog import PreferencesDialog

import logging
logger = logging.getLogger('jenkins')


class PreferencesJenkinsDialog(PreferencesDialog):
    __gtype_name__ = "PreferencesJenkinsDialog"

    def finish_initializing(self, builder):  # pylint: disable=E1002
        """Set up the preferences dialog"""
        super(PreferencesJenkinsDialog, self).finish_initializing(builder)

        # Bind each preference widget to gsettings
        settings = Gio.Settings("net.launchpad.jenkins-ycny")

        widget = self.builder.get_object('proj_dir_entry')
        settings.bind(
            "project-dir", widget, "text", Gio.SettingsBindFlags.DEFAULT)

        widget = self.builder.get_object('ci_url_entry')
        settings.bind(
            "ci-url", widget, "text", Gio.SettingsBindFlags.DEFAULT)

        widget = self.builder.get_object('m_job_entry')
        settings.bind(
            "master-job", widget, "text", Gio.SettingsBindFlags.DEFAULT)

        widget = self.builder.get_object('s_job_entry')
        settings.bind(
            "slave-jobs", widget, "text", Gio.SettingsBindFlags.DEFAULT)

        # Code for other initialization actions should be added here.
