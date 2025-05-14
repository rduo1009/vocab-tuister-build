# Build resources for macOS

These are needed because fat (multi-arch) binaries are needed to create a universal macOS
binary.

- The standard library modules and some dynamic libraries are taken from the Python installer pkg.

- The remaining dynamic libraries are created from an x84_64 binary and an arm64 binary (installed by homebrew).

```bash
lipo -create first.dylib second.dylib -output combined.dylib
```

- The numpy wheels are created using delocate.

```bash
delocate-merge first.whl second.whl
```

Despite this, the error
`58160 WARNING: Ignoring non-existent resource src/_build/macos/dylib/libncursesw.6.dylib, meant to be collected as libncursesw.6.dylib`
occurs, but this doesn't cause any issues for some reason.
