@echo off
setlocal

if "%~1"=="/?" goto :help
if /I "%~1"=="--help" goto :help
if /I "%~1"=="-h" goto :help

if "%~1"=="" (
  python "%~dp0tools\build_v600.py"
) else (
  python "%~dp0tools\build_v600.py" "%~1"
)
exit /b %ERRORLEVEL%

:help
echo Build aardvark_py 6.0.0 from the official Total Phase Aardvark API v6.00.
echo.
echo Usage:
echo   build_v600.bat ^<api-directory-or-zip^>
echo   build_v600.bat
echo.
echo If no source is supplied, tools\build_v600.py checks AARDVARK_API_V600
echo and standard local package names. For full help run:
echo   python tools\build_v600.py --help
echo.
echo Official API download:
echo   https://www.totalphase.com/products/aardvark-software-api/
exit /b 0
