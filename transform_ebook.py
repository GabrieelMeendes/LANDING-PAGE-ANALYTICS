"""Adapta a landing Peach Up de produto físico para venda de e-book."""
from pathlib import Path
import math
import re

from berryup_cookies import inject_cookie_consent_script
from berryup_social_proof import inject_social_proof
from berryup_wheel import inject_berryup_wheel

CHECKOUT = "https://pay.cakto.com.br/7xpxsf5_902702"
HERO_IMG_OLD = (
    "https://files.greatpages.com.br/arquivos/paginas_editor/386522-2216fe3cca5af4344fbf26f9b7e7f908.png"
)
HERO_IMG_NEW = "assets/hero-berry-up.png"
HERO_POT_EID = "e_1002625_1_173566432642631883"
HERO_WOMAN_EID = "e_1002625_1_173566432642696494"
POT_IMG_OLD = (
    "https://files.greatpages.com.br/arquivos/paginas_editor/386522-25ba58276bb95d57a554e49d38487d1f.webp"
)
POT_IMG_NEW = "assets/pot-sem-texto.webp"
CLINICAL_IMG_OLD = (
    "https://files.greatpages.com.br/arquivos/paginas_editor/386522-7158090f878e8fd863d4260deb25086f.png"
)
CLINICAL_IMG_NEW = "assets/clinical-berry-up.png"
CLINICAL_IMG_EID = "e_1002625_1_17307234956728bea7d10a4634604284"

LOGO_HTML_OLD = (
    '<div id="e_1002625_1_173566432642603045" ll_src="https://files.greatpages.com.br/arquivos/paginas_editor/386522-7986bc54f585bd686727cbafa1a9a8f7.png" ll_src_mobile="https://files.greatpages.com.br/arquivos/paginas_editor/386522-7986bc54f585bd686727cbafa1a9a8f7.png" class="gpc-e e_imagem dd dm e_1002625_1_173566432642603045 se_imagem"><div class="c imagem e_imagem"></div></div>'
)
LOGO_HTML_NEW = (
    '<div id="e_1002625_1_173566432642603045" class="gpc-e e_titulo dd dm e_1002625_1_173566432642603045"><div class="c e_titulo se_fonte"><h1><span>Berry Up</span></h1></div></div>'
)
FOOTER_LOGO_HTML_OLD = (
    '<div id="e_1002625_1_17307234956728bea7c94af486216338" ll_src="https://files.greatpages.com.br/arquivos/paginas_editor/386522-7986bc54f585bd686727cbafa1a9a8f7.png" ll_src_mobile="https://files.greatpages.com.br/arquivos/paginas_editor/386522-7986bc54f585bd686727cbafa1a9a8f7.png" class="gpc-e e_imagem dd dm e_1002625_1_17307234956728bea7c94af486216338 se_imagem"><div class="c imagem e_imagem"></div></div>'
)
FOOTER_LOGO_HTML_NEW = (
    '<div id="e_1002625_1_17307234956728bea7c94af486216338" class="gpc-e e_titulo dd dm e_1002625_1_17307234956728bea7c94af486216338"><div class="c e_titulo se_fonte"><h2><span>BERRY UP</span></h2></div></div>'
)
FOOTER_ADDRESS_RE = re.compile(
    r'<div id="e_1002625_1_17307234956728bea829440424203792" class="gpc-e e_texto dd dm e_1002625_1_17307234956728bea829440424203792"><div class="c e_texto se_fonte"><p><span>.*?</span></p></div></div>',
    re.DOTALL,
)
CAIXA_REMOVE = (
    '<div id="e_1002625_1_17307234956728bea7ca2c1685897819" class="gpc-e e_caixa dd dm e_1002625_1_17307234956728bea7ca2c1685897819"><div class="c borda_igual e_caixa"></div></div>'
)
IMG_REMOVE = (
    '<div id="e_1002625_1_17307234956728bea7e1289253492220" ll_src="https://files.greatpages.com.br/arquivos/paginas_editor/386522-6cb62e365aa4d2896e6ddb5f3818be82.png" ll_src_mobile="https://files.greatpages.com.br/arquivos/paginas_editor/386522-6cb62e365aa4d2896e6ddb5f3818be82.png" class="gpc-e e_imagem esconder_mobile dd e_1002625_1_17307234956728bea7e1289253492220 se_imagem"><div class="c imagem e_imagem"></div></div>'
)
VIDEO_REMOVE = (
    '<div id="e_1002625_1_17307234956728bea81b4e8524656078" ll_src="https://www.youtube.com/embed/HlIurLo_SvE?autoplay=0&controls=1&playsinline=1&showinfo=0&rel=0" class="gpc-e e_video dd dm e_1002625_1_17307234956728bea81b4e8524656078 se_video"><div class="carregando"></div></div>'
)
TITULO_DEPOIMENTO_REMOVE = (
    '<div id="e_1002625_1_17307234956728bea7e14fa031033880" class="gpc-e e_titulo dd dm e_1002625_1_17307234956728bea7e14fa031033880"><div class="c e_titulo se_fonte"><h2><span>Veja o depoimento<br>de uma cliente</span></h2></div></div>'
)

PAGE_BG_BLOCKS = (
    "b_1002625_1_173566432642604808",
    "b_1002625_1_17307234956728bea7c7c35",
)
BERRYUP_ORANGE = "#ff6316"
BERRYUP_YELLOW_HEADLINE = "#FFE600"
CLINICAL_BLOCK_ID = "b_1002625_1_17307234956728bea7c7c35"
CLINICAL_TITLE_EID = "e_1002625_1_17307234956728bea7d084d783509482"
URGENCY_BLOCK_ID = "b_1002625_1_17307234956728bea7c7c12"
URGENCY_SHOW_DELAY_SEC = 10
CLINICAL_VIDEO_SRC = "VIDEOS/AD4.mp4"
CLINICAL_YOUTUBE_EMBED = "https://www.youtube.com/embed/HlIurLo_SvE?rel=0&modestbranding=1&playsinline=1"
UTMIFY_SCRIPT_SRC = "https://cdn.utmify.com.br/scripts/utmify.js"
META_PIXEL_ID = "969268506077683"
GUARANTEE_FOOTER_EIDS = (
    "e_1002625_1_173566432642628699",
    "e_1002625_1_17307234956728bea7d9524815599139",
    "e_1002625_1_17307234956728bea7cf917054800283",
    "e_1002625_1_174828414165541607",
)


def guarantee_footer_css() -> str:
    """Rodapé 'Resultados garantidos…' — era 8px no GreatPages."""
    blocks = ",".join(f"#{eid}" for eid in GUARANTEE_FOOTER_EIDS)
    inner = ",".join(f"#{eid} .c" for eid in GUARANTEE_FOOTER_EIDS)
    spans = ",".join(f"#{eid} .c h4 span" for eid in GUARANTEE_FOOTER_EIDS)
    return f"""
{blocks}{{
  height:auto!important;width:auto!important;max-width:min(300px,44vw)!important;
  z-index:1520!important;text-align:center!important}}
{inner},{spans}{{
  font-size:clamp(11px,1.9vw,13px)!important;line-height:1.45!important;letter-spacing:.01em!important;
  text-align:center!important;display:block!important}}
@media(max-width:800px){{
{blocks}{{max-width:min(92vw,340px)!important}}
{inner},{spans}{{font-size:clamp(12px,3vw,14px)!important}}
}}
"""


def clinical_video_html() -> str:
    """MP4 local se existir; senão iframe YouTube (vídeo original da seção)."""
    if Path(CLINICAL_VIDEO_SRC).is_file():
        return (
            '<div id="berryup-clinical-video" class="berryup-clinical-video">'
            f'<video controls playsinline preload="metadata">'
            f'<source src="{CLINICAL_VIDEO_SRC}" type="video/mp4">'
            "</video></div>"
        )
    return (
        '<div id="berryup-clinical-video" class="berryup-clinical-video">'
        f'<iframe src="{CLINICAL_YOUTUBE_EMBED}" title="Testes clínicos Berry Up" '
        'allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" '
        'allowfullscreen loading="lazy"></iframe></div>'
    )

CLINICAL_MOBILE_CSS = f"""
@media(max-width:800px){{
#{CLINICAL_IMG_EID}{{display:none!important;visibility:hidden!important;height:0!important;overflow:hidden!important;pointer-events:none!important}}
#b_1002625_1_17307234956728bea7c7c35 .gpc-e.e_texto.dd.dm{{max-width:100%!important;width:min(100%,calc(100vw - 32px))!important}}
}}
"""

EBOOK_CSS = """
/* BerryUp — oferta e-book */
@import url('https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,600;9..144,700&display=swap');
body.berryup-urgency-ready #b_1002625_1_17307234956728bea7c7c12,
body.berryup-urgency-scrolled #b_1002625_1_17307234956728bea7c7c12{
  display:block!important;position:fixed!important;top:0!important;left:0!important;right:0!important;
  width:100%!important;z-index:2000!important;margin:0!important}
body.berryup-urgency-ready:not(.berryup-wheel-won) #site{padding-top:var(--berryup-urgency-h,141px)}
html,body{background-color:#ff6316!important;background-image:none!important}
#site{background-color:#ff6316!important}
#b_1002625_1_173566432642604808,#b_1002625_1_17307234956728bea7c7c35{background-image:none!important;background-color:#ff6316!important;background-size:auto!important}
/* Hero — textos acima da arte; só o título Berry Up maior */
#b_1002625_1_173566432642604808 .centralizar .gpc-e.e_titulo,
#b_1002625_1_173566432642604808 .centralizar .gpc-e.e_texto,
#b_1002625_1_173566432642604808 .centralizar .gpc-e.e_botao,
#b_1002625_1_173566432642604808 .centralizar .gpc-e.e_caixa{z-index:1500!important}
#e_1002625_1_173566432642631883{display:none!important;visibility:hidden!important;pointer-events:none!important}
#e_1002625_1_173566432642696494{z-index:1450!important}
#e_1002625_1_173566432642603045{left:-132px!important;top:108px!important;width:auto!important;height:auto!important;max-width:min(480px,48vw)!important;z-index:1501!important}
#e_1002625_1_173566432642603045 .c h1{margin:0;padding:0;line-height:0.95;height:auto;display:flex;align-items:flex-start;justify-content:flex-start}
#e_1002625_1_173566432642603045 .c h1 span{color:#fff!important;font-family:"Fraunces",Georgia,"Times New Roman",serif!important;font-weight:700;font-size:clamp(3.25rem,6.5vw,5.5rem)!important;letter-spacing:-0.02em;white-space:nowrap;text-shadow:0 3px 14px rgba(0,0,0,.18);line-height:1}
#e_1002625_1_173566432642615795{
  top:176px!important;width:min(720px,52vw)!important;height:auto!important;
  line-height:1.25!important}
#e_1002625_1_173566432642615795 .c p,#e_1002625_1_173566432642615795 .c p b{
  white-space:normal!important;line-height:1.22!important;margin:0!important}
#e_1002625_1_173566432642658588{
  top:258px!important;height:auto!important;line-height:1.18!important}
#e_1002625_1_173566432642658588 .c h1,
#e_1002625_1_173566432642658588 .c h1 span{
  line-height:1.12!important;margin:0!important}
/* hero mobile fino — regras completas em BERRYUP_MOBILE_CSS */
#e_1002625_1_174828414165582009{top:34.0509px!important}
#e_1002625_1_174828414165585672{top:83.9034px!important}
@media(max-width:800px){#e_1002625_1_174828414165582009{top:19.8906px!important}#e_1002625_1_174828414165585672{top:101px!important}}
#e_1002625_1_17307234956728bea7c94af486216338 .c h2{margin:0;padding:0;line-height:1;height:100%;display:flex;align-items:center}
#e_1002625_1_17307234956728bea7c94af486216338 .c h2 span{font-family:system-ui,-apple-system,"Segoe UI",Roboto,sans-serif;font-weight:800;font-size:22px;letter-spacing:.12em;white-space:nowrap;color:#ff6316;text-transform:uppercase}
#e_1002625_1_17307234956728bea7d10a4634604284 .c .imagem_fundo{background-size:contain!important;background-position:center center!important}
#b_1002625_1_17307234956728bea7c7c35 .centralizar{position:relative!important}
#berryup-clinical-video{position:absolute!important;left:32px!important;top:110px!important;width:min(440px,44vw)!important;max-width:480px!important;z-index:220!important;display:block!important;visibility:visible!important;opacity:1!important;border-radius:16px;overflow:hidden;box-shadow:0 16px 48px rgba(0,0,0,.22);background:#000}
#berryup-clinical-video video,#berryup-clinical-video iframe{width:100%!important;display:block!important;border:0;vertical-align:top}
#berryup-clinical-video iframe{aspect-ratio:16/9;min-height:248px;height:auto}
#berryup-clinical-video video{height:auto}
@media(min-width:801px){#b_1002625_1_17307234956728bea7c7c35 .centralizar{min-height:520px}}
@media(max-width:800px){#berryup-clinical-video{position:relative!important;left:auto!important;top:auto!important;width:min(100%,420px)!important;max-width:none!important;margin:16px auto 28px!important}}
#b_1002625_1_17307234956728bea7c7c2e{overflow:visible!important}
@media(max-width:800px){{
#b_1002625_1_17307234956728bea7c7c2e,
#b_1002625_1_17307234956728bea7c7c2e .centralizar,
#b_1002625_1_17307234956728bea7c7c2e .gpc-b_sobreposicao{{
  display:none!important;visibility:hidden!important;height:0!important;
  min-height:0!important;max-height:0!important;overflow:hidden!important;
  margin:0!important;padding:0!important;pointer-events:none!important}}
}}
#b_1002625_1_174828442056623927{display:none!important}
#berryup-ebook-preview,#berryup-ebook-oferta{font-family:system-ui,-apple-system,"Segoe UI",Roboto,sans-serif;box-sizing:border-box}
#berryup-ebook-preview *,#berryup-ebook-oferta *{box-sizing:border-box}
#berryup-ebook-preview{background:linear-gradient(180deg,#fff8f3 0%,#fff 45%);padding:48px 20px 32px}
#berryup-ebook-preview .be-wrap{max-width:1100px;margin:0 auto}
#berryup-ebook-preview .be-head{text-align:center;margin-bottom:36px}
#berryup-ebook-preview .be-head h2{margin:0 0 10px;font-size:clamp(1.55rem,4.2vw,2.05rem);color:#2d2d2d;font-weight:800}
#berryup-ebook-preview .be-head p{margin:0;color:#444;font-size:clamp(1.05rem,2.8vw,1.12rem);max-width:560px;margin-inline:auto;line-height:1.55}
#berryup-ebook-preview .be-grid{display:grid;grid-template-columns:minmax(220px,280px) 1fr;gap:32px;align-items:center}
@media(max-width:768px){#berryup-ebook-preview .be-grid{grid-template-columns:1fr;justify-items:center;text-align:center}}
.be-cover{position:relative;width:min(300px,88vw);perspective:900px}
.be-cover-book{width:100%;aspect-ratio:527/746;border-radius:8px 14px 14px 8px;background:#fff;box-shadow:0 24px 48px rgba(255,99,22,.35),0 8px 20px rgba(0,0,0,.12);transform:rotateY(-8deg);padding:0;display:block;overflow:hidden;color:#fff}
.be-cover-book::before{content:"";position:absolute;inset:0;border-radius:inherit;background:linear-gradient(90deg,rgba(0,0,0,.12) 0%,transparent 18%);pointer-events:none}
.be-cover-book img{width:100%;height:100%;display:block;object-fit:cover;border-radius:inherit}
.be-cover-badge,.be-cover-book h3,.be-cover-book p{display:none!important}
.be-pages{display:grid;grid-template-columns:repeat(3,1fr);gap:14px}
@media(max-width:900px){.be-pages{grid-template-columns:1fr;max-width:360px;margin:0 auto}}
.be-page{background:#fff;border-radius:12px;padding:18px 16px;box-shadow:0 8px 28px rgba(255,99,22,.12);border:1px solid #ffe5d6;min-height:140px;display:flex;flex-direction:column;gap:8px}
.be-page-num{font-size:.78rem;font-weight:700;color:#ff6316;letter-spacing:.06em;text-transform:uppercase}
.be-page h4{margin:0;font-size:1.05rem;color:#333;line-height:1.3}
.be-page p{margin:0;font-size:.92rem;color:#555;line-height:1.5;flex:1}
.be-page-preview{height:52px;border-radius:6px;background:linear-gradient(135deg,#fff5ee,#ffe8d9);margin-top:4px;position:relative;overflow:hidden}
.be-page-preview::after{content:"";position:absolute;left:12px;right:12px;top:10px;height:6px;background:rgba(255,99,22,.2);border-radius:3px;box-shadow:0 14px 0 rgba(255,99,22,.12),0 28px 0 rgba(255,99,22,.08)}
#berryup-ebook-oferta{background:rgb(255,99,22);padding:44px 20px 52px}
#berryup-ebook-oferta .beo-wrap{max-width:560px;margin:0 auto;text-align:center;color:#fff}
#berryup-ebook-oferta .beo-tag{display:inline-block;background:rgba(255,255,255,.22);padding:8px 16px;border-radius:20px;font-size:.88rem;font-weight:800;letter-spacing:.06em;margin-bottom:16px}
#berryup-ebook-oferta h2{margin:0 0 10px;font-size:clamp(1.55rem,4.5vw,2.05rem);font-weight:800;line-height:1.2}
#berryup-ebook-oferta .beo-sub{opacity:.98;margin:0 0 26px;font-size:clamp(1.05rem,2.8vw,1.15rem);line-height:1.5;max-width:480px;margin-inline:auto}
#berryup-ebook-oferta .beo-card{background:#fff;color:#1a1a1a;border-radius:18px;padding:32px 28px;box-shadow:0 16px 40px rgba(0,0,0,.18);text-align:left}
#berryup-ebook-oferta .beo-card h3{margin:0 0 10px;font-size:clamp(1.25rem,3.6vw,1.4rem);color:#ff6316;line-height:1.25}
#berryup-ebook-oferta .beo-card .beo-desc{margin:0 0 20px;font-size:clamp(1rem,2.6vw,1.08rem);color:#444;line-height:1.55}
#berryup-ebook-oferta .beo-price{display:flex;flex-wrap:wrap;align-items:baseline;gap:10px 14px;margin-bottom:20px}
#berryup-ebook-oferta .beo-price .old{font-size:1.05rem;color:#888;text-decoration:line-through;display:none!important}
body.berryup-wheel-won #berryup-ebook-oferta .beo-price .old{display:inline!important}
#berryup-ebook-oferta .beo-price .now{font-size:clamp(2.15rem,7vw,2.65rem);font-weight:800;color:#ff6316;line-height:1}
#berryup-ebook-oferta .beo-price .inst{font-size:clamp(.95rem,2.4vw,1.05rem);color:#444;font-weight:600}
#berryup-ebook-oferta .beo-list{list-style:none;margin:0 0 26px;padding:0}
#berryup-ebook-oferta .beo-list li{padding:11px 0 11px 32px;position:relative;font-size:clamp(1rem,2.6vw,1.08rem);line-height:1.45;color:#333;border-bottom:1px solid #eee}
#berryup-ebook-oferta .beo-list li:last-child{border:0}
#berryup-ebook-oferta .beo-list li::before{content:"✓";position:absolute;left:0;font-size:1.15em;color:#ff6316;font-weight:800}
#berryup-ebook-oferta .beo-cta{display:block;width:100%;padding:18px 28px;background:#FFF133!important;background-image:none!important;color:#1a1a1a!important;text-decoration:none!important;border-radius:999px;font-weight:800;font-size:clamp(1.12rem,3.6vw,1.3rem);text-align:center;box-shadow:0 4px 14px rgba(0,0,0,.14);transition:transform .15s,box-shadow .15s,filter .15s;border:none;min-height:56px;line-height:1.2;text-shadow:none}
#berryup-ebook-oferta .beo-cta:hover{transform:translateY(-1px);filter:brightness(1.03);box-shadow:0 6px 18px rgba(0,0,0,.16)}
#berryup-ebook-oferta .beo-secure{margin:16px 0 0;font-size:clamp(.9rem,2.4vw,.98rem);color:#666;text-align:center;line-height:1.4}
#berryup-ebook-oferta a.beo-cta .berryup-cta-tag,
#berryup-ebook-oferta a.beo-cta .berryup-cta-tag *{
  font-size:clamp(.9rem,2.8vw,1.02rem)!important;padding:5px 14px!important}
#berryup-ebook-oferta a.beo-cta .berryup-cta-main,
#berryup-ebook-oferta a.beo-cta .berryup-cta-main-text{
  font-size:clamp(1.15rem,3.8vw,1.35rem)!important}
@media(max-width:800px){
#berryup-ebook-oferta{padding:40px 16px 48px!important}
#berryup-ebook-oferta .beo-wrap{max-width:100%!important;padding:0 4px}
#berryup-ebook-oferta .beo-card{padding:28px 22px!important}
#berryup-ebook-oferta .beo-list li{padding:12px 0 12px 34px!important}
}
"""

