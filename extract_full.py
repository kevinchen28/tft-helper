import json, re, html, urllib.request, base64, ssl

ctx = ssl.create_default_context(); ctx.check_hostname=False; ctx.verify_mode=ssl.CERT_NONE
M = json.load(open('metatft_set18.json', encoding='utf-8'))
# trait icons are cached in the committed set18_full.json (all 36 are stable for the set)
try:
    _prev_icons = json.load(open('set18_full.json', encoding='utf-8'))
    trait_icon = {t['name']: t.get('iconData') for t in _prev_icons.get('traits', []) if t.get('iconData')}
except Exception:
    trait_icon = {}
roles = M['roles']

STYLE = {1:'bronze', 3:'silver', 4:'gold', 5:'prismatic', 6:'unique'}

def fmt(v, mode=None):
    if mode=='percent': return f'{round(v*100)}%'
    if mode=='invertedPercent': return f'{round((1-v)*100)}%'
    if mode=='percentMinusOne': return f'{round((v-1)*100)}%'
    if isinstance(v,(int,float)) and abs(v-round(v))<1e-6: return str(int(round(v)))
    return str(round(v,2))

def mode_of(tag):
    if 'percentMinusOne' in tag: return 'percentMinusOne'
    if 'invertedPercent' in tag: return 'invertedPercent'
    if 'format="percent"' in tag: return 'percent'
    return None

def join_vals(vals, mode=None):
    seq = vals[:3] if len(vals) >= 3 else vals
    parts = [fmt(v,mode) for v in seq]
    return parts[0] if len(set(parts))==1 else '/'.join(parts)

def resolve(desc, attrVals=None, curve=None):
    # Robust MetaTFT ability/trait text resolver. Key rules that prevent whole
    # descriptions from vanishing: decorative <TFTAttribute> (no attributeID) -> '';
    # curve rows matched case-insensitively; unresolved values kept inline as '?'
    # (never drop a whole line for it); only genuine "Current …: ?" readouts dropped.
    attrVals = attrVals or {}; curve = curve or {}
    curl = {k.lower(): v for k, v in curve.items()}
    def attr_rep(m):
        tag=m.group(0); aid=re.search(r'attributeID="([^"]+)"',tag)
        if not aid: return ''                       # decorative icon, not a value
        vals=attrVals.get(aid.group(1))
        return join_vals(vals,mode_of(tag)) if vals else '?'
    def curve_rep(m):
        tag=m.group(0); row=re.search(r'row="([^"]+)"',tag).group(1)
        ct=curve.get(row) or curl.get(row.lower())  # case-insensitive
        if not ct: return '?'
        vals=[p[1] for p in ct] if isinstance(ct[0],(list,tuple)) else ct
        return join_vals(vals,mode_of(tag))
    s=desc or ''
    s=re.sub(r'%i:[A-Za-z0-9]+%','',s)
    s=re.sub(r'<TFTAttribute[^>]*/>', attr_rep, s)
    s=re.sub(r'<TFTCurveTable[^>]*/>', curve_rep, s)
    s=re.sub(r'<[^>]+>', '', s)          # strip remaining tags incl <Bright> <dim> </>
    s=re.sub(r'\{[^}]*\}', '', s)         # strip {Set18...} tokens
    s=html.unescape(s)
    s=re.sub(r'[ \t]+',' ', s)
    s=re.sub(r' *\n *','\n', s)
    s='\n'.join(ln for ln in s.split('\n') if not (re.match(r'\s*current\b',ln,re.I) and '?' in ln))
    s=re.sub(r'\s+([%,.;:])',r'\1', s)
    s=re.sub(r'\n{3,}','\n\n', s)
    return s.strip()

apiname = {u['apiName']: u.get('name') for u in M['units']}

# ---- traits ----
traits=[]
for t in M['traits']:
    name=t['name']
    cat = 'Hidden' if name=='Eclipse' else t.get('type','origin').capitalize()
    curve=t.get('curveTable',{})
    bps=[{'min':e['minUnits'],'style':STYLE.get(e.get('style'),'bronze')} for e in t.get('effects',[]) if e.get('minUnits') is not None]
    rows=[]
    for e in t.get('effects',[]):
        r=resolve(e.get('desc',''), {}, curve)
        r=re.sub(r'^\(\s*\d+\s*\)\s*','',r)
        if re.search(r'[A-Za-z]{3,}', r): rows.append(r)
    # header: lead of main desc before first breakpoint marker
    head=resolve(re.split(r'\(@?\d', t.get('desc') or '')[0], {}, curve)
    head=re.sub(r'<[^>]+>','',head).strip()
    units=sorted({apiname.get(x['unit'], x['unit'].replace('TFT18_','')) : x['unit_cost'] for x in t.get('units',[])}.items(), key=lambda kv:(kv[1],kv[0]))
    traits.append({'name':name,'cat':cat,'breakpoints':bps,
                   'desc':{'header':head,'rows':rows},
                   'units':[{'name':n,'cost':c} for n,c in units],
                   'iconData':trait_icon.get(name)})

