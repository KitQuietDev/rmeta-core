# rmeta-core

Shared metadata-scrubbing logic behind [rMeta](https://github.com/KitQuietDev/rMeta) (the Docker/web frontend) and [rMetaCLI](https://github.com/KitQuietDev/rMetaCLI) (the command-line frontend).

This is not a standalone tool — it's the handler/postprocessor/cleanup logic both frontends import so a fix or new file-type handler only has to be written once.

## What's in here

- `rmeta_core/handlers/` — one module per file type (PDF, DOCX, XLSX, HEIC, JPEG, TXT/CSV), auto-discovered by extension
- `rmeta_core/postprocessors/` — SHA256 hashing, GPG encryption
- `rmeta_core/utils/` — chunked/memory-aware processing, session cleanup (with secure overwrite-before-delete), PII scanning

## Installing

Not published to PyPI. Both frontends pin it via git URL in their `requirements.txt`:

```
rmeta-core @ git+https://github.com/KitQuietDev/rmeta-core.git@v0.1.0
```

## Adding a file handler

1. Add `rmeta_core/handlers/<type>_handler.py`.
2. Define `SUPPORTED_EXTENSIONS = {"ext1", "ext2"}` (lowercase) and a `scrub(file_path)` function.
3. `rmeta_core/handlers/__init__.py` auto-discovers any `*_handler.py` module and registers it by extension — nothing else to wire up.

Both rMeta and rMetaCLI pick up new handlers automatically once they bump their pinned `rmeta-core` version.

## Versioning

Tag a release (`vX.Y.Z`) when core changes; bump the pin in each frontend's `requirements.txt` to pick it up. There's no compatibility guarantee across versions yet — check both frontends still work before tagging a breaking change.

## License

MIT.
