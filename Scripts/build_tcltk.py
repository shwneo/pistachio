#!/usr/bin/python
from build import BaseBuild
import os
import re
import platform

class TclBuilding(BaseBuild):
	def __init__(self):
		BaseBuild.__init__(self, 'tcl')

	def do_build_win32(self, install_path):
		os.system("cd ./Build && build_tcl.bat %s %s" % (self.source_name(), install_path))

	def do_build(self, install_path):
		if not self.check_srouce():
			if not self.check_pack():
				self.download_source()
			self.unpack_source()
		if platform.system() == 'Windows':
			self.do_build_win32(install_path)

class TkBuilding(BaseBuild):
	def __init__(self):
		BaseBuild.__init__(self, 'tk')

	def do_build_win32(self, tcl_path, install_path):
		os.system("cd ./Build && build_tk.bat %s %s %s" % (self.source_name(), tcl_path, install_path))

	def do_build(self, tcl_path, install_path):
		if not self.check_srouce():
			if not self.check_pack():
				self.download_source()
			self.unpack_source()
		if platform.system() == 'Windows':
			self.do_build_win32(tcl_path, install_path)

class TclTkBuilding():

	@staticmethod
	def do_build(install_path):
		tcl_build = TclBuilding()
		tcl_build.do_build(install_path)
		tk_build = TkBuilding()
		tk_build.do_build('..' + os.sep + '..' + os.sep + tcl_build.source_name(), install_path)
