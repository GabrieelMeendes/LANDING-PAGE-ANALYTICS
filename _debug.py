import pathlib
p = pathlib.Path(r"C:\Users\CLIENTE\Desktop\LANDING-PAGE-BERRYUP\berryup_wheel.py")
c = p.read_text(encoding="utf-8")

# Find transition string
idx = c.find("transition:transform")
print("Transition context:")
print(repr(c[idx:idx+90]))

# Find end of WHEEL_CSS constant - look for br-save line and what follows
idx2 = c.find("br-save{margin")
print("\nbr-save and next 300 chars:")
print(repr(c[idx2:idx2+300]))

# Find closing of WHEEL_CSS
idx3 = c.find("WHEEL_CSS = ")
# Find first triple-quote after position 5000 (skip the opening one)
pos = idx3 + 50
while True:
    tpos = c.find('"""', pos)
    if tpos < 0:
        break
    # Check if this looks like it ends a CSS block
    chunk = c[max(0,tpos-50):tpos]
    if "}" in chunk or "\n" in chunk:
        print(f"\nTriple-quote at {tpos}, preceding 50 chars:")
        print(repr(chunk))
        break
    pos = tpos + 3