BERRYUP_MOBILE_CSS = """
/* BerryUp — correções mobile (≤800px, alinhado ao css_mobile GreatPages) */
@media(max-width:800px){
html,body,#site{overflow-x:hidden!important;max-width:100vw}
#b_1002625_1_173566432642604808{height:auto!important;min-height:0!important;padding-bottom:20px!important}
#b_1002625_1_173566432642604808 .centralizar{
  min-height:0!important;height:auto!important;position:relative!important;padding-bottom:12px!important}
#e_1002625_1_173566432642603045{
  left:50%!important;top:clamp(12px,3vw,20px)!important;width:auto!important;max-width:92vw!important;
  height:auto!important;transform:translateX(-50%)!important;z-index:1512!important}
#e_1002625_1_173566432642603045 .c h1{justify-content:center!important;height:auto!important}
#e_1002625_1_173566432642603045 .c h1 span{
  white-space:normal!important;text-align:center!important;
  font-size:clamp(1.85rem,8.5vw,2.75rem)!important;line-height:1.05!important}
#e_1002625_1_173566432642615795{
  left:50%!important;top:clamp(52px,14vw,78px)!important;width:min(94vw,420px)!important;
  max-width:94vw!important;height:auto!important;transform:translateX(-50%)!important;z-index:1511!important}
#e_1002625_1_173566432642615795 .c,.e_1002625_1_173566432642615795 .c p{text-align:center!important}
#e_1002625_1_173566432642615795 .c p,#e_1002625_1_173566432642615795 .c p b{
  white-space:normal!important;line-height:1.25!important;margin:0!important}
#e_1002625_1_173566432642615795 .c p b{
  font-size:clamp(1rem,4.2vw,1.35rem)!important;display:block!important}
#e_1002625_1_173566432642658588{
  left:50%!important;top:clamp(126px,33vw,156px)!important;width:min(92vw,362px)!important;
  max-width:92vw!important;height:auto!important;transform:translateX(-50%)!important;z-index:1510!important}
#e_1002625_1_173566432642658588 .c h1,.e_1002625_1_173566432642658588 .c h1 span{
  text-align:center!important;line-height:1.15!important}
#e_1002625_1_173566432642658588 .c h1 span{
  font-size:clamp(1.25rem,5.8vw,1.65rem)!important;white-space:normal!important}
#e_1002625_1_173566432642696494{
  left:50%!important;top:clamp(248px,58vw,318px)!important;
  width:clamp(300px,92vw,440px)!important;height:clamp(360px,88vw,520px)!important;
  max-width:94vw!important;transform:translateX(-50%)!important;z-index:1240!important}
#e_1002625_1_173566432642696494 .c{width:100%!important;height:100%!important}
#e_1002625_1_173566432642696494 .c .imagem_fundo{
  width:100%!important;height:100%!important;
  background-size:contain!important;background-position:center bottom!important;background-repeat:no-repeat!important}
#b_1002625_1_17307234956728bea7c7c35{height:auto!important;min-height:0!important;padding-bottom:24px!important}
#b_1002625_1_17307234956728bea7c7c35 .centralizar{
  min-height:920px!important;padding-bottom:32px!important;box-sizing:border-box!important}
#berryup-clinical-video{
  position:relative!important;left:auto!important;top:auto!important;
  width:min(calc(100% - 24px),400px)!important;margin:20px auto 24px!important;display:block!important}
#berryup-clinical-video iframe{min-height:200px!important}
#berryup-ebook-preview{padding:32px 14px 24px!important}
#berryup-ebook-preview .be-head h2{font-size:clamp(1.5rem,5.5vw,1.85rem)!important}
#berryup-ebook-preview .be-head p{font-size:1.08rem!important}
.be-page h4{font-size:1.08rem!important}
.be-page p{font-size:.98rem!important}
#berryup-ebook-oferta .beo-card h3{font-size:1.32rem!important}
#berryup-ebook-oferta .beo-card .beo-desc{font-size:1.06rem!important}
#berryup-ebook-oferta .beo-list li{font-size:1.05rem!important}
#berryup-ebook-oferta .beo-price .now{font-size:2.5rem!important}
#berryup-ebook-oferta .beo-secure{font-size:.95rem!important}
.be-cover{width:min(240px,78vw)!important}
}
@media(max-width:480px){
#b_1002625_1_173566432642604808,#b_1002625_1_173566432642604808 .centralizar{
  min-height:0!important;height:auto!important}
#e_1002625_1_173566432642696494{
  top:clamp(236px,60vw,288px)!important;
  width:clamp(280px,90vw,400px)!important;height:clamp(340px,92vw,460px)!important}
}
@media(min-width:481px) and (max-width:800px){
#e_1002625_1_173566432642696494{
  width:clamp(320px,90vw,440px)!important;height:clamp(380px,86vw,520px)!important}
}
"""

EBOOK_HTML = f"""
<div id="berryup-ebook-preview">
<div class="be-wrap">
<div class="be-head">
<h2>Conheça o método Bumbum Up.</h2>
<p>O mesmo protocolo que milhares de mulheres usaram para pele mais lisa, firme e livre da aparência da celulite — agora em formato de e-book, para você aplicar em casa.</p>
</div>
<div class="be-grid">
<div class="be-cover">
<div class="be-cover-badge">PDF + bônus</div>
<div class="be-cover-book">
<img src="assets/capa_bumbum.png" alt="Capa do e-book Metodo Bumbum Up" loading="lazy">
<h3>Método Bumbum Up</h3>
<p>7 dias para resgatar sua autoconfiança · BERRY UP</p>
</div>
</div>
<div class="be-pages">
<div class="be-page">
<span class="be-page-num">Cap. 01</span>
<h4>Entenda a celulite</h4>
<p>Como funciona, mitos e o que realmente reduz a aparência da pele.</p>
<div class="be-page-preview"></div>
</div>
<div class="be-page">
<span class="be-page-num">Cap. 04</span>
<h4>Rotina de 7 dias</h4>
<p>Passo a passo diário com massagens e hábitos que potencializam os resultados.</p>
<div class="be-page-preview"></div>
</div>
<div class="be-page">
<span class="be-page-num">Cap. 07</span>
<h4>Protocolo firmador</h4>
<p>Técnicas para tonificar, reduzir medidas e deixar a pele mais uniforme.</p>
<div class="be-page-preview"></div>
</div>
</div>
</div>
</div>
</div>
<div id="berryup-ebook-oferta">
<div class="beo-wrap">
<span class="beo-tag">ACESSO IMEDIATO</span>
<h2>Garanta seu e-book agora</h2>
<p class="beo-sub">Download instantâneo após a confirmação do pagamento. Leia no celular, tablet ou computador.</p>
<div class="beo-card">
<h3>Guia Completo Bumbum Up</h3>
<p class="beo-desc">Método digital com o passo a passo para os mesmos resultados citados nesta página — sem depender de envio ou estoque.</p>
<div class="beo-price">
<span class="old">De R$ 97,00</span>
<span class="now">R$ 38,80</span>
<span class="inst">60% OFF liberado hoje</span>
</div>
<ul class="beo-list">
<li>Acesso imediato e vitalício ao guia atualizado</li>
<li>Passo a passo de 7 dias para aplicar na sua rotina</li>
<li>Guia completo do creme Bumbum Up</li>
<li>Dicas concretas de como ter um corpo saudável</li>
</ul>
<a class="beo-cta" href="{CHECKOUT}" target="_blank" rel="noopener">Garantir meu e-book</a>
<p class="beo-secure">🔒 Pagamento 100% seguro · Satisfação garantida</p>
</div>
</div>
</div>
"""

CONVERSION_CSS = """
/* BerryUp conversion-first landing */
body.berryup-conversion-page{background:#fff7f1!important}
body.berryup-conversion-page #site{
  position:absolute!important;left:-99999px!important;top:auto!important;width:1px!important;height:1px!important;
  overflow:hidden!important;opacity:0!important;pointer-events:none!important
}
#berryup-conversion{font-family:system-ui,-apple-system,"Segoe UI",Roboto,Arial,sans-serif;color:#231914;background:#fff7f1;line-height:1.45}
#berryup-conversion *{box-sizing:border-box}
#berryup-conversion a{text-decoration:none}
.bc-topbar{position:sticky;top:0;z-index:5000;background:#231914;color:#fff;padding:8px 14px;text-align:center;font-weight:800;font-size:14px;letter-spacing:.01em}
.bc-topbar b{color:#fff133}
.bc-wrap{width:min(1120px,calc(100% - 32px));margin:0 auto}
.bc-hero{background:linear-gradient(135deg,#ff6316 0%,#ff7d2d 48%,#ffb238 100%);color:#fff;overflow:hidden}
.bc-hero-grid{display:grid;grid-template-columns:minmax(0,1.02fr) minmax(280px,.86fr);gap:28px;align-items:center;min-height:680px;padding:34px 0 54px}
.bc-brand{font-weight:900;font-size:18px;letter-spacing:.16em;text-transform:uppercase;margin-bottom:38px;color:#fff}
.bc-eyebrow{display:inline-flex;align-items:center;gap:8px;background:rgba(255,255,255,.18);border:1px solid rgba(255,255,255,.32);border-radius:999px;padding:8px 14px;font-weight:900;font-size:13px;text-transform:uppercase;letter-spacing:.05em;margin-bottom:18px}
.bc-hero h1{font-size:clamp(38px,5.8vw,70px);line-height:.98;margin:0 0 18px;font-weight:950;letter-spacing:0;max-width:720px}
.bc-hero h1 span{color:#fff133}
.bc-sub{font-size:clamp(18px,2vw,23px);line-height:1.42;max-width:650px;margin:0 0 22px;color:#fffef9;font-weight:650}
.bc-bullets{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:10px;margin:24px 0 24px;max-width:650px}
.bc-bullet{background:rgba(255,255,255,.16);border:1px solid rgba(255,255,255,.26);border-radius:8px;padding:12px 12px;font-weight:800;font-size:14px;color:#fff}
.bc-cta-row{display:flex;flex-wrap:wrap;align-items:center;gap:12px;margin:26px 0 14px}
.bc-cta{position:relative;isolation:isolate;display:inline-grid;grid-template-columns:1fr auto;align-items:center;gap:14px;min-height:68px;padding:13px 18px 13px 24px;border-radius:14px;background:linear-gradient(180deg,#fff86b 0%,#fff133 54%,#ffd21c 100%);color:#201713!important;font-weight:950;font-size:clamp(17px,2.2vw,21px);box-shadow:0 9px 0 #bd7b00,0 20px 34px rgba(0,0,0,.22);text-align:left;border:2px solid rgba(255,255,255,.65);transition:transform .16s,box-shadow .16s,filter .16s;overflow:hidden}
.bc-cta:before{content:"";position:absolute;inset:-40% auto -40% -28%;width:28%;background:linear-gradient(90deg,transparent,rgba(255,255,255,.72),transparent);transform:skewX(-18deg);animation:bcShine 3.8s ease-in-out infinite;z-index:-1}
.bc-cta:hover{transform:translateY(-2px);filter:brightness(1.02);box-shadow:0 11px 0 #bd7b00,0 24px 38px rgba(0,0,0,.24)}
.bc-cta:active{transform:translateY(3px);box-shadow:0 5px 0 #bd7b00,0 12px 22px rgba(0,0,0,.18)}
.bc-cta-content{display:flex;flex-direction:column;gap:2px;min-width:0}
.bc-cta-main{display:block;font-size:clamp(18px,2.2vw,22px);line-height:1.05;letter-spacing:0;text-transform:uppercase}
.bc-cta-sub{display:block;font-size:12px;line-height:1.2;font-weight:850;color:#5b3c00;text-transform:none}
.bc-cta-arrow{display:grid;place-items:center;width:42px;height:42px;border-radius:50%;background:#231914;color:#fff;font-size:24px;line-height:1;box-shadow:inset 0 -2px 0 rgba(255,255,255,.18);flex:0 0 auto}
@keyframes bcShine{0%,45%{left:-34%;opacity:0}58%{opacity:1}76%,100%{left:110%;opacity:0}}
@media(prefers-reduced-motion:reduce){.bc-cta:before{animation:none}}
.bc-mini{font-size:14px;font-weight:750;color:#fff9e6}
.bc-price-card{background:#fff;color:#231914;border-radius:8px;padding:14px 16px;display:inline-flex;align-items:baseline;gap:10px;box-shadow:0 16px 36px rgba(95,31,0,.18);margin-top:10px}
.bc-price-card .bc-old{color:#8a7b73;text-decoration:line-through;font-weight:800}
.bc-price-card .bc-now{color:#ff6316;font-weight:950;font-size:34px;line-height:1}
.bc-price-card .bc-inst{color:#5b4a42;font-weight:800}
.bc-media{position:relative;min-height:560px;display:flex;align-items:flex-end;justify-content:center}
.bc-hero-img{position:absolute;right:-40px;bottom:-40px;width:min(580px,54vw);max-height:670px;object-fit:contain;filter:drop-shadow(0 28px 42px rgba(85,31,0,.24))}
.bc-cover-float{position:absolute;left:2px;bottom:72px;width:min(230px,21vw);border-radius:8px;box-shadow:0 26px 52px rgba(0,0,0,.28);transform:rotate(-5deg);background:#fff}
.bc-proofbar{background:#231914;color:#fff;padding:16px 0}
.bc-proofgrid{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:12px;text-align:center}
.bc-proofgrid strong{display:block;font-size:22px;color:#fff133;line-height:1.1}
.bc-proofgrid span{display:block;font-size:13px;font-weight:750;color:#fff4e7;margin-top:4px}
.bc-proofnote{margin:10px 0 0;text-align:center;color:#ffe0cf;font-size:12px;font-weight:650;line-height:1.35}
.bc-section{padding:56px 0;background:#fff}
.bc-section.alt{background:#fff7f1}
.bc-section h2{font-size:clamp(28px,4vw,46px);line-height:1.08;margin:0 auto 12px;text-align:center;color:#231914;font-weight:950;max-width:850px}
.bc-lead{text-align:center;max-width:760px;margin:0 auto 34px;color:#5b4a42;font-size:18px;font-weight:600}
.bc-cards{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:16px}
.bc-card{background:#fff;border:1px solid #f0ded2;border-radius:8px;padding:22px;box-shadow:0 10px 28px rgba(82,35,11,.08)}
.bc-card strong{display:block;color:#ff6316;font-size:18px;margin-bottom:8px;font-weight:950}
.bc-card p{margin:0;color:#5b4a42;font-size:15px;font-weight:600}
.bc-video-grid{display:grid;grid-template-columns:minmax(0,1fr) minmax(300px,.8fr);gap:28px;align-items:center}
.bc-video{border-radius:8px;overflow:hidden;background:#000;box-shadow:0 20px 48px rgba(35,25,20,.18)}
.bc-video video,.bc-video iframe{display:block;width:100%;border:0;aspect-ratio:16/9}
.bc-checklist{display:grid;gap:12px;margin-top:18px}
.bc-check{display:flex;gap:10px;align-items:flex-start;font-size:17px;color:#44342c;font-weight:750}
.bc-check:before{content:"";flex:0 0 22px;width:22px;height:22px;border-radius:50%;background:#ff6316;margin-top:2px;box-shadow:inset 0 0 0 6px #fff;border:2px solid #ff6316}
.bc-results{background:#231914;color:#fff;padding:58px 0}
.bc-results .bc-lead,.bc-results h2{color:#fff}
.bc-results .bc-lead{color:#fff2e8}
.bc-results-grid{display:grid;grid-template-columns:minmax(0,.92fr) minmax(360px,1.08fr);gap:30px;align-items:center}
.bc-results-copy h2{text-align:left;margin-left:0}
.bc-results-copy .bc-lead{text-align:left;margin-left:0;margin-bottom:22px}
.bc-results-list{display:grid;gap:10px;margin-top:18px}
.bc-result-point{display:flex;gap:10px;align-items:flex-start;color:#fff8ef;font-size:16px;font-weight:750}
.bc-result-point:before{content:"";width:10px;height:10px;border-radius:50%;background:#fff133;flex:0 0 10px;margin-top:7px}
.bc-before-after{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:12px}
.bc-ba-card{position:relative;min-height:360px;border-radius:8px;overflow:hidden;background:#fff;box-shadow:0 24px 54px rgba(0,0,0,.32)}
.bc-ba-card img{display:block;width:100%;height:100%;min-height:360px;object-fit:cover;object-position:center top}
.bc-ba-label{position:absolute;left:12px;top:12px;background:#fff133;color:#231914;border-radius:999px;padding:7px 12px;font-size:13px;font-weight:950;text-transform:uppercase;letter-spacing:.04em}
.bc-ba-caption{position:absolute;left:0;right:0;bottom:0;padding:34px 14px 14px;background:linear-gradient(180deg,rgba(35,25,20,0),rgba(35,25,20,.9));color:#fff;font-size:14px;font-weight:850}
.bc-results-note{margin:14px 0 0;color:#ffe4d5;font-size:13px;font-weight:650;line-height:1.45}
.bc-offer{background:#ff6316;color:#fff;padding:62px 0}
.bc-offer-box{max-width:760px;margin:0 auto;background:#fff;color:#231914;border-radius:8px;padding:30px;box-shadow:0 24px 54px rgba(80,25,0,.22)}
.bc-offer-head{text-align:center;margin-bottom:22px}
.bc-offer-head h2{color:#231914;margin-bottom:8px}
.bc-tag{display:inline-block;background:#fff133;color:#231914;border-radius:999px;padding:8px 14px;font-size:13px;font-weight:950;text-transform:uppercase;letter-spacing:.04em;margin-bottom:14px}
.bc-offer-list{display:grid;gap:10px;margin:22px 0 24px;padding:0;list-style:none}
.bc-offer-list li{position:relative;padding-left:30px;font-size:17px;font-weight:750;color:#44342c}
.bc-offer-list li:before{content:"";position:absolute;left:0;top:4px;width:18px;height:18px;border-radius:4px;background:#ff6316}
.bc-offer .bc-price-card{display:flex;justify-content:center;box-shadow:none;border:1px solid #f1e1d7;margin:0 auto 18px;width:max-content;max-width:100%;flex-wrap:wrap}
.bc-offer .bc-cta{display:grid;width:100%;margin-top:8px}
.bc-safe{text-align:center;margin:16px 0 0;color:#64544c;font-weight:700}
.bc-faq{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:12px}
.bc-faq details{background:#fff;border:1px solid #f0ded2;border-radius:8px;padding:18px 18px}
.bc-faq summary{cursor:pointer;font-weight:900;color:#231914}
.bc-faq p{margin:10px 0 0;color:#5b4a42;font-weight:600}
.bc-footer{background:#231914;color:#fff;padding:30px 0 92px;text-align:center;font-size:13px}
.bc-footer a{color:#fff133;text-decoration:underline}
.bc-sticky{position:fixed;left:0;right:0;bottom:0;z-index:6000;background:rgba(35,25,20,.96);backdrop-filter:blur(10px);padding:10px 14px;border-top:1px solid rgba(255,255,255,.12)}
.bc-sticky-inner{width:min(1020px,100%);margin:0 auto;display:flex;align-items:center;justify-content:space-between;gap:12px;color:#fff}
.bc-sticky-text{font-weight:850;font-size:14px}
.bc-sticky-text b{display:block;color:#fff133;font-size:16px}
.bc-sticky .bc-cta{min-height:52px;padding:9px 13px 9px 17px;font-size:16px;box-shadow:none;border-radius:12px}
.bc-sticky .bc-cta-main{font-size:16px}
.bc-sticky .bc-cta-sub{font-size:11px}
.bc-sticky .bc-cta-arrow{width:34px;height:34px;font-size:20px}
@media(max-width:900px){
  .bc-topbar{position:relative;padding:7px 12px;font-size:12px;line-height:1.25}
  .bc-hero-grid{grid-template-columns:1fr;gap:12px;min-height:0;padding:18px 0 22px;text-align:center}
  .bc-brand{margin-bottom:12px;font-size:15px;letter-spacing:.14em}
  .bc-eyebrow{margin-bottom:12px;padding:7px 11px;font-size:11px;line-height:1.2}
  .bc-hero h1{font-size:clamp(32px,9.2vw,44px);line-height:1.02;margin-bottom:12px}
  .bc-sub{font-size:16px;line-height:1.35;margin-bottom:14px}
  .bc-sub,.bc-hero h1{margin-left:auto;margin-right:auto}
  .bc-bullets{grid-template-columns:repeat(3,minmax(0,1fr));gap:7px;max-width:420px;margin:14px auto}
  .bc-bullet{font-size:12px;line-height:1.15;padding:9px 6px;min-height:48px;display:flex;align-items:center;justify-content:center}
  .bc-cta-row{justify-content:center}
  .bc-cta-row{margin:16px 0 8px}
  .bc-cta{width:100%;min-height:62px;padding:12px 13px 12px 17px;font-size:17px;box-shadow:0 8px 0 #bd7b00,0 16px 26px rgba(0,0,0,.18)}
  .bc-cta-main{font-size:17px}
  .bc-cta-sub{font-size:11.5px}
  .bc-cta-arrow{width:38px;height:38px;font-size:22px}
  .bc-mini{display:block;width:100%;font-size:12px;line-height:1.35}
  .bc-price-card{margin:6px auto 0;padding:10px 12px;gap:7px;justify-content:center}
  .bc-price-card .bc-old{font-size:12px}
  .bc-price-card .bc-now{font-size:29px}
  .bc-price-card .bc-inst{font-size:13px}
  .bc-media{min-height:300px;margin-top:0;overflow:hidden}
  .bc-hero-img{right:50%;transform:translateX(50%);width:min(330px,84vw);bottom:-64px;max-height:420px}
  .bc-cover-float{display:none}
  .bc-proofgrid,.bc-cards,.bc-video-grid,.bc-results-grid,.bc-faq{grid-template-columns:1fr}
  .bc-results-copy h2,.bc-results-copy .bc-lead{text-align:center;margin-left:auto;margin-right:auto}
  .bc-before-after{max-width:620px;margin:0 auto}
  .bc-proofbar{padding:12px 0}
  .bc-proofgrid{grid-template-columns:repeat(2,minmax(0,1fr));gap:10px}
  .bc-proofgrid strong{font-size:18px}
  .bc-proofgrid span{font-size:12px}
  .bc-proofnote{font-size:11px}
  .bc-section{padding:38px 0}
  .bc-section h2{font-size:clamp(25px,7.4vw,34px)}
  .bc-lead{font-size:16px;margin-bottom:22px}
  .bc-card{padding:17px}
  .bc-video-grid h2{text-align:center!important;margin-left:auto!important}
  .bc-video-grid .bc-lead{text-align:center!important;margin-left:auto!important}
  .bc-check{font-size:15px}
  .bc-offer{padding:40px 0}
  .bc-offer-box{padding:22px 18px}
  .bc-offer-list{margin:18px 0}
  .bc-offer-list li{font-size:15px}
}
@media(max-width:560px){
  .bc-wrap{width:min(100% - 24px,520px)}
  .bc-topbar{font-size:12px}
  .bc-hero h1{font-size:34px}
  .bc-sub{font-size:15.5px}
  .bc-media{min-height:258px}
  .bc-hero-img{width:min(300px,82vw);bottom:-62px}
  .bc-price-card{display:flex;flex-wrap:wrap;justify-content:center}
  .bc-price-card .bc-now{font-size:30px}
  .bc-section,.bc-offer{padding:34px 0}
  .bc-results{padding:38px 0}
  .bc-before-after{grid-template-columns:1fr;max-width:360px}
  .bc-ba-card,.bc-ba-card img{min-height:300px}
  .bc-offer-box{padding:20px 14px}
  .bc-sticky{padding:8px 10px}
  .bc-sticky-inner{display:grid;grid-template-columns:1fr;gap:6px;text-align:center}
  .bc-sticky-text{font-size:12px;line-height:1.25}
  .bc-sticky-text b{font-size:13px}
  .bc-sticky .bc-cta{width:100%}
  .bc-sticky .bc-cta{min-height:48px;padding:9px 11px 9px 14px;font-size:15px}
  .bc-sticky .bc-cta-main{font-size:15px}
  .bc-sticky .bc-cta-sub{font-size:10.5px}
  .bc-sticky .bc-cta-arrow{width:32px;height:32px;font-size:19px}
}
"""

