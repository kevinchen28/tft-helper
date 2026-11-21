# -*- coding: utf-8 -*-
"""Assemble the self-contained opener-finder HTML page (set-driven via config)."""
import json, io
import config

DATA = open('openers_page.json', encoding='utf-8').read()  # already minified
d = json.loads(DATA)
setName = d['setName']

HEAD = '''<meta name="claude:viewport-fit-sides" content="cover">
<title>__SETNAME__ Openers</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;600;700&family=Inter:wght@400;500;600&display=swap">
<style>
/* Layout: sticky header with controls over a responsive card gallery of opener boards */
:root{
  --bg:#f4f5f8; --panel:#ffffff; --panel2:#eef0f5; --ink:#1a1c22; --muted:#5b6071;
  --line:#dfe2ea; --accent:#7c4dff; --accent2:#e0b23f; --good:#3fae6a;
  --ring:rgba(124,77,255,.22); --shadow:0 1px 2px rgba(20,22,34,.06),0 6px 18px rgba(20,22,34,.06);
  --c1:#8a9a8d;--c2:#3fae6a;--c3:#2f8fd4;--c4:#a06fe0;--c5:#e0b23f;--c6:#e07b53;--c7:#e0556f;
}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){
  --bg:#0f1017; --panel:#181a23; --panel2:#1f2230; --ink:#eceef5; --muted:#9aa0b4;
  --line:#2a2e3d; --accent:#a98bff; --accent2:#e6c05a; --good:#55c57f;
  --ring:rgba(169,139,255,.28); --shadow:0 1px 2px rgba(0,0,0,.4),0 8px 24px rgba(0,0,0,.35);
  color-scheme:dark;
}}
:root[data-theme="dark"]{
  --bg:#0f1017; --panel:#181a23; --panel2:#1f2230; --ink:#eceef5; --muted:#9aa0b4;
  --line:#2a2e3d; --accent:#a98bff; --accent2:#e6c05a; --good:#55c57f;
  --ring:rgba(169,139,255,.28); --shadow:0 1px 2px rgba(0,0,0,.4),0 8px 24px rgba(0,0,0,.35);
  color-scheme:dark;
}
*{box-sizing:border-box}
body{background:var(--bg);color:var(--ink);font-family:Inter,system-ui,sans-serif;line-height:1.45;margin:0}
h1,h2,h3,.dsp{font-family:"Space Grotesk",Inter,sans-serif}
.wrap{padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px))}
.shell{max-width:1240px;margin:0 auto}
body::before{content:"";position:fixed;inset:0 0 auto;height:env(safe-area-inset-top,0px);z-index:30;background:var(--panel)}

header.top{position:sticky;top:env(safe-area-inset-top,0px);z-index:20;background:var(--panel);
  border-bottom:1px solid var(--line);padding-block:14px}
.brand{display:flex;align-items:baseline;gap:10px;flex-wrap:wrap}
.brand h1{font-size:clamp(20px,3.4vw,27px);margin:0;letter-spacing:-.4px}
.brand .set{font-size:12px;font-weight:600;color:#fff;background:linear-gradient(90deg,var(--accent),var(--accent2));
  padding:3px 9px;border-radius:999px;letter-spacing:.3px}
.lede{color:var(--muted);font-size:13.5px;margin:7px 0 0;max-width:72ch}
.lede b{color:var(--ink);font-weight:600}

.controls{display:flex;gap:14px;flex-wrap:wrap;align-items:center;margin-top:13px}
.seg{display:inline-flex;background:var(--panel2);border:1px solid var(--line);border-radius:10px;padding:3px}
.seg button{font:inherit;font-weight:600;font-size:13px;border:0;background:transparent;color:var(--muted);
  padding:7px 13px;border-radius:7px;cursor:pointer;display:flex;align-items:center;gap:6px}
.seg button .u{font-size:11px;color:var(--muted);font-weight:500}
.seg button[aria-pressed="true"]{background:var(--panel);color:var(--ink);box-shadow:var(--shadow)}
.seg button[aria-pressed="true"] .u{color:var(--accent)}
.count{font-size:12.5px;color:var(--muted);margin-left:auto}
.count b{color:var(--ink)}
.usel{display:inline-flex;align-items:center;gap:7px;font-size:11px;color:var(--muted);font-weight:600;
  text-transform:uppercase;letter-spacing:.4px}
.usel select{font:inherit;font-weight:600;font-size:13px;letter-spacing:0;text-transform:none;color:var(--ink);
  background:var(--panel2);border:1px solid var(--line);border-radius:9px;padding:7px 10px;cursor:pointer;max-width:168px}
.usel select:focus-visible{outline:2px solid var(--accent);outline-offset:1px}

.filters{display:flex;gap:7px;flex-wrap:wrap;margin-top:12px}
.chip{font:inherit;font-size:12px;font-weight:600;border:1px solid var(--line);background:var(--panel);
  color:var(--muted);padding:5px 10px;border-radius:999px;cursor:pointer;display:inline-flex;align-items:center;gap:6px}
.chip img{width:14px;height:14px;filter:saturate(0) brightness(1.3);opacity:.8}
.chip[aria-pressed="true"]{background:var(--accent);border-color:var(--accent);color:#fff}
.chip[aria-pressed="true"] img{filter:brightness(0) invert(1);opacity:1}
.chip .n{font-weight:500;opacity:.7;font-size:11px}

main{padding-block:20px 48px}
.grid{display:grid;gap:14px;grid-template-columns:repeat(auto-fill,minmax(330px,1fr))}
.card{background:var(--panel);border:1px solid var(--line);border-radius:14px;box-shadow:var(--shadow);
  padding:14px;display:flex;flex-direction:column;gap:11px;min-width:0}
.chead{display:flex;align-items:center;gap:9px}
.tier{font-family:"Space Grotesk";font-weight:700;font-size:14px;width:26px;height:26px;border-radius:7px;
  display:grid;place-items:center;color:#fff;flex:none}
.tier.S{background:linear-gradient(135deg,#e0556f,#e0b23f)}.tier.A{background:#a06fe0}
.tier.B{background:#2f8fd4}.tier.C{background:#6b7180}
.ptitle{font-family:"Space Grotesk";font-weight:600;font-size:15px;display:flex;align-items:center;gap:6px;min-width:0}
.ptitle img{width:17px;height:17px;flex:none}
.ptitle span{white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.meter{margin-left:auto;flex:none;text-align:right}
.meter .bar{width:58px;height:6px;border-radius:3px;background:var(--panel2);overflow:hidden;margin-top:3px}
.meter .bar i{display:block;height:100%;background:linear-gradient(90deg,var(--accent),var(--accent2))}
.meter .lab{font-size:10px;color:var(--muted);letter-spacing:.3px;text-transform:uppercase}

.units{display:flex;gap:7px;flex-wrap:wrap}
.unit{width:60px;text-align:center;position:relative;cursor:pointer}
.unit .pf{transition:border-color .1s,box-shadow .1s}
.unit.sel .pf{border-color:var(--accent)!important;box-shadow:0 0 0 2px var(--panel),0 0 0 3px var(--accent)!important}
.unit.dim{opacity:.4}
.unit .pf{width:54px;height:54px;border-radius:10px;object-fit:cover;border:2px solid var(--uc,#888);
  background:var(--panel2);display:block;margin:0 auto}
.unit .nm{font-size:10.5px;color:var(--muted);margin-top:3px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;font-weight:500}
.unit .gem{position:absolute;top:-4px;left:50%;transform:translateX(-50%);font-size:9px;font-weight:700;color:#fff;
  background:var(--uc,#888);border-radius:999px;padding:1px 6px;line-height:1.5}
.unit.carry .pf{border-color:var(--accent2);box-shadow:0 0 0 2px var(--panel),0 0 0 3px var(--accent2)}
.unit .star{position:absolute;top:-5px;right:4px;color:var(--accent2);font-size:12px;filter:drop-shadow(0 1px 1px rgba(0,0,0,.5))}

.traits{display:flex;gap:6px;flex-wrap:wrap}
.tr{display:inline-flex;align-items:center;gap:5px;font-size:11.5px;font-weight:600;padding:3px 8px;border-radius:7px;
  background:var(--panel2);color:var(--ink);cursor:default}
.tr img{width:14px;height:14px}
.tr .b{color:var(--muted);font-weight:600;font-variant-numeric:tabular-nums}
.tr.prim{background:var(--ring);box-shadow:inset 0 0 0 1px var(--accent)}
.tr.sig{opacity:.55;font-size:11px}
.tr.sig img{opacity:.7}

.foot{border-top:1px dashed var(--line);padding-top:10px;display:flex;flex-direction:column;gap:9px}
.row{display:flex;align-items:center;gap:8px;font-size:12px;min-width:0}
.row .k{color:var(--muted);font-weight:600;font-size:10.5px;text-transform:uppercase;letter-spacing:.4px;flex:none;width:72px}
.row .v{min-width:0;display:flex;align-items:center;gap:6px;flex-wrap:wrap}
.hold{font-weight:600}
.items{color:var(--muted);font-size:11.5px}
.leads{display:flex;gap:5px;flex-wrap:wrap}
.leads .mini{display:inline-flex;align-items:center;gap:4px;font-size:11px;color:var(--muted);
  background:var(--panel2);border-radius:6px;padding:2px 6px 2px 2px}
.leads .mini img{width:18px;height:18px;border-radius:5px;border:1.5px solid var(--lc,#888)}
.leads .mini.carry{color:var(--ink);font-weight:600}

.note{color:var(--muted);font-size:12px;margin:0 auto;max-width:76ch;text-align:center;padding-top:8px}
footer{color:var(--muted);font-size:12px;padding-block:22px 36px;border-top:1px solid var(--line);margin-top:10px}
footer a{color:var(--accent)}
.empty{grid-column:1/-1;text-align:center;color:var(--muted);padding:40px 0}

#tip{position:fixed;z-index:50;max-width:260px;background:var(--panel);color:var(--ink);border:1px solid var(--line);
  box-shadow:var(--shadow);border-radius:9px;padding:9px 11px;font-size:12px;line-height:1.5;pointer-events:none;
  opacity:0;transition:opacity .1s}
#tip .tt{font-weight:700;font-family:"Space Grotesk";margin-bottom:3px;display:flex;gap:6px;align-items:center}
#tip .tt img{width:15px;height:15px}
#tip .bp{color:var(--muted);font-size:11px;margin-top:4px}
@media (max-width:460px){.grid{grid-template-columns:1fr}.count{width:100%;margin:4px 0 0;order:5}}
@media (prefers-reduced-motion:reduce){*{transition:none!important}}
</style>'''

