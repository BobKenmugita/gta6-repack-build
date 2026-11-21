# Repack manifest format

`repack.manifest.json` describes every file that should land in the GTA6
install directory when the launcher runs `install.run`.

```json
{
  "entries": [
    { "src": "update/update.rpf", "dst": "update/update.rpf", "kind": "rpf",
      "size": 1048576, "sha256": "…" }
  ]
}
```

Fields:

- `src` — path relative to the repack staging folder
- `dst` — path relative to the game install directory
- `kind` — `file`, `rpf`, or `dlc`
- `size` — bytes, used for progress reporting
- `sha256` — used by `verify.check`