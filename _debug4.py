import pathlib
p = pathlib.Path(r"C:\Users\CLIENTE\Desktop\LANDING-PAGE-BERRYUP\berryup_wheel.py")
c = p.read_text(encoding="utf-8")

# WHEEL_CSS ends at triple-quote at pos 32556
# Show the last 400 chars of WHEEL_CSS
print("Last 400 chars of WHEEL_CSS:")
print(repr(c[32556-400:32556]))

# Show what comes right after (should be " + BERRY...")
print("\nAfter closing:")
print(repr(c[32556:32590]))

# Exact transition string with full context
idx = c.find("transition:transform 4.2s")
print("\nFull transition line:")
# Find start of this rule (the # or . before it)
line_start = c.rfind("\n", 0, idx)
line_end = c.find("\n", idx)
print(repr(c[line_start:line_end]))
