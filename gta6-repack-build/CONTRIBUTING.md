# Contributing to gta6-repack-build

Thanks for helping out. This repo is the desktop launcher + repack tooling
for GTA6 mod packs. Everything lives under `src/` — no build step beyond
`pip install -r requirements.txt`.

## Ground rules

- Keep handlers thin. Real logic belongs in `src/repack_services/`.
- Platform-specific code goes in `src/platform/` — never leak Windows
  paths into the services.
- New manifest kinds must be added to `ManifestEntry` and
  `InstallPipeline._apply` together.
- Tests live in `tests/` and run with `pytest -q`.

## Pull requests

1. Fork, branch from `main`.
2. Add or update a test in `tests/`.
3. Run `pytest -q` and `python -m src.main.repack_launcher --selftest`.
4. Describe what changed in the manifest format, if anything.

Questions about RPF internals are best asked in the `docs/rpf-notes.md`
threads before opening a PR.