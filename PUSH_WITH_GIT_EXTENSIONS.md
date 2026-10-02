# Put this into cabbott9/aardvark_py with Git Extensions

## 1. Create the fork once

If you have not already created it, open the Total Phase `aardvark_py` repository on GitHub, click **Fork**, choose owner **cabbott9**, keep the repository name `aardvark_py`, and create the fork.

Your fork URL will be:

```text
https://github.com/cabbott9/aardvark_py
```

## 2. Clone your fork in Git Extensions

In Git Extensions:

1. Choose **Clone repository**.
2. Repository to clone: `https://github.com/cabbott9/aardvark_py.git`
3. Choose the local destination folder.
4. Click **Clone**.

## 3. Copy these fork-ready files into the clone

Copy the following from this package into the root of the cloned repository:

```text
.gitignore
README_V600.md
build_v600.bat
install_v600.bat
verify_installed.bat
tools\build_v600.py
.github\workflows\repo-check.yml
```

Do **not** copy the Total Phase v6.00 API ZIP, extracted API directory, generated `dist` directory, `aardvark.dll`, or `aardvark_py.py` into the repository.

## 4. Test before committing

Open a command prompt in the cloned repository and run:

```bat
build_v600.bat
```

With your current machine setup it should automatically use:

```text
C:\sys\total_phase\aardvark-api-windows-x86_64-v6.00
```

Confirm this file appears:

```text
dist\aardvark_py-6.0.0-py3-none-win_amd64.whl
```

`dist` is ignored by Git and should not appear in the commit list.

## 5. Commit in Git Extensions

1. Click **Commit**.
2. Check that only the fork-ready source/build files are staged.
3. Suggested commit message:

```text
Add local Aardvark API v6.00 wheel builder
```

4. Click **Commit**.
5. Click **Push** and push the `master` branch to `origin`.

After that, GitHub will contain the reproducible build scripts, but the Total Phase v6.00 vendor payload and wheel remain only on your PC.
