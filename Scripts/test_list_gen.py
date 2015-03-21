import ConfigParser
import os
import sys

new_list = ConfigParser.ConfigParser()
target_root = ''

if len(sys.argv) > 1:
	target_root = sys.argv[1]
else:
	print('Need a target root dir to generat the test file list')
	exit(1)

if os.path.isdir(target_root):
	target_root = os.path.abspath(target_root)
	print('# Generating test file list for : ' + target_root)
else:
	print(target_root + ' is not a dir, give up')
	exit(1)

new_list.add_section(target_root)

def scan_dir(target_dir):
	for item in os.listdir(target_dir):
		if os.path.isdir(target_dir + os.sep + item):
			new_list.add_section(target_dir + os.sep + item)
			scan_dir(target_dir + os.sep + item)
		else:
			if item.endswith('.py'):
				new_list.set(target_dir, item, 'NoTesting')

if __name__ == '__main__':
	scan_dir(target_root)
	new_list.write(sys.stdout)
