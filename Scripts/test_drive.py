import ConfigParser
import os
import sys
import traceback
import python_yacc2

list_file_name = ''
test_list = ConfigParser.ConfigParser()
error_mode = False
prudent_mode = False
test_passed = 0
test_total = 0

if len(sys.argv) > 1:
	list_file_name = sys.argv[1]
else:
	print('Need a test list file')
	exit(1)

if len(sys.argv) > 2:
	if sys.argv[2] == '-e':
		error_mode = True
	if sys.argv[2] == '-p':
		prudent_mode = True

with open(list_file_name, 'r+') as list_file:
	test_list.readfp(list_file)
	for test_dir in test_list.sections():
		#print('Going into dir : ' + test_dir)
		for test_file in test_list.items(test_dir):
			#print('AA ' + test_file[0] + ' ' + test_file[1])
			if error_mode and test_file[1] != 'Error' and test_file[1] != 'NoTesting':
				continue
			try:
				test_total += 1
				python_yacc2.do_test_parsing(test_dir + os.sep + test_file[0])
				test_list.set(test_dir, test_file[0], 'Pass')
				test_passed += 1
			except:
				test_list.set(test_dir, test_file[0], 'Error')
				if error_mode or prudent_mode:
					print('Parsing File : ' + test_dir + os.sep + test_file[0])
					traceback.print_exc()
					with open(list_file_name, 'w') as list_file:
						test_list.write(list_file)
					exit(1)

print('Testing Count : %d of %d passed' % (test_passed, test_total))

with open(list_file_name, 'w') as list_file:
	test_list.write(list_file)