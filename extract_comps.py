import json, re, urllib.request, base64, ssl
ctx=ssl.create_default_context(); ctx.check_hostname=False; ctx.verify_mode=ssl.CERT_NONE

m=json.load(open('metatft_set18.json',encoding='utf-8'))
full=json.load(open('set18_full.json',encoding='utf-8'))
raw=json.load(open('mt_comps_data.json',encoding='utf-8'))['results']['data']['cluster_details']
stats={s.get('cluster'):s.get('count') for s in json.load(open('mt_comps_stats.json',encoding='utf-8'))['results'] if s.get('cluster')}

amap={}
for u in m['units']:
    for a in (u.get('assetNames') or []): amap[a]={'name':u['name'],'cost':u['cost']}
    amap[u['apiName']]={'name':u['name'],'cost':u['cost']}
traitApi={t['apiName']:t['name'] for t in m['traits']}
iname={x['apiName']:x['name'] for x in m['items']}
iapi={x['name']:x['apiName'] for x in m['items']}
portrait={c['name']:c.get('portrait') for c in full['champions']}
ticon={t['name']:t.get('iconData') for t in full['traits']}
icons=full.get('itemIcons',{})

def strip_tier(tok): return re.sub(r'_\d+$','',tok.strip())

comps=[]; needicons=set()
for cid,c in raw.items():
    units=[]
    starset=set(c.get('stars') or [])
    carryset={b['unit'] for b in c.get('builds',[]) if b.get('num_items',0)>=2}
    for tok in [t.strip() for t in c.get('units_string','').split(',') if t.strip()]:
        info=amap.get(tok)
        if not info: continue
        units.append({'name':info['name'],'cost':info['cost'],
                      'star3':tok in starset,'carry':tok in carryset})
    traits=[]
    for tok in [t.strip() for t in c.get('traits_string','').split(',') if t.strip()]:
        nm=traitApi.get(strip_tier(tok))
        if nm: traits.append(nm)
    carries=[]
    for b in sorted(c.get('builds',[]),key=lambda b:-(b.get('count',0) or 0)):
        if b.get('num_items',0)<2: continue
        info=amap.get(b['unit'])
        if not info: continue
        its=[iname.get(x,x) for x in (b.get('buildName') or []) if isinstance(x,str)]
        for it in its: needicons.add(it)
        carries.append({'name':info['name'],'cost':info['cost'],'avg':round(b.get('avg',0),2),'items':its})
    # display name from name_string
    us=[]; ts=[]
    for tok in [t.strip() for t in c.get('name_string','').split(',') if t.strip()]:
        if tok in amap: us.append(amap[tok]['name'])
        elif strip_tier(tok) in traitApi: ts.append(traitApi[strip_tier(tok)])
        elif tok in traitApi: ts.append(traitApi[tok])
    disp=' '.join(us+ts) or 'Flexible'
    ov=c.get('overall') or {}
    comps.append({'name':disp,'level':c.get('levelling',''),
                  'games':stats.get(str(cid)) or ov.get('count') or 0,
                  'avg':round(ov.get('avg',0),2),'units':units,'traits':traits,'carries':carries})

# fetch any missing item icons
def ficon(name):
    api=iapi.get(name)
    if not api: return None
    url=f'https://cdn.metatft.com/cdn-cgi/image/width=56,height=56,format=webp,quality=85/https://cdn.metatft.com/file/metatft/items/{api.lower()}.png'
    try:
        d=urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'}),timeout=20,context=ctx).read()
        if len(d)>200: return 'data:image/webp;base64,'+base64.b64encode(d).decode()
    except Exception: pass
    return None
added=0
for it in needicons:
    if it not in icons:
        ic=ficon(it)
        if ic: icons[it]=ic; added+=1

comps.sort(key=lambda x:-x['games'])
full['itemIcons']=icons
full['comps']=comps
try:
    full['source']=open('data_source.txt',encoding='utf-8').read().strip() or 'PBE'
except Exception:
    full['source']='PBE'
json.dump(full,open('set18_full.json','w',encoding='utf-8'),ensure_ascii=False)
import os
print('comps:',len(comps),'| new item icons:',added,'| total icons:',len(icons))
print('size MB:',round(os.path.getsize('set18_full.json')/1048576,2))
for c in comps[:6]:
    print('  %6dg %.2f %-6s %-22s units:%d carries:%s'%(c['games'],c['avg'],c['level'],c['name'],len(c['units']),[x['name'] for x in c['carries']]))
