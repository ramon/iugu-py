Project purpose
- This repository provides a Python library (iugupy) to integrate with the IUGU API (https://iugu.com.br).
- Scope: offer a simple, typed HTTP client to access API resources (e.g., customers, invoices, charges), with token authentication, timeouts, controlled retries, and basic error mapping, using only `requests` as a runtime dependency.
- Non-goals: avoid global session state, complex CLIs, and heavy dependencies; keep the public surface small and stable.
- Quality and compatibility: static typing (py.typed), Python >= 3.13, tests with pytest, use `uv` for build/dependency management, and `black` for code style.
