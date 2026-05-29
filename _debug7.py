import pathlib
p = pathlib.Path(r"C:\Users\CLIENTE\Desktop\LANDING-PAGE-BERRYUP\berryup_wheel.py")
c = p.read_text(encoding="utf-8")
lines = c.split("\n")

# Find the wheel_script function and trace braces
in_func = False
depth = 0
for i, line in enumerate(lines):
    if "def wheel_script" in line:
        in_func = True
        print("START at line %d: %s" % (i+1, line.strip()[:80]))
    if in_func:
        opens = line.count("{") - line.count("{{") * 2  
        closes = line.count("}") - line.count("}}") * 2
        # More accurate: count single braces
        # In Python source, {{ means literal { in f-string, }} means literal }
        # Actual brace counting for f-string:
        import re
        singles_open = len(re.findall(r'(?<!\{)\{(?!\{)', line))
        singles_close = len(re.findall(r'(?<!\})\}(?!\})', line))
        depth += singles_open - singles_close
        if i > 950:
            print("  L%d depth=%d singles(+%d -%d): %s" % (i+1, depth, singles_open, singles_close, line.strip()[:100]))
    if in_func and depth <= 0 and i > 10:
        print("END at line %d" % (i+1))
        break
