1. Build and configuration
- Python version: The package targets Python >= 3.13 (see pyproject.toml). Use a 3.13 interpreter for development and testing.
- Build backend: uv_build is used as the PEP 517 backend. A uv.lock is present in the repo.
  - Build artifacts (wheel/sdist):
    - If you have uv installed: `uv build` (produces dist/*.whl and dist/*.tar.gz).
    - Using pip/PEP 517 tooling: `python -m pip wheel .` or `python -m build` will invoke the uv_build backend automatically (pip will install the backend in an isolated build env). This requires the `build` package if you use `python -m build`.
- Editable install for local development:
  - With uv: `uv venv && . .venv/bin/activate && uv pip install -e .`
  - With pip: create/activate a venv of Python 3.13, then `pip install -e .`
- Runtime dependencies: requests>=2.32.5 (managed via pyproject). No optional extras are defined at this time.
