Total Phase v6.00 license notes
===============================

Purpose of this document
------------------------

This file explains why the v6.00 builder in this fork does not commit or host
the Total Phase API payload.  It is not a substitute for the Total Phase End
User License Agreement included with the official API package.

Official API source
-------------------

Download the Aardvark Software API directly from Total Phase:

https://www.totalphase.com/products/aardvark-software-api/

Repository policy
-----------------

The Total Phase v6.00 ``LICENSE.txt`` states, among other conditions, that the
Product must not be placed on a publicly accessible Internet server.  It also
contains specific conditions for distribution of a Separate Work that makes
use of ``aardvark.dll`` or ``aardvark_py.py``.

Accordingly, this public repository intentionally contains only the local build
logic and documentation.  The following are excluded from source control:

* Total Phase API ZIP downloads;
* extracted Total Phase v6.00 API directories;
* ``aardvark_py.py`` copied from the v6.00 API;
* ``aardvark.dll`` copied from the v6.00 API; and
* locally generated v6.00 wheel files.

The builder requires each user to obtain the official API package directly
from Total Phase.

Generated wheels
----------------

A generated wheel includes unmodified Total Phase API files.  Before sharing,
uploading, publishing, or otherwise distributing such a wheel, read and comply
with the ``LICENSE.txt`` included in the Total Phase API package.  The license
contains approval and notification requirements for some forms of distribution.

Source control protection
-------------------------

The repository ``.gitignore`` excludes common Total Phase v6.00 download,
extraction, and wheel-output paths.  The GitHub Actions repository check also
looks for known v6.00 payload names so accidental commits are easier to catch.
