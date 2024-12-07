# Build tools for macOS

These are needed because fat (multi-arch) binaries are needed to create a universal macOS
binary.

- Standard library modules are created from an x84_64 binary and an arm64 binary.

```bash
lipo -create first.so second.so -output combined.so
```

- The lz4 wheel was created using delocate.

```bash
delocate-merge first.whl second.whl
```

- Numpy wheels cannot be merged by delocate at the moment, so I merged them manually.
