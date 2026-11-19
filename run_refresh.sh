#!/usr/bin/env bash
# Codex daily refresh runner (cloud-safe). Set is configured in config.py.
# Pulls fresh MetaTFT data, rebuilds, and runs the QA gate.
# Exit 0 + "REPUBLISH" -> data changed & QA clean: build_full.py + republish.
# Exit 0 + "NOOP"      -> QA clean, no data change: do nothing.
# Exit 1               -> QA gate failed: DO NOT republish; report.
set -euo pipefail
cd "$(dirname "$0")"

UA="Mozilla/5.0"; REF="Referer: https://www.metatft.com/"
COMPS="https://api-hc.metatft.com/tft-comps-api"
SET=$(python -c "import config;print(config.SET)")
TFT_SET="TFTSet${SET}"
DUMP="metatft_set${SET}.json"

# Champion/trait/item data: prefer the `latest` (live) branch; pre-launch it may
# be absent or mirror PBE, so fall back to the `_pbe` branch.
if ! curl -sf -A "$UA" -o "$DUMP" "https://data.metatft.com/lookups/${TFT_SET}_latest_en_us.json"; then
  curl -s  -A "$UA" -o "$DUMP" "https://data.metatft.com/lookups/${TFT_SET}_pbe_en_us.json"
fi
# If latest came back but isn't the target set yet (rare pre-launch), use pbe.
got=$(python -c "import json;print(json.load(open('$DUMP',encoding='utf-8')).get('setNumber',''))" 2>/dev/null || true)

# Comps: prefer live Ranked (queue 1100) once it actually serves this set.
# Before launch that queue returns the previous set, so fall back to PBE.
live_set=$(curl -s -A "$UA" -H "$REF" "$COMPS/comps_data?queue=1100" \
  | python -c "import sys,json;print(json.load(sys.stdin).get('results',{}).get('data',{}).get('tft_set',''))" 2>/dev/null || true)
if [ "$live_set" = "$TFT_SET" ]; then Q=1100; SRC="Live"; else Q=PBE; SRC="PBE"; fi
echo "set=$TFT_SET | comps source: queue=$Q ($SRC)"
printf '%s' "$SRC" > data_source.txt

curl -s -A "$UA" -H "$REF" -o mt_comps_data.json  "$COMPS/comps_data?queue=$Q"
curl -s -A "$UA" -H "$REF" -o mt_comps_stats.json "$COMPS/comps_stats?queue=$Q&patch=current&days=3&permit_filter_adjustment=true"

python extract_full.py
python enrich_meta.py
python extract_comps.py

# QA gate — non-zero aborts the run before any publish
python qa.py

# change detection vs committed baseline fingerprint
python - "$DUMP" <<'PY'
import hashlib, json, os, sys
dump=sys.argv[1]
def sig(f):
    d=json.load(open(f,encoding='utf-8'))
    if 'units' in d:
        key=json.dumps([(u.get('apiName'),u.get('ability',{}).get('desc'),u.get('stats')) for u in d['units']],sort_keys=True)
    else:
        key=json.dumps(d.get('results',{}).get('data',{}).get('cluster_details',{}),sort_keys=True)[:200000]
    return hashlib.sha256(key.encode()).hexdigest()[:16]
fp=sig(dump)+'-'+sig('mt_comps_data.json')
prev=open('last_fingerprint.txt').read().strip() if os.path.exists('last_fingerprint.txt') else ''
open('last_fingerprint.txt','w').write(fp)
print('REPUBLISH' if fp!=prev else 'NOOP')
PY
