"""Fecha o aviso de cookies/LGPD da GreatPages (#gpc-lgpd) ao clicar em OK."""

from __future__ import annotations

COOKIE_SCRIPT_ID = "berryup-cookie-consent"
STORAGE_LGPD_DISMISSED = "berryup_lgpd_dismissed_v1"
GPAGES_LGPD_BANNER_ID = "gpc-lgpd"

COOKIE_CONSENT_SCRIPT = f"""<script id="{COOKIE_SCRIPT_ID}">(function(){{
var SK="{STORAGE_LGPD_DISMISSED}";
var BANNER_ID="{GPAGES_LGPD_BANNER_ID}";
function lgpdDismissed(){{
  try{{if(sessionStorage.getItem(SK)==="1")return true;}}catch(e){{}}
  var c=document.cookie||"";
  return c.indexOf("gpages_lgpd")>=0||c.indexOf("gpages_lgpd_consentimento")>=0;
}}
function persistLgpd(){{
  try{{sessionStorage.setItem(SK,"1");}}catch(e){{}}
  var exp=new Date();
  exp.setFullYear(exp.getFullYear()+1);
  var tail=";path=/;expires="+exp.toUTCString()+";SameSite=Lax";
  document.cookie="gpages_lgpd=1"+tail;
  document.cookie="gpages_lgpd_consentimento=1"+tail;
}}
function closeBanner(){{
  var el=document.getElementById(BANNER_ID);
  if(!el)return;
  el.classList.remove("posicionado");
  el.classList.add("posicionar");
  el.setAttribute("hidden","");
  el.setAttribute("aria-hidden","true");
  el.style.display="none";
  el.style.visibility="hidden";
  el.style.pointerEvents="none";
  persistLgpd();
}}
function onClose(e){{
  if(e){{e.preventDefault();e.stopPropagation();}}
  closeBanner();
}}
function bindBanner(){{
  if(lgpdDismissed()){{closeBanner();return true;}}
  var el=document.getElementById(BANNER_ID);
  if(!el)return false;
  var confirm=document.getElementById("gpc-lgpd_botoes-confirmar");
  var fechar=document.getElementById("gpc-lgpd_fechar");
  if(confirm&&!confirm.getAttribute("data-berryup-bound")){{
    confirm.setAttribute("data-berryup-bound","1");
    confirm.addEventListener("click",onClose,true);
  }}
  if(fechar&&!fechar.getAttribute("data-berryup-bound")){{
    fechar.setAttribute("data-berryup-bound","1");
    fechar.addEventListener("click",onClose,true);
  }}
  el.querySelectorAll(".gpc-lgpd_botoes-botao,button,[role=button]").forEach(function(btn){{
    if(btn.getAttribute("data-berryup-bound"))return;
    var t=(btn.textContent||"").trim();
    if(/^ok\\.?$/i.test(t)||/aceitar/i.test(t)||/entendi/i.test(t)||/confirmar/i.test(t)){{
      btn.setAttribute("data-berryup-bound","1");
      btn.addEventListener("click",onClose,true);
    }}
  }});
  return true;
}}
function watch(){{
  if(bindBanner())return;
  var obs=new MutationObserver(function(){{
    if(bindBanner())obs.disconnect();
  }});
  obs.observe(document.documentElement,{{childList:true,subtree:true}});
  var n=0;
  var iv=setInterval(function(){{
    if(bindBanner()||++n>=100)clearInterval(iv);
  }},200);
}}
function start(){{
  watch();
  window.addEventListener("load",watch);
}}
if(document.readyState==="loading")document.addEventListener("DOMContentLoaded",start);
else start();
}})();</script>"""


def inject_cookie_consent_script(html: str) -> str:
    """Garante que o botão OK do aviso LGPD (GreatPages) fecha o banner."""
    if f'id="{COOKIE_SCRIPT_ID}"' in html:
        return html
    marker = "</body>"
    if marker not in html:
        return html
    return html.replace(marker, COOKIE_CONSENT_SCRIPT + marker, 1)
