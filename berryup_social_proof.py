"""Pop-ups de prova social — compras recentes (desktop: canto inferior esquerdo; mobile: superior direito)."""

from __future__ import annotations

import json
import re
from pathlib import Path

DATA_PATH = Path(__file__).resolve().parent / "dados" / "prova-social-compras.json"
ROOT_ID = "berryup-social-proof"
STYLE_ID = "berryup-social-proof-css"
SCRIPT_ID = "berryup-social-proof-script"

# Primeiro aviso: 3–15 s; entre avisos: 8–15 s; visível ~5,5 s
FIRST_DELAY_MIN_MS = 3000
FIRST_DELAY_MAX_MS = 15000
INTERVAL_MIN_MS = 8000
INTERVAL_MAX_MS = 15000
TOAST_VISIBLE_MS = 5500


def load_social_proof_data() -> dict:
    raw = json.loads(DATA_PATH.read_text(encoding="utf-8"))
    nomes = [str(n).strip() for n in raw.get("nomes", []) if str(n).strip()]
    cidades = [str(c).strip() for c in raw.get("cidades", []) if str(c).strip()]
    mensagens = [str(m).strip() for m in raw.get("mensagens", []) if str(m).strip()]
    if not nomes or not cidades or not mensagens:
        raise ValueError(f"Dados inválidos em {DATA_PATH}")
    return {"nomes": nomes, "cidades": cidades, "mensagens": mensagens}


def _js_string_array(items: list[str]) -> str:
    return "[" + ",".join(json.dumps(x, ensure_ascii=False) for x in items) + "]"


SOCIAL_PROOF_CSS = f"""
/* Prova social — compras recentes */
#{ROOT_ID}{{
  position:fixed;left:12px;bottom:16px;z-index:1900;
  display:flex;flex-direction:column-reverse;align-items:flex-start;
  gap:10px;max-width:min(340px,calc(100vw - 24px));pointer-events:none;
  font-family:system-ui,-apple-system,"Segoe UI",Roboto,sans-serif}}
.berryup-sp-toast{{
  pointer-events:auto;display:flex;align-items:flex-start;gap:10px;
  padding:12px 14px 12px 12px;background:#fff;color:#1a1030;
  border-radius:12px;border-left:4px solid #ff6316;
  box-shadow:0 8px 28px rgba(0,0,0,.14),0 2px 8px rgba(255,99,22,.12);
  font-size:clamp(.78rem,2.4vw,.88rem);line-height:1.4;
  opacity:0;transform:translateY(24px);animation:berryupSpIn .45s ease forwards}}
.berryup-sp-toast.is-leaving{{
  animation:berryupSpOut .35s ease forwards}}
.berryup-sp-toast-icon{{
  flex-shrink:0;width:32px;height:32px;border-radius:50%;
  background:linear-gradient(145deg,#fff3eb,#ffe5d6);
  border:1px solid rgba(255,99,22,.25);
  display:flex;align-items:center;justify-content:center;font-size:1rem;line-height:1}}
.berryup-sp-toast-text{{flex:1;min-width:0}}
.berryup-sp-toast-text strong{{color:#ff6316;font-weight:800}}
.berryup-sp-toast-meta{{
  display:block;margin-top:3px;font-size:.72rem;color:#666;font-weight:600}}
@keyframes berryupSpIn{{
  from{{opacity:0;transform:translateY(24px)}}
  to{{opacity:1;transform:translateY(0)}}}}
@keyframes berryupSpOut{{
  from{{opacity:1;transform:translateY(0)}}
  to{{opacity:0;transform:translateY(-12px)}}}}
@keyframes berryupSpInMob{{
  from{{opacity:0;transform:translateY(-18px)}}
  to{{opacity:1;transform:translateY(0)}}}}
@keyframes berryupSpOutMob{{
  from{{opacity:1;transform:translateY(0)}}
  to{{opacity:0;transform:translateY(-14px)}}}}
@media(max-width:800px){{
  #{ROOT_ID}{{
    left:auto!important;right:10px!important;bottom:auto!important;
    top:max(8px,env(safe-area-inset-top,0px))!important;
    align-items:flex-end!important;flex-direction:column!important;
    max-width:min(300px,calc(100vw - 20px))!important}}
  body.berryup-urgency-ready:not(.berryup-wheel-won) #{ROOT_ID},
  body.berryup-urgency-scrolled:not(.berryup-wheel-won) #{ROOT_ID}{{
    top:max(8px,calc(var(--berryup-urgency-h,141px) - 28px))!important}}
  body.berryup-wheel-won #{ROOT_ID}{{
    top:max(118px,calc(env(safe-area-inset-top,0px) + 8px))!important}}
  .berryup-sp-toast{{
    border-left:none!important;border-right:4px solid #ff6316!important;
    animation:berryupSpInMob .45s ease forwards!important}}
  .berryup-sp-toast.is-leaving{{
    animation:berryupSpOutMob .35s ease forwards!important}}
}}
"""


