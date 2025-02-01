# Build tools for macOS

These are needed because fat (multi-arch) binaries are needed to create a universal macOS
binary.

- Standard library modules and dynamic libraries are created from an x84_64 binary and an arm64 binary.

```bash
lipo -create first.so second.so -output combined.so
lipo -create first.dylib second.dylib -output combined.dylib
```

- The lz4 and numpy wheels were created using delocate.

```bash
delocate-merge first.whl second.whl
```