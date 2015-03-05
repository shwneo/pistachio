@set PATH=%PATH%;%VS90COMNTOOLS%
@set PATH=%PATH%;%VS90COMNTOOLS%\..\..\VC
call vcvarsall.bat x86
cd %1\win && nmake -f makefile.vc TCLDIR=%2 INSTALLDIR=%3 all install