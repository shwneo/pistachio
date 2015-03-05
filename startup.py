import os
import platform
from Scripts.build_perl import PerlBuilding
from Scripts.build_svn import SvnBuilding
from Scripts.build_nasm import NasmBuilding
from Scripts.build_python import PythonBuilding
from Scripts.build_tcltk import TclTkBuilding
ENVIRON_SPLIT = ':'
# check the environment
if platform.system() == 'Windows':
	VC90 = os.environ.get('VS90COMNTOOLS')
	ENVIRON_SPLIT = ';'
	if VC90 is None:
		print('Visual C++ 2008 is not found, quit')
		exit(1)
elif platform.system() == 'Linux':
	pass
elif platform.system() == 'Drawin':
	pass

os.environ['PATH'] = os.environ.get('PATH') + ENVIRON_SPLIT +\
						os.getcwd() + os.sep + 'Tools' + os.sep + 'bin'

#PerlBuilding.do_build()
#SvnBuilding.do_build()
#NasmBuilding.do_build()
#PythonBuilding.do_build()
TclTkBuilding.do_build('C:\\Users\\IBM_ADMIN\\workspace\\pistachio\\Build\\Python-2.7.9\\externals')