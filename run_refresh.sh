#!/usr/bin/env bash
# Enchanted Wilds Codex — daily refresh runner (cloud-safe).
# Pulls fresh MetaTFT PBE data, rebuilds, and runs the QA gate.
# Exit 0 + "REPUBLISH" on stdout  -> data changed & QA clean: the agent should
#   run `python build_full.py`, `node --check`, and republish the artifact.
# Exit 0 + "NOOP"                 -> QA clean, no data change: do nothing.
# Exit 1                          -> QA gate failed: DO NOT republish; report.
set -euo pipefail
cd "$(dirname "$0")"

UA="Mozilla/5.0"
curl -s -A "$UA" -o metatft_set18.json "https://data.metatft.com/lookups/TFTSet18_pbe_en_us.json"
curl -s -A "$UA" -H "Referer: https://www.metatft.com/" -o mt_comps_data.json  "https://api-hc.metatft.com/tft-comps-api/comps_data?queue=PBE"
curl -s -A "$UA" -H "Referer: https://www.metatft.com/" -o mt_comps_stats.json "https://api-hc.metatft.com/tft-comps-api/comps_stats?queue=PBE&patch=current&days=3&permit_filter_adjustment=true"

python extract_full.py
python enrich_meta.py
python extract_comps.py

# QA gate — non-zero aborts the run before any publish
python qa.py

# change detection vs committed baseline fingerprint
python - <<'PY'
import hashlib, json, os
def sig(f):
    d=json.load(open(f,encoding='utf-8'))
    if 'units' in d:
        key=json.dumps([(u.get('apiName'),u.get('ability',{}).get('desc'),u.get('stats')) for u in d['units']],sort_keys=True)
    else:
        key=json.dumps(d.get('results',{}).get('data',{}).get('cluster_details',{}),sort_keys=True)[:200000]
    return hashlib.sha256(key.encode()).hexdigest()[:16]
fp=sig('metatft_set18.json')+'-'+sig('mt_comps_data.json')
prev=open('last_fingerprint.txt').read().strip() if os.path.exists('last_fingerprint.txt') else ''
open('last_fingerprint.txt','w').write(fp)
print('REPUBLISH' if fp!=prev else 'NOOP')
PY
