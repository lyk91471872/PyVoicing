# Repository Guidelines

## Project Structure & Module Organization
- Source code lives in `src/pyvoicing/` with core modules like `pitch.py`, `chroma.py`, `interval.py`, and `voicing.py`.
- Package metadata and tooling config are in `pyproject.toml`.
- Documentation is primarily `README.md`; release notes are in `CHANGELOG.md`.
- There is no `tests/` directory yet; add one if introducing tests.

## Build, Test, and Development Commands
- `pip install -e .` installs the library in editable mode for local development.
- `python -m build` produces sdist/wheel artifacts using the configured build backend.
- `python -m black src` formats code to the project’s style.
- `python -m isort src` sorts imports to match Black’s profile.
- `python -m mypy src` runs type checks (strict typing is enabled).

## Coding Style & Naming Conventions
- Use 4-space indentation and keep lines within 88 characters (Black defaults).
- Follow standard Python naming: `CapWords` for classes, `snake_case` for functions/variables, `UPPER_SNAKE_CASE` for constants.
- Prefer explicit, typed APIs; `mypy` is configured with `disallow_untyped_defs`.
- Avoid adding dependencies unless they are essential and lightweight.
- For most derived attributes (e.g., `abc`, `csv`), use `@property` with an `@xxx.setter` for a pythonic getter/setter pair.
- Use `Pitch.freq` as a read-only `@property` (no setter).
- Keep operator overloads numeric-like and consistent; prefer named methods for collection or analysis behavior.

## Testing Guidelines
- No testing framework is configured. If you add tests, use `pytest` and place files under `tests/` with names like `test_pitch.py`.
- Keep tests fast and deterministic; include regression tests for bug fixes.

## Commit & Pull Request Guidelines
- Commit subjects in history are short, lowercase, and descriptive (e.g., “fixed abc parsing for pitch”).
- Keep commits scoped to one change; update `CHANGELOG.md` if behavior changes.
- PRs should include a clear description, rationale, and usage example when APIs change.

## Agent-Specific Notes
- Keep utilities generic; avoid coupling to CLAMiP schemas or paths.
- When adding pitch helpers, ensure notation output reflects explicit enharmonic spelling.
