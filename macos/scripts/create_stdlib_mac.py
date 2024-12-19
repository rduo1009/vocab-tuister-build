import os
import subprocess
import sys

if sys.platform != "darwin":
    raise ValueError(
        f"This script should only be run on macOS (got {sys.platform})"
    )

PYTHON_NAME = os.environ["PYTHON_NAME"]
PYTHON_VERSION_SSHORT = os.environ["PYTHON_VERSION_SSHORT"]
PYTHON_VERSION_SHORT = os.environ["PYTHON_VERSION_SHORT"]
PYTHON_VERSION_LONG = os.environ["PYTHON_VERSION_LONG"]
BREW_PYTHON_FORMULA = os.environ["BREW_PYTHON_FORMULA"]

# fmt: off
STDLIB_EXTENSIONS = ["_asyncio", "_bisect", "_blake2", "_bz2", "_codecs_cn", "_codecs_hk", "_codecs_iso2022", "_codecs_jp", "_codecs_kr", "_codecs_tw", "_contextvars", "_csv", "_ctypes", "_curses", "_datetime", "_dbm", "_decimal", "_elementtree", "_hashlib", "_heapq", "_json", "_lzma", "_md5", "_multibytecodec", "_multiprocessing", "_opcode", "_pickle", "_posixshmem", "_posixsubprocess", "_queue", "_random", "_scproxy", "_sha1", "_sha2", "_sha3", "_socket", "_sqlite3", "_ssl", "_statistics", "_struct", "_uuid", "array", "binascii", "fcntl", "grp", "math", "mmap", "pyexpat", "readline", "resource", "select", "syslog", "termios", "unicodedata", "zlib"]
# fmt: on

for extension in STDLIB_EXTENSIONS:
    arm64_binary = (
        f"/opt/homebrew/opt/{BREW_PYTHON_FORMULA}/Frameworks/Python.framework/"
        f"Versions/{PYTHON_VERSION_SHORT}/lib/{PYTHON_NAME}/lib-dynload/"
        f"{extension}.cpython-{PYTHON_VERSION_SSHORT}-darwin.so"
    )
    x86_binary = (
        f"/usr/local/opt/{BREW_PYTHON_FORMULA}/Frameworks/Python.framework/"
        f"Versions/{PYTHON_VERSION_SHORT}/lib/{PYTHON_NAME}/lib-dynload/"
        f"{extension}.cpython-{PYTHON_VERSION_SSHORT}-darwin.so"
    )
    output_binary = (
        f"macos/stdlib/{extension}.cpython-{PYTHON_VERSION_SSHORT}-darwin.so"
    )

    subprocess.run(
        [
            "/usr/bin/lipo",
            "-create",
            arm64_binary,
            x86_binary,
            "-o",
            output_binary,
        ],
        check=True,
    )

    check_arch = subprocess.run(
        ["/usr/bin/lipo", "-archs", output_binary],
        check=True,
        capture_output=True,
        text=True,
    )
    if not ("x86_64" in check_arch.stdout and "arm64" in check_arch.stdout):
        raise ValueError(
            f"The created extension {extension} is not universal (got arch {check_arch.stdout})."
        )
