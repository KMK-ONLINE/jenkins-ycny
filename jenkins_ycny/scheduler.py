from gi.repository import GLib

from . api import *

import logging
logger = logging.getLogger('jenkins')

class UpdateObject(object):
    def __init__(self):
        self.m_job = None
        self.s_jobs = dict()

        self.m_result = None
        self.s_results = dict()

    def check_result(self, job):        
        try:
            return (job.lastBuild.result, job.lastCompletedBuild.result)
        except Exception as e:
            logger.exception(e)
            return ('ERROR', 'ERROR')

    def update_results(self):
        self.m_result = self.check_result( self.m_job )

        for slave_job in self.s_jobs:
            s_job = self.s_jobs[slave_job]

            self.s_results[slave_job] = self.check_result( s_job )

class JenkinsScheduler(object):
    def __init__(self, window):
        self.window = window        
        self.parse_settings()
        self.displays = []

    def parse_settings(self):
        self.ci_url = self.window.settings.get_string('ci-url')
        self.master_job = self.window.settings.get_string('master-job')
        self.slave_jobs = [x.strip() for x in self.window.settings.get_string('slave-jobs').split(',')]

    def start(self):
        self.poll_jenkins()
        GLib.timeout_add_seconds(10, self.poll_jenkins)

    def poll_jenkins(self):        
        m_job = Job(self.master_job, self.ci_url)
        s_jobs = dict()
        for slave_job in self.slave_jobs:
            s_job = Job(slave_job, self.ci_url)
            s_jobs[slave_job] = s_job

        obj = UpdateObject()
        obj.m_job = m_job
        obj.s_jobs = s_jobs

        obj.update_results()

        for display in self.displays:
            if hasattr(display, 'update_display'):
                display.update_display( obj )

        return True

    def register_display(self, display):
        self.displays.append(display)