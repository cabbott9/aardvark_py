@echo off
setlocal

if "%~1"=="/?" goto :help
if /I "%~1"=="--help" goto :help
if /I "%~1"=="-h" goto :help

call "%~dp0build_v600.bat" %*
if errorlevel 1 exit /b %ERRORLEVEL%

python -m pip install --upgrade --force-reinstall "%~dp0dist\aardvark_py-6.0.0-py3-none-win_amd64.whl"
exit /b %ERRORLEVEL%

:help
echo Build and install aardvark_py 6.0.0 from the official Total Phase API v6.00.
echo.
echo Usage:
echo   install_v600.bat ^<api-directory-or-zip^>
echo   install_v600.bat
echo.
echo Official API download:
echo   https://www.totalphase.com/products/aardvark-software-api/
exit /b 0
