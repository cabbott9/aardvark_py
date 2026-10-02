Building aardvark_py 6.0.0 locally
==================================

Overview
--------

``tools/build_v600.py`` creates a Windows x86-64 Python wheel using the
unmodified ``aardvark_py.py`` and ``aardvark.dll`` from the official Total
Phase Aardvark Software API v6.00 package.

Official API download
---------------------

Obtain the API from Total Phase:

https://www.totalphase.com/products/aardvark-software-api/

For this builder, select **Aardvark Software API v6.00 (Windows x86 64-bit)**.
The Total Phase download page requires a login.

Accepted source forms
---------------------

The builder accepts either:

1. The extracted API root directory, for example:

   ::

       C:\Tools\aardvark-api-windows-x86_64-v6.00

2. The ``python`` subdirectory inside that extracted package.

3. The original downloaded ZIP, for example:

   ::

       C:\Downloads\aardvark-api-windows-x86_64-v6.00.zip

Source selection order
----------------------

When no positional source argument is supplied, the builder searches in this
order:

1. ``AARDVARK_API_V600`` environment variable.
2. ``aardvark-api-windows-x86_64-v6.00`` in the repository root.
3. ``aardvark-api-windows-x86_64-v6.00.zip`` in the repository root.
4. The same directory and ZIP names in the repository parent directory.

If no source is found, the builder exits with an error and prints the official
Total Phase download URL.

Build commands
--------------

Using an extracted directory:

::

    build_v600.bat "C:\Tools\aardvark-api-windows-x86_64-v6.00"

Using the original ZIP:

::

    build_v600.bat "C:\Downloads\aardvark-api-windows-x86_64-v6.00.zip"

Using an environment variable:

::

    set AARDVARK_API_V600=C:\Tools\aardvark-api-windows-x86_64-v6.00
    build_v600.bat

Direct Python invocation:

::

    python tools\build_v600.py --help
    python tools\build_v600.py "C:\Tools\aardvark-api-windows-x86_64-v6.00"

Custom output directory:

::

    python tools\build_v600.py --output-dir C:\temp\wheels "C:\Tools\aardvark-api-windows-x86_64-v6.00"

Output
------

The default output is:

::

    dist\aardvark_py-6.0.0-py3-none-win_amd64.whl

The wheel contains:

* package initializer reporting version ``6.0.0``;
* the unmodified v6.00 Total Phase Python wrapper as the package API module;
* the unmodified v6.00 Windows x86-64 ``aardvark.dll``;
* the Total Phase license from the API package; and
* wheel metadata describing the local package.

Validation performed by the builder
-----------------------------------

Before creating the wheel, the builder verifies that:

* the required wrapper, DLL, and license files are present;
* the wrapper contains ``AA_API_VERSION = 0x0600``;
* the DLL is a Windows PE file; and
* the PE machine type is x86-64 (``0x8664``).

These checks are intended to prevent accidentally building the v6.00 wheel
from an older API release or the wrong Windows architecture.

Install
-------

Use the helper:

::

    install_v600.bat "C:\Tools\aardvark-api-windows-x86_64-v6.00"

or build first and install manually:

::

    python -m pip install --upgrade --force-reinstall dist\aardvark_py-6.0.0-py3-none-win_amd64.whl

Verify
------

With an Aardvark connected:

::

    verify_installed.bat

The helper prints the package version, API version, and detected devices.
Expected API version:

::

    AA_API_VERSION 0x600

Troubleshooting
---------------

``Aardvark API v6.00 source was not found``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Pass the extracted folder or ZIP explicitly, or set ``AARDVARK_API_V600``.
The API can be downloaded from:

https://www.totalphase.com/products/aardvark-software-api/

``AA_API_VERSION 0x0600 not found``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The supplied API package is not the expected v6.00 release.  Download v6.00
from the official Total Phase page and rebuild.

``aardvark.dll is not x86-64``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The source package is for a different Windows architecture.  Download
**Aardvark Software API v6.00 (Windows x86 64-bit)**.

An older aardvark_py package is still imported
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Reinstall the newly built wheel with:

::

    python -m pip install --upgrade --force-reinstall dist\aardvark_py-6.0.0-py3-none-win_amd64.whl

Then verify which file Python is loading:

::

    python -c "import aardvark_py; print(aardvark_py.__file__)"

No Aardvark devices are reported
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Confirm the adapter is connected, that Windows recognizes it, and that no
other application currently owns the Aardvark device.  Also review the Total
Phase API documentation included with the official download.
