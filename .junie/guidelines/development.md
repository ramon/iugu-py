3. Additional development information
- Package layout: src/ layout (`src/iugupy`). Import as `import iugupy` after ensuring `src/` is on path for local runs.
- Public API and typing: The package ships a `py.typed` marker indicating it provides type hints at runtime. Maintain strict type annotations for new public APIs. If you add modules, ensure the `py.typed` file remains at `src/iugupy/py.typed` and is included in sdists/wheels (uv_build respects package data from src by default). Consider running a type checker (mypy or pyright) locally, but there is no pinned config in the repo yet.
- Code style: Use `black` as the default formatter. Configuration (line-length, target-version) is in `pyproject.toml`. Keep imports and dependencies lean; the runtime footprint should remain minimal.
- HTTP layer: requests is the only runtime dependency. When adding API clients, centralize HTTP concerns (timeouts, retries, error mapping) and avoid leaking requests.Session state across modules. Consider providing a thin client class that accepts auth/token/timeout in the constructor.
- Versioning: Project version is set in pyproject.toml. If you need dynamic versioning, coordinate changes to avoid duplication between code and metadata.
- CI considerations: If adding CI, include Python 3.13 and run `pytest -q`.
