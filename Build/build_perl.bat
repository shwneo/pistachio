@set PATH=%PATH%;%VS90COMNTOOLS%
@set PATH=%PATH%;%VS90COMNTOOLS%\..\..\VC
@set WIN64=undef
call vcvarsall.bat x86
call cd %1\win32
call nmake && nmake install

