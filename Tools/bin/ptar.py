import tarfile
import os
import zipfile
from argparse import ArgumentParser
from zipfile import ZipFile

class TarWorker:
	def __init__(self):
		self.__directive = {'tar_action':None,
							'tar_filter':None,
							'tar_mode':None,
							'tar_from':None,
							'tar_to':None}
		self.__arg_parser = ArgumentParser()
		self.__arg_parser.add_argument('options', 
										nargs='?',
										default='')
		self.__arg_parser.add_argument('input_item',
										nargs='?',
										default=None)
		self.__arg_parser.add_argument('output_item',
										nargs='?',
										default='.')
		self.__arg_parser.add_argument('-x',
										'--extract',
										action='store_true',
										help='extract files from an archive')
		self.__arg_parser.add_argument('-c',
										'--create',
										action='store_true',
										help='create a new archive')
		self.__arg_parser.add_argument('-z',
										'--gzip',
										action='store_true',
										help='useing gzip filter')
		self.__arg_parser.add_argument('-j',
										'--bzip2',
										action='store_true',
										help='useing bzip2 filter')
		self.__arg_parser.add_argument('-v',
										'--verbose',
										action='store_true',
										help='verbose mode')
		self.__arg_parser.add_argument('-f',
										'--file',
										help='archive file')
		self.__args = self.__arg_parser.parse_args()
		self.__short_options = self.__args.options
		#self.__input = self.__args.input_item
		#self.__output = self.__args.output_item
		#self.__input = None
		#self.__output = None
		self.__file = self.__args.file
	# __init__

	def __checkOneArgDirective(self, arg_name, dct_key, short):
		arg_dict = vars(self.__args)
		arg_set = False
		if arg_dict.get(arg_name):
			arg_set = arg_dict.get(arg_name)
		else:
			if self.__short_options.find(short) > -1:
				arg_set = True

		if arg_set:
			if self.__directive[dct_key] is not None:
				raise Exception("--%s is not compatible with --%s" %\
				 				(self.__directive[dct_key], arg_name))
			else:
				self.__directive[dct_key] = arg_name

	def parseArguments(self):
		try:
			self.__checkOneArgDirective('extract', 'tar_action', 'x')
			self.__checkOneArgDirective('create', 'tar_action', 'c')
			self.__checkOneArgDirective('gzip', 'tar_filter', 'z')
			self.__checkOneArgDirective('bzip2', 'tar_filter', 'j')
			self.__checkOneArgDirective('verbose', 'tar_mode', 'v')
		except Exception as e:
			print("Error: %s\n--help for details" % str(e))
			exit(1)
		
		if self.__directive['tar_action'] == 'extract':
			if self.__file:
				self.__directive['tar_from'] = self.__file
			else:
				self.__directive['tar_from'] = self.__args.input_item
			self.__directive['tar_to'] = self.__args.output_item
		if self.__directive['tar_action'] == 'create':
			if self.__file:
				self.__directive['tar_to'] = self.__file
			else:
				self.__directive['tar_to'] = self.__args.input_item
			self.__directive['tar_from'] = self.__args.input_item
		"""
		print("Summary: " + str(self.__directive['tar_action']) +\
		 " From " + str(self.__directive['tar_from']) + " to " + str(self.__directive['tar_to']) +\
		  " with " + str(self.__directive['tar_filter']) + " filter")
		"""

	def doTar(self):
		tar_obj = None
		if self.__directive['tar_action'] == 'extract':
			tar_file_name = self.__directive['tar_from']
			tar_file_mode = self.determineCompression()
			if not tarfile.is_tarfile(tar_file_name):
				if self.tryUnZip():
					return 0
				print('The given file ' + tar_file_name +' is not a valid archive.')
				return -1
			try:
				tar_obj = tarfile.open(tar_file_name, 'r:' + tar_file_mode)
			except Exception as e:
				print('Cannot open file ' + tar_file_mode + " to do extract.")
				print(str(e))
				return -1
			try:
				tar_members = tar_obj.getmembers()
				for member in tar_members:
					tar_obj.extract(member, self.__directive['tar_to'])
					if self.__directive['tar_mode'] == 'verbose':
						print(member.name)
			except Exception as e:
				print('Fail to extract archive from `' + tar_file_name)
				print(str(e))
		elif self.__directive['tar_action'] == 'create':
			return 0
		else:
			return 0

	def tryUnZip(self):
		zip_object = None
		zip_file_name = self.__directive['tar_from']
		zip_file_mode = self.__directive['tar_mode']
		if not zipfile.is_zipfile(zip_file_name):
			print('Cannot extract ' + zip_file_name + ' as a zip archive')
			return False
		try:
			with ZipFile(zip_file_name) as zip_obj:
				zip_members = zip_obj.infolist()
				for member in zip_members:
					if zip_file_mode == 'verbose':
						print(member.filename)
					zip_obj.extract(member, self.__directive['tar_to'])
		except Exception as e:
			print('Fail to extract ' + zip_file_name)
			print(str(e))
			return False
		return True

	

	def determineCompression(self):
		tar_filter = self.__directive['tar_filter']
		if tar_filter is None:
			return "*"
		if tar_filter == 'gzip':
			return "gz"
		if tar_filter == 'bzip2':
			return "bz2"
		


def main():
	worker = TarWorker()
	worker.parseArguments()
	return worker.doTar()
	

if __name__ == "__main__":
	exit(main())




