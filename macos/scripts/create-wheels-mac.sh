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
  echo "${arm64_wheel:t}    $(shasum -a 256 "$arm64_wheel" | awk '{ print $1 }')"
  echo "${x86_64_wheel:t}    $(shasum -a 256 "$x86_64_wheel" | awk '{ print $1 }')"
  echo "${output_wheel:t}    $(shasum -a 256 "$output_wheel" | awk '{ print $1 }')"
  echo ""
} >> logs/macos.log

rm "$x86_64_wheel" "$arm64_wheel"

# ------------------------------------------------------------------------
# MARKUPSAFE WHEEL

curl -L "$MARKUPSAFE_WHEEL_X86_URL" -O
curl -L "$MARKUPSAFE_WHEEL_ARM_URL" -O

x86_64_wheel=$(basename "$MARKUPSAFE_WHEEL_X86_URL")
arm64_wheel=$(basename "$MARKUPSAFE_WHEEL_ARM_URL")

delocate-merge "$x86_64_wheel" "$arm64_wheel" --wheel-dir macos/wheels

wheels=(macos/wheels/*.whl) 
for w in $wheels; do
  [[ $w == "$output_wheel" ]] && continue
  output_wheel=$w
done

{
  echo "${arm64_wheel:t}    $(shasum -a 256 "$arm64_wheel" | awk '{ print $1 }')"
  echo "${x86_64_wheel:t}    $(shasum -a 256 "$x86_64_wheel" | awk '{ print $1 }')"
  echo "${output_wheel:t}    $(shasum -a 256 "$output_wheel" | awk '{ print $1 }')"
  echo ""
} >> logs/macos.log

rm "$x86_64_wheel" "$arm64_wheel"