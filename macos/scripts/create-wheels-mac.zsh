#!/bin/zsh

if [[ "$OSTYPE" != "darwin"* ]]; then
    echo "This script should only be run on macOS (got $OSTYPE)"
    exit 1
fi

export $(cat macos/.env | xargs)

rm -rf macos/wheels
mkdir -p macos/wheels

# lz4 wheel
curl -L "$LZ4_WHEEL_X86_URL" -O
curl -L "$LZ4_WHEEL_ARM_URL" -O

x86_64_wheel=$(basename "$LZ4_WHEEL_X86_URL")
arm64_wheel=$(basename "$LZ4_WHEEL_ARM_URL")

delocate-merge "$x86_64_wheel" "$arm64_wheel" --wheel-dir macos/wheels

rm "$x86_64_wheel" "$arm64_wheel"

# numpy wheel
curl -L "$NUMPY_WHEEL_X86_URL" -O
curl -L "$NUMPY_WHEEL_ARM_URL" -O

x86_64_wheel=$(basename "$NUMPY_WHEEL_X86_URL")
arm64_wheel=$(basename "$NUMPY_WHEEL_ARM_URL")

delocate-merge "$x86_64_wheel" "$arm64_wheel" --wheel-dir macos/wheels

rm "$x86_64_wheel" "$arm64_wheel"