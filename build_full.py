import json
d = json.load(open('set18_full.json', encoding='utf-8'))
DATA = json.dumps(d, ensure_ascii=False)

HTML = r'''<title>Enchanted Wilds Codex</title>
<style>
:root{
  --bg:#eef2ea; --bg2:#e4ebe0; --surface:#ffffff; --surface2:#f5f8f2;
  --text:#17251b; --muted:#5c6d60; --faint:#8a9a8d; --border:#d6ded0;
  --green:#2f9e5f; --green-ink:#1d7d47; --gold:#b8892a; --violet:#7c5fd0; --sky:#2f7fc4;
  --ad:#c9702f; --ap:#2f80c4;
  --shadow:0 1px 2px rgba(20,40,25,.06),0 8px 24px rgba(20,40,25,.06);
  --t-bronze:#b06a3f; --t-silver:#7f8f9b; --t-gold:#c99524; --t-prismatic:#8a6fd0; --t-unique:#2f9bbf;
}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){
  --bg:#0b1210; --bg2:#0e1712; --surface:#131e17; --surface2:#17241b;
  --text:#e9f1e7; --muted:#93a897; --faint:#6d8073; --border:#26362b;
  --green:#4ade80; --green-ink:#7be6a3; --gold:#e8c86a; --violet:#b697ec; --sky:#6bb6ee;
  --ad:#e8975a; --ap:#6bb6ee;
  --shadow:0 1px 2px rgba(0,0,0,.35),0 10px 30px rgba(0,0,0,.35);
  --t-bronze:#cd8455; --t-silver:#adbcc7; --t-gold:#e8c86a; --t-prismatic:#b79bf0; --t-unique:#5fd0ef;
}}
:root[data-theme="dark"]{
  --bg:#0b1210; --bg2:#0e1712; --surface:#131e17; --surface2:#17241b;
  --text:#e9f1e7; --muted:#93a897; --faint:#6d8073; --border:#26362b;
  --green:#4ade80; --green-ink:#7be6a3; --gold:#e8c86a; --violet:#b697ec; --sky:#6bb6ee;
  --ad:#e8975a; --ap:#6bb6ee;
  --shadow:0 1px 2px rgba(0,0,0,.35),0 10px 30px rgba(0,0,0,.35);
  --t-bronze:#cd8455; --t-silver:#adbcc7; --t-gold:#e8c86a; --t-prismatic:#b79bf0; --t-unique:#5fd0ef;
}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--text);
  font-family:system-ui,-apple-system,"Segoe UI",Roboto,sans-serif;line-height:1.5;-webkit-font-smoothing:antialiased;}
.serif{font-family:"Iowan Old Style","Palatino Linotype",Palatino,"Book Antiqua",Georgia,serif;}
.wrap{max-width:1180px;margin:0 auto;padding:0 20px 72px;}

header{position:relative;overflow:hidden;border-bottom:1px solid var(--border);
  background:radial-gradient(120% 140% at 82% -10%,color-mix(in srgb,var(--gold) 16%,transparent),transparent 55%),
             radial-gradient(120% 120% at 6% 0%,color-mix(in srgb,var(--green) 15%,transparent),transparent 52%),var(--bg2);}
.head-in{max-width:1180px;margin:0 auto;padding:32px 20px 26px;position:relative;}
.eyebrow{font-size:12px;letter-spacing:.22em;text-transform:uppercase;color:var(--green-ink);font-weight:600;}
h1{font-size:clamp(32px,5.5vw,54px);margin:.1em 0 .12em;line-height:1.02;font-weight:600;text-wrap:balance;letter-spacing:-.01em;}
.sub{color:var(--muted);max-width:62ch;font-size:15px;}
.stats{display:flex;flex-wrap:wrap;gap:10px;margin-top:18px;}
.stat{background:color-mix(in srgb,var(--surface) 70%,transparent);border:1px solid var(--border);
  border-radius:12px;padding:8px 14px;display:flex;align-items:baseline;gap:7px;backdrop-filter:blur(4px);}
.stat b{font-size:19px;font-variant-numeric:tabular-nums;} .stat span{font-size:12px;color:var(--muted);}
.theme{position:absolute;top:16px;right:20px;background:var(--surface);border:1px solid var(--border);
  color:var(--text);border-radius:10px;padding:7px 11px;font-size:13px;cursor:pointer;display:flex;gap:6px;align-items:center;}
.theme:hover{border-color:var(--green);}

.calls{display:grid;grid-template-columns:1fr 1fr;gap:14px;margin:22px 0 4px;}
@media(max-width:640px){.calls{grid-template-columns:1fr}}
.call{border:1px solid var(--border);border-radius:14px;padding:14px 16px;background:var(--surface);box-shadow:var(--shadow);}
.call h3{margin:0 0 4px;font-size:14px;display:flex;align-items:center;gap:8px;}
.call.wisp h3{color:var(--gold)} .call.eclipse h3{color:var(--violet)}
.call p{margin:0;font-size:13px;color:var(--muted);} .call b{color:var(--text)}
.dot{width:9px;height:9px;border-radius:50%;flex:none} .dot.g{background:var(--gold)} .dot.v{background:var(--violet)}

/* tabs */
.tabs{display:flex;gap:6px;margin:26px 0 4px;border-bottom:1px solid var(--border);}
.tab{background:none;border:0;border-bottom:2px solid transparent;color:var(--muted);font-size:15px;font-weight:600;
  padding:10px 16px;cursor:pointer;margin-bottom:-1px;}
.tab:hover{color:var(--text)} .tab[aria-selected="true"]{color:var(--green-ink);border-color:var(--green);}

.controls{display:flex;flex-wrap:wrap;gap:9px;align-items:center;margin:18px 0;position:sticky;top:0;z-index:6;
  padding:12px 0;background:linear-gradient(var(--bg),var(--bg) 72%,transparent);}
.search{flex:1;min-width:170px;position:relative;}
.search input{width:100%;padding:10px 12px 10px 34px;border-radius:11px;border:1px solid var(--border);background:var(--surface);color:var(--text);font-size:14px;}
.search input:focus{outline:2px solid var(--green);outline-offset:1px;border-color:transparent;}
.search svg{position:absolute;left:11px;top:11px;color:var(--faint)}
.chips{display:flex;gap:6px;flex-wrap:wrap}
.chip{border:1px solid var(--border);background:var(--surface);color:var(--muted);border-radius:999px;padding:7px 13px;font-size:13px;cursor:pointer;font-weight:500;white-space:nowrap;transition:.12s}
.chip:hover{color:var(--text);border-color:var(--faint)}
.chip[aria-pressed="true"]{background:var(--green);border-color:var(--green);color:#05130b;font-weight:600;}
.chip.ad[aria-pressed="true"]{background:var(--ad);border-color:var(--ad)} .chip.ap[aria-pressed="true"]{background:var(--ap);border-color:var(--ap);color:#fff}
select.chip{-webkit-appearance:none;appearance:none;padding-right:26px;background-image:linear-gradient(45deg,transparent 50%,var(--faint) 50%),linear-gradient(135deg,var(--faint) 50%,transparent 50%);background-position:calc(100% - 14px) 15px,calc(100% - 9px) 15px;background-size:5px 5px;background-repeat:no-repeat;}

.count{font-size:12.5px;color:var(--faint);margin:2px 2px 14px;}

/* champion grid */
.cgrid{display:grid;grid-template-columns:repeat(auto-fill,minmax(224px,1fr));gap:15px;}
.cc{border:1px solid var(--border);border-radius:15px;background:var(--surface);box-shadow:var(--shadow);overflow:hidden;cursor:pointer;transition:.14s;display:flex;flex-direction:column;}
.cc:hover{transform:translateY(-2px);border-color:var(--cc)}
.cc1{--cc:#8a9a8d} .cc2{--cc:#3fae6a} .cc3{--cc:#2f8fd4} .cc4{--cc:#a06fe0} .cc5{--cc:#e0b23f}
.art{position:relative;aspect-ratio:240/128;background:#0a120d center/cover no-repeat;}
.art::after{content:"";position:absolute;inset:0;background:linear-gradient(to top,var(--surface) 2%,transparent 46%);}
.corner{position:absolute;top:8px;left:8px;z-index:3;display:flex;gap:5px;align-items:center}
.gem{width:24px;height:24px;border-radius:7px;display:grid;place-items:center;
  font-size:12px;font-weight:800;color:#0a120d;background:var(--cc);box-shadow:0 1px 4px rgba(0,0,0,.4);font-variant-numeric:tabular-nums}
.dmg{position:absolute;top:8px;right:8px;z-index:2;font-size:10px;font-weight:800;letter-spacing:.06em;padding:3px 7px;border-radius:6px;color:#fff;}
.dmg.AD{background:var(--ad)} .dmg.AP{background:var(--ap)} .dmg.Hybrid{background:var(--violet)}
.carrystar{position:absolute;bottom:6px;right:8px;z-index:2;font-size:12px;color:var(--gold);filter:drop-shadow(0 1px 2px rgba(0,0,0,.6))}
.metabadge{position:absolute;bottom:6px;right:7px;z-index:2;display:flex;align-items:center;gap:5px;font-size:10.5px;font-weight:700;
  padding:2px 7px;border-radius:6px;background:rgba(10,18,14,.82);color:#fff;backdrop-filter:blur(2px);font-variant-numeric:tabular-nums}
.rankno{min-width:24px;height:24px;padding:0 6px;border-radius:7px;display:grid;place-items:center;
  font-size:12px;font-weight:800;color:#0a120d;background:var(--gold);box-shadow:0 1px 5px rgba(0,0,0,.5);font-variant-numeric:tabular-nums}
.tierP{font-weight:800;letter-spacing:.02em}
.tS{color:#ff6b6b} .tA{color:#ffa94d} .tB{color:#e8c86a} .tC{color:#9fb0bc} .tT{color:#93a897}
.metaBox{margin-bottom:11px;padding:10px;border-radius:10px;background:var(--surface2);border:1px solid var(--border)}
.metaHead{font-size:11.5px;color:var(--muted);display:flex;align-items:center;gap:6px;flex-wrap:wrap;margin-bottom:8px}
.metaHead b{color:var(--text);font-variant-numeric:tabular-nums}
.tierChip{font-size:11px;font-weight:800;padding:1px 7px;border-radius:5px;background:rgba(0,0,0,.15)}
.items{display:flex;flex-wrap:wrap;gap:5px}
.itemchip{display:flex;align-items:center;gap:5px;font-size:10.5px;color:var(--muted);background:var(--surface);border:1px solid var(--border);border-radius:6px;padding:2px 6px 2px 3px}
.itemchip img{width:18px;height:18px;border-radius:4px;object-fit:cover}
.buildLbl{font-size:10px;letter-spacing:.1em;text-transform:uppercase;color:var(--faint);font-weight:700;margin:9px 0 5px}
.cbody{padding:10px 13px 13px;margin-top:-14px;position:relative;z-index:2;flex:1;display:flex;flex-direction:column;}
.cn{font-size:18px;font-weight:600;letter-spacing:-.01em;line-height:1.1}
.crole{font-size:11px;color:var(--muted);margin:2px 0 8px;letter-spacing:.02em}
.ctr{display:flex;flex-wrap:wrap;gap:5px;margin-top:auto}
.tt{font-size:11px;background:var(--surface2);border:1px solid var(--border);border-radius:6px;padding:2px 7px;color:var(--muted)}
.cdesc{max-height:0;overflow:hidden;transition:max-height .3s ease}
.cc.open .cdesc{max-height:900px}
.cdesc-in{padding-top:11px;margin-top:11px;border-top:1px dashed var(--border)}
.statline{display:flex;flex-wrap:wrap;gap:5px;margin-bottom:10px}
.sb{font-size:11px;background:var(--surface2);border:1px solid var(--border);border-radius:6px;padding:2px 7px;color:var(--muted);font-variant-numeric:tabular-nums}
.sb b{color:var(--text);font-weight:600}
.an{font-size:13.5px;font-weight:700;color:var(--green-ink);display:flex;align-items:center;gap:7px;margin-bottom:4px}
.an .mana{font-size:10.5px;font-weight:600;color:var(--sky);background:color-mix(in srgb,var(--sky) 14%,transparent);padding:1px 6px;border-radius:5px;letter-spacing:.02em}
.abd{font-size:12.5px;color:var(--muted);white-space:pre-line;line-height:1.5}
.abd .num{color:var(--text);font-weight:600;font-variant-numeric:tabular-nums}
.tbd{color:var(--faint);font-style:italic;cursor:help}
.chint{font-size:10.5px;color:var(--faint);margin-top:9px} .cc.open .chint{display:none}

/* comps */
.pnote{font-size:12.5px;color:var(--muted);background:var(--surface2);border:1px solid var(--border);border-radius:10px;padding:10px 13px;margin-bottom:14px}
.pnote b{color:var(--text)}
.pgrid{display:grid;grid-template-columns:repeat(auto-fill,minmax(340px,1fr));gap:15px}
.pc{border:1px solid var(--border);border-radius:16px;background:var(--surface);box-shadow:var(--shadow);overflow:hidden;cursor:pointer;transition:.14s}
.pc:hover{transform:translateY(-2px);border-color:var(--faint)}
.phead{display:flex;align-items:center;gap:11px;padding:13px 15px;border-bottom:1px solid var(--border2)}
.prank{width:26px;height:26px;border-radius:8px;flex:none;display:grid;place-items:center;font-size:12px;font-weight:800;color:#0a120d;background:var(--gold);font-variant-numeric:tabular-nums}
.pname{font-size:16.5px;font-weight:600;line-height:1.12;letter-spacing:-.01em;flex:1}
.pmetrics{display:flex;gap:6px;flex-wrap:wrap;margin-top:3px}
.pm{font-size:10.5px;color:var(--muted);background:var(--surface2);border:1px solid var(--border);border-radius:5px;padding:1px 6px;font-variant-numeric:tabular-nums}
.pm b{color:var(--text)}
.plevel{font-size:10px;font-weight:700;letter-spacing:.04em;color:var(--green-ink);background:color-mix(in srgb,var(--green) 15%,transparent);border:1px solid color-mix(in srgb,var(--green) 30%,transparent);border-radius:5px;padding:1px 6px;white-space:nowrap}
.board{display:flex;flex-wrap:wrap;gap:6px;padding:13px 15px 6px}
.unit{position:relative;width:46px}
.uimg{width:46px;height:46px;border-radius:9px;object-fit:cover;border:2px solid var(--uc);background:#0a120d;display:block}
.unit.u1{--uc:#8a9a8d} .unit.u2{--uc:#3fae6a} .unit.u3{--uc:#2f8fd4} .unit.u4{--uc:#a06fe0} .unit.u5{--uc:#e0b23f}
.unit.iscarry .uimg{border-color:var(--gold);box-shadow:0 0 0 2px color-mix(in srgb,var(--gold) 45%,transparent)}
.uname{font-size:9px;color:var(--muted);text-align:center;margin-top:2px;line-height:1.05;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;width:46px}
.star3{position:absolute;top:-4px;right:-4px;font-size:11px;color:var(--gold);filter:drop-shadow(0 1px 1px rgba(0,0,0,.7))}
.pcarry{position:absolute;bottom:13px;left:3px;font-size:9px}
.ptraits{display:flex;flex-wrap:wrap;gap:5px;padding:8px 15px 14px}
.ptrait{display:flex;align-items:center;gap:5px;font-size:11px;color:var(--muted);background:var(--surface2);border:1px solid var(--border);border-radius:6px;padding:2px 7px 2px 4px}
.ptrait img{width:16px;height:16px;object-fit:contain}
.pdesc{max-height:0;overflow:hidden;transition:max-height .3s ease}.pc.open .pdesc{max-height:800px}
.pdesc-in{padding:0 15px 15px;border-top:1px dashed var(--border);margin-top:2px;padding-top:12px}
.pcarrow{margin-bottom:11px}
.pcarrow .cnm{font-size:12.5px;font-weight:600;margin-bottom:5px;display:flex;align-items:center;gap:6px}
.pcarrow .cnm .av{font-size:10.5px;color:var(--muted);font-weight:500}
.phint{font-size:10.5px;color:var(--faint);padding:0 15px 12px}.pc.open .phint{display:none}

/* builder */
.builder{display:grid;grid-template-columns:224px 1fr;gap:16px;align-items:start;margin-top:18px}
@media(max-width:720px){.builder{grid-template-columns:1fr}}
.bside{border:1px solid var(--border);border-radius:14px;background:var(--surface);padding:12px;box-shadow:var(--shadow);position:sticky;top:62px}
@media(max-width:720px){.bside{position:static}}
.bside-top{display:flex;gap:6px}
.bnew{flex:1;padding:9px;border:0;border-radius:10px;background:var(--green);color:#05130b;font-weight:700;font-size:13.5px;cursor:pointer}
.bnew:hover{filter:brightness(1.05)}
.bfolder-add{flex:none;width:42px;border:1px solid var(--border);background:var(--surface);border-radius:10px;cursor:pointer;font-size:13px;color:var(--muted)}
.bfolder-add:hover{color:var(--text);border-color:var(--green)}
.bnewfolder{display:flex;gap:5px;margin-top:8px}
.bnewfolder input{flex:1;min-width:0;padding:7px 9px;border:1px solid var(--border);border-radius:8px;background:var(--surface2);color:var(--text);font-size:12.5px}
.bnewfolder input:focus{outline:none;border-color:var(--green)}
.bnewfolder button{border:0;border-radius:8px;background:var(--green);color:#05130b;font-weight:700;font-size:12px;padding:0 11px;cursor:pointer}
.blist{display:flex;flex-direction:column;gap:6px;margin:12px 0}
.bfolder{display:flex;align-items:center;gap:4px;margin-top:9px}
.bfolder.plain{margin-top:12px}
.bfhdr{display:flex;align-items:center;gap:6px;flex:1;background:none;border:0;color:var(--text);font-weight:700;font-size:11px;letter-spacing:.08em;text-transform:uppercase;cursor:pointer;padding:3px 2px;min-width:0}
.bfcaret{font-size:9px;transition:.15s;flex:none}
.bfolder.collapsed .bfcaret{transform:rotate(-90deg)}
.bfname{white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.bfname.ung{color:var(--faint);opacity:.8}
.bfcount{flex:none;font-size:10px;color:var(--faint);background:var(--surface2);border:1px solid var(--border);border-radius:5px;padding:0 5px;font-weight:700;font-variant-numeric:tabular-nums}
.bfdel{flex:none;cursor:pointer;color:var(--faint);font-size:11px;padding:2px 5px;border-radius:5px}
.bfdel:hover{color:#c0392b;background:color-mix(in srgb,#c0392b 10%,transparent)}
.bfitems{display:flex;flex-direction:column;gap:6px;padding-left:8px;border-left:2px solid var(--border);margin:2px 0 2px 5px}
.bfitems .blist-empty{padding:5px 2px}
.bitem{width:100%;text-align:left;border:1px solid var(--border);background:var(--surface2);color:var(--text);border-radius:10px;padding:9px 11px;cursor:pointer;transition:.12s;font:inherit}
.bitem:hover{border-color:var(--green)} .bitem.active{border-color:var(--green);background:color-mix(in srgb,var(--green) 12%,transparent)}
.bitem .bt{font-size:13.5px;font-weight:600;line-height:1.15;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.bitem .bs{font-size:11px;color:var(--muted);margin-top:2px;font-variant-numeric:tabular-nums}
.blist-empty{font-size:12px;color:var(--faint);font-style:italic;padding:8px 2px;text-align:center}
.bio{display:flex;gap:6px;border-top:1px solid var(--border);padding-top:11px}
.bio-btn{flex:1;padding:7px;border:1px solid var(--border);background:var(--surface);color:var(--muted);border-radius:8px;font-size:12px;cursor:pointer;font-weight:600}
.bio-btn:hover{color:var(--text);border-color:var(--faint)}
.bio-msg{font-size:11px;color:var(--green-ink);margin-top:8px;min-height:14px}

.bmain{min-width:0}
.btop{display:grid;grid-template-columns:1fr 300px;gap:16px;align-items:start;margin-bottom:6px}
@media(max-width:820px){.btop{grid-template-columns:1fr}}
.bleft{min-width:0}
.bright{position:sticky;top:62px;display:flex;flex-direction:column}
@media(max-width:820px){.bright{position:static}}
.bright .bnotes{min-height:220px;flex:1}
.bfolder-sel{max-width:150px}
.bmhead{display:flex;align-items:center;gap:12px;flex-wrap:wrap;margin-bottom:12px}
.bname-in{flex:1;min-width:160px;font-family:"Iowan Old Style","Palatino Linotype",Palatino,Georgia,serif;font-size:22px;font-weight:600;
  background:none;border:0;border-bottom:2px solid var(--border);color:var(--text);padding:4px 2px}
.bname-in:focus{outline:none;border-color:var(--green)}
.bmeta{display:flex;gap:10px;font-size:12px;color:var(--muted);font-variant-numeric:tabular-nums}
.bboard{display:flex;flex-wrap:wrap;gap:8px;min-height:66px;padding:11px;border:1px dashed var(--border);border-radius:13px;background:var(--surface2);margin-bottom:14px}
.bboard:empty::before{content:"Click champions below to build your team";color:var(--faint);font-style:italic;font-size:13px;margin:auto}
.btile{position:relative;width:52px}
.btile img{width:52px;height:52px;border-radius:10px;object-fit:cover;border:2px solid var(--tc);background:#0a120d;display:block}
.btile.b1{--tc:#8a9a8d}.btile.b2{--tc:#3fae6a}.btile.b3{--tc:#2f8fd4}.btile.b4{--tc:#a06fe0}.btile.b5{--tc:#e0b23f}
.btile .bx{position:absolute;top:-6px;right:-6px;width:18px;height:18px;border-radius:50%;background:#c0392b;color:#fff;border:2px solid var(--surface);
  font-size:11px;line-height:1;display:grid;place-items:center;cursor:pointer;opacity:0;transition:.12s}
.btile:hover .bx{opacity:1}
.btile .bn{font-size:9px;color:var(--muted);text-align:center;margin-top:2px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;width:52px}

.btraits{display:flex;flex-wrap:wrap;gap:7px;margin-bottom:16px;min-height:10px}
.btrait{display:flex;align-items:center;gap:7px;border:1px solid var(--border);border-radius:9px;padding:4px 10px 4px 5px;background:var(--surface);opacity:.5}
.btrait.on{opacity:1;border-color:color-mix(in srgb,var(--tier) 55%,var(--border));background:color-mix(in srgb,var(--tier) 9%,transparent)}
.btrait img{width:22px;height:22px;object-fit:contain;background:radial-gradient(circle at 50% 35%,#1b2a20,#0a120d);border-radius:6px;padding:2px}
.btrait .bcnt{font-weight:800;font-variant-numeric:tabular-nums;color:var(--tier)}
.btrait .btn2{font-size:12.5px;font-weight:600} .btrait .bnext{font-size:10.5px;color:var(--faint);font-variant-numeric:tabular-nums}
.btrait.tier-bronze{--tier:var(--t-bronze)}.btrait.tier-silver{--tier:var(--t-silver)}.btrait.tier-gold{--tier:var(--t-gold)}
.btrait.tier-prismatic{--tier:var(--t-prismatic)}.btrait.tier-unique{--tier:var(--t-unique)}.btrait.tier-none{--tier:var(--faint)}
.btrait.eclipse{--tier:var(--violet);opacity:1;border-color:color-mix(in srgb,var(--violet) 55%,var(--border));background:color-mix(in srgb,var(--violet) 12%,transparent)}

.blabel{display:block;font-size:11px;letter-spacing:.14em;text-transform:uppercase;color:var(--faint);font-weight:700;margin:4px 0 6px}
.blabel-sub{letter-spacing:0;text-transform:none;font-weight:400;color:var(--faint)}
.bnotes{width:100%;min-height:66px;resize:vertical;border:1px solid var(--border);border-radius:11px;background:var(--surface);color:var(--text);
  font-family:inherit;font-size:13.5px;padding:10px 12px;line-height:1.5}
.bnotes:focus{outline:2px solid var(--green);outline-offset:1px;border-color:transparent}
.bactions{display:flex;gap:9px;flex-wrap:wrap;margin:13px 0 22px}
.bsave{padding:9px 20px;border:0;border-radius:10px;background:var(--green);color:#05130b;font-weight:700;font-size:14px;cursor:pointer}
.bsave:hover{filter:brightness(1.05)}
.bclear,.bdel{padding:9px 16px;border:1px solid var(--border);border-radius:10px;background:var(--surface);color:var(--muted);font-size:13px;cursor:pointer;font-weight:600}
.bclear:hover{color:var(--text);border-color:var(--faint)} .bdel{color:#c0392b;border-color:color-mix(in srgb,#c0392b 40%,var(--border))}
.bdel:hover{background:color-mix(in srgb,#c0392b 10%,transparent)}
.bpicker{display:grid;grid-template-columns:repeat(auto-fill,minmax(88px,1fr));gap:8px}
.pk{position:relative;border:1px solid var(--border);border-radius:10px;overflow:hidden;cursor:pointer;background:var(--surface);transition:.1s}
.pk:hover{border-color:var(--pc);transform:translateY(-1px)} .pk.picked{border-color:var(--green);box-shadow:0 0 0 2px color-mix(in srgb,var(--green) 40%,transparent)}
.pk.b1{--pc:#8a9a8d}.pk.b2{--pc:#3fae6a}.pk.b3{--pc:#2f8fd4}.pk.b4{--pc:#a06fe0}.pk.b5{--pc:#e0b23f}
.pk img{width:100%;aspect-ratio:88/50;object-fit:cover;display:block;background:#0a120d}
.pk .pkn{font-size:10.5px;font-weight:600;padding:3px 6px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;border-left:3px solid var(--pc)}
.pk .pkg{position:absolute;top:4px;left:4px;width:16px;height:16px;border-radius:5px;background:var(--pc);color:#0a120d;font-size:9px;font-weight:800;display:grid;place-items:center;font-variant-numeric:tabular-nums}
.pk .pkck{position:absolute;top:4px;right:4px;color:var(--green);font-size:13px;opacity:0}.pk.picked .pkck{opacity:1}

/* trait grid (reused) */
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(272px,1fr));gap:14px;}
.card{border:1px solid var(--border);border-radius:16px;background:var(--surface);box-shadow:var(--shadow);padding:16px;cursor:pointer;transition:.14s;position:relative;overflow:hidden;}
.card:hover{transform:translateY(-2px);border-color:color-mix(in srgb,var(--accent) 60%,var(--border))}
.card.origin{--accent:var(--green)} .card.class{--accent:var(--sky)} .card.unique{--accent:var(--gold)} .card.hidden{--accent:var(--violet)}
.card::before{content:"";position:absolute;left:0;top:0;bottom:0;width:3px;background:var(--accent);opacity:.85}
.crow{display:flex;gap:12px;align-items:center}
.badge{width:46px;height:46px;border-radius:12px;flex:none;display:grid;place-items:center;background:radial-gradient(circle at 50% 35%,#1b2a20,#0a120d);border:1px solid var(--border)}
.badge img{width:34px;height:34px;object-fit:contain}
.tname{font-size:17px;font-weight:600;line-height:1.15}
.tcat{font-size:10.5px;letter-spacing:.12em;text-transform:uppercase;color:var(--accent);font-weight:700;margin-top:3px}
.pills{display:flex;flex-wrap:wrap;gap:6px;margin-top:13px}
.pill{font-size:12px;font-weight:700;font-variant-numeric:tabular-nums;min-width:24px;text-align:center;padding:3px 8px;border-radius:7px;border:1px solid;background:transparent}
.pill.bronze{color:var(--t-bronze);border-color:color-mix(in srgb,var(--t-bronze) 45%,transparent)}
.pill.silver{color:var(--t-silver);border-color:color-mix(in srgb,var(--t-silver) 45%,transparent)}
.pill.gold{color:var(--t-gold);border-color:color-mix(in srgb,var(--t-gold) 50%,transparent)}
.pill.prismatic{color:var(--t-prismatic);border-color:color-mix(in srgb,var(--t-prismatic) 50%,transparent)}
.pill.unique{color:var(--t-unique);border-color:color-mix(in srgb,var(--t-unique) 55%,transparent);background:color-mix(in srgb,var(--t-unique) 12%,transparent)}
.desc{max-height:0;overflow:hidden;transition:max-height .3s ease}.card.open .desc{max-height:1600px}
.desc-in{padding-top:13px;margin-top:13px;border-top:1px dashed var(--border)}
.dhead{font-size:13px;color:var(--muted);margin-bottom:9px;font-style:italic}
.brk{display:flex;gap:9px;font-size:13px;padding:3px 0;color:var(--text)}
.brk b{color:var(--accent);font-variant-numeric:tabular-nums;flex:none;width:20px;text-align:right}
.brk .num{font-weight:600;font-variant-numeric:tabular-nums}
.tunits{display:flex;flex-wrap:wrap;gap:5px;margin-top:12px;padding-top:11px;border-top:1px dashed var(--border)}
.tu{font-size:11px;background:var(--surface2);border:1px solid var(--border);border-radius:6px;padding:2px 7px;color:var(--muted);display:flex;gap:5px;align-items:center}
.tu i{width:6px;height:6px;border-radius:50%;font-style:normal}
.hint{margin-top:11px;font-size:11px;color:var(--faint)}.card.open .hint{display:none}
.empty{grid-column:1/-1;text-align:center;color:var(--faint);padding:40px;font-style:italic}
footer{margin-top:44px;padding-top:20px;border-top:1px solid var(--border);font-size:12.5px;color:var(--faint);display:flex;flex-wrap:wrap;gap:6px 18px;justify-content:space-between}
footer b{color:var(--muted)}
.hide{display:none!important}
@media(prefers-reduced-motion:reduce){*{transition:none!important}}
</style>

<header>
  <button class="theme" id="themeBtn" aria-label="Toggle theme">🌙 <span id="themeTxt">Auto</span></button>
  <div class="head-in">
    <div class="eyebrow">Teamfight Tactics · Set 18</div>
    <h1 class="serif">Enchanted Wilds Codex</h1>
    <p class="sub">Every champion and trait in the enchanted forest — portraits, roles, carries, breakpoints, and resolved ability numbers. Tap any card to open its details.</p>
    <div class="stats">
      <div class="stat"><b id="sChamp">0</b><span>Champions</span></div>
      <div class="stat"><b id="sTrait">0</b><span>Traits</span></div>
      <div class="stat"><b id="sCarry">0</b><span>Carries</span></div>
      <div class="stat"><b id="sComp">0</b><span>PBE comps</span></div>
    </div>
  </div>
</header>

<div class="wrap">
  <div class="calls">
    <div class="call wisp"><h3><span class="dot g"></span>New mechanic · Wisps</h3><p>Single-use magic that appears in the far-right shop slot every other round — combat power, gold, XP, or risky gambles. Buy one per round.</p></div>
    <div class="call eclipse"><h3><span class="dot v"></span>Hidden trait · Eclipse</h3><p>Field <b style="color:var(--gold)">Solar</b> and <b style="color:var(--sky)">Lunar</b> together to unlock Eclipse — a beam that executes the lowest-health enemy on a timer.</p></div>
  </div>

  <div class="tabs" role="tablist">
    <button class="tab" role="tab" aria-selected="true" data-view="champs">Champions</button>
    <button class="tab" role="tab" aria-selected="false" data-view="traits">Traits</button>
    <button class="tab" role="tab" aria-selected="false" data-view="comps">Comps</button>
    <button class="tab" role="tab" aria-selected="false" data-view="builder">Builder</button>
  </div>

  <!-- CHAMPIONS -->
  <section id="view-champs">
    <div class="controls">
      <label class="search"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="7"/><path d="m21 21-4-4"/></svg>
        <input id="cq" type="search" placeholder="Search champions, traits, roles…" autocomplete="off"></label>
      <div class="chips" id="costChips">
        <button class="chip" data-c="all" aria-pressed="true">All costs</button>
        <button class="chip" data-c="1" aria-pressed="false">1</button>
        <button class="chip" data-c="2" aria-pressed="false">2</button>
        <button class="chip" data-c="3" aria-pressed="false">3</button>
        <button class="chip" data-c="4" aria-pressed="false">4</button>
        <button class="chip" data-c="5" aria-pressed="false">5</button>
      </div>
      <div class="chips" id="dmgChips">
        <button class="chip ad" data-d="AD" aria-pressed="false">AD</button>
        <button class="chip ap" data-d="AP" aria-pressed="false">AP</button>
      </div>
      <div class="chips"><button class="chip" id="carryOnly" aria-pressed="false">★ Carries only</button>
        <button class="chip" id="metaRank" aria-pressed="false">🏆 Meta carries (PBE)</button></div>
      <select class="chip" id="traitSel"><option value="">All traits</option></select>
    </div>
    <div class="count" id="cCount"></div>
    <div class="cgrid" id="cgrid"></div>
  </section>

  <!-- TRAITS -->
  <section id="view-traits" class="hide">
    <div class="controls">
      <label class="search"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="7"/><path d="m21 21-4-4"/></svg>
        <input id="tq" type="search" placeholder="Search traits… (Lunar, Brawler, Coven)" autocomplete="off"></label>
      <div class="chips" id="tcat">
        <button class="chip" data-f="all" aria-pressed="true">All</button>
        <button class="chip" data-f="Origin" aria-pressed="false">Origins</button>
        <button class="chip" data-f="Class" aria-pressed="false">Classes</button>
        <button class="chip" data-f="Unique" aria-pressed="false">Unique</button>
        <button class="chip" data-f="Hidden" aria-pressed="false">Hidden</button>
      </div>
    </div>
    <div class="grid" id="grid"></div>
  </section>

  <!-- COMPS -->
  <section id="view-comps" class="hide">
    <div class="controls">
      <label class="search"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="7"/><path d="m21 21-4-4"/></svg>
        <input id="pq" type="search" placeholder="Search comps by carry, trait, or unit…" autocomplete="off"></label>
      <div class="chips" id="psort">
        <button class="chip" data-s="games" aria-pressed="true">Most played</button>
        <button class="chip" data-s="avg" aria-pressed="false">Best placement</button>
      </div>
    </div>
    <div class="pnote">Aggregated from live <b>PBE ranked games</b>. Boards show units, active traits, and itemized carries with best-in-slot items. Riot's PBE feed doesn't expose <b>hex positioning</b> or <b>augments</b> yet, so those aren't shown.</div>
    <div class="count" id="pCount"></div>
    <div class="pgrid" id="pgrid"></div>
  </section>

  <!-- BUILDER -->
  <section id="view-builder" class="hide">
    <div class="builder">
      <aside class="bside">
        <div class="bside-top">
          <button class="bnew" id="bNew">+ New build</button>
          <button class="bfolder-add" id="bFolderAdd" title="New folder">📁+</button>
        </div>
        <div class="bnewfolder hide" id="bNewFolder">
          <input id="bFolderName" type="text" placeholder="Folder name…" autocomplete="off" maxlength="28">
          <button id="bFolderCreate">Add</button>
        </div>
        <div class="blist" id="bList"></div>
        <div class="bio">
          <button class="bio-btn" id="bExport">⭳ Export</button>
          <button class="bio-btn" id="bImport">⭱ Import</button>
          <input type="file" id="bFile" accept="application/json,.json" hidden>
        </div>
        <div class="bio-msg" id="bMsg"></div>
      </aside>

      <div class="bmain">
        <div class="bmhead">
          <input id="bName" class="bname-in" type="text" placeholder="Untitled build" autocomplete="off">
          <select id="bFolder" class="chip bfolder-sel"><option value="">Ungrouped</option></select>
          <div class="bmeta"><span id="bUnitCount">0 units</span><span id="bCostSum"></span></div>
        </div>

        <div class="btop">
          <div class="bleft">
            <div class="bboard" id="bBoard"></div>
            <div class="btraits" id="bTraits"></div>
            <div class="bactions">
              <button class="bsave" id="bSave">Save build</button>
              <button class="bclear" id="bClear">Clear board</button>
              <button class="bdel hide" id="bDel">Delete</button>
            </div>
          </div>
          <div class="bright">
            <label class="blabel">Notes</label>
            <textarea id="bNotes" class="bnotes" placeholder="Positioning reminders, item priority, when to play this, augments to look for…"></textarea>
          </div>
        </div>

        <label class="blabel">Add champions <span class="blabel-sub">— click to add / remove</span></label>
        <div class="controls" style="margin:6px 0 12px;position:static;padding:0;background:none">
          <label class="search" style="min-width:150px"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="7"/><path d="m21 21-4-4"/></svg>
            <input id="bSearch" type="search" placeholder="Filter champions…" autocomplete="off"></label>
          <div class="chips" id="bCostFilter">
            <button class="chip" data-c="all" aria-pressed="true">All</button>
            <button class="chip" data-c="1" aria-pressed="false">1</button>
            <button class="chip" data-c="2" aria-pressed="false">2</button>
            <button class="chip" data-c="3" aria-pressed="false">3</button>
            <button class="chip" data-c="4" aria-pressed="false">4</button>
            <button class="chip" data-c="5" aria-pressed="false">5</button>
          </div>
        </div>
        <div class="bpicker" id="bPicker"></div>
      </div>
    </div>
  </section>

  <footer>
    <span>Champions, portraits &amp; items from <b>MetaTFT</b> · trait icons from <b>CommunityDragon</b>. Carry tiers, avg placement &amp; best-in-slot items aggregated from live <b>PBE ranked comps</b> — early data, will shift before launch.</span>
    <span>Set 18 · <b>Enchanted Wilds</b> · launches Aug 26 2026</span>
  </footer>
</div>

<script>
const DATA = __DATA__;
document.getElementById('sChamp').textContent = DATA.champions.length;
document.getElementById('sTrait').textContent = DATA.traits.length;
document.getElementById('sCarry').textContent = DATA.champions.filter(c=>c.carry).length;
document.getElementById('sComp').textContent = (DATA.comps||[]).length;
const costGem={1:'#8a9a8d',2:'#3fae6a',3:'#2f8fd4',4:'#a06fe0',5:'#e0b23f'};
const ICONS=DATA.itemIcons||{};
const num = s => (s||'').replace(/(\d[\d.]*(?:\/\d[\d.]*)*%?)/g,'<span class="num">$1</span>')
  .replace(/\?/g,'<span class="tbd" title="value not published on PBE yet">?</span>');
const itemChip = n => `<span class="itemchip">${ICONS[n]?`<img src="${ICONS[n]}" alt="">`:''}${n}</span>`;
const tierName={S:'S',A:'A',B:'B',C:'C',T:'Tank'};

/* tabs */
document.querySelectorAll('.tab').forEach(t=>t.addEventListener('click',()=>{
  document.querySelectorAll('.tab').forEach(x=>x.setAttribute('aria-selected',x===t));
  document.getElementById('view-champs').classList.toggle('hide',t.dataset.view!=='champs');
  document.getElementById('view-traits').classList.toggle('hide',t.dataset.view!=='traits');
  document.getElementById('view-comps').classList.toggle('hide',t.dataset.view!=='comps');
  document.getElementById('view-builder').classList.toggle('hide',t.dataset.view!=='builder');
}));

/* champions */
const cgrid=document.getElementById('cgrid');
let cFilter={q:'',cost:'all',dmg:null,carry:false,trait:'',meta:false};
// populate trait dropdown
[...new Set(DATA.champions.flatMap(c=>c.traits))].sort().forEach(t=>{
  const o=document.createElement('option');o.value=t;o.textContent=t;document.getElementById('traitSel').appendChild(o);
});
function champCard(c,showRank){
  const el=document.createElement('div');el.className='cc cc'+c.cost;el.style.setProperty('--cc',costGem[c.cost]);el.tabIndex=0;
  const s=c.stats||{}, mt=c.meta;
  const stat=(l,v)=>v==null?'':`<span class="sb">${l} <b>${v}</b></span>`;
  const adline=s.adByStar?s.adByStar.join('/'):s.ad;
  // top-right art badge: meta tier+avg place if we have it, else damage type
  let cornerBadge='';
  if(mt&&!mt.tank) cornerBadge=`<span class="metabadge"><span class="tierP t${mt.tier}">${mt.tier}</span> ${mt.avg} avg</span>`;
  else if(mt&&mt.tank) cornerBadge=`<span class="metabadge"><span class="tierP tT">🛡</span> ${mt.avg} avg</span>`;
  const metaBox = mt ? `
    <div class="metaBox">
      <div class="metaHead"><span class="tierChip t${mt.tier}">${mt.tank?'Itemized tank':'Carry · tier '+mt.tier}</span>
        <b>${mt.avg}</b> avg place · <b>${mt.games.toLocaleString()}</b> PBE games${mt.rank?` · #${mt.rank} most-played carry`:''}</div>
      <div class="items">${(mt.items||[]).map(itemChip).join('')}</div>
      ${mt.build&&mt.build.length?`<div class="buildLbl">Most common full build</div><div class="items">${mt.build.map(itemChip).join('')}</div>`:''}
    </div>` : '';
  el.innerHTML=`
    <div class="art" style="background-image:url('${c.portrait||''}')">
      <div class="corner">${showRank&&mt&&mt.rank?`<span class="rankno">${mt.rank}</span>`:''}<span class="gem">${c.cost}</span></div>
      <span class="dmg ${c.dmg}">${c.dmg}</span>
      ${cornerBadge}
    </div>
    <div class="cbody">
      <div class="cn serif">${c.name}</div>
      <div class="crole">${c.carry?'':'🛡 '}◆ ${c.cost}-cost · ${c.role}${c.carry?(mt&&!mt.tank?` · #${mt.rank} carry`:' · Carry'):' · Frontline'}</div>
      <div class="ctr">${c.traits.map(t=>`<span class="tt">${t}</span>`).join('')}</div>
      <div class="cdesc"><div class="cdesc-in">
        ${metaBox}
        <div class="statline">${stat('HP',s.hpByStar?s.hpByStar.join('/'):s.hp)}${stat('AD',adline)}${stat('AS',s.as)}${stat('Range',s.range)}${stat('Mana',s.mana)}</div>
        ${c.ability&&c.ability.name?`<div class="an">✦ ${c.ability.name}${s.mana?`<span class="mana">${s.mana} mana</span>`:''}</div><div class="abd">${num(c.ability.desc||'')}</div>`:''}
      </div></div>
      <div class="chint">▾ tap for ${mt?'build, ':''}ability &amp; stats</div>
    </div>`;
  const open=()=>el.classList.toggle('open');
  el.addEventListener('click',open);
  el.addEventListener('keydown',e=>{if(e.key==='Enter'||e.key===' '){e.preventDefault();open();}});
  return el;
}
function renderChamps(){
  const q=cFilter.q;
  let list=DATA.champions.filter(c=>
    (cFilter.cost==='all'||c.cost==+cFilter.cost) &&
    (!cFilter.dmg||c.dmg===cFilter.dmg) &&
    (!cFilter.carry||c.carry) &&
    (!cFilter.meta||(c.meta&&!c.meta.tank)) &&
    (!cFilter.trait||c.traits.includes(cFilter.trait)) &&
    (!q||c.name.toLowerCase().includes(q)||c.role.toLowerCase().includes(q)||c.traits.join(' ').toLowerCase().includes(q)));
  if(cFilter.meta) list=list.slice().sort((a,b)=>(b.meta.score-a.meta.score));
  cgrid.innerHTML='';
  const label=cFilter.meta?`${list.length} carries · ranked by PBE play`:`${list.length} champion${list.length!==1?'s':''}`;
  document.getElementById('cCount').textContent=label;
  if(!list.length){cgrid.innerHTML='<div class="empty">No champions match.</div>';return;}
  list.forEach(c=>cgrid.appendChild(champCard(c,cFilter.meta)));
}
document.getElementById('cq').addEventListener('input',e=>{cFilter.q=e.target.value.toLowerCase().trim();renderChamps();});
document.getElementById('costChips').addEventListener('click',e=>{const b=e.target.closest('.chip');if(!b)return;
  cFilter.cost=b.dataset.c;[...e.currentTarget.children].forEach(c=>c.setAttribute('aria-pressed',c===b));renderChamps();});
document.getElementById('dmgChips').addEventListener('click',e=>{const b=e.target.closest('.chip');if(!b)return;
  const on=b.getAttribute('aria-pressed')==='true';[...e.currentTarget.children].forEach(c=>c.setAttribute('aria-pressed','false'));
  cFilter.dmg=on?null:b.dataset.d;b.setAttribute('aria-pressed',!on);renderChamps();});
document.getElementById('carryOnly').addEventListener('click',e=>{const on=e.target.getAttribute('aria-pressed')==='true';
  e.target.setAttribute('aria-pressed',!on);cFilter.carry=!on;
  if(!on){cFilter.meta=false;document.getElementById('metaRank').setAttribute('aria-pressed','false');}renderChamps();});
document.getElementById('metaRank').addEventListener('click',e=>{const on=e.target.getAttribute('aria-pressed')==='true';
  e.target.setAttribute('aria-pressed',!on);cFilter.meta=!on;
  if(!on){cFilter.carry=false;document.getElementById('carryOnly').setAttribute('aria-pressed','false');}renderChamps();});
document.getElementById('traitSel').addEventListener('change',e=>{cFilter.trait=e.target.value;renderChamps();});
renderChamps();

/* traits */
const grid=document.getElementById('grid');
let tFilter='all',tQuery='';
function traitCard(t){
  const el=document.createElement('div');el.className='card '+t.cat.toLowerCase();el.tabIndex=0;
  const pills=(t.breakpoints||[]).map(b=>`<span class="pill ${b.style}">${b.min}</span>`).join('');
  const rows=(t.desc&&t.desc.rows||[]).map((r,i)=>{const bp=(t.breakpoints[i]||{}).min||'';
    return `<div class="brk"><b>${bp}</b><span>${num(r)}</span></div>`;}).join('');
  const head=t.desc&&t.desc.header?`<div class="dhead">${t.desc.header}</div>`:'';
  const units=(t.units||[]).length?`<div class="tunits">${t.units.map(u=>`<span class="tu"><i style="background:${costGem[u.cost]}"></i>${u.name}</span>`).join('')}</div>`:'';
  el.innerHTML=`
    <div class="crow">
      <div class="badge">${t.iconData?`<img src="${t.iconData}" alt="">`:''}</div>
      <div><div class="tname serif">${t.name}</div><div class="tcat">${t.cat==='Unique'?'Champion-unique':t.cat==='Hidden'?'Hidden combo':t.cat}</div></div>
    </div>
    <div class="pills">${pills}</div>
    <div class="desc"><div class="desc-in">${head}${rows}${units}</div></div>
    <div class="hint">▾ tap for breakpoints &amp; champions</div>`;
  const open=()=>el.classList.toggle('open');
  el.addEventListener('click',open);
  el.addEventListener('keydown',e=>{if(e.key==='Enter'||e.key===' '){e.preventDefault();open();}});
  return el;
}
function renderTraits(){
  grid.innerHTML='';
  const list=DATA.traits.filter(t=>(tFilter==='all'||t.cat===tFilter)&&
    (t.name.toLowerCase().includes(tQuery)||(t.units||[]).some(u=>u.name.toLowerCase().includes(tQuery))));
  if(!list.length){grid.innerHTML='<div class="empty">No traits match.</div>';return;}
  list.forEach(t=>grid.appendChild(traitCard(t)));
}
document.getElementById('tcat').addEventListener('click',e=>{const b=e.target.closest('.chip');if(!b)return;
  tFilter=b.dataset.f;[...e.currentTarget.children].forEach(c=>c.setAttribute('aria-pressed',c===b));renderTraits();});
document.getElementById('tq').addEventListener('input',e=>{tQuery=e.target.value.toLowerCase().trim();renderTraits();});
renderTraits();

/* comps */
const champByName=Object.fromEntries(DATA.champions.map(c=>[c.name,c]));
const traitIcon=Object.fromEntries(DATA.traits.map(t=>[t.name,t.iconData]));
const pgrid=document.getElementById('pgrid');
let pSort='games',pQuery='';
function compCard(p,rank){
  const el=document.createElement('div');el.className='pc';el.tabIndex=0;
  const units=p.units.map(u=>{
    const c=champByName[u.name]||{};
    return `<div class="unit u${u.cost}${u.carry?' iscarry':''}" title="${u.name}${u.star3?' ★3':''}">
      <img class="uimg" src="${c.portrait||''}" alt="${u.name}">
      ${u.star3?'<span class="star3">★</span>':''}
      <div class="uname">${u.name}</div></div>`;}).join('');
  const traits=p.traits.map(t=>`<span class="ptrait">${traitIcon[t]?`<img src="${traitIcon[t]}" alt="">`:''}${t}</span>`).join('');
  const carries=p.carries.map(cy=>`
    <div class="pcarrow"><div class="cnm">${cy.name} <span class="av">· ${cy.avg} avg place</span></div>
      <div class="items">${(cy.items||[]).map(itemChip).join('')}</div></div>`).join('');
  el.innerHTML=`
    <div class="phead">
      ${rank?`<span class="prank">${rank}</span>`:''}
      <div><div class="pname serif">${p.name}</div>
        <div class="pmetrics"><span class="pm"><b>${p.avg}</b> avg place</span><span class="pm"><b>${p.games.toLocaleString()}</b> games</span></div></div>
      ${p.level?`<span class="plevel">${p.level}</span>`:''}
    </div>
    <div class="board">${units}</div>
    <div class="ptraits">${traits}</div>
    <div class="pdesc"><div class="pdesc-in"><div class="buildLbl">Carry builds (best-in-slot)</div>${carries||'<span class="phint">No itemized carry recorded.</span>'}</div></div>
    <div class="phint">▾ tap for carry items</div>`;
  const open=()=>el.classList.toggle('open');
  el.addEventListener('click',e=>{if(!e.target.closest('a'))open();});
  el.addEventListener('keydown',e=>{if(e.key==='Enter'||e.key===' '){e.preventDefault();open();}});
  return el;
}
function renderComps(){
  let list=(DATA.comps||[]).filter(p=>{
    if(!pQuery)return true;
    return p.name.toLowerCase().includes(pQuery)||p.traits.join(' ').toLowerCase().includes(pQuery)
      ||p.units.some(u=>u.name.toLowerCase().includes(pQuery));
  });
  list=list.slice().sort((a,b)=> pSort==='avg' ? (a.avg-b.avg) : (b.games-a.games));
  pgrid.innerHTML='';
  document.getElementById('pCount').textContent=`${list.length} comps · ${pSort==='avg'?'best average placement first':'most-played first'}`;
  if(!list.length){pgrid.innerHTML='<div class="empty">No comps match.</div>';return;}
  list.forEach((p,i)=>pgrid.appendChild(compCard(p, pSort==='games'?i+1:0)));
}
document.getElementById('psort').addEventListener('click',e=>{const b=e.target.closest('.chip');if(!b)return;
  pSort=b.dataset.s;[...e.currentTarget.children].forEach(c=>c.setAttribute('aria-pressed',c===b));renderComps();});
document.getElementById('pq').addEventListener('input',e=>{pQuery=e.target.value.toLowerCase().trim();renderComps();});
renderComps();

/* builder */
(function(){
  const traitByName=Object.fromEntries(DATA.traits.map(t=>[t.name,t]));
  const LS='ewc_set18_builds_v1', DRAFT='ewc_set18_draft_v1', COL='ewc_set18_fold_col_v1';
  const uid=()=>Date.now().toString(36)+Math.random().toString(36).slice(2,6);
  const esc=s=>String(s).replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
  let builds=[], folders=[];
  try{const s=JSON.parse(localStorage.getItem(LS));
      if(Array.isArray(s))builds=s; else if(s&&typeof s==='object'){builds=s.builds||[];folders=s.folders||[];}
  }catch(e){}
  let collapsed=new Set(); try{collapsed=new Set(JSON.parse(localStorage.getItem(COL))||[])}catch(e){}
  let cur={id:null,name:'',champs:[],notes:'',folder:''};
  try{const d=JSON.parse(localStorage.getItem(DRAFT)); if(d&&d.champs)cur=Object.assign({folder:''},d);}catch(e){}
  let pQ='',pCost='all';
  const $=id=>document.getElementById(id);
  const persist=()=>{try{localStorage.setItem(LS,JSON.stringify({v:2,builds,folders}))}catch(e){}};
  const saveDraft=()=>{try{localStorage.setItem(DRAFT,JSON.stringify(cur))}catch(e){}};
  const saveCol=()=>{try{localStorage.setItem(COL,JSON.stringify([...collapsed]))}catch(e){}};
  const msg=t=>{const m=$('bMsg');m.textContent=t;if(t)setTimeout(()=>{if(m.textContent===t)m.textContent=''},3500);};

  function activeTier(t,count){
    let style='none',activeMin=0,nextMin=null;
    for(const b of (t.breakpoints||[])){
      if(count>=b.min){style=b.style;activeMin=b.min;}
      else{nextMin=b.min;break;}
    }
    return {on:activeMin>0,style,activeMin,nextMin};
  }
  function computeTraits(champs){
    const cnt={};
    champs.forEach(n=>((champByName[n]||{}).traits||[]).forEach(t=>cnt[t]=(cnt[t]||0)+1));
    let rows=Object.keys(cnt).map(name=>{
      const t=traitByName[name]||{breakpoints:[]};
      const a=activeTier(t,cnt[name]);
      return {name,count:cnt[name],icon:t.iconData,...a};
    });
    // Eclipse hidden combo
    if(cnt['Solar']&&cnt['Lunar']){const ec=traitByName['Eclipse']||{};rows.push({name:'Eclipse',count:Math.min(cnt['Solar'],cnt['Lunar']),icon:ec.iconData,on:true,style:'unique',eclipse:true,nextMin:null});}
    rows.sort((a,b)=>(b.on-a.on)||(b.count-a.count)||a.name.localeCompare(b.name));
    return rows;
  }
  function renderBoard(){
    const bd=$('bBoard');bd.innerHTML='';
    cur.champs.forEach((n,i)=>{
      const c=champByName[n]||{};const el=document.createElement('div');el.className='btile b'+(c.cost||1);
      el.innerHTML=`<img src="${c.portrait||''}" alt="${n}" title="${n}"><span class="bx" data-i="${i}">✕</span><div class="bn">${n}</div>`;
      el.querySelector('.bx').addEventListener('click',e=>{e.stopPropagation();cur.champs.splice(i,1);sync();});
      bd.appendChild(el);
    });
    $('bUnitCount').textContent=cur.champs.length+' unit'+(cur.champs.length!==1?'s':'');
    const gold=cur.champs.reduce((s,n)=>s+(champByName[n]?.cost||0),0);
    $('bCostSum').textContent=gold?('◆ '+gold+' gold @1★'):'';
    // traits
    const tr=$('bTraits');tr.innerHTML='';
    computeTraits(cur.champs).forEach(r=>{
      const el=document.createElement('div');
      el.className='btrait '+(r.eclipse?'eclipse ':(r.on?'on ':''))+'tier-'+r.style;
      el.innerHTML=`${r.icon?`<img src="${r.icon}" alt="">`:''}<span><span class="bcnt">${r.count}</span> <span class="btn2">${r.name}</span></span>${r.nextMin?`<span class="bnext">→ ${r.nextMin}</span>`:(r.eclipse?'<span class="bnext">hidden</span>':'')}`;
      tr.appendChild(el);
    });
  }
  function renderPicker(){
    const pk=$('bPicker');pk.innerHTML='';
    const list=DATA.champions.filter(c=>(pCost==='all'||c.cost==+pCost)&&(!pQ||c.name.toLowerCase().includes(pQ)||c.traits.join(' ').toLowerCase().includes(pQ)));
    list.forEach(c=>{
      const picked=cur.champs.includes(c.name);
      const el=document.createElement('div');el.className='pk b'+c.cost+(picked?' picked':'');
      el.innerHTML=`<span class="pkg">${c.cost}</span><span class="pkck">✓</span><img src="${c.portrait||''}" alt="${c.name}"><div class="pkn">${c.name}</div>`;
      el.addEventListener('click',()=>{
        const i=cur.champs.indexOf(c.name);
        if(i>=0)cur.champs.splice(i,1); else cur.champs.push(c.name);
        sync();
      });
      pk.appendChild(el);
    });
  }
  function buildItem(b){
    const el=document.createElement('button');el.className='bitem'+(b.id===cur.id?' active':'');
    el.innerHTML=`<div class="bt">${esc(b.name||'Untitled build')}</div><div class="bs">${b.champs.length} units</div>`;
    el.addEventListener('click',()=>loadBuild(b.id));
    return el;
  }
  function renderSidebar(){
    const l=$('bList');l.innerHTML='';
    folders.forEach(f=>{
      const items=builds.filter(b=>b.folder===f);
      const hdr=document.createElement('div');hdr.className='bfolder'+(collapsed.has(f)?' collapsed':'');
      hdr.innerHTML=`<button class="bfhdr"><span class="bfcaret">▾</span><span class="bfname">${esc(f)}</span><span class="bfcount">${items.length}</span></button><span class="bfdel" title="Delete folder (keeps its builds)">✕</span>`;
      hdr.querySelector('.bfhdr').addEventListener('click',()=>{collapsed.has(f)?collapsed.delete(f):collapsed.add(f);saveCol();renderSidebar();});
      hdr.querySelector('.bfdel').addEventListener('click',e=>{e.stopPropagation();folders=folders.filter(x=>x!==f);builds.forEach(b=>{if(b.folder===f)b.folder='';});if(cur.folder===f){cur.folder='';$('bFolder').value='';}persist();populateFolderSel();renderSidebar();});
      l.appendChild(hdr);
      if(!collapsed.has(f)){const w=document.createElement('div');w.className='bfitems';if(items.length)items.forEach(b=>w.appendChild(buildItem(b)));else w.innerHTML='<div class="blist-empty">empty</div>';l.appendChild(w);}
    });
    const ung=builds.filter(b=>!b.folder||!folders.includes(b.folder));
    if(ung.length){
      if(folders.length){const h=document.createElement('div');h.className='bfolder plain';h.innerHTML='<span class="bfname ung">Ungrouped</span>';l.appendChild(h);}
      ung.forEach(b=>l.appendChild(buildItem(b)));
    }
    if(!builds.length&&!folders.length)l.innerHTML='<div class="blist-empty">No saved builds yet</div>';
  }
  function populateFolderSel(){
    const sel=$('bFolder');
    sel.innerHTML='<option value="">Ungrouped</option>'+folders.map(f=>`<option value="${esc(f)}">${esc(f)}</option>`).join('');
    sel.value=folders.includes(cur.folder)?cur.folder:'';
  }
  function createFolder(){
    const inp=$('bFolderName');const name=inp.value.trim();
    if(!name){inp.focus();return;}
    if(!folders.includes(name))folders.push(name);
    inp.value='';$('bNewFolder').classList.add('hide');
    cur.folder=name;persist();populateFolderSel();renderSidebar();saveDraft();
    msg('Folder “'+name+'” added.');
  }
  function sync(){renderBoard();renderPicker();saveDraft();}
  function loadBuild(id){
    const b=builds.find(x=>x.id===id);if(!b)return;
    cur={id:b.id,name:b.name,champs:b.champs.slice(),notes:b.notes||'',folder:b.folder||''};
    $('bName').value=cur.name;$('bNotes').value=cur.notes;populateFolderSel();$('bDel').classList.remove('hide');
    renderSidebar();sync();document.querySelector('.bmain').scrollIntoView({behavior:'smooth',block:'start'});
  }
  function newBuild(){cur={id:null,name:'',champs:[],notes:'',folder:''};$('bName').value='';$('bNotes').value='';$('bFolder').value='';$('bDel').classList.add('hide');renderSidebar();sync();}
  function saveBuild(){
    cur.name=$('bName').value.trim()||'Untitled build';cur.notes=$('bNotes').value;cur.folder=$('bFolder').value;
    if(!cur.champs.length){msg('Add at least one champion first.');return;}
    if(cur.id){const b=builds.find(x=>x.id===cur.id);if(b)Object.assign(b,{name:cur.name,champs:cur.champs.slice(),notes:cur.notes,folder:cur.folder});}
    else{cur.id=uid();builds.unshift({id:cur.id,name:cur.name,champs:cur.champs.slice(),notes:cur.notes,folder:cur.folder});$('bDel').classList.remove('hide');}
    persist();renderSidebar();msg('Saved “'+cur.name+'”'+(cur.folder?' in “'+cur.folder+'”':'')+'.');
  }
  function delBuild(){if(!cur.id)return;builds=builds.filter(x=>x.id!==cur.id);persist();newBuild();msg('Build deleted.');}
  async function exportBuilds(){
    if(!builds.length){msg('Nothing to export yet.');return;}
    const payload=JSON.stringify({app:'ewc-set18-builds',v:1,builds,folders},null,2);
    let dl=null;try{if(window.claude&&claude.use)dl=await claude.use('downloads');}catch(e){}
    if(dl){try{await dl.save({filename:'set18-builds.json',data:payload});msg('Exported '+builds.length+' builds.');return;}catch(e){}}
    try{await navigator.clipboard.writeText(payload);msg('Copied '+builds.length+' builds to clipboard (paste to save).');}
    catch(e){console.log(payload);msg('Export unavailable here — builds JSON logged to console.');}
  }
  function importBuilds(text){
    let d;try{d=JSON.parse(text)}catch(e){msg('Import failed: not valid JSON.');return;}
    const inc=Array.isArray(d)?d:d.builds;
    if(!Array.isArray(inc)){msg('Import failed: no builds found.');return;}
    if(Array.isArray(d.folders))d.folders.forEach(f=>{if(typeof f==='string'&&f&&!folders.includes(f))folders.push(f);});
    let added=0;
    inc.forEach(b=>{if(b&&Array.isArray(b.champs)){const folder=(typeof b.folder==='string')?b.folder:'';if(folder&&!folders.includes(folder))folders.push(folder);builds.unshift({id:uid(),name:b.name||'Imported build',champs:b.champs.filter(n=>champByName[n]),notes:b.notes||'',folder});added++;}});
    persist();populateFolderSel();renderSidebar();msg('Imported '+added+' build'+(added!==1?'s':'')+'.');
  }
  // wire
  $('bName').addEventListener('input',e=>{cur.name=e.target.value;saveDraft();});
  $('bNotes').addEventListener('input',e=>{cur.notes=e.target.value;saveDraft();});
  $('bSearch').addEventListener('input',e=>{pQ=e.target.value.toLowerCase().trim();renderPicker();});
  $('bCostFilter').addEventListener('click',e=>{const b=e.target.closest('.chip');if(!b)return;pCost=b.dataset.c;[...e.currentTarget.children].forEach(c=>c.setAttribute('aria-pressed',c===b));renderPicker();});
  $('bFolder').addEventListener('change',e=>{cur.folder=e.target.value;saveDraft();});
  $('bFolderAdd').addEventListener('click',()=>{const nf=$('bNewFolder');nf.classList.toggle('hide');if(!nf.classList.contains('hide'))$('bFolderName').focus();});
  $('bFolderCreate').addEventListener('click',createFolder);
  $('bFolderName').addEventListener('keydown',e=>{if(e.key==='Enter'){e.preventDefault();createFolder();}});
  $('bNew').addEventListener('click',newBuild);
  $('bSave').addEventListener('click',saveBuild);
  $('bClear').addEventListener('click',()=>{cur.champs=[];sync();});
  $('bDel').addEventListener('click',delBuild);
  $('bExport').addEventListener('click',exportBuilds);
  $('bImport').addEventListener('click',()=>$('bFile').click());
  $('bFile').addEventListener('change',e=>{const f=e.target.files[0];if(!f)return;const r=new FileReader();r.onload=()=>importBuilds(r.result);r.readAsText(f);e.target.value='';});
  // init
  $('bName').value=cur.name;$('bNotes').value=cur.notes;populateFolderSel();if(cur.id)$('bDel').classList.remove('hide');
  renderSidebar();renderBoard();renderPicker();
})();

/* theme (3-state) */
const btn=document.getElementById('themeBtn'),txt=document.getElementById('themeTxt');
const sysDark=()=>matchMedia('(prefers-color-scheme:dark)').matches;let mode=null;
function apply(){const r=document.documentElement;
  if(mode==null){r.removeAttribute('data-theme');txt.textContent='Auto';btn.firstChild.textContent=sysDark()?'🌙 ':'☀️ ';}
  else{r.setAttribute('data-theme',mode);txt.textContent=mode==='dark'?'Dark':'Light';btn.firstChild.textContent=mode==='dark'?'🌙 ':'☀️ ';}}
btn.addEventListener('click',()=>{const cur=mode==null?(sysDark()?'dark':'light'):mode;mode=cur==='dark'?'light':'dark';apply();});
apply();
</script>'''

open('set18_explorer.html','w',encoding='utf-8').write(HTML.replace('__DATA__',DATA))
print('wrote set18_explorer.html', round(len(HTML)/1048576,2),'MB')