JA_TENTEI_CEO_IMG_LEFT_URL = (
    "https://files.greatpages.com.br/arquivos/paginas_editor/"
    "386522-22a8a6d6b3cc62dfd9bbc2cedb3f67a3.JPG"
)
JA_TENTEI_CEO_IMG_RIGHT_URL = (
    "https://files.greatpages.com.br/arquivos/paginas_editor/"
    "386522-ede39e81eacd6fc95c6b5ab05addf6bf.PNG"
)

CONVERSION_HTML = f"""
<main id="berryup-conversion">
  <div class="bc-topbar">Oferta ativa hoje: <b>descubra o Bum Bum Up, o creme-chave do protocolo</b></div>
  <section class="bc-hero">
    <div class="bc-wrap bc-hero-grid">
      <div class="bc-copy">
        <div class="bc-brand">Berry Up</div>
        <div class="bc-eyebrow">Metodo digital + Bum Bum Up</div>
        <h1>Inicie da forma certa utilizando o creme numero um <span>das queridinhas do Brasil</span></h1>
        <p class="bc-sub">O e-book mostra como encaixar o Bum Bum Up na rotina certa, onde obter o creme indicado e como usar com massagens e habitos para melhorar a aparencia da pele.</p>
        <div class="bc-bullets">
          <div class="bc-bullet">Bum Bum Up explicado</div>
          <div class="bc-bullet">Como obter o creme</div>
          <div class="bc-bullet">Modo de uso guiado</div>
        </div>
        <div class="bc-price-card" aria-label="Preco do ebook">
          <span class="bc-old">De R$ 97,00</span>
          <span class="bc-now">R$ 38,80</span>
          <span class="bc-inst">60% OFF hoje</span>
        </div>
        <div class="bc-cta-row">
          <a class="bc-cta" href="{CHECKOUT}" target="_blank" rel="noopener"><span class="bc-cta-content"><span class="bc-cta-main">Garantir meu acesso agora</span><span class="bc-cta-sub">Acesso imediato + checkout seguro</span></span><span class="bc-cta-arrow" aria-hidden="true">&rsaquo;</span></a>
          <span class="bc-mini">Compra segura. Receba o acesso logo apos o pagamento.</span>
        </div>
      </div>
      <div class="bc-media" aria-hidden="true">
        <img class="bc-hero-img" src="assets/hero-berry-up.png" alt="">
        <img class="bc-cover-float" src="assets/capa_bumbum.png" alt="">
      </div>
    </div>
  </section>
  <section class="bc-proofbar">
    <div class="bc-wrap bc-proofgrid">
      <div><strong>94%</strong><span>perceberam melhora na celulite*</span></div>
      <div><strong>89%</strong><span>acharam eficaz para foliculite*</span></div>
      <div><strong>87%</strong><span>sentiram a pele mais hidratada*</span></div>
      <div><strong>7 dias</strong><span>para aplicar a rotina correta</span></div>
    </div>
    <p class="bc-proofnote">*Percentuais citados nos testes do produto. O e-book ajuda voce a seguir o modo de uso com mais clareza e consistencia.</p>
  </section>
  <section class="bc-section">
    <div class="bc-wrap">
      <h2>O que voce descobre dentro do guia</h2>
      <p class="bc-lead">A ideia nao e entregar so um PDF. E transformar os resultados percebidos nos testes do produto em uma rotina clara: preparar, aplicar, massagear e repetir do jeito certo.</p>
      <div class="bc-cards">
        <div class="bc-card"><strong>O creme por tras do protocolo</strong><p>O guia apresenta o Bum Bum Up, mostra como obter o creme indicado e por que ele entra como a etapa principal da rotina.</p></div>
        <div class="bc-card"><strong>Ativos e diferenciais</strong><p>Voce entende a combinacao de ativos, sensorial, aplicacao, massagem e frequencia que muda a experiencia de uso.</p></div>
        <div class="bc-card"><strong>Como usar sem desperdicar</strong><p>Ordem, quantidade, tempo e cuidados para aplicar com mais intencao e menos tentativa e erro.</p></div>
      </div>
    </div>
  </section>
  <section class="bc-section alt">
    <div class="bc-wrap bc-video-grid">
      <div class="bc-video">
        <video controls playsinline preload="metadata" poster="assets/clinical-berry-up.png">
          <source src="VIDEOS/AD4.mp4" type="video/mp4">
        </video>
      </div>
      <div>
        <h2 style="text-align:left;margin-left:0">O segredo nao e so ter o creme. E saber quando, quanto e como usar</h2>
        <p class="bc-lead" style="text-align:left;margin-left:0;margin-bottom:18px">Muita gente compra produto corporal, passa por alguns dias e abandona porque nao sabe montar uma rotina. O Metodo Bumbum Up organiza esse uso em um passo a passo simples.</p>
        <div class="bc-checklist">
          <div class="bc-check">Voce entende o papel do Bum Bum Up dentro do protocolo.</div>
          <div class="bc-check">Aprende a preparar a pele antes da aplicacao para aproveitar melhor o cuidado.</div>
          <div class="bc-check">Segue uma sequencia de uso para celulite, flacidez, foliculite e marcas.</div>
        </div>
        <div class="bc-cta-row">
          <a class="bc-cta" href="{CHECKOUT}" target="_blank" rel="noopener"><span class="bc-cta-content"><span class="bc-cta-main">Comprar o metodo agora</span><span class="bc-cta-sub">Receba no celular apos o pagamento</span></span><span class="bc-cta-arrow" aria-hidden="true">&rsaquo;</span></a>
        </div>
      </div>
    </div>
  </section>
  <section class="bc-results">
    <div class="bc-wrap bc-results-grid">
      <div class="bc-results-copy">
        <h2>Esses resultados comecam a fazer sentido quando voce entende o Bum Bum Up</h2>
        <p class="bc-lead">O antes e depois cria a pergunta certa: o que tem nesse creme, em qual ordem ele foi usado e com qual frequencia? O guia responde isso sem deixar a rotina solta.</p>
        <div class="bc-results-list">
          <div class="bc-result-point">Mostra a transformacao visual que desperta curiosidade sobre o produto usado.</div>
          <div class="bc-result-point">O e-book explica o Bum Bum Up e o jeito correto de encaixar na rotina.</div>
          <div class="bc-result-point">A compra do creme fica mais natural depois que a pessoa entende o motivo.</div>
        </div>
        <p class="bc-results-note">Resultados individuais podem variar conforme organismo, rotina, alimentacao, hidratacao e frequencia de aplicacao do metodo.</p>
      </div>
      <div>
        <div class="bc-before-after" aria-label="Antes e depois de uso">
          <figure class="bc-ba-card">
            <img src="{JA_TENTEI_CEO_IMG_LEFT_URL}" alt="Antes do protocolo Berry Up">
            <span class="bc-ba-label">Antes</span>
            <figcaption class="bc-ba-caption">Textura mais marcada e pele com aspecto irregular.</figcaption>
          </figure>
          <figure class="bc-ba-card">
            <img src="{JA_TENTEI_CEO_IMG_RIGHT_URL}" alt="Depois do protocolo Berry Up">
            <span class="bc-ba-label">Depois</span>
            <figcaption class="bc-ba-caption">Pele visualmente mais lisa, uniforme e cuidada.</figcaption>
          </figure>
        </div>
      </div>
    </div>
  </section>
  <section class="bc-section">
    <div class="bc-wrap">
      <h2>Por que o Bum Bum Up gera tanta curiosidade?</h2>
      <p class="bc-lead">Porque ele junta o desejo de resultado visual com uma formula pensada para rotina corporal: produto notificado na Anvisa, vegano e com ativos usados em dermocosmeticos de cuidado da pele.</p>
      <div class="bc-cards">
        <div class="bc-card"><strong>Notificado na Anvisa</strong><p>Produto notificado na Anvisa, reforcando seguranca e legalidade no mercado brasileiro.</p></div>
        <div class="bc-card"><strong>Vegano</strong><p>O Bum Bum Up tem proposta vegana dentro de uma rotina de body care mais consciente.</p></div>
        <div class="bc-card"><strong>Natureza + ciencia</strong><p>A formula combina ativos como cafeina, flor de arnica, pimenta preta, gengibre, po de mica e nicotinato de metila.</p></div>
      </div>
    </div>
  </section>
  <section class="bc-offer" id="oferta">
    <div class="bc-wrap">
      <div class="bc-offer-box">
        <div class="bc-offer-head">
          <span class="bc-tag">Oferta principal</span>
          <h2>Guia Completo Bumbum Up</h2>
          <p class="bc-lead">O acesso para entender o Bum Bum Up, por que ele importa e como aplicar o protocolo do jeito certo.</p>
        </div>
        <div class="bc-price-card">
          <span class="bc-old">De R$ 97,00</span>
          <span class="bc-now">R$ 38,80</span>
          <span class="bc-inst">60% OFF hoje</span>
        </div>
        <ul class="bc-offer-list">
          <li>Guia do Bum Bum Up dentro do protocolo Bumbum Up</li>
          <li>Orientacao de como obter o creme indicado dentro do guia</li>
          <li>Rotina guiada de 7 dias para aplicar sem duvida</li>
          <li>Modo de uso, massagens e habitos para potencializar o cuidado</li>
        </ul>
        <a class="bc-cta" href="{CHECKOUT}" target="_blank" rel="noopener"><span class="bc-cta-content"><span class="bc-cta-main">Finalizar minha compra</span><span class="bc-cta-sub">R$ 38,80 com 60% OFF</span></span><span class="bc-cta-arrow" aria-hidden="true">&rsaquo;</span></a>
        <p class="bc-safe">Pagamento 100% seguro. Acesso enviado apos confirmacao.</p>
      </div>
    </div>
  </section>
  <section class="bc-section">
    <div class="bc-wrap">
      <h2>Duvidas comuns antes de comprar</h2>
      <p class="bc-lead">As respostas mais importantes antes de garantir o acesso ao Metodo Bumbum Up.</p>
      <div class="bc-faq">
        <details open><summary>Quando recebo o e-book?</summary><p>O acesso e liberado apos a confirmacao do pagamento, para voce comecar ainda hoje.</p></details>
        <details><summary>Funciona no celular?</summary><p>Sim. O guia pode ser lido no celular, tablet ou computador.</p></details>
        <details><summary>Preciso ja ter o creme para comprar o guia?</summary><p>Nao. O guia foi feito justamente para quem quer comecar do jeito certo: dentro dele voce entende como o Bum Bum Up entra no protocolo, como obter o creme indicado e como usar depois que estiver com ele.</p></details>
        <details><summary>Para quem e indicado?</summary><p>Para mulheres que querem melhorar a aparencia da pele, reduzir aspecto de celulite e ter uma rotina mais clara de autocuidado corporal.</p></details>
      </div>
    </div>
  </section>
  <footer class="bc-footer">
    <div class="bc-wrap">
      <p>Berry Up - CNPJ: 98.581.467/0001-77</p>
      <p>Os resultados podem variar conforme rotina, organismo e consistencia de aplicacao. <a href="#popup" class="link_popup">Politica de troca e devolucao</a></p>
    </div>
  </footer>
  <div class="bc-sticky">
    <div class="bc-sticky-inner">
      <div class="bc-sticky-text"><b>Metodo Bumbum Up por R$ 38,80</b>60% OFF no acesso imediato</div>
      <a class="bc-cta" href="{CHECKOUT}" target="_blank" rel="noopener"><span class="bc-cta-content"><span class="bc-cta-main">Comprar agora</span><span class="bc-cta-sub">Acesso imediato</span></span><span class="bc-cta-arrow" aria-hidden="true">&rsaquo;</span></a>
    </div>
  </div>
</main>
"""

REPLACEMENTS = [
    ("QUERO BUMBUM DE PÊSSEGO</a>", "Quero meu ebook !!!</a>"),
    (
        "Quanto tempo demora para ver resultados com os produtos da Peach Up?",
        "Quanto tempo demora para ver resultados realizando o metodo?",
    ),
    (
        "Peach Up funciona para celulite, foliculite, estrias ou flacidez?",
        "O Metodo funciona para celulite, foliculite, estrias ou flacidez?",
    ),
    (
        "Os produtos da Peach Up são aprovados pela Anvisa?",
        "Os produtos deste metodo são aprovados pela Anvisa?",
    ),
    (
        "Peach Up é seguro para todos os tipos de pele?",
        "O metodo é seguro para todos os tipos de pele?",
    ),
    (
        "Os produtos da Peach Up têm cheiro forte?",
        "Os produtos do metodo têm cheiro forte?",
    ),
    (
        "Qual a diferença entre os produtos Peach Up?",
        "Qual a diferença entre os produtos deste metodo?",
    ),
    (
        "Qual o melhor produto da Peach Up para começar?",
        "Qual o melhor produto para começar?",
    ),
    ("ecommerce@peachup.com.br", "ecommerce@berryup.com.br"),
    (
        'href="https://www.instagram.com/peachupbrazil?utm_source=ig_web_button_share_sheet&amp;igsh=ZDNlZDc0MzIxNw==" class="link_externo" target="_blank">peachupbrazil</a>',
        'href="https://www.instagram.com/beary.up/" class="link_externo" target="_blank">beary.up</a>',
    ),
    (
        'href="https://www.instagram.com/peachupbrazil?utm_source=ig_web_button_share_sheet&igsh=ZDNlZDc0MzIxNw==" class="link_externo" target="_blank">peachupbrazil</a>',
        'href="https://www.instagram.com/beary.up/" class="link_externo" target="_blank">beary.up</a>',
    ),
    (
        "<span>Os <b>TESTES CLÍNICOS</b>, realizados por pessoas que utilizaram o BoomBoom Up, apresentaram os resultados:</span>",
        "<span>Os testes clínicos realizados por pessoas que utilizaram o método e o creme apresentam os resultados:</span>",
    ),
    (
        "<p><span>BoomBoom Up</span></p><p><span>agindo <b>em 23 dias</b></span></p>",
        "<p><span>O creme agindo em 23 dias</span></p>",
    ),
    ("<p><span>O creme agindo em 23 dias</span></p><p><span>agindo <b>em 23 dias</b></span></p>", "<p><span>O creme agindo em 23 dias</span></p>"),
    (
        "Ps: O BoomBoom Up pode deixar a sua pele vermelha e causar uma leve ardência durante aproximadamente 40 min. Não se preocupe, são os ativos agindo! 🧡",
        "Ps: O creme pode deixar a sua pele vermelha e causar uma leve ardência durante aproximadamente 40 min. Não se preocupe, são os ativos agindo! 🧡",
    ),
    (
        'content="Aproveite a maior promoção no BoomBoom Up: o famosinho contra celulite. Ofertas especiais por tempo limitado + frete grátis! Não perca! 🧡"',
        'content="Guia digital Peach Up: o protocolo contra celulite que milhares de mulheres já seguiram. Acesso imediato ao e-book com oferta por tempo limitado! 🧡"',
    ),
    ("Creme para celulite Celulite Creme para corpo Anticelulite estrias", "E-book anti celulite Guia digital Anticelulite estrias Peach Up"),
    ("<title>Peach Up | Site Oficial</title>", "<title>Bum Bum Up - Ebook</title>"),
    (
        "<b>O Creme Nº1 Contra a Celulite!</b>",
        "<b>O E-book Nº1 Contra a Celulite, Foliculite, Lipedema e Estrias!</b>",
    ),
    (
        "<b>O E-book Nº1 Contra a Celulite!</b>",
        "<b>O E-book Nº1 Contra a Celulite, Foliculite, Lipedema e Estrias!</b>",
    ),
    ("<span>POR QUE VOCÊ DEVE USAR O BOOMBOOM UP?</span>", "<span>POR QUE ESTE E-BOOK FUNCIONA?</span>"),
    (
        "<span>Usando ele sua pele vai ficar <b>mais firme, iluminada, super hidratada</b> e com as <b>imperfeições suavizadas</b>, deixando de lado o temido efeito <b>''casca de laranja''</b>.</span>",
        "<span>Por que temos o metodo perfeito junto com o melhor produto do brasil. Usando ele, sua pele vai ficar mais firme, iluminada, super hidratada e com as imperfeições suavizadas, deixando de lado o temido efeito casca de laranja.</span>",
    ),
    (
        "<span>Pele mais lisa e firme desde a primeira aplicação.</span>",
        "<span>Pele mais lisa e firme desde os primeiros dias do método.</span>",
    ),
    (">Comprar Agora</a>", ">Garantir meu e-book</a>"),
    (">COMPRAR AGORA</a>", ">GARANTIR E-BOOK</a>"),
    (
        "Se você se identifica com alguma dessas situações acima, conheça o <b>BOOMBOOM UP</b> e <b>resgate sua autoconfiança</b>",
        "Se você se identifica com alguma dessas situações acima, conheça o guia Berry Up e resgate sua sua confiança.",
    ),
    (
        "Se você se identifica com alguma dessas situações acima, conheça o <b>GUIA PEACH UP</b> e <b>resgate sua autoconfiança</b>",
        "Se você se identifica com alguma dessas situações acima, conheça o guia Berry Up e resgate sua sua confiança.",
    ),
    (
        "a Peach Up traz em seus produtos uma proposta",
        "a Peach Up traz em seu guia digital uma proposta",
    ),
    (
        "<span><b>Teste de SEGURANÇA DO PRODUTO</b></span>",
        "<span><b>CONTEÚDO VALIDADO</b></span>",
    ),
    (
        "garantem que o produto é seguro para uso",
        "garantem um método seguro e baseado em boas práticas",
    ),
    (
        "<span><b>87%</b> Das pessoas gostaram do produto</span>",
        "<span><b>87%</b> Das leitoras recomendam o guia</span>",
    ),
    (
        "O teste de estabilidade garante a qualidade e eficácia do método, avaliando sua resistência a diferentes condições de armazenamento e uso.",
        "O teste de estabilidade garante a qualidade e eficácia do produto, avaliando sua resistência a diferentes condições de armazenamento e uso.",
    ),
    (
        "eficiência do produto.</span>",
        "eficiência do protocolo.</span>",
    ),
]

