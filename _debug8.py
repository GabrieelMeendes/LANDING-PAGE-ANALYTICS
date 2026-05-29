import pathlib
p = pathlib.Path(r"C:\Users\CLIENTE\Desktop\LANDING-PAGE-BERRYUP\berryup_wheel.py")
c = p.read_text(encoding="utf-8")

# Find createConfetti and show surrounding area
idx = c.find("function createConfetti()")
if idx >= 0:
    # Show 200 chars before
    print("Before createConfetti:")
    print(repr(c[idx-50:idx]))
    print()
    # Show the function
    end = c.find("function onSpin()", idx)
    print("createConfetti function (%d chars):" % (end - idx))
    print(repr(c[idx:end]))
else:
    print("createConfetti NOT FOUND")

# Show onSpin
idx2 = c.find("function onSpin()")
if idx2 >= 0:
    end2 = c.find("function onDocClick", idx2)
    print("\nonSpin function (%d chars):" % (end2 - idx2))
    print(repr(c[idx2:end2]))
