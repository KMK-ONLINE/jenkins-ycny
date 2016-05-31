# -*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-
# ## BEGIN LICENSE
# This file is in the public domain
# ## END LICENSE

import optparse

import gi
gi.require_version("Gtk", "3.0")
gi.require_version("Gdk", "3.0")
gi.require_version("GLib", "2.0")
gi.require_version("Gio", "2.0")
gi.require_version('Notify', "0.7")

from locale import gettext as _
from gi.repository import Gtk  # pylint: disable=E0611
from jenkins_ycny import JenkinsWindow
from jenkins_lib import set_up_logging, get_version


def parse_options():
    """Support for command line options"""
    parser = optparse.OptionParser(version="%%prog %s" % get_version())
    parser.add_option(
        "-v", "--verbose", action="count", dest="verbose",
        help=_("Show debug messages (-vv debugs jenkins_lib also)"))
    (options, args) = parser.parse_args()

    set_up_logging(options)


def main():
    'constructor for your class instances'
    parse_options()

    # Run the application.    
    window = JenkinsWindow.JenkinsWindow()
    window.hide()
    Gtk.main()
