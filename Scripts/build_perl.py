#!/usr/bin/python
import os
import platform
import ConfigParser

class PerlBuilding:

	def __init__(self):
		self.__conf =  ConfigParser.ConfigParser()
		self.__conf.read('3rd_party.conf')
		self.__line_end = '\n'
		self.__pwd = os.getcwd()


	def check_perl_srouce(self):
		tools_files = os.listdir('../build')
		for file in tools_files:
			print(file)
			if file == self.__conf.get('perl', 'dir'):
				return True
		return False

	def check_perl_pack(self):
		tools_files = os.listdir('../build')
		for file in tools_files:
			if file == self.__conf.get('perl', 'pack'):
				return True
		return False

	def download_source(self):
		os.system('cd ../build && python ../Tools/bin/pwget.py %s' % (self.__conf.get('perl', 'source')))

	def unpack_source(self):
		os.system('cd ../build && python ../Tools/bin/ptar.py %s %s' % (self.__conf.get('perl', 'unpack'),
																		self.__conf.get('perl', 'pack')))

	def fix_make_file(self):
		mk_file_name = '../build/%s/win32/Makefile' % self.__conf.get('perl', 'dir')
		if (os.path.isfile(mk_file_name)):
			with open(mk_file_name, 'r+') as mk_file:
				mk_lines = mk_file.readlines()
				line_num = 0
				for line in mk_lines:
					if line.startswith('INST_TOP'):
						print(line)
						mk_lines[line_num] = 'INST_TOP\t= ' + self.__pwd + os.sep + self.__conf.get('perl', 'dist') + os.sep
					line_num = line_num + 1
					
			with open(mk_file_name, 'w+') as mk_file:
				mk_file.writelines(mk_lines)
		else:
			print('No valid Makefile found, please clean the build');
			exit(1)


def main():
	perl_building = PerlBuilding()
	if not perl_building.check_perl_srouce():
		if not perl_building.check_perl_pack():
			perl_building.download_source()
		perl_building.unpack_source()

	perl_building.fix_make_file()

if __name__ == '__main__':
	exit(main())
