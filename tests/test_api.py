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

