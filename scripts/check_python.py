import platform
import sys

if sys.version_info != (3, 13, 0, "final", 0):
    raise ValueError(
        f"Python version is not 3.13.0 (got version {sys.version_info})"
    )

if sys.executable == "/opt/homebrew/opt/python@3.13/bin/python3.13":
    if platform.machine() != "arm64":
        raise ValueError(f"Incorrect architecture (got {platform.machine()})")
elif sys.executable == "/usr/local/opt/python@3.13/bin/python3.13":
    if platform.machine() != "x86_64":
        raise ValueError(f"Incorrect architecture (got {platform.machine()})")
else:
    raise ValueError(f"Unknown Python path (got {sys.executable})")

print(sys.version)
print(sys.executable)
