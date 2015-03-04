from build import BaseBuild
import os
import re
import platform

class NasmBuilding(BaseBuild):

	def __init__(self):
		if platform.system() == 'Windows':
			BaseBuild.__init__(self, 'NASM_win32')

	def do_build_win32(self):
		if not self.check_srouce():
			if not self.check_pack():
				self.download_source()
			self.unpack_source()
		os.system('cd ./Build && build_nasm.bat %s %s' % (self.source_name(), '..\\' + self.install_dist()))
	

	@staticmethod
	def do_build():
		nasm_building = NasmBuilding()
		if platform.system() == 'Windows':
			nasm_building.do_build_win32()
