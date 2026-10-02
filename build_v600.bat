@echo off
setlocal

if "%~1"=="" (
  set "AA_SOURCE=C:\sys\total_phase\aardvark-api-windows-x86_64-v6.00"
) else (
  set "AA_SOURCE=%~1"
)

python "%~dp0tools\build_v600.py" "%AA_SOURCE%"
exit /b %ERRORLEVEL%
