# Repository Guidelines

## Project Structure & Module Organization
The CLI entry point lives in `cli.py`, orchestrating device reads, normalization, and uploads. Core logic is split across `core/`: `iclock_connector.py` handles device I/O, `normalizer.py` standardizes SDK payloads, `firestore_uploader.py` writes to Firestore, and `utils.py` maintains caching and interval management. Configuration and secrets belong in `config/`—update `settings.py` and keep `firebase-key.json` local. Cached IDs persist in `cache/uploaded_ids_cache.json`, while example payloads sit in `data/`. Runtime artifacts (log files, exported JSON) are created automatically in `logs/` and `output/`; add new documentation under `docs/`.

## Build, Test, and Development Commands
Create a virtual environment with `python -m venv .venv` and activate it before installing dependencies. Use `pip install -r requirements.txt` for reproducible environments, then `pip install -e .` to register the `iclock` CLI during development. Run a dry sync via `iclock --dry-run` to exercise the full pipeline without writing to Firestore. To inspect payloads locally, run `python -m cli --export-normalized` or `--export-simple`, which writes exports into `output/`.

## Coding Style & Naming Conventions
Follow PEP 8 with four-space indentation, imports grouped standard→third-party→local, and module-level docstrings (see existing `core/*.py` files). Use snake_case for functions and variables, PascalCase for classes like `SmartTiming`, and keep type hints on public functions when return shapes matter. Prefer descriptive logging and avoid printing secrets; add concise comments only for non-obvious logic transitions.

## Testing Guidelines
An automated suite is not yet present. Add new tests under `tests/` using `pytest` once introduced, naming files `test_<module>.py` and mirroring structures in `core/`. When adding features, validate them with `iclock --dry-run` plus targeted export commands, and inspect the freshly generated files in `output/` to confirm schema assumptions. Supply synthetic fixtures from `data/sample_logs.txt` when writing integration checks.

## Commit & Pull Request Guidelines
Commits should read as short, imperative summaries (e.g., “Update clone URL”, “Implement SmartTiming interval controls”) and focus on a single logical change. Reference issue IDs where relevant, keep bodies wrapped at 72 characters, and include rationale for risky behaviour changes. Pull requests need a clear summary, manual-test notes (e.g., dry-run commands executed), and screenshots or log excerpts when Firestore behaviour changes. Request review whenever modifying device or credential handling.

## Configuration & Security Tips
Never commit real credentials—use `.env` to supply `DEVICE_IPS`, `DEVICE_NAMES`, and `FIREBASE_KEY`, leaving `config/firebase-key.json` out of version control. When sharing configs, strip device IPs or replace them with `192.0.2.x` placeholders. Document any new environment variables in `config/settings.py` docstrings and update the README if user-visible behaviour changes.
