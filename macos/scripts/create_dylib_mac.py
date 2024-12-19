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
DYLIBS = ((BREW_PYTHON_FORMULA, f"libpython{PYTHON_VERSION_SHORT}"), ("gettext", "libintl.8"), ("xz", "liblzma.5"), ("mpdecimal", "libmpdec.4"), ("openssl@3", "libcrypto.3"), ("libb2", "libb2.1"), ("openssl@3", "libssl.3"), ("ncurses", "libncursesw.6"), ("readline", "libreadline.8"), ("lz4", "liblz4.1"), ("sqlite", "libsqlite3.0"))
# fmt: on

for dylib in DYLIBS:
    formula = dylib[0]
    filename = dylib[1]

    if formula == "python@3.13":
        assert filename == "libpython3.13"

        arm64_dylib = (
            "/opt/homebrew/opt/python@3.13/Frameworks/Python.framework/"
            "Versions/3.13/lib/libpython3.13.dylib"
        )
        x66_dylib = (
            "/usr/local/opt/python@3.13/Frameworks/Python.framework/"
            "Versions/3.13/lib/libpython3.13.dylib"
        )
        output_dylib = "macos/dylib/libpython3.13.dylib"

    else:
        arm64_dylib = f"/opt/homebrew/opt/{formula}/lib/{filename}.dylib"
        x86_dylib = f"/usr/local/opt/{formula}/lib/{filename}.dylib"
        output_dylib = f"macos/dylib/{filename}.dylib"

    subprocess.run(
        [
            "/usr/bin/lipo",
            "-create",
            arm64_dylib,
            x86_dylib,
            "-o",
            output_dylib,
        ],
        check=True,
    )

    check_arch = subprocess.run(
        ["/usr/bin/lipo", "-archs", output_dylib],
        check=True,
        capture_output=True,
        text=True,
    )
    if not ("x86_64" in check_arch.stdout and "arm64" in check_arch.stdout):
        raise ValueError(
            f"The created dynamic library {filename} is not universal "
            f"(got arch {check_arch.stdout})."
        )