JA_TENTEI_BLOCK_ID = "b_1002625_1_17307234956728bea7c7c49"
JA_TENTEI_SUBTITLE_EID = "e_1002625_1_17307234956728bea7e0b0a646306905"
JA_TENTEI_SUBTITLE_BOX_EID = "e_1002625_1_17307234956728bea7e0d4c566095029"
JA_TENTEI_VIDEO_ID = "berryup-ja-tentei-video"
JA_TENTEI_TITLE_EID = "e_1002625_1_17307234956728bea7e0766722261483"
JA_TENTEI_EID = "e_1002625_1_17307234956728bea7e0f7f008614945"
JA_TENTEI_HIDE_EIDS = (
    "e_1002625_1_17307234956728bea7e14fa031033880",
    "e_1002625_1_17307234956728bea7e1db6271581830",
    # Card decorativo duplicado (foto + estrelas) — sobrepõe título no mobile
    "e_1002625_1_17307234956728bea7ee4b7695876431",
)
JA_TENTEI_CEO_IMG_LEFT = "e_1002625_1_17307234956728bea7e1b37926645397"
JA_TENTEI_CEO_IMG_RIGHT = "e_1002625_1_17307234956728bea7e5f35416465044"
JA_TENTEI_CEO_IMG_DESK_H = 300
JA_TENTEI_YEAR_LEFT = "e_1002625_1_17307234956728bea7e679d642920167"
JA_TENTEI_YEAR_RIGHT = "e_1002625_1_17307234956728bea7e69d1777282289"
JA_TENTEI_CEO_HEADLINE_EID = "e_1002625_1_17307234956728bea7e1725589044085"
JA_TENTEI_CEO_SUBLINE_EID = "e_1002625_1_17307234956728bea7e194f892874976"
JA_TENTEI_CEO_DESKTOP_HIDE_EIDS = (
    JA_TENTEI_CEO_HEADLINE_EID,
    JA_TENTEI_CEO_SUBLINE_EID,
    JA_TENTEI_YEAR_LEFT,
    JA_TENTEI_YEAR_RIGHT,
    JA_TENTEI_CEO_IMG_LEFT,
    JA_TENTEI_CEO_IMG_RIGHT,
)
JA_TENTEI_CTA_TEXT_D = "e_1002625_1_17307234956728bea7e6eab069875421_d"
JA_TENTEI_CTA_BTN_D = "e_1002625_1_17307234956728bea7e6bc6088578960_d"
JA_TENTEI_CTA_TEXT_M = "e_1002625_1_17307234956728bea7e6eab069875421_m"
JA_TENTEI_CTA_BTN_M = "e_1002625_1_17307234956728bea7e6bc6088578960_m"
JA_TENTEI_DESK_MIN_H = 760
JA_TENTEI_CEO_IMG_W = "min(280px,26vw)"
JA_TENTEI_CEO_IMG_GAP = "20px"
JA_TENTEI_CEO_IMG_LEFT_CSS = f"calc(50% - {JA_TENTEI_CEO_IMG_W} - {JA_TENTEI_CEO_IMG_GAP} / 2)"
JA_TENTEI_CEO_IMG_RIGHT_CSS = f"calc(50% + {JA_TENTEI_CEO_IMG_GAP} / 2)"
JA_TENTEI_MOB_MIN_H = 1480
JA_TENTEI_ORANGE_BAR_M = "e_1002625_1_17307234956728bea7ee4b7695876431_m"
JA_TENTEI_HASHTAG_MOBILE = "e_1002625_1_17307234956728bea832874300193060"
JA_TENTEI_BLOCK_HTML = (
    f'<div id="{JA_TENTEI_EID}" class="gpc-e e_texto dd dm {JA_TENTEI_EID}">'
    '<div class="c e_texto se_fonte">'
    "<p><span>Entendemos que encontrar o método certo pode ser desafiador. "
    "<b>O método Bumbum Up se destaca por combinar ingredientes eficazes e comprovados em estudos clínicos, "
    "especialmente formulados para combater a celulite, estrias e flacidez de forma visível.</b></span></p>"
    "<p><span><br></span></p>"
    "<p><span>O protocolo não só melhora a textura da pele, mas também estimula a circulação, "
    "ajudando a obter resultados duradouros. E o melhor? "
    "<b>Garantimos resultados ou devolvemos seu dinheiro. Experimente o método Bumbum Up "
    "e sinta a diferença você mesma, sem risco nenhum!</b></span></p>"
    "</div></div>"
)
_DUPLICATE_GUARANTEE_RE = re.compile(
    r"</b>\s*(?:Nós garantimos|Garantimos) resultados ou devolvemos seu dinheiro\.\s*"
    r"(?:Dê uma chance ao|Experimente o (?:método )?)?(?:BoomBoom Up|Berry Up) e sinta a diferença você mesma, sem risco nenhum!\s*",
    re.IGNORECASE,
)


def patch_ceo_images(html: str) -> str:
    """Garante .imagem_fundo nas fotos CEO (lazy load do GreatPages às vezes não injeta)."""
    for eid in (JA_TENTEI_CEO_IMG_LEFT, JA_TENTEI_CEO_IMG_RIGHT):
        pat = (
            rf'(<div id="{re.escape(eid)}"[^>]*>)\s*'
            r'<div class="c imagem e_imagem borda_igual"></div>\s*(</div>)'
        )
        if re.search(pat, html) and f'id="{eid}"' in html:
            chunk = re.search(
                rf'<div id="{re.escape(eid)}"[^>]*>.*?</div></div>',
                html,
                re.DOTALL,
            )
            if chunk and "imagem_fundo" not in chunk.group(0):
                html = re.sub(
                    pat,
                    r'\1<div class="c imagem e_imagem borda_igual">'
                    r'<div class="imagem_fundo"></div></div>\2',
                    html,
                    count=1,
                )
    return html


def patch_ja_tentei_section(html: str) -> str:
    """Seção 'Já tentei de tudo': texto Berry Up único, sem duplicata BoomBoom."""
    if JA_TENTEI_EID not in html:
        return html
    html = _DUPLICATE_GUARANTEE_RE.sub("</b>", html)
    html = re.sub(
        rf"<div id=\"{re.escape(JA_TENTEI_EID)}\"[^>]*>.*?</div></div>",
        JA_TENTEI_BLOCK_HTML,
        html,
        count=1,
        flags=re.DOTALL,
    )
    return html


def ja_tentei_video_html() -> str:
    embed = CLINICAL_YOUTUBE_EMBED
    return f"""
<div id="{JA_TENTEI_VIDEO_ID}" class="berryup-ja-tentei-video">
<nav class="bjtv-menu" role="tablist" aria-label="Vídeos explicativos">
<button type="button" class="bjtv-menu-btn is-active" role="tab" aria-selected="true" data-bjtv-src="{embed}">Por que funciona</button>
<button type="button" class="bjtv-menu-btn" role="tab" aria-selected="false" data-bjtv-src="{embed}">Método Bumbum Up</button>
</nav>
<div class="bjtv-frame">
<iframe id="berryup-ja-tentei-iframe" src="{embed}" title="Por que o método Bumbum Up funciona" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen loading="lazy"></iframe>
</div>
</div>
"""


JA_TENTEI_VIDEO_SCRIPT = f"""<script id="berryup-ja-tentei-video-script">(function(){{
var root=document.getElementById("{JA_TENTEI_VIDEO_ID}");
if(!root)return;
var frame=root.querySelector(".bjtv-frame iframe");
root.querySelectorAll(".bjtv-menu-btn").forEach(function(btn){{
  btn.addEventListener("click",function(){{
    if(btn.classList.contains("is-active"))return;
    root.querySelectorAll(".bjtv-menu-btn").forEach(function(b){{
      b.classList.remove("is-active");
      b.setAttribute("aria-selected","false");
    }});
    btn.classList.add("is-active");
    btn.setAttribute("aria-selected","true");
    var src=btn.getAttribute("data-bjtv-src");
    if(frame&&src)frame.src=src;
  }});
}});
}})();</script>"""


def ja_tentei_video_css(html: str) -> str:
    hide_rules = "".join(
        f"#{JA_TENTEI_BLOCK_ID} #{eid}{{display:none!important;visibility:hidden!important;"
        f"height:0!important;overflow:hidden!important;pointer-events:none!important}}\n"
        for eid in JA_TENTEI_HIDE_EIDS
    )
    desktop_ceo_hide_rules = "".join(
        f"#{JA_TENTEI_BLOCK_ID} #{eid}{{display:none!important;visibility:hidden!important;"
        f"height:0!important;min-height:0!important;overflow:hidden!important;"
        f"pointer-events:none!important}}\n"
        for eid in JA_TENTEI_CEO_DESKTOP_HIDE_EIDS
    )
    return f"""
/* Já tentei de tudo — coluna esquerda (texto) + vídeo à direita (desktop) */
#{JA_TENTEI_BLOCK_ID}{{
  position:relative!important;top:auto!important;margin-top:0!important;
  overflow:visible!important}}
#{JA_TENTEI_BLOCK_ID} .centralizar{{position:relative!important;overflow:visible!important}}
{hide_rules}
#{JA_TENTEI_BLOCK_ID} #{JA_TENTEI_CEO_HEADLINE_EID} .c h2 span,
#{JA_TENTEI_BLOCK_ID} #{JA_TENTEI_CEO_HEADLINE_EID} .c > H2:nth-of-type(1) > SPAN:nth-of-type(1),
#{JA_TENTEI_BLOCK_ID} #{JA_TENTEI_CEO_SUBLINE_EID} .c h2 span,
#{JA_TENTEI_BLOCK_ID} #{JA_TENTEI_CEO_SUBLINE_EID} .c > H2:nth-of-type(1) > SPAN:nth-of-type(1){{
  color:{BERRYUP_ORANGE}!important}}
#{JA_TENTEI_VIDEO_ID}{{
  position:absolute;z-index:240!important;box-sizing:border-box}}
.bjtv-menu{{
  display:flex;flex-wrap:wrap;justify-content:center;gap:8px;margin:0 0 10px;padding:0}}
.bjtv-menu-btn{{
  border:2px solid #ff6316;background:#fff;color:#ff6316;font-weight:800;font-size:clamp(.78rem,2.4vw,.9rem);
  letter-spacing:.04em;text-transform:uppercase;padding:8px 16px;border-radius:999px;cursor:pointer;
  font-family:system-ui,-apple-system,"Segoe UI",Roboto,sans-serif;line-height:1.2}}
.bjtv-menu-btn.is-active{{
  background:#ff6316;color:#fff;box-shadow:0 4px 14px rgba(255,99,22,.35)}}
.bjtv-frame{{
  border-radius:14px;overflow:hidden;background:#000;box-shadow:0 12px 36px rgba(0,0,0,.2)}}
.bjtv-frame iframe{{
  display:block;width:100%;aspect-ratio:16/9;min-height:200px;border:0;vertical-align:top}}
@media(min-width:801px){{
#{JA_TENTEI_BLOCK_ID}{{
  min-height:0!important;height:auto!important;padding-bottom:0!important}}
{desktop_ceo_hide_rules}
#{JA_TENTEI_BLOCK_ID} #{JA_TENTEI_CTA_TEXT_M},
#{JA_TENTEI_BLOCK_ID} #{JA_TENTEI_CTA_BTN_M}{{
  display:none!important;visibility:hidden!important;height:0!important;
  overflow:hidden!important;pointer-events:none!important}}
#{JA_TENTEI_BLOCK_ID} #{JA_TENTEI_CTA_TEXT_D},
#{JA_TENTEI_BLOCK_ID} #{JA_TENTEI_CTA_BTN_D}{{
  display:block!important;visibility:visible!important;pointer-events:auto!important}}
#{JA_TENTEI_BLOCK_ID} #{JA_TENTEI_TITLE_EID}{{
  top:28px!important;left:24px!important;right:auto!important;
  width:min(540px,46vw)!important;max-width:48%!important;height:auto!important;
  box-sizing:border-box!important}}
#{JA_TENTEI_BLOCK_ID} #{JA_TENTEI_SUBTITLE_BOX_EID}{{
  top:200px!important;left:24px!important;
  width:min(540px,46vw)!important;max-width:48%!important;height:54px!important;
  box-sizing:border-box!important}}
#{JA_TENTEI_BLOCK_ID} #{JA_TENTEI_SUBTITLE_EID}{{
  top:206px!important;left:24px!important;z-index:366!important;
  width:min(540px,46vw)!important;max-width:48%!important;height:auto!important;
  box-sizing:border-box!important;margin-bottom:0!important}}
#{JA_TENTEI_BLOCK_ID} #{JA_TENTEI_SUBTITLE_EID} .c{{
  padding-bottom:6px!important}}
#{JA_TENTEI_BLOCK_ID} #{JA_TENTEI_SUBTITLE_EID} .c h2,
#{JA_TENTEI_BLOCK_ID} #{JA_TENTEI_SUBTITLE_EID} .c h2 span,
#{JA_TENTEI_BLOCK_ID} #{JA_TENTEI_SUBTITLE_EID} .c > H2:nth-of-type(1),
#{JA_TENTEI_BLOCK_ID} #{JA_TENTEI_SUBTITLE_EID} .c > H2:nth-of-type(1) > SPAN:nth-of-type(1){{
  color:{BERRYUP_YELLOW_HEADLINE}!important;line-height:1.28!important;margin:0 0 4px!important}}
#{JA_TENTEI_BLOCK_ID} #{JA_TENTEI_EID}{{
  top:318px!important;left:24px!important;
  max-width:48%!important;width:48%!important;box-sizing:border-box!important}}
/* CEO — antes/depois centralizado (desktop) */
#{JA_TENTEI_BLOCK_ID} #{JA_TENTEI_CEO_HEADLINE_EID}{{
  top:668px!important;left:50%!important;right:auto!important;
  transform:translateX(-50%)!important;width:min(780px,72vw)!important;
  max-width:900px!important;height:auto!important;box-sizing:border-box!important}}
#{JA_TENTEI_BLOCK_ID} #{JA_TENTEI_CEO_SUBLINE_EID}{{
  top:748px!important;left:50%!important;right:auto!important;
  transform:translateX(-50%)!important;width:min(780px,72vw)!important;
  max-width:900px!important;height:auto!important;box-sizing:border-box!important}}
#{JA_TENTEI_BLOCK_ID} #{JA_TENTEI_CEO_HEADLINE_EID} .c h1,
#{JA_TENTEI_BLOCK_ID} #{JA_TENTEI_CEO_HEADLINE_EID} .c h2,
#{JA_TENTEI_BLOCK_ID} #{JA_TENTEI_CEO_SUBLINE_EID} .c h1,
#{JA_TENTEI_BLOCK_ID} #{JA_TENTEI_CEO_SUBLINE_EID} .c h2,
#{JA_TENTEI_BLOCK_ID} #{JA_TENTEI_CEO_HEADLINE_EID} .c h1 span,
#{JA_TENTEI_BLOCK_ID} #{JA_TENTEI_CEO_HEADLINE_EID} .c h2 span,
#{JA_TENTEI_BLOCK_ID} #{JA_TENTEI_CEO_SUBLINE_EID} .c h1 span,
#{JA_TENTEI_BLOCK_ID} #{JA_TENTEI_CEO_SUBLINE_EID} .c h2 span{{
  text-align:center!important;line-height:1.2!important}}
#{JA_TENTEI_BLOCK_ID} #{JA_TENTEI_YEAR_LEFT},
#{JA_TENTEI_BLOCK_ID} #{JA_TENTEI_YEAR_RIGHT}{{
  top:824px!important;width:{JA_TENTEI_CEO_IMG_W}!important;height:auto!important;
  transform:none!important;text-align:center!important;box-sizing:border-box!important}}
#{JA_TENTEI_BLOCK_ID} #{JA_TENTEI_YEAR_LEFT}{{
  left:{JA_TENTEI_CEO_IMG_LEFT_CSS}!important}}
#{JA_TENTEI_BLOCK_ID} #{JA_TENTEI_YEAR_RIGHT}{{
  left:{JA_TENTEI_CEO_IMG_RIGHT_CSS}!important}}
#{JA_TENTEI_BLOCK_ID} #{JA_TENTEI_YEAR_LEFT} .c p,
#{JA_TENTEI_BLOCK_ID} #{JA_TENTEI_YEAR_RIGHT} .c p{{
  text-align:center!important;margin:0!important}}
#{JA_TENTEI_BLOCK_ID} #{JA_TENTEI_CEO_IMG_LEFT},
#{JA_TENTEI_BLOCK_ID} #{JA_TENTEI_CEO_IMG_RIGHT}{{
  top:864px!important;width:{JA_TENTEI_CEO_IMG_W}!important;height:300px!important;
  transform:none!important;box-sizing:border-box!important}}
#{JA_TENTEI_BLOCK_ID} #{JA_TENTEI_CEO_IMG_LEFT}{{
  left:{JA_TENTEI_CEO_IMG_LEFT_CSS}!important}}
#{JA_TENTEI_BLOCK_ID} #{JA_TENTEI_CEO_IMG_RIGHT}{{
  left:{JA_TENTEI_CEO_IMG_RIGHT_CSS}!important}}
#{JA_TENTEI_BLOCK_ID} #{JA_TENTEI_CEO_IMG_LEFT} .c,
#{JA_TENTEI_BLOCK_ID} #{JA_TENTEI_CEO_IMG_RIGHT} .c,
#{JA_TENTEI_BLOCK_ID} #{JA_TENTEI_CEO_IMG_LEFT} .c .imagem_fundo,
#{JA_TENTEI_BLOCK_ID} #{JA_TENTEI_CEO_IMG_RIGHT} .c .imagem_fundo{{
  display:block!important;opacity:1!important;
  width:100%!important;height:100%!important;min-height:{JA_TENTEI_CEO_IMG_DESK_H}px!important;
  background-size:cover!important;background-position:center top!important;
  background-repeat:no-repeat!important}}
#{JA_TENTEI_BLOCK_ID} #{JA_TENTEI_CEO_IMG_LEFT} .c .imagem_fundo{{
  background-image:url("{JA_TENTEI_CEO_IMG_LEFT_URL}")!important}}
#{JA_TENTEI_BLOCK_ID} #{JA_TENTEI_CEO_IMG_RIGHT} .c .imagem_fundo{{
  background-image:url("{JA_TENTEI_CEO_IMG_RIGHT_URL}")!important}}
#{JA_TENTEI_BLOCK_ID} #e_1002625_1_17307234956728bea7e6514907864664,
#{JA_TENTEI_BLOCK_ID} #e_1002625_1_17307234956728bea7e62d5886606273{{
  display:none!important;visibility:hidden!important;height:0!important;
  overflow:hidden!important;pointer-events:none!important}}
#{JA_TENTEI_BLOCK_ID} #{JA_TENTEI_CTA_TEXT_D}{{
  top:632px!important;left:50%!important;transform:translateX(calc(-50% - 155px))!important;
  width:auto!important;max-width:min(320px,32vw)!important;white-space:nowrap!important}}
#{JA_TENTEI_BLOCK_ID} #{JA_TENTEI_CTA_BTN_D}{{
  top:624px!important;left:50%!important;transform:translateX(calc(-50% + 155px))!important;
  width:min(320px,28vw)!important;max-width:360px!important;height:auto!important}}
#{JA_TENTEI_BLOCK_ID} #e_1002625_1_17307234956728bea7e70b4426371193_m{{
  top:648px!important;left:50%!important;transform:translateX(calc(-50% - 90px))!important}}
#{JA_TENTEI_VIDEO_ID}{{
  left:52%!important;top:88px!important;right:auto!important;
  transform:none!important;width:min(430px,44vw)!important;max-width:480px!important}}
}}
@media(max-width:800px){{
#{JA_TENTEI_BLOCK_ID}{{
  clear:both!important;min-height:0!important;height:auto!important;padding-bottom:32px!important}}
#{JA_TENTEI_BLOCK_ID} #{JA_TENTEI_TITLE_EID}{{
  top:20px!important;left:16px!important;width:calc(100% - 32px)!important;
  max-width:none!important;height:auto!important}}
#{JA_TENTEI_BLOCK_ID} #{JA_TENTEI_SUBTITLE_BOX_EID}{{
  top:152px!important;left:16px!important;width:calc(100% - 32px)!important;
  max-width:none!important;height:50px!important}}
#{JA_TENTEI_BLOCK_ID} #{JA_TENTEI_SUBTITLE_EID}{{
  top:156px!important;left:16px!important;z-index:366!important;
  width:calc(100% - 32px)!important;max-width:none!important}}
#{JA_TENTEI_VIDEO_ID}{{
  left:50%!important;top:248px!important;transform:translateX(-50%)!important;
  width:min(100%,calc(100vw - 28px))!important;max-width:560px!important}}
#{JA_TENTEI_BLOCK_ID} #{JA_TENTEI_EID}{{top:520px!important;left:16px!important;
  width:calc(100% - 32px)!important;max-width:none!important}}
#{JA_TENTEI_BLOCK_ID} #{JA_TENTEI_CEO_HEADLINE_EID}{{top:900px!important;left:16px!important;
  width:calc(100% - 32px)!important;max-width:none!important}}
#{JA_TENTEI_BLOCK_ID} #{JA_TENTEI_CEO_SUBLINE_EID}{{top:960px!important;left:16px!important;
  width:calc(100% - 32px)!important;max-width:none!important}}
#{JA_TENTEI_BLOCK_ID} #e_1002625_1_17307234956728bea7e1b37926645397{{top:1020px!important;
  left:16px!important;width:calc(50% - 24px)!important;height:auto!important}}
#{JA_TENTEI_BLOCK_ID} #e_1002625_1_17307234956728bea7e5f35416465044{{
  top:1020px!important;
  left:calc(50% + 8px)!important;width:calc(50% - 24px)!important;height:auto!important}}
#{JA_TENTEI_BLOCK_ID} #e_1002625_1_17307234956728bea7e62d5886606273{{top:1280px!important}}
#{JA_TENTEI_BLOCK_ID} #e_1002625_1_17307234956728bea7e679d642920167,
#{JA_TENTEI_BLOCK_ID} #e_1002625_1_17307234956728bea7e69d1777282289{{top:1320px!important}}
#{JA_TENTEI_BLOCK_ID} #e_1002625_1_17307234956728bea7e6514907864664{{top:1320px!important}}
#{JA_TENTEI_BLOCK_ID} #e_1002625_1_17307234956728bea7e6eab069875421_m{{top:1380px!important}}
#{JA_TENTEI_BLOCK_ID} #e_1002625_1_17307234956728bea7e70b4426371193_m{{top:1380px!important}}
#{JA_TENTEI_BLOCK_ID} #e_1002625_1_17307234956728bea7e6bc6088578960_m{{top:1420px!important}}
#{JA_TENTEI_BLOCK_ID} #{JA_TENTEI_CEO_IMG_LEFT},
#{JA_TENTEI_BLOCK_ID} #{JA_TENTEI_CEO_IMG_RIGHT}{{
  min-height:clamp(180px,48vw,240px)!important;height:auto!important;
  box-sizing:border-box!important}}
#{JA_TENTEI_BLOCK_ID} #{JA_TENTEI_CEO_IMG_LEFT} .c,
#{JA_TENTEI_BLOCK_ID} #{JA_TENTEI_CEO_IMG_RIGHT} .c{{
  width:100%!important;min-height:clamp(180px,48vw,240px)!important;height:100%!important}}
#{JA_TENTEI_BLOCK_ID} #{JA_TENTEI_CEO_IMG_LEFT} .c .imagem_fundo,
#{JA_TENTEI_BLOCK_ID} #{JA_TENTEI_CEO_IMG_RIGHT} .c .imagem_fundo{{
  display:block!important;width:100%!important;
  min-height:clamp(180px,48vw,240px)!important;
  background-size:cover!important;background-position:center top!important;
  background-repeat:no-repeat!important}}
#{JA_TENTEI_BLOCK_ID} #{JA_TENTEI_YEAR_LEFT},
#{JA_TENTEI_BLOCK_ID} #{JA_TENTEI_YEAR_RIGHT}{{
  text-align:center!important;width:calc(50% - 24px)!important;height:auto!important}}
#{JA_TENTEI_BLOCK_ID} #{JA_TENTEI_TITLE_EID} .c h2 span{{
  white-space:normal!important;line-height:1.15!important}}
#{JA_TENTEI_BLOCK_ID} #{JA_TENTEI_SUBTITLE_EID} .c h2,
#{JA_TENTEI_BLOCK_ID} #{JA_TENTEI_SUBTITLE_EID} .c h2 span,
#{JA_TENTEI_BLOCK_ID} #{JA_TENTEI_SUBTITLE_EID} .c > H2:nth-of-type(1),
#{JA_TENTEI_BLOCK_ID} #{JA_TENTEI_SUBTITLE_EID} .c > H2:nth-of-type(1) > SPAN:nth-of-type(1){{
  white-space:normal!important;line-height:1.15!important;
  color:{BERRYUP_YELLOW_HEADLINE}!important}}
/* Faixa laranja de hashtags (mobile) */
#{JA_TENTEI_BLOCK_ID} #{JA_TENTEI_ORANGE_BAR_M}{{
  left:16px!important;width:calc(100% - 32px)!important;max-width:none!important;
  height:44px!important;transform:none!important;z-index:394!important;
  box-sizing:border-box!important}}
#{JA_TENTEI_BLOCK_ID} #{JA_TENTEI_ORANGE_BAR_M} .c{{
  height:100%!important;display:flex!important;align-items:center!important;
  border:none!important;background-color:rgb(255,99,22)!important;
  background-image:none!important}}
#{JA_TENTEI_BLOCK_ID} #{JA_TENTEI_HASHTAG_MOBILE}{{
  left:16px!important;width:calc(100% - 32px)!important;max-width:none!important;
  height:44px!important;transform:none!important;z-index:397!important;
  pointer-events:none!important;box-sizing:border-box!important}}
#{JA_TENTEI_BLOCK_ID} #{JA_TENTEI_HASHTAG_MOBILE} .c{{
  height:100%!important;display:flex!important;align-items:center!important;
  justify-content:center!important;line-height:1.25!important;
  font-size:clamp(11px,3.2vw,15px)!important;padding:0 12px!important;
  box-sizing:border-box!important;text-align:center!important}}
#{JA_TENTEI_BLOCK_ID} #{JA_TENTEI_HASHTAG_MOBILE} .c p,
#{JA_TENTEI_BLOCK_ID} #{JA_TENTEI_HASHTAG_MOBILE} .c p span{{
  margin:0!important;padding:0!important;line-height:1.25!important;
  text-align:center!important}}
}}
"""


