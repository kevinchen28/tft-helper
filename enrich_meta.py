import json, urllib.request, base64, ssl
from collections import defaultdict
ctx=ssl.create_default_context(); ctx.check_hostname=False; ctx.verify_mode=ssl.CERT_NONE

m=json.load(open('metatft_set18.json',encoding='utf-8'))
full=json.load(open('set18_full.json',encoding='utf-8'))
comps=json.load(open('mt_comps_data.json',encoding='utf-8'))['results']['data']['cluster_details']

amap={}
for u in m['units']:
    for a in (u.get('assetNames') or []): amap[a]={'name':u['name'],'cost':u['cost'],'role':u.get('role','')}
    amap[u['apiName']]={'name':u['name'],'cost':u['cost'],'role':u.get('role','')}
iname={x['apiName']:x['name'] for x in m['items']}
iapi={x['name']:x['apiName'] for x in m['items']}

carry=defaultdict(lambda:{'games':0,'wsum':0.0,'items':defaultdict(int),'builds':defaultdict(lambda:[0,0.0]),'cost':0,'tank':False})
for c in comps.values():
    for b in c.get('builds',[]):
        bn=[iname.get(x,x) for x in (b.get('buildName') or []) if isinstance(x,str)]
        if len(bn)<2: continue
        info=amap.get(b['unit'])
        if not info: continue
        cnt=b.get('count',0) or 0; avg=b.get('avg',0) or 0
        e=carry[info['name']]; e['games']+=cnt; e['wsum']+=avg*cnt; e['cost']=info['cost']; e['tank']='Tank' in info['role']
        for it in bn: e['items'][it]+=cnt
        k=tuple(bn); e['builds'][k][0]+=cnt; e['builds'][k][1]+=avg*cnt

# rank damage carries
dmg=sorted([(e['games'],nm) for nm,e in carry.items() if not e['tank'] and e['games']],reverse=True)
maxg=dmg[0][0] if dmg else 1
rank={nm:i+1 for i,(g,nm) in enumerate(dmg)}
def tier(g,tank):
    if tank: return 'T'
    return 'S' if g>=6000 else 'A' if g>=2500 else 'B' if g>=1200 else 'C'

meta={}
iconset=set()
for nm,e in carry.items():
    if not e['games']: continue
    ap=round(e['wsum']/e['games'],2)
    ti=[i for i,_ in sorted(e['items'].items(),key=lambda kv:-kv[1])[:3]]
    bb=list(max(e['builds'].items(),key=lambda kv:kv[1][0])[0])
    for i in set(ti)|set(bb): iconset.add(i)
    meta[nm]={'games':e['games'],'avg':ap,'tank':e['tank'],'tier':tier(e['games'],e['tank']),
              'score':round(e['games']/maxg*100),'rank':rank.get(nm),'items':ti,'build':bb}

# fetch item icons (resized)
def ficon(name):
    api=iapi.get(name);
    if not api: return None
    url=f'https://cdn.metatft.com/cdn-cgi/image/width=56,height=56,format=webp,quality=85/https://cdn.metatft.com/file/metatft/items/{api.lower()}.png'
    try:
        d=urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'}),timeout=20,context=ctx).read()
        if len(d)>200: return 'data:image/webp;base64,'+base64.b64encode(d).decode()
    except Exception: pass
    return None
icons={}
for nm in sorted(iconset):
    ic=ficon(nm)
    if ic: icons[nm]=ic

# merge into champions
hit=0
for c in full['champions']:
    mm=meta.get(c['name'])
    if mm: c['meta']=mm; hit+=1
full['itemIcons']=icons
json.dump(full,open('set18_full.json','w',encoding='utf-8'),ensure_ascii=False)
import os
print('champions with meta:',hit,'/',len(full['champions']),' item icons:',len(icons),'/',len(iconset))
print('size MB:',round(os.path.getsize('set18_full.json')/1048576,2))
print('S/A tier carries:',[ (nm,meta[nm]['tier'],meta[nm]['avg']) for nm in rank if meta[nm]['tier'] in ('S','A')][:12])
