import subprocess
import sys

if sys.platform != "darwin":
    raise ValueError(
        f"This script should only be run on macOS (got {sys.platform})"
    )

# fmt: off
STDLIB_EXTENSIONS = ["_asyncio", "_bisect", "_blake2", "_bz2", "_codecs_cn", "_codecs_hk", "_codecs_iso2022", "_codecs_jp", "_codecs_kr", "_codecs_tw", "_contextvars", "_csv", "_ctypes", "_curses", "_datetime", "_dbm", "_decimal", "_elementtree", "_hashlib", "_heapq", "_json", "_lzma", "_md5", "_multibytecodec", "_multiprocessing", "_opcode", "_pickle", "_posixshmem", "_posixsubprocess", "_queue", "_random", "_scproxy", "_sha1", "_sha2", "_sha3", "_socket", "_sqlite3", "_ssl", "_statistics", "_struct", "_uuid", "array", "binascii", "fcntl", "grp", "math", "mmap", "pyexpat", "readline", "resource", "select", "syslog", "termios", "unicodedata", "zlib"]
# fmt: on

for extension in STDLIB_EXTENSIONS:
    arm64_binary = f"/opt/homebrew/opt/python@3.13/Frameworks/Python.framework/Versions/3.13/lib/python3.13/lib-dynload/{extension}.cpython-313-darwin.so"
    x86_binary = f"/usr/local/opt/python@3.13/Frameworks/Python.framework/Versions/3.13/lib/python3.13/lib-dynload/{extension}.cpython-313-darwin.so"
    output_binary = f"macos/stdlib/{extension}.cpython-313-darwin.so"

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