BODY = '''
<div id="tip" role="tooltip"></div>
<header class="top"><div class="wrap shell">
  <div class="brand">
    <h1>__SETNAME__ Openers</h1><span class="set">SET __SET__ · __SRC__</span>
  </div>
  <p class="lede">The strongest <b>level 4–5 opening boards</b> — cheap (1–2 cost) units whose traits actually line up,
    so every unit is doing a job. Each board shows its live <b>synergies</b>, who <b>holds items</b>, and the
    <b>trait it rolls into</b>. Ranked from current PBE placement data.</p>
  <div class="controls">
    <div class="seg" role="group" aria-label="Board size">
      <button data-sz="5" aria-pressed="true">Level 5 <span class="u">5 units</span></button>
      <button data-sz="4" aria-pressed="false">Level 4 <span class="u">4 units</span></button>
    </div>
    <label class="usel">Build around<select id="unit" aria-label="Feature a unit"></select></label>
    <div class="count" id="count"></div>
  </div>
  <div class="filters" id="filters"></div>
</div></header>
<main class="wrap shell">
  <div class="grid" id="grid"></div>
  <p class="note">Breakpoints like <b>Hyperpop 2</b> mean the board already hits that trait's first tier.
    Dimmed chips are 1-unit signature traits. PBE data shifts daily before the Dec 1 launch — treat tiers as a starting read.</p>
</main>
<footer class="wrap shell">
  Early-game opener finder · built from MetaTFT snapshot. Not affiliated with Riot Games.
  Companion to the <a href="./" id="codex" hidden>__SETNAME__ Codex &rarr;</a><b id="codextxt">__SETNAME__ Codex</b>.
</footer>
<script id="d" type="application/json">__DATA__</script>
<script>
const D=JSON.parse(document.getElementById('d').textContent);
const {boards,portraits,ticons,tdesc,costColors}=D;
const cc=costColors, vcss=['','--c1','--c2','--c3','--c4','--c5','--c6','--c7'];
const P=n=>portraits[n]||'', TI=t=>ticons[t]||'';
let SZ=5, FILT='all', UNIT='any';
try{const s=JSON.parse(localStorage.getItem('tft19_open')||'{}');if(s.sz)SZ=s.sz;if(s.f)FILT=s.f;if(s.u)UNIT=s.u;}catch(e){}
const save=()=>{try{localStorage.setItem('tft19_open',JSON.stringify({sz:SZ,f:FILT,u:UNIT}))}catch(e){}};

// unit dropdown: every opener-pool unit (1-2 cost) that appears in any board, grouped by cost
function buildUnitOptions(){
  const sel=document.getElementById('unit');
  const seen={};
  boards.forEach(b=>b.units.forEach(u=>{seen[u.name]={cost:u.cost,carry:u.carry};}));
  const names=Object.keys(seen).sort((a,b)=>seen[a].cost-seen[b].cost||a.localeCompare(b));
  let html='<option value="any">Any unit</option>';
  [1,2].forEach(c=>{
    const g=names.filter(n=>seen[n].cost==c);
    if(g.length)html+=`<optgroup label="${c}-cost">`+g.map(n=>`<option value="${esc(n)}">${esc(n)}${seen[n].carry?' ★':''}</option>`).join('')+'</optgroup>';
  });
  sel.innerHTML=html; sel.value=UNIT;
  sel.onchange=()=>{UNIT=sel.value;save();render();};
}

// trait filter list: non-signature active traits across boards, with board counts (for current size)
function buildFilters(){
  const f=document.getElementById('filters'); f.innerHTML='';
  const cnt={};
  boards.filter(b=>b.size==SZ).forEach(b=>b.traits.filter(t=>!t.sig).forEach(t=>cnt[t.name]=(cnt[t.name]||0)+1));
  const all=document.createElement('button');
  all.className='chip';all.textContent='All comps';all.setAttribute('aria-pressed',FILT=='all');
  all.onclick=()=>{FILT='all';save();render()};f.appendChild(all);
  Object.keys(cnt).sort().forEach(t=>{
    const c=document.createElement('button');c.className='chip';c.setAttribute('aria-pressed',FILT==t);
    c.innerHTML=(TI(t)?`<img src="${TI(t)}" alt="">`:'')+`${t} <span class="n">${cnt[t]}</span>`;
    c.onclick=()=>{FILT=(FILT==t?'all':t);save();render()};f.appendChild(c);
  });
}
const esc=s=>(s||'').replace(/[&<>"]/g,m=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[m]));

function unitTile(u){
  const col=`var(${vcss[u.cost]})`;
  const sel=(UNIT!=='any'&&u.name===UNIT)?' sel':'';
  return `<div class="unit ${u.carry?'carry':''}${sel}" data-u="${esc(u.name)}">
    <span class="gem" style="--uc:${col}">${u.cost}</span>
    ${u.carry?'<span class="star">★</span>':''}
    <img class="pf" style="--uc:${col}" src="${P(u.name)}" alt="${esc(u.name)}" loading="lazy">
    <div class="nm">${esc(u.name)}</div></div>`;
}
function traitChip(t){
  const cls='tr'+(t.primary?' prim':'')+(t.sig?' sig':'');
  const lab=t.sig?'':`<span class="b">${t.count}/${t.bp}</span>`;
  return `<span class="${cls}" data-t="${esc(t.name)}">${TI(t.name)?`<img src="${TI(t.name)}" alt="">`:''}${esc(t.name)} ${lab}</span>`;
}
function leadTile(l){
  const col=`var(${vcss[l.cost]})`;
  return `<span class="mini ${l.carry?'carry':''}" data-u="${esc(l.name)}"><img style="--lc:${col}" src="${P(l.name)}" alt="">${esc(l.name)}</span>`;
}
function card(b){
  const pct=Math.max(12,Math.min(100,Math.round((b.score/95)*100)));
  const items=(b.carry.items||[]).join(' · ');
  return `<div class="card">
    <div class="chead">
      <div class="tier ${b.tier}">${b.tier}</div>
      <div class="ptitle" data-t="${esc(b.primary)}">${TI(b.primary)?`<img src="${TI(b.primary)}" alt="">`:''}<span>${esc(b.primary)}</span></div>
      <div class="meter"><div class="lab">Strength</div><div class="bar"><i style="width:${pct}%"></i></div></div>
    </div>
    <div class="units">${b.units.map(unitTile).join('')}</div>
    <div class="traits">${b.traits.map(traitChip).join('')}</div>
    <div class="foot">
      <div class="row"><span class="k">Hold items</span><span class="v"><span class="hold">${esc(b.carry.name)}</span>${items?`<span class="items">${esc(items)}</span>`:''}</span></div>
      ${b.leads.length?`<div class="row"><span class="k">Rolls into</span><span class="v leads">${b.leads.map(leadTile).join('')}</span></div>`:''}
    </div></div>`;
}
function render(){
  buildFilters();
  document.getElementById('unit').value=UNIT;
  let list=boards.filter(b=>b.size==SZ);
  if(UNIT!='any')list=list.filter(b=>b.units.some(u=>u.name==UNIT));
  if(FILT!='all')list=list.filter(b=>b.traits.some(t=>t.name==FILT&&!t.sig));
  list.sort((a,b)=>b.score-a.score);
  const g=document.getElementById('grid');
  let empty='No openers match those filters at this level.';
  if(!list.length&&UNIT!='any')empty=`${esc(UNIT)} isn't in a qualifying ${SZ=='5'?'level-5':'level-4'} opener`+(FILT!='all'?` with ${esc(FILT)}`:'')+'. Try the other level or clear a filter.';
  g.innerHTML=list.length?list.map(card).join(''):`<div class="empty">${empty}</div>`;
  const tags=[UNIT!='any'?esc(UNIT):'',FILT!='all'?esc(FILT):''].filter(Boolean).join(' · ');
  document.getElementById('count').innerHTML=`<b>${list.length}</b> opener${list.length!=1?'s':''}`+(tags?` · ${tags}`:'');
  document.querySelectorAll('.seg button').forEach(x=>x.setAttribute('aria-pressed',x.dataset.sz==SZ));
}
document.querySelectorAll('.seg button').forEach(x=>x.onclick=()=>{SZ=+x.dataset.sz;FILT='all';save();render()});

// tooltip
const tip=document.getElementById('tip');let tHide;
function showTip(html,x,y){clearTimeout(tHide);tip.innerHTML=html;tip.style.opacity='1';
  const w=tip.offsetWidth,h=tip.offsetHeight;let L=x+14,T=y+14;
  if(L+w>innerWidth-8)L=x-w-14;if(T+h>innerHeight-8)T=y-h-14;
  tip.style.left=Math.max(8,L)+'px';tip.style.top=Math.max(8,T)+'px';}
function hideTip(){tHide=setTimeout(()=>tip.style.opacity='0',40);}
document.getElementById('grid').addEventListener('mouseover',e=>{
  const tr=e.target.closest('[data-t]');const un=e.target.closest('[data-u]');
  if(tr){const t=tr.dataset.t;showTip(`<div class="tt">${TI(t)?`<img src="${TI(t)}">`:''}${esc(t)}</div>${esc(tdesc[t]||'')}`,e.clientX,e.clientY);}
  else if(un){const n=un.dataset.u;showTip(`<div class="tt">${esc(n)}</div>`,e.clientX,e.clientY);}
});
document.getElementById('grid').addEventListener('mousemove',e=>{if(tip.style.opacity=='1'){const el=e.target.closest('[data-t],[data-u]');if(el)showTip(tip.innerHTML,e.clientX,e.clientY);else hideTip();}});
document.getElementById('grid').addEventListener('mouseleave',hideTip);
// click a board unit to build around it (toggle off if already selected)
document.getElementById('grid').addEventListener('click',e=>{
  const un=e.target.closest('.unit[data-u]');if(!un)return;
  const n=un.dataset.u;UNIT=(UNIT===n?'any':n);save();render();
  window.scrollTo({top:0,behavior:'smooth'});
});
// on the GitHub Pages site the Codex sits next to this page — show the link there
try{if(location.hostname.endsWith('github.io')||location.protocol==='file:'){
  document.getElementById('codex').hidden=false;document.getElementById('codextxt').hidden=true;}}catch(e){}
buildUnitOptions();
render();
</script>'''

src = (d.get('source') or '').lower()
SRC = 'Live' if 'live' in src or '1100' in src else 'PBE'
html = (HEAD + BODY).replace('__DATA__', DATA).replace('__SETNAME__', setName) \
    .replace('__SET__', str(config.SET)).replace('__SRC__', SRC)
open(config.OPENERS, 'w', encoding='utf-8').write(html)
print('wrote', config.OPENERS, '%.2f MB' % (len(html.encode('utf-8'))/1e6))
