"""Enchanted Wilds Codex — consolidated QA. Run: python qa.py
Reports data-integrity + static CSS contrast-risk issues. Exit 0 = clean."""
import json, re, sys

d=json.load(open('set18_full.json',encoding='utf-8'))
HTML=open('set18_explorer.html',encoding='utf-8').read() if __import__('os').path.exists('set18_explorer.html') else ''
issues=[]
add=lambda cat,*rest: issues.append((cat,)+rest)
def okimg(u): return isinstance(u,str) and u.startswith('data:image')

champByName={c['name']:c for c in d['champions']}
traitNames={t['name'] for t in d['traits']}
icons=d.get('itemIcons',{})

# ---- DATA: champions ----
for c in d['champions']:
    ab=c.get('ability',{})
    if not ab.get('name'): add('ABILITY_NO_NAME',c['name'])
    desc=ab.get('desc','')
    if not desc: add('ABILITY_EMPTY',c['name'])
    elif len(desc)<25: add('ABILITY_SHORT',c['name'],len(desc))
    if not okimg(c.get('portrait','')): add('NO_PORTRAIT',c['name'])
    if c['cost'] not in (1,2,3,4,5): add('BAD_COST',c['name'])
    for t in c['traits']:
        if t not in traitNames: add('CHAMP_TRAIT_MISSING',c['name'],t)
# ---- DATA: traits ----
for t in d['traits']:
    if not okimg(t.get('iconData','')): add('TRAIT_NO_ICON',t['name'])
    if t['cat'] not in ('Origin','Class','Unique','Hidden'): add('BAD_CAT',t['name'])
    dd=t.get('desc',{})
    if not dd.get('header') and not dd.get('rows'): add('TRAIT_DESC_EMPTY',t['name'])
# ---- DATA: comps ----
for cp in d.get('comps',[]):
    if not cp['units']: add('COMP_EMPTY',cp['name'])
    for u in cp['units']:
        if u['name'] not in champByName: add('COMP_UNIT_MISSING',cp['name'],u['name'])
    for t in cp['traits']:
        if t not in traitNames: add('COMP_TRAIT_MISSING',cp['name'],t)
    for cy in cp['carries']:
        for it in cy['items']:
            if it not in icons: add('COMP_ITEM_NO_ICON',cp['name'],it)
# ---- DATA: meta item icons ----
for c in d['champions']:
    mt=c.get('meta')
    if mt:
        for it in mt.get('items',[])+mt.get('build',[]):
            if it not in icons: add('META_ITEM_NO_ICON',c['name'],it)

# ---- KNOWN SOURCE GAPS (informational, not failures) ----
source_gaps=[]
for c in d['champions']:
    s=c.get('stats',{})
    if not s.get('hp') or not s.get('ad'): source_gaps.append(('PBE_MISSING_STAT',c['name']))
    if '?' in c.get('ability',{}).get('desc',''): source_gaps.append(('PBE_MISSING_ABILITY_VALUE',c['name']))

# ---- STATIC CSS: contrast-risk lint (themed bg w/o explicit color on text elements) ----
css=''
for mm in re.finditer(r'<style>(.*?)</style>', HTML, re.S): css+=mm.group(1)
# split into top-level rules (naive: on '}' at depth handled by media-block skip)
css_flat=re.sub(r'@media[^{]*\{','',css)  # drop media wrappers (tokens redefined there are fine)
for block in re.findall(r'([^{}]+)\{([^{}]+)\}', css_flat):
    sel,body=block[0].strip(),block[1]
    if 'background' not in body: continue
    if not re.search(r'background:\s*(var\(--(surface|bg)|#fff|#ffffff)',body): continue
    if 'color:' in body: continue
    # only care about elements that render user-facing text
    if re.search(r'\b(button|\.bitem|\.chip|\.tab|\.card|\.cc|\.pc|\.stat|input|select|textarea|\.tt|\.sb|\.pm)\b',sel):
        add('CONTRAST_RISK', sel.replace('\n',' ')[:60])

from collections import Counter
crit=[i for i in issues]
print('=== QA REPORT ===')
print('Blocking issues: %d'%len(crit))
for k,c in Counter(i[0] for i in crit).most_common(): print('  %-22s %d'%(k,c))
for i in crit[:40]: print('   ',i)
print('\nKnown PBE source gaps (informational, render gracefully): %d'%len(source_gaps))
for k,c in Counter(x[0] for x in source_gaps).most_common(): print('  %-28s %d'%(k,c))
sys.exit(1 if crit else 0)
