#!/usr/bin/env python3
"""Build a local Windows x86-64 aardvark_py 6.0.0 wheel.

The Total Phase v6.00 API payload is intentionally NOT stored in this
repository. Supply either the extracted API directory or the original ZIP
obtained directly from Total Phase.

Official download:
https://www.totalphase.com/products/aardvark-software-api/
"""

from __future__ import annotations

import argparse
import base64
import csv
import hashlib
import io
import os
import re
import struct
import sys
import zipfile
from pathlib import Path

VERSION = "6.0.0"
DIST_NAME = "aardvark_py"
WHEEL_NAME = f"{DIST_NAME}-{VERSION}-py3-none-win_amd64.whl"
API_BASENAME = "aardvark-api-windows-x86_64-v6.00"
API_DOWNLOAD_URL = "https://www.totalphase.com/products/aardvark-software-api/"
ENV_SOURCE = "AARDVARK_API_V600"


def _repository_root() -> Path:
  return Path(__file__).resolve().parents[1]


def _source_candidates() -> list[Path]:
  root = _repository_root()
  candidates: list[Path] = []

  env_source = os.environ.get(ENV_SOURCE, "").strip()
  if env_source:
    candidates.append(Path(env_source).expanduser())

  for base in (root, root.parent):
    candidates.append(base / API_BASENAME)
    candidates.append(base / f"{API_BASENAME}.zip")

  return candidates


def resolve_source(argument: str | None) -> Path:
  if argument:
    source = Path(argument).expanduser()
    if source.exists():
      return source
    raise FileNotFoundError(f"Aardvark API source does not exist: {source}")

  for candidate in _source_candidates():
    if candidate.exists():
      return candidate

  searched = "\n  ".join(str(path) for path in _source_candidates())
  raise FileNotFoundError(
    "Aardvark API v6.00 source was not found.\n\n"
    "Download 'Aardvark Software API v6.00 (Windows x86 64-bit)' from:\n"
    f"  {API_DOWNLOAD_URL}\n\n"
    "Then either pass the extracted directory/ZIP on the command line or set\n"
    f"the {ENV_SOURCE} environment variable.\n\n"
    "Automatic search locations were:\n"
    f"  {searched}"
  )


def _read_from_directory(source: Path) -> tuple[bytes, bytes, bytes]:
  if source.name.lower() == "python":
    root = source.parent
    python_dir = source
  else:
    root = source
    python_dir = root / "python"

  wrapper = python_dir / "aardvark_py.py"
  dll = python_dir / "aardvark.dll"
  license_file = root / "LICENSE.txt"

  missing = [path for path in (wrapper, dll, license_file) if not path.is_file()]
  if missing:
    names = "\n  ".join(str(path) for path in missing)
    raise FileNotFoundError(f"Required Total Phase files were not found:\n  {names}")

  return wrapper.read_bytes(), dll.read_bytes(), license_file.read_bytes()


def _find_zip_member(names: list[str], suffix: str) -> str:
  matches = [name for name in names if name.replace("\\", "/").lower().endswith(suffix.lower())]
  if len(matches) != 1:
    raise FileNotFoundError(f"Expected exactly one ZIP member ending in {suffix!r}; found {len(matches)}")
  return matches[0]


def _read_from_zip(source: Path) -> tuple[bytes, bytes, bytes]:
  with zipfile.ZipFile(source, "r") as archive:
    names = archive.namelist()
    wrapper_name = _find_zip_member(names, "/python/aardvark_py.py")
    dll_name = _find_zip_member(names, "/python/aardvark.dll")
    license_name = _find_zip_member(names, "/license.txt")
    return (
      archive.read(wrapper_name),
      archive.read(dll_name),
      archive.read(license_name),
    )


def read_vendor_payload(source: Path) -> tuple[bytes, bytes, bytes]:
  if source.is_dir():
    return _read_from_directory(source)
  if source.is_file() and source.suffix.lower() == ".zip":
    return _read_from_zip(source)
  raise FileNotFoundError(f"Aardvark API source is not a directory or ZIP: {source}")


def validate_wrapper(wrapper: bytes) -> None:
  text = wrapper.decode("utf-8", errors="strict")
  if re.search(r"AA_API_VERSION\s*=\s*0x0600\b", text) is None:
    raise ValueError(
      "aardvark_py.py is not the Total Phase v6.00 API wrapper "
      "(AA_API_VERSION 0x0600 not found)."
    )


def validate_windows_x64_dll(dll: bytes) -> None:
  if len(dll) < 0x40 or dll[:2] != b"MZ":
    raise ValueError("aardvark.dll is not a valid Windows PE file.")

  pe_offset = struct.unpack_from("<I", dll, 0x3C)[0]
  if pe_offset + 6 > len(dll) or dll[pe_offset:pe_offset + 4] != b"PE\x00\x00":
    raise ValueError("aardvark.dll does not contain a valid PE header.")

  machine = struct.unpack_from("<H", dll, pe_offset + 4)[0]
  if machine != 0x8664:
    raise ValueError(f"aardvark.dll is not x86-64 (PE machine 0x{machine:04X}).")


def sha256_record(data: bytes) -> str:
  digest = hashlib.sha256(data).digest()
  encoded = base64.urlsafe_b64encode(digest).rstrip(b"=").decode("ascii")
  return f"sha256={encoded}"