# ---- champions ----
def parse_role(role):
    r=role.replace('DA_Role_','')
    dmg = 'AD' if r.startswith('Attack') else 'AP' if r.startswith('Magic') else 'Hybrid'
    arch = re.sub(r'^(Attack|Magic|Hybrid)','',r)
    arch = arch.split('_')[0]
    tank = 'Tank' in r
    return dmg, arch, tank

seen=set(); champs=[]
for u in M['units']:
    if str(u.get('cost')) not in ('1','2','3','4','5') or not u.get('traits'): continue
    if u['name'] in seen: continue
    seen.add(u['name'])
    dmg,arch,tank = parse_role(u.get('role',''))
    st=u.get('stats',{})
    ab=u.get('ability',{})
    champs.append({
        'name':u['name'], 'apiName':u['apiName'], 'cost':u['cost'],
        'traits':u['traits'], 'dmg':dmg, 'arch':arch,
        'role':roles.get(u.get('role',''),arch), 'carry':(not tank),
        'stats':{'hp':st.get('hp'),'ad':st.get('damage'),'as':st.get('attackSpeed'),
                 'range':st.get('range'),'mana':f"{st.get('initialMana',0)}/{st.get('mana',0)}",
                 'hpByStar':st.get('hpByStar'),'adByStar':st.get('damageByStar')},
        'ability':{'name':ab.get('name'),
                   'desc':resolve(ab.get('desc',''), ab.get('attributeValues',{}), u.get('curveTable',{}))},
    })

# ---- fetch portraits ----
def fetch(api):
    fn=api.lower()
    base=f'https://cdn.metatft.com/file/metatft/championsplashes/{fn}.png'
    url=f'https://cdn.metatft.com/cdn-cgi/image/width=240,height=142,fit=cover,format=webp,quality=82/{base}'
    try:
        req=urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'})
        data=urllib.request.urlopen(req,timeout=25,context=ctx).read()
        if len(data)>300 and data[:4]!=b'<!DO':
            mime='image/webp' if data[:4]==b'RIFF' else 'image/png'
            return f'data:{mime};base64,'+base64.b64encode(data).decode()
    except Exception: pass
    return None

# reuse cached images across runs so loop cycles don't re-download everything
prevP={}; prevIcons={}
try:
    _p=json.load(open('set18_full.json',encoding='utf-8'))
    prevP={x['name']:x.get('portrait') for x in _p.get('champions',[]) if x.get('portrait')}
    prevIcons=_p.get('itemIcons',{})
except Exception: pass

ok=0; cached=0; fail=[]
for c in champs:
    img=prevP.get(c['name'])
    if img: cached+=1
    else: img=fetch(c['apiName'])
    if img: c['portrait']=img; ok+=1
    else: fail.append(c['name'])

out={'setName':'Enchanted Wilds','setNumber':18,
     'traits':sorted(traits,key=lambda t:({'Origin':0,'Class':1,'Unique':2,'Hidden':3}[t['cat']],t['name'])),
     'champions':sorted(champs,key=lambda c:(c['cost'],c['name'])),
     'itemIcons':prevIcons}   # carried forward; enrich_meta/extract_comps top up
json.dump(out,open('set18_full.json','w',encoding='utf-8'),ensure_ascii=False)
import os
print(f'champions:{len(champs)} traits:{len(traits)} portraits:{ok}/{len(champs)} (cached {cached}) fail:{fail}')
print('size MB:', round(os.path.getsize('set18_full.json')/1048576,2))
# sample resolved ability
dv=[c for c in champs if c['name']=='Veigar'][0]
print('--- Veigar:',dv['ability']['name']); print(dv['ability']['desc'][:300])
el=[t for t in traits if t['name']=='Elderwood'][0]
print('--- Elderwood rows:'); [print('  ',r) for r in el['desc']['rows']]
