@echo off
setlocal

if "%~1"=="/?" goto :help
if /I "%~1"=="--help" goto :help
if /I "%~1"=="-h" goto :help

python -c "import aardvark_py; print('module', aardvark_py.__file__); print('aardvark_py', aardvark_py.__version__); print('AA_API_VERSION', hex(aardvark_py.AA_API_VERSION)); print('devices', aardvark_py.aa_find_devices(16))"
exit /b %ERRORLEVEL%

:help
echo Verify the installed aardvark_py package and search for attached Aardvark devices.
echo Expected v6.00 API version: 0x600
exit /b 0
