#!/usr/bin/python
from build import BaseBuild
import os
import re
import platform

class PythonBuilding(BaseBuild):
	def __init__(self):
		BaseBuild.__init__(self, 'python')

	@staticmethod
	def do_build():
		python_building = PythonBuilding()
		if not python_building.check_srouce():
			if not python_building.check_pack():
				python_building.download_source()
			python_building.unpack_source()
		SOURCE_PATH = '.' + os.sep + 'Build' + os.sep + python_building.source_name()
		if platform.system() == 'Windows':
			os.system('cd ' + SOURCE_PATH + ' && Tools\\buildbot\\external.bat')
		
