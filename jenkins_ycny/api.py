#!/usr/bin/env python2
import requests
import json
from datetime import datetime, timedelta


class JsonAble(object):
	def __init__(self, url):
		self._url = url
		self._data = None
		self._lastBuild = None

	@property
	def data(self):
		if self._data is None:
			url = self._url + '/api/json'
			# print url
			r = requests.get(url)
			if r.status_code == 200:
				self._data = json.loads(r.content)
			else:
				print url, r
		return self._data

	@property
	def url(self):
		return self._url
	

class Job(JsonAble):

	def __init__(self, name, ci_url):
		self._name = name
		
		url = ci_url + '/job/' + name
		JsonAble.__init__(self, url)

		self._builds = None

	@property
	def name(self):
		return self._name
	
	@property
	def color(self):
		return self.data['color']

	def build(self, number):
		if self._builds is None:
			self._builds = dict()
			for b in self.data['builds']:
				self._builds[b['number']] = None	

		if number not in self._builds: return

		b = self._builds[number]
		if not b:
			b = Build(self, number)
			self._builds[number] = b
		return b

	@property
	def lastBuild(self):
		return self.build( self.data['lastBuild']['number'] )

	@property
	def lastStableBuild(self):
		return self.build( self.data['lastStableBuild']['number'] )

	@property
	def lastCompletedBuild(self):
		return self.build( self.data['lastCompletedBuild']['number'] )

	@property
	def lastFailedBuild(self):
		return self.build( self.data['lastFailedBuild']['number'] )

	def __repr__(self):
		return "Job(%s)" % (self._name, )
	

class Build(JsonAble):

	def __init__(self, job, number):
		self._job = job
		self._number = number

		url = job.url + '/' + str(number)
		JsonAble.__init__(self, url)

		self._changes = None
		self._report = None

	@property
	def result(self):
		if self.data['building']:
			return 'BUILDING'
		return self.data['result']

	@property
	def timestamp(self):
		return datetime.fromtimestamp(self.data['timestamp'] / 1000.0)

	@property
	def duration(self):
		return timedelta(seconds=self.data['duration'] / 1000.0)

	@property
	def changes(self):
		if self._changes is None:
			self._changes = []
			for i in self.data['changeSet']['items']:
				self._changes.append( Change(self, i) )

		return self._changes

	@property
	def culprits(self):
		return [a['fullName'] for a in self.data['culprits']]

	@property
	def report(self):
		if self._report is None:
			self._report = Report(self)
		return self._report
	
	def __repr__(self):
		return "Build(%d) of Job(%s)" % (self._number, self._job.name)


class Change(object):
	def __init__(self, build, change_dict):
		self._data = change_dict
		self._paths = None
		self._build = build

	@property
	def data(self):
		return self._data

	@property
	def message(self):
		return self.data['msg']

	@property		
	def commit(self):
		return self.data['commitId']

	@property
	def timestamp(self):
		return datetime.fromtimestamp(self.data['timestamp'] / 1000.0)

	@property
	def paths(self):		
		return self.data['affectedPaths']

	@property
	def author(self):
		return self.data['author']['fullName']

	def __repr__(self):
		return "Change %s %s by %s with message:\n%s, affected:\n- " % (self.timestamp,
			self.commit, self.author, self.message) + ",\n- ".join(self.paths)


class Report(JsonAble):
	def __init__(self, build):
		self._build = build
		
		url = build.url + '/testReport'
		JsonAble.__init__(self, url)

		self._suites = None
		self._fails = None

	@property
	def suites(self):
		if self._suites is None:
			self._suites = []
			for s in self.data['suites']:
				self._suites.append( Suite(self, s) )

		return self._suites

	@property
	def duration(self):
		return timedelta(seconds=self.data['duration'])

	@property
	def isEmpty(self):
		return self.data['empty']

	@property
	def failCount(self):
		return self.data['failCount']

	@property
	def passCount(self):
		return self.data['passCount']

	@property
	def skipCount(self):
		return self.data['skipCount']

	@property
	def fails(self):
		if self._fails is None:
			self._fails = []
			for s in self.suites:
				for c in s.cases:
					if c.status != 'PASSED':
						self._fails.append(c)

		return self._fails
	
	
	def __repr__(self):
		return "Report for " + repr(self._build) + " with %d fails, %d skips, %d passes for " % (self.failCount,
			self.skipCount, self.passCount) + str(self.duration)


class Suite(object):
	def __init__(self, report, suite_dict):
		self._data = suite_dict
		self._cases = None
		self._report = report

	@property
	def data(self):
		return self._data

	@property
	def cases(self):
		if self._cases is None:
			self._cases = []
			for c in self.data['cases']:
				self._cases.append( Case(self, c) )
		return self._cases

	@property
	def name(self):
		return self.data['name']

	@property
	def duration(self):
		return timedelta(seconds=self.data['duration'])

	def __repr__(self):
		return "Suite %s for " % (self.name, ) + str(self.duration)


class Case(object):
	def __init__(self, suite, case_dict):
		self._data = case_dict
		self._suite = suite

	@property
	def data(self):
		return self._data

	@property
	def className(self):
		return self.data['className']

	@property
	def name(self):
		return self.data['name']

	@property
	def duration(self):
		return timedelta(seconds=self.data['duration'])

	@property
	def status(self):
		return self.data['status']

	@property
	def isSkipped(self):
		return self.data['skipped']

	@property
	def errorStackTrace(self):
		return self.data['errorStackTrace']
	
	def __repr__(self):
		return "Suite %s | Case %s | %s with status %s" % (self._suite.name, self.className, self.name, self.status)


if __name__ == '__main__':
	from pprint import pprint
	from colorama import Fore, Back, Style

	def print_build(build, info, style=Style.NORMAL):
		color = ''

		if build.result == 'SUCCESS':
			color = Fore.GREEN + style
		elif build.result == 'FAILURE':
			color = Fore.RED + style
		elif build.result == 'BUILDING':
			color = Fore.YELLOW + style

		color_default = Fore.RESET + Style.NORMAL
		
		print color + info, build, build.timestamp, build.duration, build.result + color_default


	for job in jobs:
		print '**********'
		print job

		latest = job.lastBuild

		print_build(latest, 'Last Build:', style=Style.BRIGHT)	

		completed = job.lastCompletedBuild

		build = latest
		if latest.result == 'BUILDING':
			build = completed
			print_build(build, 'Last Completed:')

		if build.result == 'SUCCESS':
			if len(build.report.fails):
				print "\nFlaky:"
				pprint( build.report.fails )

		else:
			if build.report.isEmpty:
				print "NO REPORT !"

			print "\nCulprit:"
			pprint( build.culprits )

			print "\nFail:"
			pprint( build.report.fails )

			print "\nChange:"
			pprint( build.changes )

			good = job.lastStableBuild
			print "\nLast Stable:", good, good.timestamp, good.duration, good.result

		print "\n"
