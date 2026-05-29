import pathlib
p = pathlib.Path(r"C:\Users\CLIENTE\Desktop\LANDING-PAGE-BERRYUP\berryup_wheel.py")
c = p.read_text(encoding="utf-8")

# Find ALL triple-quotes after WHEEL_CSS start
start = c.find('WHEEL_CSS = ')
pos = start + 20
found = []
while True:
    tpos = c.find('"""', pos)
    if tpos < 0:
        break
    found.append(tpos)
    pos = tpos + 3

print(f"Found {len(found)} triple-quotes after pos {start}")
for i, tp in enumerate(found[:10]):
    after = c[tp+3:tp+30].strip()
    before = c[max(0,tp-40):tp].replace(chr(10)," ")
    print(f"  [{i}] pos={tp} | before: ...{before[-30:]} | after: {after[:40]}")
