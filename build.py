#!/usr/bin/env python3
"""enc.json(암호화된 카탈로그) -> index.html (단일 파일, 비밀번호 잠금 폰 발주 웹앱)."""
import json, pathlib

root = pathlib.Path(__file__).parent
enc = json.load(open(root / "enc.json", encoding="utf-8"))
enc_js = json.dumps({k: enc[k] for k in ("salt", "iv", "ct", "iter")}, ensure_ascii=False)

html = """<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no">
<meta name="robots" content="noindex, nofollow">
<meta name="theme-color" content="#3d6fb4">
<title>백년양말 발주</title>
<style>
  * { box-sizing: border-box; -webkit-tap-highlight-color: transparent; }
  :root { --blue:#3d6fb4; --bg:#eef4fb; --line:#d7e2f0; --ink:#1f2a3a; }
  body { margin:0; font-family:-apple-system,BlinkMacSystemFont,"Apple SD Gothic Neo","Malgun Gothic",sans-serif;
         background:var(--bg); color:var(--ink); padding-bottom:120px; }
  header { position:sticky; top:0; z-index:20; background:var(--blue); color:#fff; padding:12px 14px 10px; }
  header h1 { margin:0; font-size:19px; font-weight:800; letter-spacing:-.5px; }
  header .sub { font-size:11px; opacity:.9; margin-top:2px; }
  .search { position:sticky; top:54px; z-index:19; background:var(--bg); padding:8px 10px; border-bottom:1px solid var(--line); }
  .search input { width:100%; padding:11px 12px; font-size:16px; border:1px solid #c5d3e6; border-radius:10px; outline:none; }
  .list { padding:8px 10px; }
  .card { background:#fff; border:1px solid var(--line); border-radius:12px; margin-bottom:9px; padding:11px 12px; }
  .card.hidden { display:none; }
  .chead { display:flex; align-items:baseline; gap:7px; flex-wrap:wrap; margin-bottom:8px; }
  .pname { font-size:16px; font-weight:800; letter-spacing:-.4px; }
  .badge { font-size:11px; font-weight:700; padding:2px 7px; border-radius:6px; background:#eaf1fb; color:var(--blue); }
  .price { font-size:12px; color:#6b7686; margin-left:auto; font-weight:600; }
  .note { font-size:11px; color:#c0392b; font-weight:700; }
  .crow { display:flex; align-items:center; gap:9px; padding:6px 0; border-top:1px dashed #eef0f3; }
  .crow:first-of-type { border-top:none; }
  .swatch { width:20px; height:20px; border-radius:50%; flex:0 0 auto; border:1px solid #cfd6e0; }
  .cname { font-size:14px; flex:1; }
  .stepper { display:flex; align-items:center; gap:0; }
  .stepper button { width:38px; height:38px; font-size:22px; border:1px solid #c5d3e6; background:#f7faff; color:var(--blue);
                    border-radius:9px; font-weight:700; line-height:1; display:flex; align-items:center; justify-content:center; }
  .stepper button:active { background:#e3edfb; }
  .stepper .qty { width:42px; text-align:center; font-size:16px; font-weight:800; }
  .crow.on .qty { color:var(--blue); }
  .memo input { width:100%; padding:9px 10px; font-size:15px; border:1px solid #c5d3e6; border-radius:9px; }
  .bar { position:fixed; left:0; right:0; bottom:0; z-index:30; background:#fff; border-top:1px solid var(--line);
         padding:10px 12px calc(10px + env(safe-area-inset-bottom)); box-shadow:0 -3px 14px rgba(0,0,0,.07); }
  .bar .sum { font-size:13px; color:#46506b; margin-bottom:7px; font-weight:600; }
  .bar .sum b { color:var(--blue); font-size:15px; }
  .bar .btns { display:flex; gap:8px; }
  .bar button { flex:1; padding:14px; font-size:16px; font-weight:800; border:none; border-radius:11px; }
  .btn-make { background:var(--blue); color:#fff; flex:2; }
  .btn-reset { background:#eef1f5; color:#55607a; }
  .modal { position:fixed; inset:0; z-index:50; background:rgba(20,28,40,.55); display:none; align-items:flex-end; }
  .modal.show { display:flex; }
  .sheet { background:#fff; width:100%; border-radius:16px 16px 0 0; padding:16px 14px calc(16px + env(safe-area-inset-bottom)); max-height:86vh; display:flex; flex-direction:column; }
  .sheet h2 { margin:0 0 4px; font-size:17px; }
  .sheet .cnt { font-size:12px; color:#6b7686; margin-bottom:8px; }
  .sheet textarea { width:100%; flex:1; min-height:200px; font-size:15px; line-height:1.7; padding:11px; border:1px solid #c5d3e6;
                    border-radius:10px; resize:none; font-family:inherit; }
  .sheet .row { display:flex; gap:8px; margin-top:10px; }
  .sheet button { flex:1; padding:14px; font-size:16px; font-weight:800; border:none; border-radius:11px; }
  .btn-copy { background:#2e7d32; color:#fff; }
  .btn-close { background:#eef1f5; color:#55607a; }
  .empty { text-align:center; color:#9aa3b2; padding:40px 0; font-size:14px; }
  .toast { position:fixed; left:50%; bottom:140px; transform:translateX(-50%); background:#1f2a3a; color:#fff;
           padding:11px 18px; border-radius:22px; font-size:14px; z-index:60; opacity:0; transition:opacity .2s; pointer-events:none; }
  .toast.show { opacity:.95; }
  /* 잠금 화면 */
  .lock { position:fixed; inset:0; z-index:100; background:var(--blue); color:#fff; display:flex; flex-direction:column;
          align-items:center; justify-content:center; padding:24px; text-align:center; }
  .lock.hide { display:none; }
  .lock h1 { font-size:24px; margin:0 0 6px; font-weight:800; }
  .lock p { opacity:.9; font-size:13px; margin:0 0 24px; }
  .lock input { width:220px; max-width:80vw; padding:14px; font-size:22px; text-align:center; letter-spacing:6px;
                border:none; border-radius:12px; outline:none; }
  .lock button { margin-top:14px; width:220px; max-width:80vw; padding:14px; font-size:17px; font-weight:800;
                 border:none; border-radius:12px; background:#fff; color:var(--blue); }
  .lock .err { color:#ffd5d5; font-size:13px; height:18px; margin-top:12px; font-weight:700; }
  #app.locked { display:none; }
</style>
</head>
<body>

<div class="lock" id="lock">
  <h1>🧦 백년양말 발주</h1>
  <p>비밀번호를 입력하세요</p>
  <input id="pw" type="password" inputmode="numeric" autocomplete="off" placeholder="••••">
  <button id="unlockBtn">열기</button>
  <div class="err" id="pwErr"></div>
</div>

<div id="app" class="locked">
<header>
  <h1>백년양말 발주서</h1>
  <div class="sub">색상별 수량(죽)을 누르고 → 발주서 만들기 → 복사해서 카톡 전송 · 1죽 = 10켤레</div>
</header>
<div class="search"><input id="q" type="search" placeholder="제품명 검색 (예: 발가락, 중목, 덧신)" autocomplete="off"></div>
<div class="list" id="list"></div>
<div class="empty" id="empty" style="display:none">검색 결과가 없어요</div>

<div class="bar">
  <div class="sum">선택 <b id="sumJuk">0</b>죽 · 예상 <b id="sumWon">0</b>원</div>
  <div class="btns">
    <button class="btn-reset" id="resetBtn">초기화</button>
    <button class="btn-make" id="makeBtn">발주서 만들기</button>
  </div>
</div>

<div class="modal" id="modal">
  <div class="sheet">
    <h2>발주서</h2>
    <div class="cnt" id="modalCnt"></div>
    <textarea id="out" readonly></textarea>
    <div class="row">
      <button class="btn-close" id="closeBtn">닫기</button>
      <button class="btn-copy" id="copyBtn">복사하기</button>
    </div>
  </div>
</div>
<div class="toast" id="toast"></div>
</div>

<script>
const ENC = __ENC__;
let CATALOG = [];

// ---- 복호화 ----
function b64d(s){ const bin=atob(s); const u=new Uint8Array(bin.length); for(let i=0;i<bin.length;i++)u[i]=bin.charCodeAt(i); return u; }
async function decryptCatalog(pass){
  const enc=new TextEncoder();
  const km=await crypto.subtle.importKey("raw", enc.encode(pass), "PBKDF2", false, ["deriveKey"]);
  const key=await crypto.subtle.deriveKey(
    {name:"PBKDF2", salt:b64d(ENC.salt), iterations:ENC.iter, hash:"SHA-256"},
    km, {name:"AES-GCM", length:256}, false, ["decrypt"]);
  const pt=await crypto.subtle.decrypt({name:"AES-GCM", iv:b64d(ENC.iv)}, key, b64d(ENC.ct));
  return JSON.parse(new TextDecoder().decode(pt));
}
// 사이즈가 "M / L" 처럼 여러 개면 사이즈별 카드로 분리 (각각 따로 주문)
function expandSizes(cat){
  const out=[];
  cat.forEach(p=>{
    const parts=String(p.size||"").split("/").map(s=>s.trim()).filter(Boolean);
    if(parts.length<=1){ out.push(p); return; }
    parts.forEach(sz=> out.push(Object.assign({}, p, {size:sz})));
  });
  return out;
}
async function tryUnlock(pass){
  try{ const cat=await decryptCatalog(pass); CATALOG=expandSizes(cat); return true; }
  catch(e){ return false; }
}
function startApp(){
  document.getElementById("lock").classList.add("hide");
  document.getElementById("app").classList.remove("locked");
  render();
}
async function doUnlock(){
  const pass=document.getElementById("pw").value.trim();
  const err=document.getElementById("pwErr");
  err.textContent="";
  if(!pass){ err.textContent="비밀번호를 입력하세요"; return; }
  if(await tryUnlock(pass)){ localStorage.setItem("bny_pass", pass); startApp(); }
  else { err.textContent="비밀번호가 틀렸어요"; document.getElementById("pw").value=""; }
}
document.getElementById("unlockBtn").addEventListener("click", doUnlock);
document.getElementById("pw").addEventListener("keydown", e=>{ if(e.key==="Enter") doUnlock(); });
// 저장된 비번으로 자동 열기
(async ()=>{ const saved=localStorage.getItem("bny_pass"); if(saved && await tryUnlock(saved)) startApp(); })();

// ---- 색상 ----
const COLORS = {
  "스킨":"#e7c4a0","커피":"#6f4b32","블랙":"#262626","검정":"#262626","화이트":"#ffffff","그레이":"#a0a6ad","회색":"#a0a6ad",
  "차콜":"#444a52","오트밀":"#d9cdb6","베이지":"#d8c39c","아이보리":"#f4eedb","네이비":"#22304f","소라":"#a9cdec",
  "민트":"#a9e6cf","스카이":"#86cfe9","핑크":"#f3b3c1","옐로우":"#f1d24f","퍼플":"#9a7cb6","보라":"#9a7cb6","레드":"#d24148",
  "와인":"#7b1f2c","그린":"#3f7d50","브라운":"#7a4a2b","블루":"#3a5bd0","투명블랙":"#3a3a3a",
  "삼선 화이트":"#ffffff","삼선 블랙":"#262626","삼선 차콜":"#444a52"
};
const MULTI = new Set(["색상랜덤","랜덤","혼합","문의"]);
function swatch(c){
  if(MULTI.has(c)) return "background:conic-gradient(#f3b3c1,#f1d24f,#a9e6cf,#86cfe9,#9a7cb6,#f3b3c1)";
  const hex = COLORS[c];
  if(hex) return "background:"+hex;
  return "background:#eef1f5;color:#8a93a3";
}
function isCode(c){ return !MULTI.has(c) && !COLORS[c]; }

const state = {};
const memo = {};
const KEY = (i,c)=> i+"__"+c;
try{ Object.assign(state, JSON.parse(localStorage.getItem("bny_state")||"{}")); }catch(e){}
try{ Object.assign(memo, JSON.parse(localStorage.getItem("bny_memo")||"{}")); }catch(e){}
function save(){ localStorage.setItem("bny_state", JSON.stringify(state)); localStorage.setItem("bny_memo", JSON.stringify(memo)); }
function priceText(p){ return p.priceText || (p.price!=null ? p.price.toLocaleString()+"원" : "문의"); }

function render(){
  const list = document.getElementById("list");
  list.innerHTML = "";
  CATALOG.forEach((p,i)=>{
    const card = document.createElement("div");
    card.className = "card";
    card.dataset.name = p.name + " " + p.size;
    let h = '<div class="chead"><span class="pname">'+p.name+'</span>'
          + '<span class="badge">'+p.size+'</span>'
          + (p.note?'<span class="note">'+p.note+'</span>':'')
          + '<span class="price">'+priceText(p)+' · '+p.origin+'</span></div>';
    if(p.inquiry){
      h += '<div class="memo"><input type="text" data-memo="'+i+'" placeholder="특가양말 문의내용 입력 (수량·종류 등)" value="'+(memo[i]||"").replace(/"/g,"&quot;")+'"></div>';
    } else {
      p.colors.forEach(c=>{
        const q = state[KEY(i,c)]||0;
        h += '<div class="crow'+(q>0?' on':'')+'" data-i="'+i+'" data-c="'+c+'">'
           + '<span class="swatch" style="'+swatch(c)+'"></span>'
           + '<span class="cname">'+(isCode(c)?'색상 '+c:c)+'</span>'
           + '<span class="stepper"><button class="minus">−</button>'
           + '<span class="qty">'+q+'</span><button class="plus">+</button></span></div>';
      });
    }
    card.innerHTML = h;
    list.appendChild(card);
  });
  updateSum();
}

function setQty(i,c,delta){
  const k = KEY(i,c);
  let q = (state[k]||0) + delta;
  if(q<0) q=0;
  if(q===0) delete state[k]; else state[k]=q;
  const row = document.querySelector('.crow[data-i="'+i+'"][data-c="'+c+'"]');
  if(row){ row.querySelector(".qty").textContent=q; row.classList.toggle("on", q>0); }
  save(); updateSum();
}

function updateSum(){
  let juk=0, won=0;
  for(const k in state){
    const q=state[k]; juk+=q;
    const i=+k.split("__")[0]; const p=CATALOG[i];
    if(p && p.price!=null) won += q*10*p.price;
  }
  document.getElementById("sumJuk").textContent = juk;
  document.getElementById("sumWon").textContent = won.toLocaleString();
}

function buildOrder(){
  const lines=[];
  CATALOG.forEach((p,i)=>{
    if(p.inquiry){
      const m=(memo[i]||"").trim();
      if(m) lines.push(p.name+" / 문의: "+m);
      return;
    }
    p.colors.forEach(c=>{
      const q=state[KEY(i,c)]||0;
      if(q>0) lines.push(p.name+" / "+p.size+" / "+c+" / "+q+"죽");
    });
  });
  return lines;
}

document.getElementById("list").addEventListener("click", e=>{
  const btn=e.target.closest("button"); if(!btn) return;
  const row=e.target.closest(".crow"); if(!row) return;
  setQty(+row.dataset.i, row.dataset.c, btn.classList.contains("plus")?1:-1);
});
document.getElementById("list").addEventListener("input", e=>{
  const m=e.target.dataset.memo;
  if(m!==undefined){ memo[m]=e.target.value; save(); }
});
document.getElementById("q").addEventListener("input", e=>{
  const t=e.target.value.trim().toLowerCase();
  let shown=0;
  document.querySelectorAll(".card").forEach(c=>{
    const hit = !t || c.dataset.name.toLowerCase().includes(t);
    c.classList.toggle("hidden", !hit); if(hit) shown++;
  });
  document.getElementById("empty").style.display = shown? "none":"block";
});

const modal=document.getElementById("modal");
document.getElementById("makeBtn").addEventListener("click", ()=>{
  const lines=buildOrder();
  if(!lines.length){ toast("선택된 품목이 없어요"); return; }
  document.getElementById("out").value = lines.join("\\n");
  document.getElementById("modalCnt").textContent = lines.length+"개 품목";
  modal.classList.add("show");
});
document.getElementById("closeBtn").addEventListener("click", ()=> modal.classList.remove("show"));
modal.addEventListener("click", e=>{ if(e.target===modal) modal.classList.remove("show"); });
document.getElementById("copyBtn").addEventListener("click", async ()=>{
  const ta=document.getElementById("out");
  try{ await navigator.clipboard.writeText(ta.value); toast("복사됐어요! 카톡에 붙여넣으세요"); }
  catch(e){ ta.removeAttribute("readonly"); ta.select(); document.execCommand("copy"); ta.setAttribute("readonly",""); toast("복사됐어요!"); }
});
document.getElementById("resetBtn").addEventListener("click", ()=>{
  if(!confirm("전체 수량을 0으로 초기화할까요?")) return;
  for(const k in state) delete state[k];
  for(const k in memo) delete memo[k];
  save(); render();
});

let toastT;
function toast(msg){
  const el=document.getElementById("toast"); el.textContent=msg; el.classList.add("show");
  clearTimeout(toastT); toastT=setTimeout(()=>el.classList.remove("show"), 1900);
}
</script>
</body>
</html>
"""

html = html.replace("__ENC__", enc_js)
(root / "index.html").write_text(html, encoding="utf-8")
print("index.html written:", len((root / "index.html").read_text(encoding="utf-8")), "bytes (encrypted catalog)")
