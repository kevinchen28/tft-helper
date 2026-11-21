"""Build the rich dataset for the early-game opener finder page (set-driven via config)."""
import json, itertools
from collections import defaultdict
import config

d = json.load(open(config.DATA, encoding='utf-8'))
champs = {c['name']: c for c in d['champions']}
traits = {t['name']: t for t in d['traits']}

def bps(tn):
    return [b.get('min') for b in traits.get(tn, {}).get('breakpoints', []) if isinstance(b.get('min'), int)]
trait_unit_count = {tn: len(t.get('units', [])) for tn, t in traits.items()}
def is_signature(tn):
    return (bps(tn) == [1]) or trait_unit_count.get(tn, 0) <= 1
def ut(n): return champs[n]['traits']
def mavg(n):
    m = champs[n].get('meta') or {}; return m.get('avg')
def mtier(n):
    m = champs[n].get('meta') or {}; return m.get('tier')
def is_carry(n): return bool(champs[n].get('carry'))

pool = [c['name'] for c in d['champions'] if c['cost'] in (1, 2)]

def active_traits(board):
    cnt = defaultdict(int)
    for n in board:
        for t in ut(n): cnt[t] += 1
    out = {}
    for t, c in cnt.items():
        b = bps(t)
        if not b: continue
        reached = [i for i, m in enumerate(b) if c >= m]
        if reached: out[t] = (c, max(reached), b[max(reached)])
    return out

def score(board):
    act = active_traits(board)
    multi = {t: v for t, v in act.items() if not is_signature(t)}
    if len(multi) < 2: return None
    contrib = set()
    for t in multi:
        for n in board:
            if t in ut(n): contrib.add(n)
    coverage = len(contrib) / len(board)
    if coverage < 0.75: return None
    tscore = 0; tw = {}
    for t, (c, idx, mn) in multi.items():
        w = 10 + idx * 6 + min(c, 4); tw[t] = w; tscore += w
    tscore += 2 * sum(1 for t in act if is_signature(t))
    carries = [n for n in board if is_carry(n)]
    carry_bonus = 8 if carries else 0
    avgs = [mavg(n) for n in board if mavg(n) is not None]
    mq = (4.5 - sum(avgs)/len(avgs)) * 6 if avgs else 0
    cov_bonus = (coverage - 0.75) * 20
    total = tscore + carry_bonus + mq + cov_bonus
    primary = max(tw, key=lambda t: (tw[t], act[t][0]))
    return dict(score=round(total,1), coverage=round(coverage,2), act=act,
                multi=list(multi.keys()), primary=primary, carries=carries)

results = []
for size in (4, 5):
    for board in itertools.combinations(pool, size):
        sc = score(board)
        if sc:
            sc['board'] = list(board); sc['size'] = size
            results.append(sc)

# dedupe by (size, trait identity) keep best
best = {}
for r in results:
    k = (r['size'], tuple(sorted(r['multi'])))
    if k not in best or r['score'] > best[k]['score']:
        best[k] = r
ranked = sorted(best.values(), key=lambda r: -r['score'])

# assign a tier letter by score percentile within size
def letter(s, size):
    arr = sorted((r['score'] for r in ranked if r['size']==size), reverse=True)
    rank = arr.index(s) if s in arr else len(arr)
    p = rank/max(1,len(arr))
    return 'S' if p<0.08 else 'A' if p<0.25 else 'B' if p<0.55 else 'C'

# leads-into: for the primary trait, the higher-cost (3-5) carries/units it unlocks
def leads_into(trait):
    us = traits[trait].get('units', [])
    hi = [u for u in us if u.get('cost',0) >= 3]
    hi = sorted(hi, key=lambda u: u['cost'])
    out = []
    for u in hi[:5]:
        nm = u['name']; c = champs.get(nm)
        out.append(dict(name=nm, cost=u['cost'], carry=bool(c and c.get('carry'))))
    return out

# suggested carry for a board: best carry by meta avg (known), else first carry, else best unit
def suggest_carry(board, carries):
    cand = carries or board
    known = [n for n in cand if mavg(n) is not None]
    pick = min(known, key=lambda n: mavg(n)) if known else cand[0]
    m = champs[pick].get('meta') or {}
    items = (m.get('build') or m.get('items') or [])[:3]
    return dict(name=pick, items=items)

# build per-board payload; cap boards per primary trait for variety
PER_PRIMARY = 4
grouped = defaultdict(lambda: defaultdict(list))  # size -> primary -> list
for r in ranked:
    grouped[r['size']][r['primary']]
boards_out = []
used = defaultdict(lambda: defaultdict(int))
for r in ranked:
    if used[r['size']][r['primary']] >= PER_PRIMARY:
        continue
    used[r['size']][r['primary']] += 1
    units = []
    for n in r['board']:
        c = champs[n]
        units.append(dict(name=n, cost=c['cost'], traits=c['traits'],
                          carry=is_carry(n), tier=mtier(n), avg=mavg(n)))
    at = []
    for t,(cnt,idx,mn) in sorted(r['act'].items(), key=lambda kv:(-(not is_signature(kv[0])), -kv[1][1])):
        at.append(dict(name=t, count=cnt, bp=mn, bps=bps(t), sig=is_signature(t),
                       primary=(t==r['primary'])))
    boards_out.append(dict(
        id=f"{r['size']}-{'-'.join(sorted(r['multi']))}",
        size=r['size'], score=r['score'], tier=letter(r['score'], r['size']),
        primary=r['primary'], coverage=r['coverage'],
        units=units, traits=at,
        carry=suggest_carry(r['board'], r['carries']),
        leads=leads_into(r['primary']),
    ))

boards_out.sort(key=lambda b:(b['size'], -b['score']))

# collect images needed
needed_units = set()
for b in boards_out:
    for u in b['units']: needed_units.add(u['name'])
    for l in b['leads']: needed_units.add(l['name'])
    needed_units.add(b['carry']['name'])
portraits = {n: champs[n].get('portrait') for n in needed_units if champs.get(n) and champs[n].get('portrait')}
needed_traits = set()
for b in boards_out:
    for t in b['traits']: needed_traits.add(t['name'])
    needed_traits.add(b['primary'])
ticons = {t: traits[t].get('iconData') for t in needed_traits if traits.get(t) and traits[t].get('iconData')}
# trait descriptions (short) for tooltip
tdesc = {}
for t in needed_traits:
    h = (traits[t].get('desc') or {}).get('header') or ''
    tdesc[t] = h[:280]

out = dict(
    set=d.get('setNumber', 19), setName=d.get('setName','Prismatic Tour'),
    source=d.get('source',''),
    boards=boards_out, portraits=portraits, ticons=ticons, tdesc=tdesc,
    costColors={1:"#8a9a8d",2:"#3fae6a",3:"#2f8fd4",4:"#a06fe0",5:"#e0b23f",6:"#e07b53",7:"#e0556f"},
)
json.dump(out, open('openers_page.json','w'), separators=(',',':'))
print('boards:', len(boards_out),
      '| L4:', sum(1 for b in boards_out if b['size']==4),
      '| L5:', sum(1 for b in boards_out if b['size']==5))
print('distinct primary traits:', len(set(b['primary'] for b in boards_out)))
print('portraits embedded:', len(portraits), 'trait icons:', len(ticons))
import os; print('json size: %.2f MB' % (os.path.getsize('openers_page.json')/1e6))
print('\nprimary-trait spread (L5):')
from collections import Counter
cc=Counter(b['primary'] for b in boards_out if b['size']==5)
for t,n in cc.most_common(): print(' ',t,n)
