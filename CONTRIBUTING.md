# Contributing

Please open an issue for changes to the Python examples or documentation.
Include reproducible steps and a sanitized input; omit credentials and personal
contact data. Keep changes focused and include tests for behavior changes.

Run `python -m pytest -q` and `python -m ruff check examples tests` before a
pull request. Tests use local fixtures and mocked clients, without paid runs.
