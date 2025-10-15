#!/usr/bin/env python3

# ruff: noqa: S404, ANN202, S603, D100

import hashlib
import subprocess
from pathlib import Path

log_file_path = Path(__file__).parent.parent.parent / "logs" / "macos.log"

PYTHON_DYLIBS = ("libpython3.14", "libssl.3", "libcrypto.3", "libzstd.1")
HOMEBREW_DYLIBS = (
    ("gettext", "libintl.8"),
    ("xz", "liblzma.5"),
    ("mpdecimal", "libmpdec.4"),
    ("readline", "libreadline.8"),
    ("zlib", "libz.1"),
)


def _sha256sum(filename: Path):
    with filename.open("rb", buffering=0) as f:
        return hashlib.file_digest(f, "sha256").hexdigest()


for dylib in PYTHON_DYLIBS:
    original_dylib = Path(
        f"python-pkg-framework/Versions/Current/lib/{dylib}.dylib"
    )
    output_dylib = Path(f"macos/dylib/{dylib}.dylib")

    subprocess.run(["/bin/cp", original_dylib, output_dylib], check=True)

    check_arch = subprocess.run(
        ["/usr/bin/lipo", "-archs", output_dylib],
        check=True,
        capture_output=True,
        text=True,
    )
    if not ("x86_64" in check_arch.stdout and "arm64" in check_arch.stdout):
        raise ValueError(
            f"Dylib {output_dylib} is not universal (got {check_arch.stdout})."
        )

    with log_file_path.open(mode="a") as log_file:
        log_file.write(f"{output_dylib.name}    {_sha256sum(output_dylib)}")
        log_file.write("\n")

with log_file_path.open(mode="a") as log_file:
    log_file.write("\n")

for dylib in HOMEBREW_DYLIBS:
    formula = dylib[0]
    filename = dylib[1]

    arm64_dylib = Path(f"/opt/homebrew/opt/{formula}/lib/{filename}.dylib")
    x86_dylib = Path(f"/usr/local/opt/{formula}/lib/{filename}.dylib")
    output_dylib = Path(f"macos/dylib/{filename}.dylib")

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
            f"Dylib {filename} is not universal (got {check_arch.stdout})."
        )

    with log_file_path.open(mode="a") as log_file:
        log_file.write(
            f"{arm64_dylib.name} (arm64)    {_sha256sum(arm64_dylib)}\n"
        )
        log_file.write(
            f"{x86_dylib.name} (x86_64)    {_sha256sum(x86_dylib)}\n"
        )
        log_file.write(
            f"{output_dylib.name} (universal2)    {_sha256sum(output_dylib)}\n"
        )
        log_file.write("\n")
