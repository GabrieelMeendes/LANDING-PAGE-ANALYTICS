import pathlib
p = pathlib.Path(r"C:\Users\CLIENTE\Desktop\LANDING-PAGE-BERRYUP\berryup_wheel.py")
c = p.read_text(encoding="utf-8")

# Show exact chars around closing """ of WHEEL_CSS
idx = 32556
print("Around closing triple-quote:")
print(repr(c[idx-60:idx+10]))

# Also find onSpin function boundaries
idx2 = c.find("function onSpin()")
print("\nonSpin context:")
print(repr(c[idx2:idx2+120]))

# Find the disk.classList.add line
idx3 = c.find("disk.classList.add")
print("\ndisk.classList.add context:")
print(repr(c[idx3-5:idx3+40]))