def _apply_ja_tentei_block_heights(html: str) -> str:
    """Alinha altura do bloco no CSS GreatPages ao layout BerryUp (evita sobreposição)."""
    bid = JA_TENTEI_BLOCK_ID
    html = re.sub(
        rf"(#{re.escape(bid)}\{{[^}}]*?)height:([0-9.]+)px",
        rf"\1height:{JA_TENTEI_DESK_MIN_H}px",
        html,
        count=1,
    )
    mob_marker = html.find('id="css_mobile"')
    if mob_marker >= 0:
        mob = html[mob_marker:]
        mob = re.sub(
            rf"(#{re.escape(bid)}\{{[^}}]*?)height:([0-9.]+)px",
            rf"\1height:{JA_TENTEI_MOB_MIN_H}px",
            mob,
            count=1,
        )
        html = html[:mob_marker] + mob
    return html


JA_TENTEI_CTA_BAR_ID = "b_1002625_1_17307234956728bea7c7c4c"
JA_TENTEI_CTA_BAR_CSS = f"""
/* Faixa 60% OFF — após depoimentos / já tentei, sem sobrepor */
#{JA_TENTEI_CTA_BAR_ID}{{
  position:relative!important;top:auto!important;clear:both!important;overflow:visible!important}}
@media(min-width:801px){{
#{JA_TENTEI_CTA_BAR_ID}{{min-height:368px!important;height:auto!important}}
}}
@media(max-width:800px){{
#{JA_TENTEI_CTA_BAR_ID}{{min-height:120px!important;height:auto!important}}
}}
"""


def inject_ja_tentei_video(html: str) -> str:
    """Vídeo com menu de abas à direita do título (desktop) ou abaixo do subtítulo (mobile)."""
    if JA_TENTEI_SUBTITLE_EID not in html:
        return html
    html = remove_element(html, JA_TENTEI_VIDEO_ID)
    insert_at = _div_close_index(html, JA_TENTEI_SUBTITLE_EID)
    if insert_at < 0:
        return html
    html = html[:insert_at] + ja_tentei_video_html() + html[insert_at:]
    html = _apply_ja_tentei_block_heights(html)
    css = (ja_tentei_video_css(html) + JA_TENTEI_CTA_BAR_CSS).strip() + "\n"
    ja_css = re.search(
        r"/\* Já tentei de tudo —.*?(?=\n/\* [^*]|\nhtml,body|\n/\* Depoimentos)",
        html,
        re.DOTALL,
    )
    if ja_css:
        html = html[: ja_css.start()] + css + html[ja_css.end() :]
    elif f"#{JA_TENTEI_VIDEO_ID}" not in html:
        html = html.replace("</style>", css + "</style>", 1)
    if 'id="berryup-ja-tentei-video-script"' not in html:
        html = html.replace("</body>", JA_TENTEI_VIDEO_SCRIPT + "</body>", 1)
    return html

BLOCKS_REMOVE = [
    "b_1002625_1_17307234956728bea7c7c56",
    "b_1002625_1_17307234956728bea7c7c5c",
]

ELEMENTS_REMOVE = [
    "e_1002625_1_17307234956728bea7ceb61071553269",  # ícone animado na barra de urgência
    "e_1002625_1_17307234956728bea7c96e4590600997",
    "e_1002625_1_17307234956728bea7de2a2802025722",
    "e_1002625_1_17307234956728bea7c9790012299580",
    "e_1002625_1_17307234956728bea7c9631048042763",
    "e_1002625_1_17307234956728bea7c9858650364500",
    "e_1002625_1_17307234956728bea7c992a944701328",
]


DEPOIMENTOS_BLOCK_ID = "b_1002625_1_17307234956728bea7c7c2e"
DEPOIMENTOS_NEXT_TEXT_PREFIX = "e_1002625_1_17307234956728bea7e6eab069875421"
DEPOIMENTOS_NEXT_BTN_PREFIX = "e_1002625_1_17307234956728bea7e6bc6088578960"
# Sprite de estrelas do editor — no mobile fica solto (2 fileiras no mesmo PNG)
DEPOIMENTOS_ORPHAN_STARS_EID = "e_1002625_1_17307234956728bea7e053b484331025"
DEPOIMENTOS_SHIFT_DESKTOP = 314
DEPOIMENTOS_SHIFT_MOBILE = 72
DEPOIMENTOS_ROW2_EXTRA_DESKTOP = 50
DEPOIMENTOS_BOTTOM_PAD = 72
DEPOIMENTOS_MOBILE_START_Y = 96
DEPOIMENTOS_MOBILE_CARD_GAP = 20
DEPOIMENTOS_MOBILE_CLUSTER_GAP = 40
DEPOIMENTOS_MOBILE_CARD_MIN_H = 228
DEPOIMENTOS_MOBILE_BLOCK_MARGIN_TOP = 48
DEPOIMENTOS_HIDE_ON_MOBILE = True

DEPOIMENTOS_CTA_ROW_CSS = f"""
/* Depoimentos — "Você pode ser a próxima" + botão lado a lado (sem sobrepor) */
#{DEPOIMENTOS_BLOCK_ID} [id^="{DEPOIMENTOS_NEXT_TEXT_PREFIX}"]{{
  z-index:376!important;width:auto!important;max-width:min(300px,42vw)!important;height:auto!important}}
#{DEPOIMENTOS_BLOCK_ID} [id^="{DEPOIMENTOS_NEXT_BTN_PREFIX}"].gpc-e.e_botao,
#{DEPOIMENTOS_BLOCK_ID} [id^="{DEPOIMENTOS_NEXT_BTN_PREFIX}"].gpc-e.e_botao.berryup-cta-wrap-centered{{
  z-index:377!important;transform:none!important;height:auto!important;box-sizing:border-box!important}}
#{DEPOIMENTOS_BLOCK_ID} [id^="{DEPOIMENTOS_NEXT_BTN_PREFIX}"] a.berryup-checkout-cta{{
  width:100%!important;max-width:100%!important}}
@media(min-width:801px){{
#{DEPOIMENTOS_BLOCK_ID} [id^="{DEPOIMENTOS_NEXT_TEXT_PREFIX}"]{{
  left:50%!important;transform:translateX(calc(-50% - 125px))!important;white-space:nowrap!important}}
#{DEPOIMENTOS_BLOCK_ID} [id^="{DEPOIMENTOS_NEXT_BTN_PREFIX}"]{{
  left:50%!important;transform:translateX(calc(-50% + 150px))!important;
  width:min(300px,34vw)!important;max-width:340px!important}}
}}
@media(max-width:800px){{
#{DEPOIMENTOS_BLOCK_ID} [id^="{DEPOIMENTOS_NEXT_TEXT_PREFIX}"]{{
  left:50%!important;transform:translateX(-50%)!important;width:auto!important;max-width:92vw!important;
  text-align:center!important}}
#{DEPOIMENTOS_BLOCK_ID} [id^="{DEPOIMENTOS_NEXT_TEXT_PREFIX}"] .c,
#{DEPOIMENTOS_BLOCK_ID} [id^="{DEPOIMENTOS_NEXT_TEXT_PREFIX}"] .c p{{text-align:center!important}}
#{DEPOIMENTOS_BLOCK_ID} [id^="{DEPOIMENTOS_NEXT_BTN_PREFIX}"]{{
  left:50%!important;transform:translateX(-50%)!important;
  width:min(300px,92vw)!important;max-width:92vw!important}}
}}
"""

DEPOIMENTOS_MOBILE_CSS = f"""
/* Depoimentos — oculto no mobile (≤800px); desktop inalterado */
@media(max-width:800px){{
#{DEPOIMENTOS_BLOCK_ID},
#{DEPOIMENTOS_BLOCK_ID} .centralizar,
#{DEPOIMENTOS_BLOCK_ID} .gpc-b_sobreposicao{{
  display:none!important;visibility:hidden!important;height:0!important;
  min-height:0!important;max-height:0!important;overflow:hidden!important;
  margin:0!important;padding:0!important;pointer-events:none!important}}
}}
"""

