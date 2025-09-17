4. Common local workflows
- Quick local run (no install): `PYTHONPATH=src python -c "import iugupy; c=iugupy.IuguClient(iugupy.IuguConfig(api_token='TOKEN', client_id='CLIENT')); print(c.base_url)"`
- Editable install + interactive dev: create a venv (3.13) with uv and install with dev extras: `uv venv && . .venv/bin/activate && uv pip install -e .[dev]`
- Run tests: `pytest`
- Format code: `black .`
- Build wheel for distribution: `uv build` (or `python -m pip wheel .`).
