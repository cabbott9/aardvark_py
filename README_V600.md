# aardvark_py v6.00 local wheel builder

This adds a local build path for the Total Phase Aardvark Python API v6.00 without committing the v6.00 vendor payload to GitHub.

## Why it works this way

The Total Phase v6.00 API package contains `python\aardvark_py.py`, `python\aardvark.dll`, and its license. The build script reads those files from a copy you downloaded directly from Total Phase and packages them into a Windows x86-64 Python wheel.

The v6.00 vendor files are deliberately excluded from this repository. Do not add the v6.00 API ZIP, extracted API directory, generated wheel, `aardvark_py.py`, or `aardvark.dll` to a public fork unless you have confirmed that your intended distribution is permitted by Total Phase.

## Build on Chris's PC

The default API location is already set to:

```text
C:\sys\total_phase\aardvark-api-windows-x86_64-v6.00
```

From the repository root, run:

```bat
build_v600.bat
```

The result is:

```text
dist\aardvark_py-6.0.0-py3-none-win_amd64.whl
```

You can also build directly from the original Total Phase ZIP:

```bat
build_v600.bat "C:\path\to\aardvark-api-windows-x86_64-v6.00.zip"
```

## Build and install

```bat
install_v600.bat
```

This builds the wheel and then runs:

```bat
python -m pip install --upgrade --force-reinstall dist\aardvark_py-6.0.0-py3-none-win_amd64.whl
```

## Verify

With an Aardvark attached:

```bat
verify_installed.bat
```

Expected API version:

```text
AA_API_VERSION 0x600
```

## No virtual environment

The builder uses only the Python standard library. It does not create a virtual environment and does not require `setuptools`, `wheel`, or `build` to generate the wheel.
