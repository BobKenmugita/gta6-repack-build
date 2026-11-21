# RPF import notes

The `rpf` kind entries are delegated to `rpf-cli.exe` (or the C# helper in
`src-native/rpf_helper` when the binary is not on PATH). Only the outer
archive container is touched — the inner block layout must remain
byte-identical or the game's streaming loader will reject the archive.

Known open-source tools that speak the same container format:
- OpenRPF (community fork)
- CodeWalker's RPF importer (CLI mode)

Do not try to repack `x64a.rpf` in place — always stage to a temporary
copy and swap at the end via `WinFsAdapter.copy_over`.