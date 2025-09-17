# IUGU Python SDK

Library to integrate with the IUGU API.

## Development

This project targets Python >= 3.13 and uses `uv` as the build backend/manager.

### Setup (with uv)

- Create a virtualenv and activate it:
  - `uv venv`
  - `. .venv/bin/activate`
- Install in editable mode with dev tools (pytest, black):
  - `uv pip install -e .[dev]`

### Running tests (pytest)

- Run all tests:
  - `pytest`
- Tests live under `tests/` and follow the pattern `test_*.py`.
- Imports resolve either via the editable install above or the provided `tests/conftest.py` which adds `src/` to `sys.path` for local runs.

### Code style (black)

- Format the codebase:
  - `black .`
- The configuration (line length, Python version) is in `pyproject.toml`.

### Build artifacts

- Build wheel/sdist using uv build backend:
  - `uv build`

### Contribution policy

- Every new feature or bugfix must include corresponding tests in `tests/`.
- Keep runtime dependencies minimal (the library depends only on `requests`).
- Public API should be typed; `py.typed` is included.