BERRYUP_MOBILE_LAYOUT_SCRIPT = f"""<script id="berryup-mobile-sections-script">(function(){{
var DEPO="{DEPOIMENTOS_BLOCK_ID}";
var JA="{JA_TENTEI_BLOCK_ID}";
function mob(){{return window.matchMedia("(max-width:800px)").matches;}}
function setPos(el,top,left,width){{
  if(!el)return;
  el.style.setProperty("position","absolute","important");
  el.style.setProperty("top",Math.round(top)+"px","important");
  el.style.setProperty("left",left||"16px","important");
  el.style.setProperty("right","auto","important");
  el.style.setProperty("transform","none","important");
  if(width)el.style.setProperty("width",width,"important");
  var isCeoImg=el.id==="{JA_TENTEI_CEO_IMG_LEFT}"||el.id==="{JA_TENTEI_CEO_IMG_RIGHT}";
  if(!isCeoImg){{
    el.style.setProperty("height","auto","important");
    el.style.setProperty("min-height","0","important");
  }}
  el.style.setProperty("max-width","92vw","important");
}}
var CEO_IMG_LEFT_URL="{JA_TENTEI_CEO_IMG_LEFT_URL}";
var CEO_IMG_RIGHT_URL="{JA_TENTEI_CEO_IMG_RIGHT_URL}";
var CEO_IMG_DESK_H={JA_TENTEI_CEO_IMG_DESK_H};
function ensureCeoImage(el,fallbackUrl){{
  if(!el)return;
  var desk=window.matchMedia("(min-width:801px)").matches;
  var h=desk?CEO_IMG_DESK_H:Math.max(200,Math.round(window.innerWidth*0.48));
  el.style.setProperty("display","block","important");
  el.style.setProperty("visibility","visible","important");
  el.style.setProperty("opacity","1","important");
  el.style.setProperty("height",h+"px","important");
  el.style.setProperty("min-height",h+"px","important");
  el.style.setProperty("overflow","hidden","important");
  var c=el.querySelector(".c");
  if(c){{
    c.style.setProperty("width","100%","important");
    c.style.setProperty("height","100%","important");
    c.style.setProperty("min-height",h+"px","important");
    c.style.setProperty("display","block","important");
    c.style.setProperty("position","relative","important");
  }}
  var bg=el.querySelector(".imagem_fundo");
  if(!bg&&c){{
    bg=document.createElement("div");
    bg.className="imagem_fundo";
    c.appendChild(bg);
  }}
  if(!bg)return;
  var src=el.getAttribute("ll_src")||el.getAttribute("ll_src_mobile")||fallbackUrl||"";
  if(src)bg.style.setProperty("background-image",'url("'+src+'")',"important");
  bg.style.setProperty("display","block","important");
  bg.style.setProperty("opacity","1","important");
  bg.style.setProperty("width","100%","important");
  bg.style.setProperty("height","100%","important");
  bg.style.setProperty("min-height",h+"px","important");
  bg.style.setProperty("background-size","cover","important");
  bg.style.setProperty("background-position","center top","important");
  bg.style.setProperty("background-repeat","no-repeat","important");
}}
function hideDepoStars(block){{
  block.querySelectorAll(".gpc-e.e_imagem.dd.dm").forEach(function(el){{
    el.style.setProperty("display","none","important");
    el.style.setProperty("visibility","hidden","important");
    el.style.setProperty("height","0","important");
    el.style.setProperty("overflow","hidden","important");
    el.style.setProperty("pointer-events","none","important");
  }});
}}
function layoutDepoimentos(){{
  if(!mob())return;
  var block=document.getElementById(DEPO);
  if(!block)return;
  block.style.setProperty("display","none","important");
  block.style.setProperty("visibility","hidden","important");
  block.style.setProperty("height","0","important");
  block.style.setProperty("min-height","0","important");
  block.style.setProperty("overflow","hidden","important");
  block.style.setProperty("pointer-events","none","important");
  return;
  var cen=block.querySelector(".centralizar");
  if(!cen)return;
  hideDepoStars(block);
  var caixas=[].slice.call(block.querySelectorAll(".gpc-e.e_caixa.esconder_mobile"));
  if(!caixas.length)return;
  caixas.sort(function(a,b){{return a.offsetTop-b.offsetTop;}});
  var y=96;
  var cardW="min(calc(92vw - 8px), 400px)";
  var cardL="calc(50% - min(46vw, 190px))";
  var cardPadL="calc(50% - min(46vw, 190px) + 12px)";
  var metaL="calc(50% - min(46vw, 190px) + 76px)";
  caixas.forEach(function(caixa,i){{
    var bandTop=caixa.offsetTop;
    var next=caixas[i+1];
    var bandBottom=next?next.offsetTop:bandTop+900;
    var kids=[].slice.call(block.querySelectorAll(".gpc-e.e_circulo.dd.dm,.gpc-e.e_texto.dd.dm"));
    kids=kids.filter(function(el){{
      var ot=el.offsetTop;
      return ot>=bandTop-40&&ot<bandBottom-8;
    }});
    setPos(caixa,y,cardL,cardW);
    var innerY=y+14;
    var circ=kids.filter(function(e){{return e.classList.contains("e_circulo");}})[0];
    var texts=kids.filter(function(e){{return e.classList.contains("e_texto");}});
    texts.sort(function(a,b){{return a.offsetHeight-b.offsetHeight;}});
    var shorts=texts.filter(function(e){{return e.offsetHeight<56;}});
    var longs=texts.filter(function(e){{return e.offsetHeight>=56;}});
    if(circ)setPos(circ,innerY,cardPadL,"52px");
    var metaY=innerY;
    shorts.slice(0,2).forEach(function(el){{
      setPos(el,metaY,metaL,"min(calc(92vw - 96px), 280px)");
      metaY+=Math.max(el.offsetHeight,26)+6;
    }});
    var quoteY=Math.max(innerY+58,metaY)+8;
    longs.concat(shorts.slice(2)).forEach(function(el){{
      setPos(el,quoteY,cardPadL,"min(calc(92vw - 24px), 400px)");
      quoteY+=Math.max(el.offsetHeight,32)+10;
    }});
    var cardH=Math.max(200,quoteY-y+18);
    caixa.style.setProperty("height",cardH+"px","important");
    y+=cardH+20;
  }});
  var ctaText=block.querySelector('[id^="{DEPOIMENTOS_NEXT_TEXT_PREFIX}"]');
  var ctaBtn=block.querySelector('[id^="{DEPOIMENTOS_NEXT_BTN_PREFIX}"]');
  if(ctaText){{setPos(ctaText,y+8,"50%","auto");ctaText.style.setProperty("transform","translateX(-50%)","important");y+=ctaText.offsetHeight+12;}}
  if(ctaBtn){{setPos(ctaBtn,y,"50%","min(300px,92vw)");ctaBtn.style.setProperty("transform","translateX(-50%)","important");y+=ctaBtn.offsetHeight+16;}}
  var blockH=y+32;
  block.style.setProperty("height","auto","important");
  block.style.setProperty("min-height",blockH+"px","important");
  cen.style.setProperty("min-height",blockH+"px","important");
}}
function layoutJaTentei(){{
  if(!mob())return;
  var block=document.getElementById(JA);
  if(!block)return;
  var cen=block.querySelector(".centralizar");
  if(!cen)return;
  var stack=[
    "{JA_TENTEI_TITLE_EID}",
    "{JA_TENTEI_SUBTITLE_BOX_EID}",
    "{JA_TENTEI_SUBTITLE_EID}",
    "{JA_TENTEI_VIDEO_ID}",
    "{JA_TENTEI_EID}",
    "{JA_TENTEI_CEO_HEADLINE_EID}",
    "{JA_TENTEI_CEO_SUBLINE_EID}"
  ];
  var y=16;
  stack.forEach(function(id){{
    var el=document.getElementById(id);
    if(!el)return;
    var disp=getComputedStyle(el).display;
    if(disp==="none")return;
    setPos(el,y,"16px","calc(100% - 32px)");
    y+=Math.max(el.offsetHeight,8)+12;
  }});
  var imgL=document.getElementById("{JA_TENTEI_CEO_IMG_LEFT}");
  var imgR=document.getElementById("{JA_TENTEI_CEO_IMG_RIGHT}");
  if(imgL&&imgR){{
    var rowY=y;
    setPos(imgL,rowY,"16px","calc(50% - 24px)");
    setPos(imgR,rowY,"calc(50% + 8px)","calc(50% - 24px)");
    ensureCeoImage(imgL,CEO_IMG_LEFT_URL);
    ensureCeoImage(imgR,CEO_IMG_RIGHT_URL);
    y+=Math.max(imgL.offsetHeight,imgR.offsetHeight,200)+10;
  }}
  var yearL=document.getElementById("{JA_TENTEI_YEAR_LEFT}");
  var yearR=document.getElementById("{JA_TENTEI_YEAR_RIGHT}");
  if(yearL){{setPos(yearL,y,"16px","calc(50% - 24px)");}}
  if(yearR){{setPos(yearR,y,"calc(50% + 8px)","calc(50% - 24px)");}}
  if(yearL||yearR)y+=32;
  ["e_1002625_1_17307234956728bea7e6eab069875421_m",
   "e_1002625_1_17307234956728bea7e70b4426371193_m",
   "e_1002625_1_17307234956728bea7e6bc6088578960_m"].forEach(function(id){{
    var el=document.getElementById(id);
    if(!el)return;
    setPos(el,y,"16px","calc(100% - 32px)");
    if(el.classList.contains("e_botao"))el.style.setProperty("width","min(300px,92vw)","important");
    y+=Math.max(el.offsetHeight,8)+12;
  }});
  var orange=document.getElementById("{JA_TENTEI_ORANGE_BAR_M}");
  var tags=document.getElementById("{JA_TENTEI_HASHTAG_MOBILE}");
  if(orange){{
    var barY=y+12;
    var barH=44;
    var barW="calc(100% - 32px)";
    setPos(orange,barY,"16px",barW);
    orange.style.setProperty("height",barH+"px","important");
    var oc=orange.querySelector(".c");
    if(oc){{
      oc.style.setProperty("height","100%","important");
      oc.style.setProperty("display","flex","important");
      oc.style.setProperty("align-items","center","important");
      oc.style.setProperty("border","none","important");
    }}
    if(tags){{
      setPos(tags,barY,"16px",barW);
      tags.style.setProperty("height",barH+"px","important");
      tags.style.setProperty("z-index","500","important");
      var tc=tags.querySelector(".c");
      if(tc){{
        tc.style.setProperty("height","100%","important");
        tc.style.setProperty("display","flex","important");
        tc.style.setProperty("align-items","center","important");
        tc.style.setProperty("justify-content","center","important");
        tc.style.setProperty("line-height","1.25","important");
        tc.style.setProperty("padding","0 12px","important");
        tc.style.setProperty("box-sizing","border-box","important");
      }}
      var tp=tags.querySelector("p");
      if(tp)tp.style.setProperty("margin","0","important");
    }}
    y+=barH+16;
  }}
  var blockH=y+24;
  block.style.setProperty("height","auto","important");
  block.style.setProperty("min-height",blockH+"px","important");
  cen.style.setProperty("min-height",blockH+"px","important");
}}
function layoutJaTenteiDesktop(){{
  if(!window.matchMedia("(min-width:801px)").matches)return;
  var block=document.getElementById(JA);
  if(!block)return;
  var cen=block.querySelector(".centralizar");
  if(!cen)return;
  var headline=document.getElementById("{JA_TENTEI_CEO_HEADLINE_EID}");
  var subline=document.getElementById("{JA_TENTEI_CEO_SUBLINE_EID}");
  var yearL=document.getElementById("{JA_TENTEI_YEAR_LEFT}");
  var yearR=document.getElementById("{JA_TENTEI_YEAR_RIGHT}");
  var imgL=document.getElementById("{JA_TENTEI_CEO_IMG_LEFT}");
  var imgR=document.getElementById("{JA_TENTEI_CEO_IMG_RIGHT}");
  [headline,subline,yearL,yearR,imgL,imgR].forEach(function(el){{
    if(!el)return;
    el.style.setProperty("display","none","important");
    el.style.setProperty("visibility","hidden","important");
    el.style.setProperty("height","0","important");
    el.style.setProperty("min-height","0","important");
    el.style.setProperty("overflow","hidden","important");
    el.style.setProperty("pointer-events","none","important");
  }});
  var y=632;
  ["{JA_TENTEI_CTA_TEXT_M}","{JA_TENTEI_CTA_BTN_M}"].forEach(function(id){{
    var el=document.getElementById(id);
    if(!el)return;
    el.style.setProperty("display","none","important");
  }});
  var ctaText=document.getElementById("{JA_TENTEI_CTA_TEXT_D}");
  var ctaBtn=document.getElementById("{JA_TENTEI_CTA_BTN_D}");
  if(ctaText){{
    ctaText.style.setProperty("display","block","important");
    ctaText.style.setProperty("visibility","visible","important");
    ctaText.style.setProperty("left","50%","important");
    ctaText.style.setProperty("transform","translateX(calc(-50% - 155px))","important");
    ctaText.style.setProperty("top",y+"px","important");
  }}
  if(ctaBtn){{
    ctaBtn.style.setProperty("display","block","important");
    ctaBtn.style.setProperty("visibility","visible","important");
    ctaBtn.style.setProperty("left","50%","important");
    ctaBtn.style.setProperty("transform","translateX(calc(-50% + 155px))","important");
    ctaBtn.style.setProperty("top",y-6+"px","important");
    y+=Math.max(ctaBtn.offsetHeight,52);
  }}
  y+=16;
  block.style.setProperty("height","auto","important");
  block.style.setProperty("min-height",y+"px","important");
  cen.style.setProperty("min-height",y+"px","important");
}}
function run(){{
  layoutDepoimentos();
  layoutJaTentei();
  layoutJaTenteiDesktop();
}}
function schedule(){{
  run();
  requestAnimationFrame(run);
  setTimeout(run,80);
  setTimeout(run,450);
}}
if(document.readyState==="loading")document.addEventListener("DOMContentLoaded",schedule);
else schedule();
window.addEventListener("resize",function(){{clearTimeout(window._berryupMobT);window._berryupMobT=setTimeout(run,120);}});
if(document.fonts&&document.fonts.ready)document.fonts.ready.then(run);
}})();</script>"""


JA_TENTEI_SUBTITLE_YELLOW_CSS = f"""
#{JA_TENTEI_BLOCK_ID} #{JA_TENTEI_SUBTITLE_EID} .c h2,
#{JA_TENTEI_BLOCK_ID} #{JA_TENTEI_SUBTITLE_EID} .c h2 span,
#{JA_TENTEI_BLOCK_ID} #{JA_TENTEI_SUBTITLE_EID} .c > H2:nth-of-type(1),
#{JA_TENTEI_BLOCK_ID} #{JA_TENTEI_SUBTITLE_EID} .c > H2:nth-of-type(1) > SPAN:nth-of-type(1){{
  color:{BERRYUP_YELLOW_HEADLINE}!important}}
"""

JA_TENTEI_HASHTAG_BAR_MOBILE_CSS = f"""/* berryup-ja-hashtag-bar */
@media(max-width:800px){{
#{JA_TENTEI_BLOCK_ID} #{JA_TENTEI_ORANGE_BAR_M}{{
  left:16px!important;width:calc(100% - 32px)!important;max-width:none!important;
  height:44px!important;transform:none!important;z-index:394!important;
  box-sizing:border-box!important}}
#{JA_TENTEI_BLOCK_ID} #{JA_TENTEI_ORANGE_BAR_M} .c{{
  height:100%!important;display:flex!important;align-items:center!important;
  border:none!important;background-color:rgb(255,99,22)!important;
  background-image:none!important}}
#{JA_TENTEI_BLOCK_ID} #{JA_TENTEI_HASHTAG_MOBILE}{{
  left:16px!important;width:calc(100% - 32px)!important;max-width:none!important;
  height:44px!important;transform:none!important;z-index:397!important;
  pointer-events:none!important;box-sizing:border-box!important}}
#{JA_TENTEI_BLOCK_ID} #{JA_TENTEI_HASHTAG_MOBILE} .c{{
  height:100%!important;display:flex!important;align-items:center!important;
  justify-content:center!important;line-height:1.25!important;
  font-size:clamp(11px,3.2vw,15px)!important;padding:0 12px!important;
  box-sizing:border-box!important;text-align:center!important}}
#{JA_TENTEI_BLOCK_ID} #{JA_TENTEI_HASHTAG_MOBILE} .c p,
#{JA_TENTEI_BLOCK_ID} #{JA_TENTEI_HASHTAG_MOBILE} .c p span{{
  margin:0!important;padding:0!important;line-height:1.25!important;
  text-align:center!important}}
}}"""


def inject_depoimentos_hide_mobile_final(html: str) -> str:
    """Regras após css_mobile do GreatPages (prioridade sobre o editor)."""
    if 'id="berryup-head-overrides"' in html:
        if "berryup-ja-hashtag-bar" not in html:
            html = re.sub(
                r'(<style id="berryup-head-overrides">)(.*?)(</style>)',
                r"\1\2\n" + JA_TENTEI_HASHTAG_BAR_MOBILE_CSS.strip() + r"\3",
                html,
                count=1,
                flags=re.DOTALL,
            )
        return html
    rule = JA_TENTEI_SUBTITLE_YELLOW_CSS.strip()
    rule += "\n" + JA_TENTEI_HASHTAG_BAR_MOBILE_CSS.strip()
    if DEPOIMENTOS_HIDE_ON_MOBILE:
        rule += "\n" + DEPOIMENTOS_MOBILE_CSS.strip()
    inject = f'<style id="berryup-head-overrides">{rule}</style>'
    if "</head>" in html:
        return html.replace("</head>", inject + "</head>", 1)
    return html.replace("</body>", inject + "</body>", 1)


def inject_mobile_layout_script(html: str) -> str:
    if 'id="berryup-mobile-sections-script"' in html:
        return html
    return html.replace("</body>", BERRYUP_MOBILE_LAYOUT_SCRIPT + "\n</body>", 1)


def _depoimentos_element_ids(html: str) -> list[str]:
    start = html.find(f'id="{DEPOIMENTOS_BLOCK_ID}"')
    if start < 0:
        return []
    next_b = re.search(
        r'<div id="b_1002625_1_[^"]+" class="gpc-b',
        html[start + 80 :],
    )
    end = start + 80 + next_b.start() if next_b else start + 80_000
    chunk = html[start:end]
    return list(
        dict.fromkeys(
            re.findall(r'id="(e_1002625_1_17307234956728bea7[^"]+)"', chunk)
        )
    )


def _depoimentos_css_chunks(html: str) -> tuple[str, str]:
    marker = 'id="css_mobile"'
    pos = html.find(marker)
    if pos < 0:
        return html, ""
    return html[:pos], html[pos:]


def _css_without_media_blocks(css: str) -> str:
    """Remove @media { ... } so desktop height ignores mobile-only tops."""
    out: list[str] = []
    i = 0
    while i < len(css):
        m = css.find("@media", i)
        if m < 0:
            out.append(css[i:])
            break
        out.append(css[i:m])
        brace = css.find("{", m)
        if brace < 0:
            break
        depth = 1
        j = brace + 1
        while j < len(css) and depth:
            if css[j] == "{":
                depth += 1
            elif css[j] == "}":
                depth -= 1
            j += 1
        i = j
    return "".join(out)


def _depoimentos_mobile_override_css(desk_css: str) -> str:
    """@media(max-width:800px) depoimentos overrides live in the desktop <style> chunk."""
    anchor = "@media(max-width:800px){#e_1002625_1_17307234956728bea7c99d8485229936"
    pos = desk_css.find(anchor)
    if pos < 0:
        return ""
    brace = desk_css.find("{", pos)
    depth = 1
    j = brace + 1
    while j < len(desk_css) and depth:
        if desk_css[j] == "{":
            depth += 1
        elif desk_css[j] == "}":
            depth -= 1
        j += 1
    return desk_css[pos:j]


def _strip_depoimentos_mobile_override_block(html: str) -> str:
    anchor = "@media(max-width:800px){#e_1002625_1_17307234956728bea7c99d8485229936"
    marker = f"#{DEPOIMENTOS_BLOCK_ID}{{overflow:visible"
    pos = html.find(anchor)
    if pos < 0:
        return html
    mpos = html.find(marker, pos)
    if mpos < 0:
        return html
    return html[:pos] + html[mpos:]


def _depoimentos_content_bottom(css: str, eid_set: set[str], max_top: float | None = None) -> float:
    bottom = 0.0
    for eid in eid_set:
        for body in re.findall(rf"#{re.escape(eid)}\{{([^}}]+)\}}", css):
            top_m = re.search(r"top:([0-9.]+)px", body)
            h_m = re.search(r"height:([0-9.]+)px", body)
            if not top_m or not h_m:
                continue
            top = float(top_m.group(1))
            if max_top is not None and top > max_top:
                continue
            bottom = max(bottom, top + float(h_m.group(1)))
    return bottom


def _depoimentos_block_heights(
    html: str, mob_h_override: int | None = None
) -> tuple[int, int]:
    eid_set = set(_depoimentos_element_ids(html))
    if not eid_set:
        return 760, mob_h_override or 1200
    cls_map = _depoimentos_element_classes(html, eid_set)
    height_eids = {
        eid
        for eid in eid_set
        if not _depoimentos_mobile_should_skip(eid, cls_map.get(eid, ""))
    }
    desk_css, mob_css = _depoimentos_css_chunks(html)
    desk_plain = _css_without_media_blocks(desk_css)
    desk = math.ceil(
        _depoimentos_content_bottom(desk_plain, height_eids) + DEPOIMENTOS_BOTTOM_PAD
    )
    mob_rules = _depoimentos_mobile_override_css(desk_css) or mob_css
    mob_from_css = math.ceil(
        _depoimentos_content_bottom(mob_rules, height_eids) + DEPOIMENTOS_BOTTOM_PAD
    )
    if mob_h_override is not None:
        # O empilhamento soma elementos ocultos; limita à extensão real no CSS mobile.
        mob = min(mob_h_override, mob_from_css)
    else:
        mob = mob_from_css
    return max(desk, 400), max(mob, 400)


def _depoimentos_block_chunk(html: str) -> str:
    start = html.find(f'id="{DEPOIMENTOS_BLOCK_ID}"')
    if start < 0:
        return ""
    next_b = re.search(
        r'<div id="b_1002625_1_[^"]+" class="gpc-b',
        html[start + 80 :],
    )
    end = start + 80 + next_b.start() if next_b else start + 80_000
    return html[start:end]


def _depoimentos_element_classes(html: str, eid_set: set[str]) -> dict[str, str]:
    chunk = _depoimentos_block_chunk(html)
    out: dict[str, str] = {}
    for eid, cls in re.findall(
        r'id="(e_1002625_1_17307234956728bea7[^"]+)"[^>]*class="gpc-e ([^"]+)"',
        chunk,
    ):
        if eid in eid_set:
            out[eid] = cls
    return out


def _depoimentos_mobile_should_skip(eid: str, cls: str) -> bool:
    if eid == DEPOIMENTOS_ORPHAN_STARS_EID or eid in ELEMENTS_REMOVE:
        return True
    if not cls:
        return True
    if "e_imagem" in cls:
        return True
    return "e_caixa" in cls and "esconder_mobile" not in cls


def _depoimentos_parse_rule(body: str) -> tuple[float, float] | None:
    top_m = re.search(r"top:([0-9.]+)px", body)
    if not top_m:
        return None
    h_m = re.search(r"height:([0-9.]+)px", body)
    height = float(h_m.group(1)) if h_m else 48.0
    return float(top_m.group(1)), height


def _depoimentos_layout_height(cls: str, height: float) -> float:
    if "e_circulo" in cls:
        return 56.0
    if "e_texto" in cls or "e_titulo" in cls:
        if height >= 72:
            return min(max(height * 0.55, 72.0), 140.0)
        if height >= 40:
            return 32.0
        return 28.0
    return max(height, 36.0)


