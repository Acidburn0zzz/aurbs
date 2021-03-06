#!/usr/bin/env python

import os
import re
from pkg_resources import parse_version

from aurbs.config import AurBSConfig
from aurbs.remotedb import RemoteDB
from aurbs.static import *

_re_strip_ver = re.compile(r"([^<>=]*)[<>]?=?")

def clean_dep_ver(deps):
	deps_out = []
	for dep in deps:
		deps_out.append(_re_strip_ver.match(dep).group(1))
	return deps_out


_remote_dbs = {}

def remote_pkgver(pkgname, arch):
	global _remote_dbs
	remote_db = _remote_dbs.get(arch, RemoteDB(chroot_root(arch)))
	if arch not in _remote_dbs:
		_remote_dbs[arch] = remote_db
	try:
		return remote_db.get_pkg(pkgname).version
	except AttributeError:
		raise KeyError("No provider found for remote pkg '%s'" % pkgname)


def version_newer(old, new):
	return parse_version(new) > parse_version(old)

def filter_dependencies(args, local=True, nofilter=False):
	deps = set()
	for arg in args:
		deps = deps.union(arg)
	if nofilter:
		return deps
	if local:
		return [d for d in deps if d in AurBSConfig().aurpkgs]
	else:
		return [d for d in deps if d not in AurBSConfig().aurpkgs]

def find_pkg_files(pkgname=None, directory=None):
	if not directory:
		return []
	respkgs = []
	for item in os.listdir(directory):
		if item.endswith('pkg.tar.xz'):
			[ipkgname, ipkgver, ipkgrel, iarch] = item.rsplit("-", 3)
			if pkgname is None or ipkgname == pkgname:
				respkgs.append(item)
	return respkgs

def by_name(dictlist, name):
	return filter(lambda i: i['name'] == name, dictlist).__next__()

def set_chmod(basedir, dirs, files):
	os.chmod(basedir, dirs)
	for r, ds, fs in os.walk(basedir):
		for d in ds:
			os.chmod(os.path.join(r, d), dirs)
		for f in fs:
			os.chmod(os.path.join(r, f), files)
