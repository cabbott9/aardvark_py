@echo off
setlocal

call "%~dp0build_v600.bat" %*
if errorlevel 1 exit /b %ERRORLEVEL%

python -m pip install --upgrade --force-reinstall "%~dp0dist\aardvark_py-6.0.0-py3-none-win_amd64.whl"
exit /b %ERRORLEVEL%
