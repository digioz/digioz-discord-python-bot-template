# Contributing

Thank you for considering contributing to this repository. The goal of this document is to provide guidance for contributing code, tests, and documentation.

## Code style
- Use `black` (88 columns) for formatting.
- Use `isort` for import sorting.
- Use `ruff` for linting.

## Commits and PRs
- Follow Conventional Commits (e.g., `feat: add new command`, `fix: handle db error`).
- Open a PR with a clear description and linking issues if applicable.
- Add tests for new behavior.

## Tests
- Use `pytest` and `pytest-asyncio` to write tests for async code.

## Database
- Use migrations for schema changes. For simple projects, add numbered SQL scripts under `infra/migrations/`.

## Secrets
- Do not commit secrets or tokens. Use environment variables or GitHub secrets.

## CI
- Pull requests should run linters and tests before merging.

## License
This project is licensed under the GNU GPLv3 (see `LICENSE`).
