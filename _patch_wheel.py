"""Patch berryup_wheel.py: confetti effect + slow-stop on 60%."""
import pathlib

p = pathlib.Path(r"C:\Users\CLIENTE\Desktop\LANDING-PAGE-BERRYUP\berryup_wheel.py")
c = p.read_text(encoding="utf-8")

# --- EDIT 1: Add confetti CSS at end of WHEEL_CSS ---
old_css_end = '#berryup-roleta .br-prize-box .br-save{color:#6a6a80;font-size:.82rem;margin:0}\n\n"""'
new_css_end = old_css_end.replace('\n"""', '') + """

/* Confetti burst on 60% win */
@keyframes confettiFall{
  0%{opacity:1;transform:translate(var(--cx),var(--cy)) rotate(0deg) scale(1)}
  100%{opacity:0;transform:translate(var(--ex),var(--ey)) rotate(var(--rot)) scale(.3)}
}
.berryup-confetti{position:fixed;top:0;left:0;width:100%;height:100%;pointer-events:none;z-index:99999;overflow:hidden}
.berryup-confetti span{position:absolute;width:var(--w);height:var(--h);border-radius:var(--br);background:var(--bg);animation:confettiFall var(--dur) cubic-bezier(.25,.46,.45,.94) forwards}

\"\"\"
"""
c = c.replace(old_css_end, new_css_end)
print("Edit 1 confetti CSS:", "OK" if "confettiFall" in c else "FAIL")

# --- EDIT 2: Remove CSS transition from disk (now JS-controlled) ---
old_trans = "transform 4.2s cubic-bezier(0.17,0.67,0.12,0.99)"
new_trans = "none  /* controlled via JS requestAnimationFrame for slow-stop drama */"
c = c.replace(old_trans, new_trans)
print("Edit 2 disk transition:", "OK" if "none  /* controlled" in c else "FAIL")

p.write_text(c, encoding="utf-8")
print("Edits 1+2 saved.")