def social_proof_script(data: dict) -> str:
    nomes = _js_string_array(data["nomes"])
    cidades = _js_string_array(data["cidades"])
    mensagens = _js_string_array(data["mensagens"])
    return f"""<script id="{SCRIPT_ID}">(function(){{
var ROOT_ID="{ROOT_ID}";
var NOMES={nomes};
var CIDADES={cidades};
var MENSAGENS={mensagens};
var FIRST_MIN={FIRST_DELAY_MIN_MS};
var FIRST_MAX={FIRST_DELAY_MAX_MS};
var GAP_MIN={INTERVAL_MIN_MS};
var GAP_MAX={INTERVAL_MAX_MS};
var VISIBLE_MS={TOAST_VISIBLE_MS};
var root=null;
var active=null;
var hideTimer=null;
var cycleTimer=null;

function rand(min,max){{return min+Math.random()*(max-min)}}
function pick(arr){{return arr[Math.floor(Math.random()*arr.length)]}}
function esc(s){{
  return String(s).replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;").replace(/"/g,"&quot;");
}}
function formatMsg(){{
  var nome=pick(NOMES);
  var cidade=pick(CIDADES);
  var tpl=pick(MENSAGENS);
  return tpl.replace(/\\{{nome\\}}/g,nome).replace(/\\{{cidade\\}}/g,cidade);
}}
function ensureRoot(){{
  if(root)return root;
  root=document.getElementById(ROOT_ID);
  if(!root){{
    root=document.createElement("div");
    root.id=ROOT_ID;
    root.setAttribute("aria-live","polite");
    root.setAttribute("aria-relevant","additions");
    document.body.appendChild(root);
  }}
  return root;
}}
function removeToast(el){{
  if(!el||!el.parentNode)return;
  el.classList.add("is-leaving");
  setTimeout(function(){{
    if(el.parentNode)el.parentNode.removeChild(el);
    if(active===el)active=null;
  }},360);
}}
function showToast(){{
  ensureRoot();
  if(active)removeToast(active);
  if(hideTimer){{clearTimeout(hideTimer);hideTimer=null;}}
  var msg=formatMsg();
  var el=document.createElement("div");
  el.className="berryup-sp-toast";
  el.setAttribute("role","status");
  el.innerHTML=
    '<span class="berryup-sp-toast-icon" aria-hidden="true">🛒</span>'+
    '<span class="berryup-sp-toast-text">'+esc(msg)+
    '<span class="berryup-sp-toast-meta">há poucos segundos · verificado</span></span>';
  root.appendChild(el);
  active=el;
  hideTimer=setTimeout(function(){{removeToast(el);hideTimer=null;}},VISIBLE_MS);
  scheduleNext();
}}
function scheduleNext(){{
  if(cycleTimer)clearTimeout(cycleTimer);
  var delay=Math.round(rand(GAP_MIN,GAP_MAX));
  cycleTimer=setTimeout(showToast,delay);
}}
function init(){{
  ensureRoot();
  var first=Math.round(rand(FIRST_MIN,FIRST_MAX));
  cycleTimer=setTimeout(showToast,first);
}}
if(document.readyState==="loading")document.addEventListener("DOMContentLoaded",init);
else init();
}})();</script>"""


def social_proof_bundle() -> str:
    data = load_social_proof_data()
    return (
        f'<style id="{STYLE_ID}">{SOCIAL_PROOF_CSS.strip()}</style>'
        f'<div id="{ROOT_ID}" aria-live="polite"></div>'
        + social_proof_script(data)
    )


def inject_social_proof(html: str) -> str:
    if f'id="{SCRIPT_ID}"' in html:
        return html
    marker = "</body>"
    if marker not in html:
        return html
    return html.replace(marker, social_proof_bundle() + marker, 1)


def _strip_old_bundle(html: str) -> str:
    html = re.sub(rf'<style id="{re.escape(STYLE_ID)}"[^>]*>.*?</style>', "", html, flags=re.DOTALL)
    html = re.sub(rf'<div id="{re.escape(ROOT_ID)}"[^>]*></div>', "", html)
    html = re.sub(
        rf'<script id="{re.escape(SCRIPT_ID)}"[^>]*>.*?</script>',
        "",
        html,
        flags=re.DOTALL,
    )
    return html
