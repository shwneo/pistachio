#!/usr/bin/python
from build import BaseBuild
import os
import re
import platform

class PerlBuilding(BaseBuild):

	def __init__(self):
		BaseBuild.__init__(self, 'perl')

	def fix_make_file(self, compiler):
		# Only for Win32!
		mk_file_name = './build/%s/win32/Makefile' % self.source_name()
		if (os.path.isfile(mk_file_name)):
			with open(mk_file_name, 'r+') as mk_file:
				mk_lines = mk_file.readlines()
				line_num = 0
				CCTYPE_PATTERN = re.compile(r'^CCTYPE\s+=\s+MSVC60')
				CCTYPE_EXPECTED = re.compile(r'^#CCTYPE\s+=\s+%s' % compiler)
				for line in mk_lines:
					if line.startswith('INST_TOP'):
						line = 'INST_TOP\t= ' + self.pwd + '\\' + self.install_dist() + '\\\n'
						mk_lines[line_num] = line
						print('New INST_TOP:\n' + line)
						line_num = line_num + 1
						continue
					if CCTYPE_EXPECTED.match(line):
						mk_lines[line_num] = line[1:]
						line_num = line_num + 1
						continue
					if CCTYPE_PATTERN.match(line):
						mk_lines[line_num] = "#%s" % line
						line_num = line_num + 1
						continue
					line_num = line_num + 1
					
			with open(mk_file_name, 'w+') as mk_file:
				mk_file.writelines(mk_lines)
		else:
			print('No valid Makefile found, please clean the build');
			exit(1)

	def do_build_win32(self):
		self.fix_make_file('MSVC90FREE')
		os.system("cd ./build && build_perl.bat %s" % self.source_name())

	@staticmethod
	def do_build():
		perl_building = PerlBuilding()
		if not perl_building.check_srouce():
			if not perl_building.check_pack():
				perl_building.download_source()
			perl_building.unpack_source()
		if platform.system() == 'Windows':
			perl_building.do_build_win32()
		else:
			pass
