#!/usr/bin/env python3

import hashlib
import os
import subprocess
import sys
from pathlib import Path

from dotenv import dotenv_values

environ = {
    **dotenv_values(Path(__file__).parent.parent / ".env"),
    **os.environ,
}

log_file_path = Path(__file__).parent.parent.parent / "logs" / "macos.log"

if sys.platform != "darwin":
    raise ValueError(
        f"This script should only be run on macOS (got {sys.platform})"
    )

PYTHON_NAME = environ["PYTHON_NAME"]
PYTHON_VERSION_SSHORT = environ["PYTHON_VERSION_SSHORT"]
PYTHON_VERSION_SHORT = environ["PYTHON_VERSION_SHORT"]
PYTHON_VERSION_LONG = environ["PYTHON_VERSION_LONG"]
BREW_PYTHON_FORMULA = environ["BREW_PYTHON_FORMULA"]

# fmt: off
STDLIB_EXTENSIONS = ("_asyncio", "_bisect", "_blake2", "_bz2", "_codecs_cn", "_codecs_hk", "_codecs_iso2022", "_codecs_jp", "_codecs_kr", "_codecs_tw", "_contextvars", "_csv", "_ctypes", "_curses", "_datetime", "_dbm", "_decimal", "_elementtree", "_hashlib", "_heapq", "_json", "_lzma", "_md5", "_multibytecodec", "_multiprocessing", "_opcode", "_pickle", "_posixshmem", "_posixsubprocess", "_queue", "_random", "_scproxy", "_sha1", "_sha2", "_sha3", "_socket", "_sqlite3", "_ssl", "_statistics", "_struct", "_uuid", "array", "binascii", "fcntl", "grp", "math", "mmap", "pyexpat", "readline", "resource", "select", "syslog", "termios", "unicodedata", "zlib")
# fmt: on

def _sha256sum(filename):
    with open(filename, "rb", buffering=0) as f:
        return hashlib.file_digest(f, "sha256").hexdigest()


for extension in STDLIB_EXTENSIONS:
    original_binary = (
        "python-pkg-framework/Versions/Current/lib/python3.13/lib-dynload/"
        f"{extension}.cpython-{PYTHON_VERSION_SSHORT}-darwin.so"
    )
    output_binary = (
        f"macos/stdlib/{extension}.cpython-{PYTHON_VERSION_SSHORT}-darwin.so"
    )

    subprocess.run(["cp", original_binary, output_binary])

    check_arch = subprocess.run(
        ["/usr/bin/lipo", "-archs", output_binary],
        check=True,
        capture_output=True,
        text=True,
    )
    if not ("x86_64" in check_arch.stdout and "arm64" in check_arch.stdout):
        raise ValueError(
            f"The created extension {extension} is not universal "
            f"(got arch {check_arch.stdout})."
        )

    with open(log_file_path, mode="a") as log_file:
        log_file.write(f"{os.path.basename(output_binary)}    {_sha256sum(output_binary)}")
        log_file.write("\n")

with open(log_file_path, mode="a") as log_file:
    log_file.write("\n")