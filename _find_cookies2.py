from pathlib import Path
import re

h = Path("index.html").read_text(encoding="utf-8")

# bloco urgência / topo
bid = "b_1002625_1_17307234956728bea7c7c12"
i = h.find(f'id="{bid}"')
if i >= 0:
    chunk = h[i : i + 8000]
    print("=== bloco urgência (8k) ===")
    print(chunk[:4000])
    print("...")

# procurar OK em botões (unicode etc)
for m in re.finditer(r"<a[^>]{0,200}>([^<]{1,20})</a>", h):
    t = m.group(1).strip()
    if re.match(r"^ok\.?!?$", t, re.I) or t.lower() in ("ok", "ok!", "aceitar", "entendi"):
        ctx = h[max(0, m.start() - 200) : m.end() + 100]
        print("\nBTN:", repr(t))
        print(ctx.replace("\n", " ")[:400])

# iframe / div aviso
for pat in ("aviso", "lgpd", "consent", "cookie"):
    for m in re.finditer(rf'id="[^"]*{pat}[^"]*"', h, re.I):
        print("id:", m.group())
