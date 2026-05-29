import pathlib
p = pathlib.Path(r"C:\Users\CLIENTE\Desktop\LANDING-PAGE-BERRYUP\berryup_wheel.py")
c = p.read_text(encoding="utf-8")

# Debug edit 2 verification
idx2 = c.find("transition:")
if idx2 >= 0:
    print("Transition context:")
    print(repr(c[idx2:idx2+80]))

# Debug edit 4 - exact onSpin body
idx = c.find("function onSpin()")
if idx >= 0:
    print("\nonSpin full function (600 chars):")
    print(repr(c[idx:idx+600]))
