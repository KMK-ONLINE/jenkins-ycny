from gi.repository import GLib

from . api import *

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
        GLib.timeout_add_seconds(20, self.poll_jenkins)

    def poll_jenkins(self):
        m_job = Job(self.master_job, self.ci_url)
        s_jobs = []
        for slave_job in self.slave_jobs:
            s_job = Job(slave_job, self.ci_url)
            s_jobs.append(s_job)

        for display in self.displays:            
            if hasattr(display, 'update_display'):
                display.update_display( m_job.lastBuild.result, m_job.lastCompletedBuild.result)

        return True

    def register_display(self, display):
        self.displays.append(display)