def _depoimentos_child_sort_key(el: dict) -> tuple:
    cls = el.get("cls", "")
    if "e_circulo" in cls:
        order = 0
    elif "e_titulo" in cls:
        order = 1
    else:
        order = 2
    return order, el["top"]


def _depoimentos_layout_card_children(
    caixa_y: float, children: list[dict]
) -> tuple[dict[str, float], dict[str, str], dict[str, str]]:
    """Avatar à esquerda; nome/cidade à direita; depoimento em largura total abaixo."""
    tops: dict[str, float] = {}
    lefts: dict[str, str] = {}
    widths: dict[str, str] = {}
    pad_top = 14.0
    card_left = "calc(50% - min(46vw, 190px) + 12px)"
    text_left = "calc(50% - min(46vw, 190px) + 76px)"
    quote_width = "min(calc(92vw - 24px), 400px)"
    short_width = "min(calc(92vw - 96px), 280px)"

    row_top = caixa_y + pad_top
    circulos = [c for c in children if "e_circulo" in c["cls"]]
    textos = sorted(
        [c for c in children if "e_texto" in c["cls"] or "e_titulo" in c["cls"]],
        key=lambda e: (e["height"], e["top"]),
    )
    short_texts = [t for t in textos if t["height"] < 56]
    long_texts = [t for t in textos if t["height"] >= 56]

    if circulos:
        el = circulos[0]
        tops[el["eid"]] = row_top
        lefts[el["eid"]] = card_left
        widths[el["eid"]] = "52px"

    meta_y = row_top
    for el in short_texts[:2]:
        tops[el["eid"]] = meta_y
        lefts[el["eid"]] = text_left
        widths[el["eid"]] = short_width
        meta_y += _depoimentos_layout_height(el["cls"], el["height"]) + 6.0

    quote_y = max(row_top + 58.0, meta_y) + 8.0
    for el in long_texts + short_texts[2:]:
        eh = _depoimentos_layout_height(el["cls"], el["height"])
        tops[el["eid"]] = quote_y
        lefts[el["eid"]] = card_left
        widths[el["eid"]] = quote_width
        quote_y += eh + 10.0

    return tops, lefts, widths


def _depoimentos_format_top(value: float) -> str:
    rounded = round(value, 4)
    if rounded == int(rounded):
        return str(int(rounded))
    return f"{rounded:.4f}".rstrip("0").rstrip(".")


def _depoimentos_replace_top(body: str, new_top: float) -> str:
    top_m = re.search(r"top:([0-9.]+)px", body)
    if not top_m:
        return body
    top_str = _depoimentos_format_top(new_top)
    return body[: top_m.start()] + f"top:{top_str}px" + body[top_m.end() :]


def _depoimentos_replace_height(body: str, new_height: float) -> str:
    h_m = re.search(r"height:([0-9.]+)px", body)
    if not h_m:
        return body + f";height:{_depoimentos_format_top(new_height)}px"
    h_str = _depoimentos_format_top(new_height)
    return body[: h_m.start()] + f"height:{h_str}px" + body[h_m.end() :]


def _depoimentos_replace_prop(body: str, prop: str, value: str) -> str:
    pat = rf"{prop}:([^;}}]+)"
    if re.search(pat, body):
        return re.sub(pat, f"{prop}:{value}", body, count=1)
    return body + f";{prop}:{value}"


def _depoimentos_rule_extra(
    eid: str,
    lefts: dict[str, str],
    widths: dict[str, str],
) -> str:
    parts: list[str] = []
    if eid in lefts:
        parts.append(f"left:{lefts[eid]}!important")
    if eid in widths:
        parts.append(f"width:{widths[eid]}!important")
        if widths[eid] in ("52px",):
            parts.append("height:52px!important")
        else:
            parts.append("height:auto!important;max-width:92vw!important")
    return ";".join(parts)


def _depoimentos_cluster_elements(
    elements: list[dict], gap: float = DEPOIMENTOS_MOBILE_CLUSTER_GAP
) -> list[list[dict]]:
    if not elements:
        return []
    ordered = sorted(elements, key=lambda e: e["top"])
    clusters: list[list[dict]] = [[ordered[0]]]
    for el in ordered[1:]:
        if el["top"] - clusters[-1][-1]["top"] > gap:
            clusters.append([el])
        else:
            clusters[-1].append(el)
    return clusters


def _depoimentos_balance_clusters(
    clusters: list[list[dict]], target: int
) -> list[list[dict]]:
    clusters = [c for c in clusters if c]
    while len(clusters) > target:
        span_i = max(
            range(len(clusters)),
            key=lambda i: clusters[i][-1]["top"] - clusters[i][0]["top"],
        )
        cl = clusters[span_i]
        if len(cl) < 2:
            break
        split_at = 1
        max_gap = 0.0
        for j in range(1, len(cl)):
            g = cl[j]["top"] - cl[j - 1]["top"]
            if g > max_gap:
                max_gap = g
                split_at = j
        if max_gap < 80:
            break
        clusters = (
            clusters[:span_i]
            + [cl[:split_at], cl[split_at:]]
            + clusters[span_i + 1 :]
        )
    while len(clusters) < target and len(clusters) > 1:
        clusters[-2].extend(clusters.pop())
    return clusters


def relayout_depoimentos_mobile_css(html: str) -> tuple[str, int]:
    """Empilha cards de depoimento no mobile (tops absolutos do editor se sobrepõem)."""
    html = _strip_depoimentos_mobile_override_block(html)
    eid_set = set(_depoimentos_element_ids(html))
    if not eid_set:
        return html, 1200

    mob_marker = html.find('id="css_mobile"')
    if mob_marker < 0:
        return html, 1200

    cls_map = _depoimentos_element_classes(html, eid_set)
    removed = set(ELEMENTS_REMOVE)
    caixas: list[dict] = []
    elements: list[dict] = []

    for eid in eid_set:
        if eid in removed:
            continue
        cls = cls_map.get(eid, "")
        if _depoimentos_mobile_should_skip(eid, cls):
            continue
        mob_rule = None
        for match in re.finditer(
            rf"#{re.escape(eid)}\{{([^}}]+)\}}", html[mob_marker:]
        ):
            mob_rule = match
            break
        if not mob_rule:
            continue
        parsed = _depoimentos_parse_rule(mob_rule.group(1))
        if not parsed:
            continue
        top, height = parsed
        item = {"eid": eid, "top": top, "height": height, "cls": cls}
        if "e_caixa" in cls and "esconder_mobile" in cls:
            caixas.append(item)
        else:
            elements.append(item)

    if not caixas:
        return html, math.ceil(
            _depoimentos_content_bottom(html[mob_marker:], eid_set)
            + DEPOIMENTOS_BOTTOM_PAD
        )

    caixas.sort(key=lambda c: c["top"])
    ordered_els = sorted(elements, key=lambda e: e["top"])
    for el in elements:
        el["caixa"] = None
    for i, caixa in enumerate(caixas):
        y0 = caixa["top"] - 8.0
        y1 = caixas[i + 1]["top"] - 8.0 if i + 1 < len(caixas) else 1e9
        for el in ordered_els:
            if y0 <= el["top"] < y1:
                el["caixa"] = caixa
    for el in ordered_els:
        if el["caixa"] is None and caixas:
            nearest = min(
                caixas,
                key=lambda c: abs(c["top"] - el["top"]),
            )
            el["caixa"] = nearest

    new_tops: dict[str, float] = {}
    new_heights: dict[str, float] = {}
    new_lefts: dict[str, str] = {}
    new_widths: dict[str, str] = {}
    y = float(DEPOIMENTOS_MOBILE_START_Y)

    for caixa in caixas:
        children = [el for el in elements if el.get("caixa") is caixa]
        new_tops[caixa["eid"]] = y
        child_tops, child_lefts, child_widths = _depoimentos_layout_card_children(
            y, children
        )
        new_tops.update(child_tops)
        new_lefts.update(child_lefts)
        new_widths.update(child_widths)
        if child_tops:
            last_eid = max(child_tops, key=child_tops.get)
            last_el = next(c for c in children if c["eid"] == last_eid)
            inner_bottom = child_tops[last_eid] + _depoimentos_layout_height(
                last_el["cls"], last_el["height"]
            )
        else:
            inner_bottom = y + 80.0
        card_bottom = max(
            y + DEPOIMENTOS_MOBILE_CARD_MIN_H,
            inner_bottom + 24.0,
        )
        new_heights[caixa["eid"]] = card_bottom - y
        y = card_bottom + DEPOIMENTOS_MOBILE_CARD_GAP

    cta_prefixes = (DEPOIMENTOS_NEXT_TEXT_PREFIX, DEPOIMENTOS_NEXT_BTN_PREFIX)
    cta_y = y + 16.0
    for eid in sorted(eid_set):
        if not any(eid.startswith(p) for p in cta_prefixes):
            continue
        cls = cls_map.get(eid, "")
        if "dm" not in cls.split():
            continue
        if _depoimentos_mobile_should_skip(eid, cls):
            continue
        mob_rule = re.search(
            rf"#{re.escape(eid)}\{{([^}}]+)\}}", html[mob_marker:]
        )
        eh = 48.0
        if mob_rule:
            parsed = _depoimentos_parse_rule(mob_rule.group(1))
            if parsed:
                eh = _depoimentos_layout_height(cls, parsed[1])
        new_tops[eid] = cta_y
        cta_y += eh + 20.0
    y = cta_y

    mob_section = html[mob_marker:]
    for eid in sorted(new_tops.keys(), key=len, reverse=True):
        if eid not in eid_set:
            continue
        top_val = new_tops[eid]

        def replace_one(match: re.Match, tv: float = top_val, eid=eid) -> str:
            body = _depoimentos_replace_top(match.group(1), tv)
            if eid in new_heights:
                body = _depoimentos_replace_height(body, new_heights[eid])
            if eid in new_lefts:
                body = _depoimentos_replace_prop(body, "left", new_lefts[eid])
            if eid in new_widths:
                body = _depoimentos_replace_prop(body, "width", new_widths[eid])
            return f"#{eid}{{{body}}}"

        mob_section, _ = re.subn(
            rf"#{re.escape(eid)}\{{([^}}]+)\}}",
            replace_one,
            mob_section,
            count=1,
        )
    html = html[:mob_marker] + mob_section
    override_rules = "".join(
        f"#{eid}{{top:{_depoimentos_format_top(new_tops[eid])}px!important;"
        + (
            f"height:{_depoimentos_format_top(new_heights[eid])}px!important;"
            if eid in new_heights
            else ""
        )
        + (
            f"{_depoimentos_rule_extra(eid, new_lefts, new_widths)};"
            if _depoimentos_rule_extra(eid, new_lefts, new_widths)
            else ""
        )
        + "}\n"
        for eid in sorted(new_tops.keys())
        if eid in eid_set
    )
    for eid in sorted(eid_set):
        if eid in new_tops or eid in removed:
            continue
        cls = cls_map.get(eid, "")
        if _depoimentos_mobile_should_skip(eid, cls):
            continue
        if "dm" not in cls.split() or "esconder_mobile" in cls:
            continue
        override_rules += (
            f"#{eid}{{display:none!important;visibility:hidden!important;"
            f"height:0!important;width:0!important;overflow:hidden!important;"
            f"pointer-events:none!important}}\n"
        )
    if override_rules:
        inject = f"@media(max-width:800px){{{override_rules}}}\n"
        marker = f"#{DEPOIMENTOS_BLOCK_ID}{{overflow:visible"
        if marker in html:
            html = html.replace(marker, inject + marker, 1)
        else:
            html = html.replace("</style>", inject + "</style>", 1)
    mob_h = math.ceil(y + DEPOIMENTOS_BOTTOM_PAD)
    return html, max(mob_h, 400)


def _shift_for_depoimento(top_val: float, rule_index: int) -> float:
    # Regra 1+ = css_mobile: deslocamento uniforme (extras quebravam o espaçamento entre cards)
    if rule_index >= 1:
        return DEPOIMENTOS_SHIFT_MOBILE
    shift = DEPOIMENTOS_SHIFT_DESKTOP
    if top_val >= 800:
        shift += DEPOIMENTOS_ROW2_EXTRA_DESKTOP
    return shift


HERO_IMG_EID = HERO_WOMAN_EID
HERO_IMG_CSS = f"""
#{HERO_IMG_EID}{{z-index:1450!important}}
#{HERO_IMG_EID} .c .imagem_fundo{{
  background-image:url("{HERO_IMG_NEW}")!important;
  background-size:contain!important;
  background-position:right bottom!important;
  background-repeat:no-repeat!important;
}}
@media(max-width:800px){{
#{HERO_IMG_EID}{{
  left:50%!important;top:clamp(200px,44vw,290px)!important;
  width:clamp(300px,92vw,440px)!important;height:clamp(360px,88vw,520px)!important;
  max-width:94vw!important;transform:translateX(-50%)!important;z-index:1240!important}}
#{HERO_IMG_EID} .c{{width:100%!important;height:100%!important}}
#{HERO_IMG_EID} .c .imagem_fundo{{
  background-image:url("{HERO_IMG_NEW}")!important;
  width:100%!important;height:100%!important;
  background-size:contain!important;
  background-position:center bottom!important;
  background-repeat:no-repeat!important}}
}}
@media(max-width:480px){{
#{HERO_IMG_EID}{{
  top:clamp(188px,48vw,260px)!important;
  width:clamp(280px,90vw,400px)!important;height:clamp(340px,92vw,460px)!important}}
}}
"""


def apply_hero_berry_image(html: str) -> str:
    """Hero: arte Berry Up (mulher + método) em assets/hero-berry-up.png."""
    html = html.replace(HERO_IMG_OLD, HERO_IMG_NEW)
    html = re.sub(
        rf"(#{re.escape(HERO_IMG_EID)} \.c \.imagem_fundo\{{[^}}]*?)background-image:url\(\"[^\"]+\"\)",
        rf'\1background-image:url("{HERO_IMG_NEW}")',
        html,
    )
    html = re.sub(
        rf"(#{re.escape(HERO_IMG_EID)} \.c \.imagem_fundo\{{[^}}]*?)background-size:[^;]+;?",
        r"\1background-size:contain!important;",
        html,
    )
    html = re.sub(
        rf"(#{re.escape(HERO_IMG_EID)} \.c \.imagem_fundo\{{[^}}]*?)background-position:[^;]+;?",
        r"\1background-position:right bottom!important;",
        html,
    )
    html = re.sub(
        rf'll_src="{re.escape(HERO_IMG_OLD)}"',
        f'll_src="{HERO_IMG_NEW}"',
        html,
    )
    html = re.sub(
        rf'll_src_mobile="{re.escape(HERO_IMG_OLD)}"',
        f'll_src_mobile="{HERO_IMG_NEW}"',
        html,
    )
    hero_marker = f'id="{HERO_IMG_EID}"'
    if hero_marker in html:
        pos = html.find(hero_marker)
        chunk = html[pos : pos + 500]
        if HERO_IMG_NEW not in chunk:
            html = html.replace(
                f'{hero_marker} ',
                f'{hero_marker} ll_src="{HERO_IMG_NEW}" ll_src_mobile="{HERO_IMG_NEW}" ',
                1,
            )
    if "berryup-hero-image" not in html:
        html = html.replace(
            "</head>",
            f'<style id="berryup-hero-image">{HERO_IMG_CSS}</style></head>',
            1,
        )
    return html


URGENCY_BAR_SCRIPT = f"""<script id="berryup-urgency-bar">(function(){{
var BID="{URGENCY_BLOCK_ID}";
var DELAY={URGENCY_SHOW_DELAY_SEC};
function bar(){{return document.getElementById(BID);}}
function syncScroll(){{
  var b=bar(),site=document.getElementById("site");
  if(!b||!document.body.classList.contains("berryup-urgency-ready")){{
    document.body.classList.remove("berryup-urgency-scrolled");
    if(site)site.style.paddingTop="";
    document.documentElement.style.removeProperty("--berryup-urgency-h");
    return;
  }}
  b.classList.remove("esconder_desktop","esconder_mobile");
  var h=b.offsetHeight;
  document.documentElement.style.setProperty("--berryup-urgency-h",h+"px");
  if(site&&!document.body.classList.contains("berryup-wheel-won"))
    site.style.paddingTop=h+"px";
  var y=window.scrollY||window.pageYOffset||0;
  document.body.classList.toggle("berryup-urgency-scrolled",y>0);
}}
function revealBar(){{
  var b=bar();
  if(!b)return;
  b.classList.remove("esconder_desktop","esconder_mobile");
  document.body.classList.add("berryup-urgency-ready");
  syncScroll();
}}
function init(){{
  var t=0;
  var iv=setInterval(function(){{
    t++;
    if(t>=DELAY){{clearInterval(iv);revealBar();}}
  }},1000);
  window.addEventListener("scroll",syncScroll,{{passive:true}});
  window.addEventListener("resize",syncScroll);
  syncScroll();
}}
if(document.readyState==="loading")document.addEventListener("DOMContentLoaded",init);
else init();
}})();</script>"""


def inject_urgency_bar_script(html: str) -> str:
    """Garante barra de urgência (desconto + timer) visível ao rolar."""
    if 'id="berryup-urgency-bar"' in html:
        return html
    if f'id="{URGENCY_BLOCK_ID}"' not in html:
        return html
    return html.replace("</body>", URGENCY_BAR_SCRIPT + "</body>", 1)


def inject_utmify_script(html: str) -> str:
    """Instala o script de tracking UTMify uma vez, preferencialmente no head."""
    if UTMIFY_SCRIPT_SRC in html:
        return html
    script = f'<script src="{UTMIFY_SCRIPT_SRC}"></script>'
    if "</head>" in html:
        return html.replace("</head>", script + "</head>", 1)
    return html.replace("</body>", script + "</body>", 1)


def inject_meta_pixel(html: str) -> str:
    """Instala o Meta Pixel do anunciante uma vez."""
    if META_PIXEL_ID in html:
        return html
    pixel = f"""<!-- Meta Pixel Code -->
<script>
!function(f,b,e,v,n,t,s)
{{if(f.fbq)return;n=f.fbq=function(){{n.callMethod?
n.callMethod.apply(n,arguments):n.queue.push(arguments)}};
if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version='2.0';
n.queue=[];t=b.createElement(e);t.async=!0;
t.src=v;s=b.getElementsByTagName(e)[0];
s.parentNode.insertBefore(t,s)}}(window, document,'script',
'https://connect.facebook.net/en_US/fbevents.js');
fbq('init', '{META_PIXEL_ID}');
fbq('track', 'PageView');
</script>
<noscript><img height="1" width="1" style="display:none"
src="https://www.facebook.com/tr?id={META_PIXEL_ID}&ev=PageView&noscript=1"
/></noscript>
<!-- End Meta Pixel Code -->"""
    if "</head>" in html:
        return html.replace("</head>", pixel + "</head>", 1)
    return html.replace("</body>", pixel + "</body>", 1)


POLICY_PHONE_CLEANUP_SCRIPT = r"""<script id="berryup-policy-phone-cleanup">(function(){
var PHONE_RE=/(\+?55\s*)?(\(?\d{2}\)?\s*)?\d{4,5}[-.\s]?\d{4}|0800[-.\s]?\d{3}[-.\s]?\d{4}/g;
var LABEL_RE=/\b(?:telefone|fone|whatsapp|whats|celular)\s*:?\s*/gi;
function cleanText(value){
  return value.replace(PHONE_RE,"").replace(LABEL_RE,"").replace(/[ \t]{2,}/g," ").replace(/\s+([,.;:])/g,"$1").trim();
}
function cleanNode(root){
  if(!root) return;
  root.querySelectorAll('a[href^="tel:"],a[href*="wa.me"],a[href*="api.whatsapp"],a[href*="whatsapp"]').forEach(function(a){
    var text=(a.textContent||"").trim();
    if(PHONE_RE.test(text) || /tel:|wa\.me|api\.whatsapp|whatsapp/i.test(a.getAttribute("href")||"")) a.remove();
    PHONE_RE.lastIndex=0;
  });
  var walker=document.createTreeWalker(root,NodeFilter.SHOW_TEXT);
  var nodes=[];
  while(walker.nextNode()) nodes.push(walker.currentNode);
  nodes.forEach(function(node){
    if(!PHONE_RE.test(node.nodeValue||"")){ PHONE_RE.lastIndex=0; return; }
    PHONE_RE.lastIndex=0;
    node.nodeValue=cleanText(node.nodeValue||"");
  });
  root.querySelectorAll("p,li,div,span,h4").forEach(function(el){
    if(!(el.textContent||"").trim() && !el.querySelector("img,iframe,video,button,a")) el.remove();
  });
}
function run(){
  document.querySelectorAll('.gpc_modal[gpc_id_elemento="e_1002625_1_52312"], [gpc_id_elemento="e_1002625_1_52312"]').forEach(cleanNode);
}
document.addEventListener("DOMContentLoaded",run);
document.addEventListener("click",function(){ setTimeout(run,80); setTimeout(run,350); },true);
new MutationObserver(run).observe(document.documentElement,{childList:true,subtree:true});
})();</script>"""


