# Security policy

## Supported versions

| Version | Supported |
|---------|-----------|
| 0.4.x   | yes       |
| < 0.4   | no        |

## Reporting a vulnerability

Email `security@example.invalid` with a description and, if possible, a
minimal reproduction. Please do **not** open a public issue for anything
that could cause a repack to overwrite unintended files or bypass the
manifest signature check.

## Scope

In scope:
- The IPC socket in `src/main/ipc/repack_channel.py` (auth, path traversal)
- `WinFsAdapter` long-path handling
- Manifest signature verification

Out of scope:
- RPF format bugs in third-party tools (report upstream)
- Anything that requires the user to run our launcher as admin

## Disclaimer

This project is an educational / hobbyist repack tool. Use it at your own
risk. Do not redistribute game assets you do not own.