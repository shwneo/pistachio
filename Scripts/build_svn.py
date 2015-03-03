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
			

	@staticmethod
	def do_build():
		svn_building = SvnBuilding()
		if platform.system() == 'Windows':
			svn_building.do_build_win32()
