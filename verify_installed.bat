@echo off
python -c "import aardvark_py; print('aardvark_py', aardvark_py.__version__); print('AA_API_VERSION', hex(aardvark_py.AA_API_VERSION)); print('devices', aardvark_py.aa_find_devices(16))"
