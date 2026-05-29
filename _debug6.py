import pathlib
p = pathlib.Path(r"C:\Users\CLIENTE\Desktop\LANDING-PAGE-BERRYUP\berryup_wheel.py")
c = p.read_text(encoding="utf-8")
lines = c.split("\n")
# Show around line 982
for i in range(max(0,975), min(len(lines),990)):
    print("%d: %s" % (i+1, repr(lines[i])))
