# Enchanted Wilds Codex — data pipeline

Rebuilds the TFT Set 18 "Enchanted Wilds Codex" artifact from live MetaTFT PBE data.
Runs daily as a cloud routine; all inputs are public HTTP (no secrets, no local files).

## Requires
- `python` 3.9+, `node` (for a JS syntax check), `curl`

## Files
- `run_refresh.sh` — orchestrates a full cycle (pull → build data → QA gate → change check)
- `extract_full.py` — champions + traits + portraits (cached in `set18_full.json`)
- `enrich_meta.py` — PBE meta carry tiers, avg placement, best-in-slot item icons
- `extract_comps.py` — the 51 PBE comps (boards, traits, itemized carries)
- `qa.py` — QA gate: data-integrity + CSS contrast lint. Exit non-zero = block publish.
- `build_full.py` — renders `set18_full.json` into the self-contained `set18_explorer.html`
- `set18_full.json` — current data + cached images (baseline; avoids re-downloading daily)
- `last_fingerprint.txt` — change-detection baseline

## Daily flow (what the routine does)
1. `bash run_refresh.sh`
2. If it exits non-zero → QA failed → **do not republish**; report the failure.
3. If stdout ends with `REPUBLISH` → `python build_full.py`, `node --check`, then republish
   the artifact (`set18_explorer.html`) to the existing URL, and report what changed.
4. If stdout ends with `NOOP` → nothing changed; quiet no-op.
5. On a successful republish, commit `set18_full.json` + `last_fingerprint.txt` back so the
   next day diffs against today (best-effort; skip if the checkout is read-only).

## Manual run
```bash
bash run_refresh.sh && python build_full.py
```
