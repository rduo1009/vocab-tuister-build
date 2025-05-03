#!/bin/zsh

if [[ "$OSTYPE" != "darwin"* ]]; then
    echo "This script should only be run on macOS (got $OSTYPE)"
    exit 1
fi

set -e

export $(cat macos/.env | xargs)

rm -rf macos/wheels
mkdir -p macos/wheels

# ------------------------------------------------------------------------
# LZ4 WHEEL

curl -L "$LZ4_WHEEL_X86_URL" -O
curl -L "$LZ4_WHEEL_ARM_URL" -O

x86_64_wheel=$(basename "$LZ4_WHEEL_X86_URL")
arm64_wheel=$(basename "$LZ4_WHEEL_ARM_URL")

delocate-merge "$x86_64_wheel" "$arm64_wheel" --wheel-dir macos/wheels

output_wheel=(macos/wheels/*.whl) 

{
  echo "$arm64_wheel   $(shasum -a 256 "$arm64_wheel")"
  echo "$x86_64_wheel    $(shasum -a 256 "$x86_64_wheel")"
  echo "${output_wheel:t}    $(shasum -a 256 "$output_wheel")"
  echo ""
} >> logs/macos.log

rm "$x86_64_wheel" "$arm64_wheel"

# ------------------------------------------------------------------------
# NUMPY WHEEL

curl -L "$NUMPY_WHEEL_X86_URL" -O
curl -L "$NUMPY_WHEEL_ARM_URL" -O

x86_64_wheel=$(basename "$NUMPY_WHEEL_X86_URL")
arm64_wheel=$(basename "$NUMPY_WHEEL_ARM_URL")

delocate-merge "$x86_64_wheel" "$arm64_wheel" --wheel-dir macos/wheels

wheels=(macos/wheels/*.whl) 
for w in $wheels; do
  [[ $w == "$output_wheel" ]] && continue
  output_wheel=$w
done

{
  echo "$arm64_wheel    $(shasum -a 256 "$arm64_wheel")"
  echo "$x86_64_wheel    $(shasum -a 256 "$x86_64_wheel")"
  echo "${output_wheel:t}    $(shasum -a 256 "$output_wheel")"
  echo ""
} >> logs/macos.log

rm "$x86_64_wheel" "$arm64_wheel"