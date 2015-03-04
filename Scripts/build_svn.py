#!/usr/bin/python
from build import BaseBuild
import os
import re
import platform

class SvnBuilding(BaseBuild):

	def __init__(self):
		if platform.system() == 'Windows':
			BaseBuild.__init__(self, 'svn_win32')

	def do_build_win32(self):
		if not self.check_srouce():
			if not self.check_pack():
				self.download_source()
			self.unpack_source()
		os.system('cd ./Build && build_svn.bat %s %s' % (self.source_name(), '..\\' + self.install_dist()))
	

	@staticmethod
	def do_build():
		svn_building = SvnBuilding()
		if platform.system() == 'Windows':
			svn_building.do_build_win32()