def inject_policy_phone_cleanup(html: str) -> str:
    """Remove telefone/WhatsApp do popup de politica de troca quando o modal for aberto."""
    if 'id="berryup-policy-phone-cleanup"' in html:
        return html
    return html.replace("</body>", POLICY_PHONE_CLEANUP_SCRIPT + "</body>", 1)


def _div_close_index(html: str, element_id: str) -> int:
    """Índice logo após o </div> de fechamento do elemento."""
    start = html.find(f'<div id="{element_id}"')
    if start < 0:
        return -1
    depth = 0
    i = start
    while i < len(html):
        if html.startswith("<div", i):
            depth += 1
            i += 4
            continue
        if html.startswith("</div>", i):
            depth -= 1
            i += 6
            if depth == 0:
                return i
            continue
        i += 1
    return -1


def hide_clinical_image_on_mobile(html: str) -> str:
    """Foto lateral da seção clínica: só desktop (no mobile cobria texto e barras)."""
    eid = CLINICAL_IMG_EID
    if f'id="{eid}"' not in html:
        return html
    html = re.sub(
        rf'(<div id="{re.escape(eid)}"[^>]*class="[^"]*)\bdd dm\b',
        r"\1esconder_mobile dd",
        html,
        count=1,
    )
    return html


def inject_clinical_video(html: str) -> str:
    """Vídeo na seção testes clínicos (desktop à esquerda; mobile após o título)."""
    marker = f'<div id="{CLINICAL_BLOCK_ID}"'
    pos = html.find(marker)
    if pos < 0:
        return html
    html = remove_element(html, "berryup-clinical-video")
    cen = html.find('<div class="centralizar">', pos)
    if cen < 0:
        return html
    insert_at = _div_close_index(html, CLINICAL_TITLE_EID)
    if insert_at < 0 or insert_at <= cen:
        insert_at = cen + len('<div class="centralizar">')
    return html[:insert_at] + clinical_video_html() + html[insert_at:]


def inject_mobile_css(html: str) -> str:
    marker = "/* BerryUp — correções mobile"
    if marker in html:
        start = html.find(marker)
        end = html.find("</style>", start)
        if end > start:
            return html[:start] + BERRYUP_MOBILE_CSS.strip() + "\n" + html[end:]
    return html.replace("</style>", BERRYUP_MOBILE_CSS + "</style>", 1)


def solid_orange_page_background(html: str) -> str:
    """Remove imagens de fundo dos blocos principais e mantém laranja sólido."""
    for block_id in PAGE_BG_BLOCKS:
        html = re.sub(
            rf"(#{re.escape(block_id)}\{{[^}}]*?)background-image:[^;]+;?",
            r"\1background-image:none;",
            html,
        )
        html = re.sub(
            rf"(#{re.escape(block_id)}\{{[^}}]*?)background-color:[^;]+;?",
            rf"\1background-color:{BERRYUP_ORANGE};",
            html,
        )
    return html


def compact_depoimentos_block(html: str, source_html: str | None = None) -> str:
    """Sobe depoimentos após remoções no topo; usa tops do peachup-source."""
    html = _strip_depoimentos_mobile_override_block(html)
    eid_set = set(_depoimentos_element_ids(html))
    if not eid_set:
        return html

    if source_html is None:
        source_path = Path("peachup-source.html")
        source_html = (
            source_path.read_text(encoding="utf-8") if source_path.exists() else html
        )

    src_tops: dict[str, list[float]] = {}
    for eid in eid_set:
        tops = []
        for rule in re.findall(rf"#{re.escape(eid)}\{{[^}}]+\}}", source_html):
            top_m = re.search(r"top:([0-9.]+)px", rule)
            if top_m:
                tops.append(float(top_m.group(1)))
        if tops:
            src_tops[eid] = tops

    counters: dict[str, int] = {}
    mob_marker = html.find('id="css_mobile"')

    def replace_rule(match: re.Match) -> str:
        eid = match.group(1)
        if eid not in eid_set:
            return match.group(0)
        # Mobile: mantém tops do GreatPages (evita cards sobrepostos)
        if mob_marker >= 0 and match.start() >= mob_marker:
            return match.group(0)
        body = match.group(2)
        top_m = re.search(r"top:([0-9.]+)px", body)
        if not top_m:
            return match.group(0)
        idx = counters.get(eid, 0)
        counters[eid] = idx + 1
        tops_list = src_tops.get(eid)
        if tops_list and idx < len(tops_list):
            top_val = tops_list[idx]
        else:
            top_val = float(top_m.group(1))
        shift = _shift_for_depoimento(top_val, idx)
        new_top = max(0, round(top_val - shift, 4))
        top_str = (
            str(int(new_top))
            if new_top == int(new_top)
            else f"{new_top:.4f}".rstrip("0").rstrip(".")
        )
        new_body = body[: top_m.start()] + f"top:{top_str}px" + body[top_m.end() :]
        return f"#{eid}{{{new_body}}}"

    html = re.sub(
        r"#(e_1002625_1_17307234956728bea7[a-f0-9]+)\{([^}]+)\}",
        replace_rule,
        html,
    )

    if DEPOIMENTOS_HIDE_ON_MOBILE:
        mob_h = 0
    else:
        html, mob_h = relayout_depoimentos_mobile_css(html)
    desk_h, mob_h = _depoimentos_block_heights(
        html, mob_h_override=mob_h if mob_h else None
    )
    if DEPOIMENTOS_HIDE_ON_MOBILE:
        mob_h = 0
    block_hits = [0]

    def replace_block_height(match: re.Match) -> str:
        block_hits[0] += 1
        new_h = mob_h if block_hits[0] >= 2 else desk_h
        return f"{match.group(1)}height:{new_h}px"

    html = re.sub(
        rf"(#{re.escape(DEPOIMENTOS_BLOCK_ID)}\{{[^}}]*?)height:([0-9.]+)px",
        replace_block_height,
        html,
    )
    html = _apply_depoimentos_height_overrides(html, desk_h, mob_h)
    return html


def _apply_depoimentos_height_overrides(
    html: str, desk_h: int, mob_h: int
) -> str:
    """Garante altura do bloco de depoimentos no CSS BerryUp (sem 1720px fixo)."""
    bid = DEPOIMENTOS_BLOCK_ID
    desk_rule = (
        f"#{bid}{{height:{desk_h}px!important;overflow:visible!important}}\n"
    )
    if DEPOIMENTOS_HIDE_ON_MOBILE:
        mob_rule = (
            f"@media(max-width:800px){{#{bid},#{bid} .centralizar{{"
            f"display:none!important;visibility:hidden!important;height:0!important;"
            f"min-height:0!important;max-height:0!important;overflow:hidden!important;"
            f"margin:0!important;padding:0!important;pointer-events:none!important}}"
            f"}}\n"
        )
    else:
        mob_rule = (
            f"@media(max-width:800px){{#{bid}{{height:auto!important;"
            f"min-height:{mob_h}px!important;overflow:visible!important}}}}\n"
        )
    block = desk_rule + mob_rule

    html = re.sub(
        rf"#{re.escape(bid)}\{{[^}}]*height:[^}}]+\}}\s*",
        "",
        html,
    )
    html = re.sub(
        rf"@media\(max-width:800px\)\{{#{re.escape(bid)}\{{[^}}]+\}}\}}\s*",
        "",
        html,
    )
    marker = f"#{DEPOIMENTOS_BLOCK_ID}{{overflow:visible"
    if marker in html:
        return html.replace(marker, block + marker, 1)
    return html.replace("</style>", block + "</style>", 1)


def remove_element(html: str, element_id: str) -> str:
    start = html.find(f'<div id="{element_id}"')
    if start < 0:
        return html
    next_e = html.find('<div id="e_', start + 10)
    next_b = html.find('<div id="b_', start + 10)
    candidates = [x for x in (next_e, next_b) if x > start]
    end = min(candidates) if candidates else len(html)
    return html[:start] + html[end:]


def remove_block(html: str, block_id: str) -> str:
    start = html.find(f'<div id="{block_id}"')
    if start < 0:
        return html
    next_block = re.search(
        r'<div id="b_1002625_1_[^"]+" class="gpc-b',
        html[start + 50 :],
    )
    if next_block:
        end = start + 50 + next_block.start()
        return html[:start] + html[end:]
    depth = 0
    pos = start
    while pos < len(html):
        open_m = html.find("<div", pos)
        close_m = html.find("</div>", pos)
        if close_m < 0:
            break
        if open_m >= 0 and open_m < close_m:
            depth += 1
            pos = open_m + 4
        else:
            depth -= 1
            pos = close_m + 6
            if depth == 0:
                return html[:start] + html[pos:]
    return html


def inject_conversion_landing(html: str) -> str:
    if 'id="berryup-conversion"' not in html:
        body_match = re.search(r"<body([^>]*)>", html, re.IGNORECASE)
        if body_match:
            body_tag = body_match.group(0)
            body_attrs = body_match.group(1)
            if "berryup-conversion-page" not in body_attrs:
                if re.search(r'\bclass="', body_tag):
                    new_body_tag = re.sub(
                        r'class="([^"]*)"',
                        r'class="\1 berryup-conversion-page"',
                        body_tag,
                        count=1,
                    )
                else:
                    new_body_tag = body_tag[:-1] + ' class="berryup-conversion-page">'
                html = html.replace(body_tag, new_body_tag + CONVERSION_HTML, 1)
            else:
                html = html.replace(body_tag, body_tag + CONVERSION_HTML, 1)
    elif "berryup-conversion-page" not in html[: html.find('id="berryup-conversion"')]:
        html = re.sub(
            r"<body([^>]*)>",
            lambda m: (
                m.group(0)[:-1] + ' class="berryup-conversion-page">'
                if 'class="' not in m.group(0)
                else re.sub(r'class="([^"]*)"', r'class="\1 berryup-conversion-page"', m.group(0), count=1)
            ),
            html,
            count=1,
            flags=re.IGNORECASE,
        )

    if "#berryup-conversion" not in html:
        html = html.replace("</style>", CONVERSION_CSS + "</style>", 1)
    return html


# Unificar links de checkout antigos
OLD_CHECKOUTS = [
    "https://seguro.peachupbrazil.com.br/r/M7GJ1KI6OA?promocode=OFERTA2",
    "https://seguro.peachupbrazil.com.br/r/R6AKXPWRYE?promocode=OFERTA3",
    "https://seguro.peachupbrazil.com.br/r/2ZLR934Z3U?promocode=OFERTA",
    "https://seguro.peachupbrazil.com.br/r/2ZLR934Z3U",
]


def scrub_forbidden_brand_text(html: str) -> str:
    """Remove nomes antigos de textos/metadados herdados sem mexer em URLs tecnicas."""
    replacements = (
        ("BoomBoom Up", "Bum Bum Up"),
        ("BOOMBOOM UP", "BUM BUM UP"),
        ("Boom Boom Up", "Bum Bum Up"),
        ("BOOM BOOM UP", "BUM BUM UP"),
        ("Peach Up", "Berry Up"),
        ("PEACH UP", "BERRY UP"),
    )
    for old, new in replacements:
        html = html.replace(old, new)
    return html


LOCAL_ANALYTICS_SCRIPT = """
<script id="berryup-local-analytics">
(function(){
  if(window.__berryupLocalAnalytics)return;
  window.__berryupLocalAnalytics=true;
  var endpoint="/track";
  var start=Date.now();
  var lastActive=Date.now();
  var maxScroll=0;
  var sentScroll={};
  var visitorKey="berryup_visitor_id";
  var sessionKey="berryup_session_id";
  var visitorId=localStorage.getItem(visitorKey);
  if(!visitorId){visitorId="v_"+Date.now().toString(36)+"_"+Math.random().toString(36).slice(2,10);localStorage.setItem(visitorKey,visitorId);}
  var sessionId=sessionStorage.getItem(sessionKey);
  if(!sessionId){sessionId="s_"+Date.now().toString(36)+"_"+Math.random().toString(36).slice(2,10);sessionStorage.setItem(sessionKey,sessionId);}
  function activeSeconds(){return Math.max(0,Math.round((lastActive-start)/1000));}
  function currentScroll(){
    var doc=document.documentElement,body=document.body;
    var top=window.pageYOffset||doc.scrollTop||body.scrollTop||0;
    var h=Math.max(body.scrollHeight,doc.scrollHeight)-window.innerHeight;
    return h>0?Math.min(100,Math.round((top/h)*100)):0;
  }
  function sectionName(el){
    var section=el&&el.closest?el.closest("section,footer,.bc-proofbar,.bc-sticky,#berryup-conversion"):null;
    if(!section)return "";
    if(section.id)return section.id;
    var h=section.querySelector("h1,h2,.bc-tag,.bc-brand");
    return h?String(h.textContent||"").replace(/\\s+/g," ").trim().slice(0,90):String(section.className||"").slice(0,90);
  }
  function payload(type,data){
    data=data||{};
    return Object.assign({
      type:type,
      visitor_id:visitorId,
      session_id:sessionId,
      page_title:document.title,
      path:location.pathname+location.search,
      referrer:document.referrer,
      url:location.href,
      viewport:window.innerWidth+"x"+window.innerHeight,
      scroll_percent:maxScroll,
      active_seconds:activeSeconds(),
      timestamp:new Date().toISOString()
    },data);
  }
  function send(type,data,beacon){
    var body=JSON.stringify(payload(type,data));
    if(beacon&&navigator.sendBeacon){
      try{navigator.sendBeacon(endpoint,new Blob([body],{type:"application/json"}));return;}catch(e){}
    }
    fetch(endpoint,{method:"POST",headers:{"Content-Type":"application/json"},body:body,keepalive:!!beacon}).catch(function(){});
  }
  ["mousemove","keydown","scroll","click","touchstart"].forEach(function(ev){
    window.addEventListener(ev,function(){lastActive=Date.now();},{passive:true});
  });
  send("page_view",{utm:Object.fromEntries(new URLSearchParams(location.search))});
  window.addEventListener("scroll",function(){
    maxScroll=Math.max(maxScroll,currentScroll());
    [25,50,75,90,100].forEach(function(mark){
      if(maxScroll>=mark&&!sentScroll[mark]){
        sentScroll[mark]=true;
        send("scroll_depth",{mark:mark});
      }
    });
  },{passive:true});
  document.addEventListener("click",function(e){
    var target=e.target.closest&&e.target.closest("a,button,summary,details");
    if(!target)return;
    var href=target.href||"";
    var text=String(target.textContent||target.getAttribute("aria-label")||"").replace(/\\s+/g," ").trim().slice(0,140);
    var type="click";
    if(target.matches(".bc-cta,.beo-cta,.link_interno,.link_externo")||/checkout|comprar|garantir|finalizar|acesso/i.test(text))type="cta_click";
    if(/pay\\.cakto|seguro\\./i.test(href))type="checkout_click";
    if(target.tagName&&target.tagName.toLowerCase()==="summary")type="faq_open";
    send(type,{text:text,href:href,section:sectionName(target)});
  },true);
  if("IntersectionObserver" in window){
    var seen={};
    var observer=new IntersectionObserver(function(entries){
      entries.forEach(function(entry){
        if(entry.isIntersecting&&entry.intersectionRatio>=0.45){
          var name=sectionName(entry.target);
          if(name&&!seen[name]){
            seen[name]=true;
            send("section_view",{section:name});
          }
        }
      });
    },{threshold:[0.45]});
    document.querySelectorAll("section,footer,.bc-proofbar").forEach(function(el){observer.observe(el);});
  }
  setInterval(function(){send("heartbeat");},15000);
  document.addEventListener("visibilitychange",function(){
    if(document.visibilityState==="hidden")send("page_hidden",{},true);
  });
  window.addEventListener("pagehide",function(){send("page_exit",{},true);});
})();
</script>
"""


def inject_local_analytics(html: str) -> str:
    if 'id="berryup-local-analytics"' in html:
        return html
    marker = "</body>"
    if marker in html:
        return html.replace(marker, LOCAL_ANALYTICS_SCRIPT + marker, 1)
    return html + LOCAL_ANALYTICS_SCRIPT


def transform(html: str) -> str:
    html = html.replace(POT_IMG_OLD, POT_IMG_NEW)
    html = html.replace(CLINICAL_IMG_OLD, CLINICAL_IMG_NEW)
    html = hide_clinical_image_on_mobile(html)
    html = html.replace(LOGO_HTML_OLD, LOGO_HTML_NEW)
    html = html.replace(FOOTER_LOGO_HTML_OLD, FOOTER_LOGO_HTML_NEW)
    html = FOOTER_ADDRESS_RE.sub("", html, count=1)
    html = html.replace(CAIXA_REMOVE, "")
    html = html.replace(IMG_REMOVE, "")
    html = html.replace(VIDEO_REMOVE, "")
    html = html.replace(TITULO_DEPOIMENTO_REMOVE, "")

    for block_id in BLOCKS_REMOVE:
        html = remove_block(html, block_id)

    for element_id in ELEMENTS_REMOVE:
        html = remove_element(html, element_id)

    for old, new in REPLACEMENTS:
        html = html.replace(old, new)

    html = html.replace("CNPJ: 48.244.208/0001-82", "CNPJ: 98.581.467/0001-77")

    for url in OLD_CHECKOUTS:
        html = html.replace(url, CHECKOUT)

    inject_marker = '<div id="b_1002625_1_174828442056623927"'
    if inject_marker in html and "berryup-ebook-preview" not in html:
        html = html.replace(
            inject_marker,
            EBOOK_HTML + inject_marker,
            1,
        )

    style_close = "</style>"
    if "berryup-ebook-preview" in html and "#berryup-ebook-preview" not in html:
        html = html.replace(
            style_close,
            EBOOK_CSS
            + guarantee_footer_css()
            + CLINICAL_MOBILE_CSS
            + DEPOIMENTOS_CTA_ROW_CSS
            + DEPOIMENTOS_MOBILE_CSS
            + style_close,
            1,
        )

    html = inject_mobile_css(html)
    html = solid_orange_page_background(html)
    html = inject_clinical_video(html)
    html = inject_berryup_wheel(html, CHECKOUT)
    html = inject_urgency_bar_script(html)
    html = inject_utmify_script(html)
    html = inject_meta_pixel(html)
    html = inject_policy_phone_cleanup(html)
    html = inject_cookie_consent_script(html)
    html = inject_social_proof(html)
    html = compact_depoimentos_block(html)
    html = apply_hero_berry_image(html)
    html = hide_hero_pot_image(html)
    html = patch_ceo_images(html)
    html = patch_ja_tentei_section(html)
    html = inject_ja_tentei_video(html)
    html = inject_mobile_layout_script(html)
    html = inject_depoimentos_hide_mobile_final(html)
    html = inject_conversion_landing(html)
    html = scrub_forbidden_brand_text(html)
    html = inject_local_analytics(html)

    return html


def hide_hero_pot_image(html: str) -> str:
    """Remove pote do hero; mulher (hero-berry-up.png) fica na frente."""
    pot_rule = f"#{HERO_POT_EID}{{display:none!important"
    if pot_rule not in html:
        pot_css = (
            f"#{HERO_POT_EID}{{display:none!important;visibility:hidden!important;"
            f"pointer-events:none!important}}\n"
            f"#{HERO_WOMAN_EID}{{z-index:1450!important}}\n"
        )
        html = html.replace("</style>", pot_css + "</style>", 1)
    html = remove_element(html, HERO_POT_EID)
    return html


def main():
    path = Path("index.html")
    html = path.read_text(encoding="utf-8")
    html = transform(html)
    path.write_text(html, encoding="utf-8")
    print(f"Transformado: {path.stat().st_size:,} bytes")


if __name__ == "__main__":
    main()
