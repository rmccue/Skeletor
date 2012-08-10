import subprocess
import os
import os.path
import re
import urllib2
from zipfile import ZipFile


def _run(cmd, to_root=True):
	"""Run a command. Pretty standard."""
	# The following is broken in Cygwin :( Suggestions welcome.
	#top = None
	#if to_root:
	#	top = subprocess.check_output(['git', 'rev-parse', '--show-toplevel']).strip()
	#	os.chdir(top)
	p = subprocess.Popen(cmd)
	p.wait()


def _url_to_humanish(url):
	"""Convert a URL to what the probable human representation of it is.

	Based on git's processing for `git clone`"""
	name = url.rstrip('/')
	name = re.sub(':*/*\.git$', '', name)
	name = re.sub('.*[/:]', '', name)
	return name


def download_and_extract(url, name, to):
	"""Download a zip and extract it to a given location.

	Assumes the zip has a common prefix directory for all the files."""
	ziplocation = os.path.join(os.path.dirname(to), name + '.zip')

	print "Downloading: {0}".format(url)
	f = open(ziplocation, 'w+b')
	u = urllib2.urlopen(url)

	file_size = int(u.info().getheaders("Content-Length")[0])
	print "Bytes: {0}".format(file_size)

	# Stream to file
	file_size_dl = 0
	block_sz = 8192
	while True:
		buffer = u.read(block_sz)
		if not buffer:
			break

		file_size_dl += len(buffer)
		f.write(buffer)
		status = r"%10d  [%3.2f%%]" % (file_size_dl, file_size_dl * 100. / file_size)
		status = status + chr(8) * (len(status) + 1)
		#print status,

	pluginzip = ZipFile(f)
	pluginzip.extractall(os.path.dirname(to))

	# Move the directory if needed
	prefix = os.path.commonprefix(pluginzip.namelist()).rpartition('/')[0]
	if prefix != os.path.basename(to):
		print to
		os.rename(
			os.path.join(os.path.dirname(to), prefix),
			to
		)

	# Cleanup
	pluginzip.close()
	f.close()
	os.remove(ziplocation)


def initialize(args):
	"""Create a new Skeleton repository"""
	cmd = ['git', 'clone', '--recursive', '-o', 'upstream',
		args.repo, args.directory]
	_run(cmd, to_root=False)

	shared = os.path.join(args.directory, 'shared')
	if not os.path.exists(shared):
		os.makedirs(shared)


def update(args):
	"""Update a site to the latest Skeleton version"""
	_run(['git', 'pull', 'upstream'])
	_run(['git', 'submodule', 'update', '--init', '--recursive'])


def plugins_add(args):
	"""Add a new plugin to your repository"""
	if args.mustuse:
		plugindir = 'mu-plugins'
	else:
		plugindir = 'plugins'

	if re.match('^[a-zA-Z0-9_\-]+$', args.repo):
		# We've got a WP.org plugin slug
		if args.directory == '':
			args.directory = args.repo
		zipname = args.repo
		if args.version:
			zipname += '.{0}'.format(args.version)
		url = 'http://downloads.wordpress.org/plugin/{0}.zip'.format(zipname)
		download_and_extract(url, args.repo, os.path.join('content', plugindir, args.directory))

		# Use '/'.join() as Git always uses forward slashes
		_run(['git', 'add', '/'.join(['content', plugindir, args.directory])])

	else:
		# We've got a Git path
		if args.directory == '':
			args.directory = _url_to_humanish(args.repo)

		_run(['git', 'submodule', 'add', args.repo,
			os.path.join('content', plugindir, args.directory)])

	_run(['git', 'commit', '-e', '-m',
		'Added {0} to {1}'.format(args.directory, plugindir)])


def themes_add(args):
	"""Add a new theme to your repository"""
	if re.match('^[a-zA-Z0-9_\-]+$', args.repo):
		# We've got a WP.org plugin slug
		if args.directory == '':
			args.directory = args.repo

		url = 'http://wordpress.org/extend/themes/download/{0}.{1}.zip'.format(args.repo, args.version)
		download_and_extract(url, args.repo, os.path.join('content', 'themes', args.directory))

		# Use '/'.join() as Git always uses forward slashes
		_run(['git', 'add', '/'.join(['content', 'themes', args.directory])])
	else:
		if args.directory == '':
			args.directory = _url_to_humanish(args.repo)

		_run(['git', 'submodule', 'add', args.repo,
			os.path.join('content', 'themes', args.directory)])

	_run(['git', 'commit', '-e', '-m',
		'Added {0} theme'.format(args.directory)])
