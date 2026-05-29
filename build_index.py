"""Gera index.html fiel à Peach Up a partir do HTML baixado."""
from pathlib import Path

import transform_ebook

src = Path("peachup-source.html").read_text(encoding="utf-8", errors="ignore")
out = Path("index.html")

html = src

marker = "<body"
if marker in html:
    html = html.replace(
        marker,
        "<!-- LANDING-PAGE-BERRYUP -->\n<body",
        1,
    )

html = transform_ebook.transform(html)
out.write_text(html, encoding="utf-8")
print(f"index.html criado: {out.stat().st_size:,} bytes")
