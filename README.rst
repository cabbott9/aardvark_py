Total Phase Aardvark Python API - v6.00 local wheel builder
===========================================================

This fork adds a local Windows x86-64 wheel build path for the **Total Phase
Aardvark Software API v6.00**.

The upstream ``aardvark_py`` project packages the Python API supplied in Total
Phase Aardvark API releases.  The public PyPI package is older than the current
Total Phase API release, so this fork provides a reproducible way to create a
modern local wheel from the official v6.00 files downloaded directly from
Total Phase.

This repository does **not** contain or redistribute the Total Phase v6.00
``aardvark_py.py`` or ``aardvark.dll`` files.  The build script reads those
files from an API package obtained by the user from Total Phase and places
unmodified copies into the locally generated wheel.

What changed in this fork
-------------------------

* Added a local builder for **Aardvark Software API v6.00** on Windows x86-64.
* Added support for using either the extracted Total Phase API directory or the
  original downloaded ZIP as the build source.
* Added validation that the supplied Python wrapper reports
  ``AA_API_VERSION = 0x0600``.
* Added validation that the supplied ``aardvark.dll`` is a Windows x86-64 PE
  library.
* Added a Windows wheel output:
  ``aardvark_py-6.0.0-py3-none-win_amd64.whl``.
* Added ``build_v600.bat``, ``install_v600.bat``, and
  ``verify_installed.bat`` helper scripts.
* Added command-line help and source discovery through the
  ``AARDVARK_API_V600`` environment variable.
* The local builder uses only the Python standard library.  It does not create
  a virtual environment and does not require ``setuptools``, ``wheel``, or
  ``build``.
* The Total Phase v6.00 vendor payload and generated wheels are excluded from
  source control.

Requirements
------------

For the v6.00 local wheel builder you need:

* Windows x86-64.
* Python 3.10 or later.  Python 3.12 is supported by the generated wheel
  metadata.
* The **Aardvark Software API v6.00 - Windows x86 64-bit** package downloaded
  directly from Total Phase.
* A Total Phase Aardvark I2C/SPI Host Adapter for hardware operation and the
  final device verification step.

Get the Aardvark Software API
-----------------------------

Download the current Aardvark Software API from the official Total Phase page:

https://www.totalphase.com/products/aardvark-software-api/

Choose **Aardvark Software API v6.00 (Windows x86 64-bit)** for this builder.
Total Phase currently requires a login for software downloads.

Do not obtain the API files from this repository.  The build intentionally
requires the official Total Phase download.

Quick build
-----------

From the repository root, pass either the extracted v6.00 directory:

::

    build_v600.bat "C:\path\to\aardvark-api-windows-x86_64-v6.00"

or the original Total Phase ZIP:

::

    build_v600.bat "C:\path\to\aardvark-api-windows-x86_64-v6.00.zip"

The generated wheel is written to:

::

    dist\aardvark_py-6.0.0-py3-none-win_amd64.whl

You can also set the source once in an environment variable:

::

    set AARDVARK_API_V600=C:\path\to\aardvark-api-windows-x86_64-v6.00
    build_v600.bat

If no command-line source or environment variable is supplied, the builder
also checks for the standard v6.00 directory or ZIP in the repository root and
its parent directory.

Build and install
-----------------

Build and immediately install the locally generated wheel with:

::

    install_v600.bat "C:\path\to\aardvark-api-windows-x86_64-v6.00"

or, if ``AARDVARK_API_V600`` is already set:

::

    install_v600.bat

The install helper runs pip with ``--upgrade --force-reinstall`` so that an
older ``aardvark_py`` installation is replaced.

Verify the installation
-----------------------

Connect an Aardvark adapter and run:

::

    verify_installed.bat

The output should include:

::

    aardvark_py 6.0.0
    AA_API_VERSION 0x600

The final line reports the result of ``aa_find_devices(16)``.

Python usage
------------

The installed package remains compatible with the normal ``aardvark_py``
import style:

::

    from aardvark_py import *

    count, ports = aa_find_devices(16)
    print(count, ports)

The v6.00 wheel is intended as a drop-in package around the unmodified Total
Phase v6.00 Python wrapper and shared library.

Builder command-line help
-------------------------

The builder may also be run directly:

::

    python tools\build_v600.py --help

For example:

::

    python tools\build_v600.py "C:\path\to\aardvark-api-windows-x86_64-v6.00.zip"
    python tools\build_v600.py --output-dir C:\temp\wheel-output "C:\path\to\aardvark-api-windows-x86_64-v6.00"

Documentation
-------------

Detailed build and troubleshooting information is in
``docs/V600_BUILDING.rst``.  Licensing and redistribution notes are in
``docs/V600_LICENSE_NOTES.rst``.

Upstream project
----------------

This repository is a fork of the official Total Phase project:

https://github.com/totalphase/aardvark_py

The v6.00 local-builder additions are separate from Total Phase's upstream
release process.

License and redistribution
--------------------------

The Total Phase API package is subject to the license included with the API
download.  Among other restrictions, that license states that the Product must
not be placed on a publicly accessible Internet server and specifies additional
conditions for distribution of a Separate Work using ``aardvark.dll`` or
``aardvark_py.py``.

For that reason, this public fork contains the builder only.  It does not
contain the v6.00 Total Phase API payload or a generated v6.00 wheel.

Read the ``LICENSE.txt`` supplied with your Total Phase API download before
redistributing any generated wheel.  See ``docs/V600_LICENSE_NOTES.rst`` for a
short repository-specific explanation.
