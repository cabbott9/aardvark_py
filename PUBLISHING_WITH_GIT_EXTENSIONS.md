# Publishing the v6.00 builder changes with Git Extensions

These instructions are for contributors using Git Extensions on Windows.

## 1. Fork the upstream repository

Open the official Total Phase repository:

https://github.com/totalphase/aardvark_py

Use GitHub's **Fork** action and create the fork under your own GitHub account.

## 2. Clone your fork

In Git Extensions:

1. Choose **Clone repository**.
2. Enter your fork URL, for example `https://github.com/<username>/aardvark_py.git`.
3. Choose a local destination folder.
4. Click **Clone**.

## 3. Copy the v6.00 builder files into the clone

Copy these files/directories into the repository root, replacing the existing
`README.rst` when prompted:

```text
.gitignore
README.rst
build_v600.bat
install_v600.bat
verify_installed.bat
tools\build_v600.py
docs\V600_BUILDING.rst
docs\V600_LICENSE_NOTES.rst
.github\workflows\repo-check.yml
```

The public repository should **not** contain the Total Phase v6.00 ZIP,
extracted API payload, generated wheel, `aardvark_py.py`, or `aardvark.dll`.

## 4. Test locally

Download **Aardvark Software API v6.00 (Windows x86 64-bit)** from:

https://www.totalphase.com/products/aardvark-software-api/

Then run, for example:

```bat
build_v600.bat "C:\path\to\aardvark-api-windows-x86_64-v6.00"
```

Confirm this file is created:

```text
dist\aardvark_py-6.0.0-py3-none-win_amd64.whl
```

`dist` is ignored by Git and should not appear in the commit list.

## 5. Review the commit

In Git Extensions, open **Commit** and verify that no Total Phase API payload
or generated wheel is staged.  A suitable commit message is:

```text
Add Aardvark API v6.00 local wheel builder
```

Commit the files and push the branch to your fork.

## 6. Check GitHub

Open the fork on GitHub.  The repository front page should now display the new
`README.rst`, including the v6.00 build instructions and the link to the
official Total Phase API download page.

The repository workflow also performs a syntax check of the builder and checks
for common accidentally committed v6.00 payload paths.
