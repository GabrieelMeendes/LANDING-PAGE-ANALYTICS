import re
from pathlib import Path

t = Path("index.html").read_text(encoding="utf-8", errors="ignore")
for pat in [r".{0,40}entendi.{0,40}", r"berryup-win[\w-]*", r"win-modal[\w-]*"]:
    m = re.search(pat, t, re.I)
    print(pat, "->", m.group() if m else "NOT FOUND")
i = t.find('textContent="OK"')
print("textContent OK at", i)
if i > 0:
    print(t[i - 80 : i + 80])
