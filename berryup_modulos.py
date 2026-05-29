"""Seção «O que você vai aprender» — módulos do e-book Berry Up."""

MODULOS_ID = "berryup-ebook-modulos"

MODULOS_CSS = """
#berryup-ebook-modulos{font-family:system-ui,-apple-system,"Segoe UI",Roboto,sans-serif;box-sizing:border-box;background:linear-gradient(180deg,#fff 0%,#fff8f3 55%,#fff5ee 100%);padding:52px 20px 56px}
#berryup-ebook-modulos *{box-sizing:border-box}
#berryup-ebook-modulos .bm-wrap{max-width:1100px;margin:0 auto}
#berryup-ebook-modulos .bm-head{text-align:center;margin-bottom:36px}
#berryup-ebook-modulos .bm-tag{margin:0 0 10px;font-size:.72rem;font-weight:800;letter-spacing:.14em;text-transform:uppercase;color:#ff6316}
#berryup-ebook-modulos .bm-head h2{margin:0;font-size:clamp(1.45rem,4vw,2rem);font-weight:800;color:#1a1a2e;line-height:1.25}
#berryup-ebook-modulos .bm-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:18px}
@media(max-width:1024px){#berryup-ebook-modulos .bm-grid{grid-template-columns:repeat(2,1fr)}}
@media(max-width:520px){#berryup-ebook-modulos .bm-grid{grid-template-columns:1fr}}
.bm-card{background:#fff;border-radius:14px;padding:22px 18px 20px;box-shadow:0 8px 28px rgba(255,99,22,.08);border:1px solid #ffe8d9;min-height:168px;display:flex;flex-direction:column;gap:10px;transition:transform .2s,box-shadow .2s}
.bm-card:hover{transform:translateY(-3px);box-shadow:0 12px 32px rgba(255,99,22,.14)}
.bm-icon{width:40px;height:40px;border-radius:10px;background:linear-gradient(135deg,#fff5ee,#ffe0cc);display:flex;align-items:center;justify-content:center;flex-shrink:0}
.bm-icon svg{width:22px;height:22px;stroke:#ff6316;fill:none;stroke-width:1.8;stroke-linecap:round;stroke-linejoin:round}
.bm-num{margin:0;font-size:.68rem;font-weight:800;letter-spacing:.1em;text-transform:uppercase;color:#ff8a4c}
.bm-card h3{margin:0;font-size:1rem;font-weight:800;color:#1a1a2e;line-height:1.3}
.bm-card p{margin:0;font-size:.86rem;color:#5c5c6e;line-height:1.45;flex:1}
"""

MODULOS_HTML = """
<section id="berryup-ebook-modulos" aria-labelledby="berryup-modulos-title">
<div class="bm-wrap">
<header class="bm-head">
<p class="bm-tag">O que você vai aprender</p>
<h2 id="berryup-modulos-title">Um guia prático, módulo por módulo</h2>
</header>
<div class="bm-grid">
<article class="bm-card">
<div class="bm-icon" aria-hidden="true"><svg viewBox="0 0 24 24"><path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/></svg></div>
<p class="bm-num">Módulo 1</p>
<h3>O que é celulite</h3>
<p>Por que aparece, mitos comuns e como o método Berry Up atua na aparência da pele.</p>
</article>
<article class="bm-card">
<div class="bm-icon" aria-hidden="true"><svg viewBox="0 0 24 24"><path d="M9 3h6l1 7H8l1-7z"/><path d="M10 14v4"/><path d="M14 14v4"/><path d="M8 21h8"/><path d="M12 10v4"/></svg></div>
<p class="bm-num">Módulo 2</p>
<h3>Ingredientes e ciência</h3>
<p>Ativos firmadores, circulação e o que a ciência diz sobre reduzir a “casca de laranja”.</p>
</article>
<article class="bm-card">
<div class="bm-icon" aria-hidden="true"><svg viewBox="0 0 24 24"><path d="M12 2v4"/><path d="M8 6h8"/><rect x="5" y="8" width="14" height="12" rx="2"/><path d="M9 14h6"/></svg></div>
<p class="bm-num">Módulo 3</p>
<h3>Preparação da pele</h3>
<p>Esfoliação, hidratação e rotina diária antes de aplicar o protocolo em casa.</p>
</article>
<article class="bm-card">
<div class="bm-icon" aria-hidden="true"><svg viewBox="0 0 24 24"><path d="M12 3l1.5 4.5L18 9l-4.5 1.5L12 15l-1.5-4.5L6 9l4.5-1.5z"/><path d="M5 19l1 2"/><path d="M19 19l-1 2"/></svg></div>
<p class="bm-num">Módulo 4</p>
<h3>Massagens anti-celulite</h3>
<p>Técnicas de pinçamento e movimentos que estimulam firmeza e melhoram a textura.</p>
</article>
<article class="bm-card">
<div class="bm-icon" aria-hidden="true"><svg viewBox="0 0 24 24"><path d="M12 21s-6-4.35-6-9a6 6 0 0 1 12 0c0 4.65-6 9-6 9z"/></svg></div>
<p class="bm-num">Módulo 5</p>
<h3>Coxas, glúteos e barriga</h3>
<p>Protocolos por região: onde aplicar, quanto tempo e frequência ideal.</p>
</article>
<article class="bm-card">
<div class="bm-icon" aria-hidden="true"><svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="4"/><path d="M12 3v2"/><path d="M12 19v2"/></svg></div>
<p class="bm-num">Módulo 6</p>
<h3>Desafio de 7 dias</h3>
<p>Calendário dia a dia para ver os primeiros resultados e criar o hábito.</p>
</article>
<article class="bm-card">
<div class="bm-icon" aria-hidden="true"><svg viewBox="0 0 24 24"><circle cx="12" cy="8" r="4"/><path d="M6 20v-1a6 6 0 0 1 12 0v1"/></svg></div>
<p class="bm-num">Módulo 7</p>
<h3>Para quem é indicado</h3>
<p>Perfil ideal, contraindicações e quando buscar orientação médica.</p>
</article>
<article class="bm-card">
<div class="bm-icon" aria-hidden="true"><svg viewBox="0 0 24 24"><path d="M12 3l7 4v6c0 4-3 7-7 8-4-1-7-4-7-8V7l7-4z"/><path d="M9 12l2 2 4-4"/></svg></div>
<p class="bm-num">Módulo 8</p>
<h3>Segurança e manutenção</h3>
<p>Cuidados pós-rotina, erros a evitar e plano de 90 dias para manter os resultados.</p>
</article>
</div>
</div>
</section>
"""


def inject_berryup_modulos(html: str) -> str:
    if MODULOS_ID in html:
        return html
    marker = '<div id="berryup-ebook-oferta">'
    if marker not in html:
        return html
    html = html.replace(marker, MODULOS_HTML + marker, 1)
    if f"#{MODULOS_ID}" not in html:
        html = html.replace("</style>", MODULOS_CSS + "</style>", 1)
    return html
