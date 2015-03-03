#!/usr/bin/python
import os
import platform
import ConfigParser

class BaseBuild:

	def __init__(self, name=None):
		self.__conf =  ConfigParser.ConfigParser()
		self.__conf.read('./Scripts/3rd_party.conf')
		self.__name = name
		self.line_end = '\n'
		if platform.system() == 'Windows':
			self.line_end = '\r\n'
		self.pwd = os.getcwd()

	def install_dist(self):
		if self.__name is None:
			raise Exception("BaseBuild: Cannot determine the building target, give up")
		return self.__conf.get(self.__name, 'dist')

	def source_name(self):
		if self.__name is None:
			raise Exception("BaseBuild: Cannot determine the building target, give up")
		return self.__conf.get(self.__name, 'dir')

	def check_srouce(self):
		if self.__name is None:
			raise Exception("BaseBuild: Cannot determine the building target, give up")
		tools_files = os.listdir('./Build')
		for file in tools_files:
			if file == self.__conf.get(self.__name, 'dir'):
				return True
		return False

	def check_pack(self):
		if self.__name is None:
			raise Exception("BaseBuild: Cannot determine the building target, give up")
		tools_files = os.listdir('./Build')
		for file in tools_files:
			if file == self.__conf.get(self.__name, 'pack'):
				return True
		return False

	def download_source(self):
		if self.__name is None:
			raise Exception("BaseBuild: Cannot determine the building target, give up")
		os.system('cd ./build && python ../Tools/bin/pwget.py %s' % (self.__conf.get(self.__name, 'source')))

	def unpack_source(self):
		if self.__name is None:
			raise Exception("BaseBuild: Cannot determine the building target, give up")
		os.system('cd ./build && python ../Tools/bin/ptar.py %s %s' % (self.__conf.get(self.__name, 'unpack'),
																		self.__conf.get(self.__name, 'pack')))

