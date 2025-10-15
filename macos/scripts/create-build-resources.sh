#!/bin/zsh

if [[ "$OSTYPE" != "darwin"* ]]; then
    echo "This script should only be run on macOS (got $OSTYPE)"
    exit 1
fi

set -e

export $(cat macos/.env | xargs)

rm -rf logs macos/dylib macos/stdlib macos/wheels
mkdir -p logs macos/dylib macos/stdlib macos/wheels

curl -L "$PYTHON_PKG_UNIVERSAL_URL" -o python-pkg.pkg
pkgutil --expand python-pkg.pkg python-expanded-pkg

mkdir -p python-pkg-framework
(cd python-pkg-framework && gunzip -c ../python-expanded-pkg/Python_Framework.pkg/Payload | cpio -idum)

./macos/scripts/create_stdlib_mac.py
./macos/scripts/create_dylib_mac.py
./macos/scripts/create-wheels-mac.sh

rm -rf python-expanded-pkg python-pkg-framework *.pkg