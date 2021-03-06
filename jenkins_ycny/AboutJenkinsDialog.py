# -*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-
# ## BEGIN LICENSE
# This file is in the public domain
# ## END LICENSE

from jenkins_lib.AboutDialog import AboutDialog

import logging
logger = logging.getLogger('jenkins')


# See jenkins_lib.AboutDialog.py for more details about how this class works.
class AboutJenkinsDialog(AboutDialog):
    __gtype_name__ = "AboutJenkinsDialog"

    def finish_initializing(self, builder):  # pylint: disable=E1002
        """Set up the about dialog"""
        super(AboutJenkinsDialog, self).finish_initializing(builder)

        # Code for other initialization actions should be added here.