def metadata_text() -> str:
  return (
    "Metadata-Version: 2.1\n"
    "Name: aardvark_py\n"
    f"Version: {VERSION}\n"
    "Summary: Local wheel built from the Total Phase Aardvark Software API v6.00\n"
    "Home-page: https://github.com/totalphase/aardvark_py\n"
    "Author: Total Phase, Inc.\n"
    "License: Proprietary License (see bundled Total Phase LICENSE.txt)\n"
    "Classifier: Development Status :: 5 - Production/Stable\n"
    "Classifier: Intended Audience :: Developers\n"
    "Classifier: License :: Other/Proprietary License\n"
    "Classifier: Operating System :: Microsoft :: Windows\n"
    "Classifier: Programming Language :: Python :: 3\n"
    "Classifier: Programming Language :: Python :: 3.10\n"
    "Classifier: Programming Language :: Python :: 3.11\n"
    "Classifier: Programming Language :: Python :: 3.12\n"
    "Classifier: Programming Language :: Python :: 3.13\n"
    "Classifier: Topic :: Software Development :: Embedded Systems\n"
    "Requires-Python: >=3.10\n"
    "Description-Content-Type: text/markdown\n"
    "\n"
    "# aardvark_py 6.0.0 local wheel\n"
    "\n"
    "Built locally from the unmodified Total Phase Aardvark Software API v6.00 "
    "Python wrapper and Windows x86-64 DLL.\n\n"
    f"Official API download: {API_DOWNLOAD_URL}\n"
  )


def build_wheel(source: Path, output_dir: Path) -> Path:
  wrapper, dll, license_data = read_vendor_payload(source)
  validate_wrapper(wrapper)
  validate_windows_x64_dll(dll)

  init_data = (
    '"""Total Phase Aardvark Python API v6.00."""\n\n'
    f'__version__ = "{VERSION}"\n\n'
    'from ._api import *  # noqa: F401,F403\n'
  ).encode("utf-8")

  dist_info = f"{DIST_NAME}-{VERSION}.dist-info"
  files: dict[str, bytes] = {
    f"{DIST_NAME}/__init__.py": init_data,
    f"{DIST_NAME}/_api.py": wrapper,
    f"{DIST_NAME}/aardvark.dll": dll,
    f"{dist_info}/licenses/LICENSE.txt": license_data,
    f"{dist_info}/METADATA": metadata_text().encode("utf-8"),
    f"{dist_info}/WHEEL": (
      "Wheel-Version: 1.0\n"
      "Generator: aardvark_py v6.00 local builder\n"
      "Root-Is-Purelib: false\n"
      "Tag: py3-none-win_amd64\n"
    ).encode("utf-8"),
    f"{dist_info}/top_level.txt": b"aardvark_py\n",
  }

  record_rows: list[list[str]] = []
  for name, data in files.items():
    record_rows.append([name, sha256_record(data), str(len(data))])

  record_name = f"{dist_info}/RECORD"
  record_rows.append([record_name, "", ""])
  record_buffer = io.StringIO(newline="")
  writer = csv.writer(record_buffer, lineterminator="\n")
  writer.writerows(record_rows)
  files[record_name] = record_buffer.getvalue().encode("utf-8")

  output_dir.mkdir(parents=True, exist_ok=True)
  wheel_path = output_dir / WHEEL_NAME
  if wheel_path.exists():
    wheel_path.unlink()

  with zipfile.ZipFile(wheel_path, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
    for name, data in files.items():
      info = zipfile.ZipInfo(name, date_time=(2024, 2, 8, 12, 0, 0))
      info.compress_type = zipfile.ZIP_DEFLATED
      info.external_attr = 0o644 << 16
      archive.writestr(info, data)

  return wheel_path


def main() -> int:
  parser = argparse.ArgumentParser(
    description=(
      "Build aardvark_py 6.0.0 from a locally downloaded Total Phase "
      "Aardvark Software API v6.00 Windows x86-64 package."
    ),
    epilog=(
      "Download the official API from:\n"
      f"  {API_DOWNLOAD_URL}\n\n"
      "Examples:\n"
      f"  python tools\\build_v600.py C:\\Downloads\\{API_BASENAME}.zip\n"
      f"  set {ENV_SOURCE}=C:\\Tools\\{API_BASENAME}\n"
      "  python tools\\build_v600.py"
    ),
    formatter_class=argparse.RawDescriptionHelpFormatter,
  )
  parser.add_argument(
    "source",
    nargs="?",
    help=(
      "Path to the extracted aardvark-api-windows-x86_64-v6.00 directory, "
      "its python subdirectory, or the original ZIP. If omitted, the builder "
      f"checks {ENV_SOURCE} and standard local paths."
    ),
  )
  parser.add_argument(
    "--output-dir",
    default=str(_repository_root() / "dist"),
    help="Directory in which to create the wheel. Default: repository dist directory.",
  )
  parser.add_argument(
    "--version",
    action="version",
    version=f"aardvark_py local wheel builder {VERSION}",
  )
  args = parser.parse_args()

  try:
    source = resolve_source(args.source)
    output_dir = Path(args.output_dir).expanduser()
    wheel_path = build_wheel(source, output_dir)
  except (OSError, ValueError, zipfile.BadZipFile) as exc:
    print(f"ERROR: {exc}", file=sys.stderr)
    return 1

  print(f"Source: {source}")
  print(f"Built:  {wheel_path}")
  print("The wheel contains unmodified Total Phase v6.00 aardvark_py.py and aardvark.dll files from the supplied API package.")
  print("Review the Total Phase LICENSE.txt before redistributing the generated wheel.")
  return 0


if __name__ == "__main__":
  raise SystemExit(main())
