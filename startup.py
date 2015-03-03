import os
import platform
from Scripts.build_perl import PerlBuilding
from Scripts.build_svn import SvnBuilding
# check the environment
if platform.system() == 'Windows':
	VC90 = os.environ.get('VS90COMNTOOLS')
	if VC90 is None:
		print('Visual C++ 2008 is not found, quit')
elif platform.system() == 'Linux':
	pass
elif platform.system() == 'Drawin':
	pass

#PerlBuilding.do_build()
SvnBuilding.do_build()