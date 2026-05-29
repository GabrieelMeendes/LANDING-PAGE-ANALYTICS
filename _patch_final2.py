"""Fix remaining edits: disk transition + onSpin rewrite with slow-stop + confetti."""
import pathlib

p = pathlib.Path(r"C:\Users\CLIENTE\Desktop\LANDING-PAGE-BERRYUP\berryup_wheel.py")
c = p.read_text(encoding="utf-8")

changes = 0

# --- RE-EDIT 2: disk transition ---
old_t = "transition:transform 4.2s cubic-bezier(.15,.85,.2,1)"
new_t = "transition:none"
if old_t in c:
    c = c.replace(old_t, new_t, 1)
    print("[OK] Edit 2: disk transition -> none")
    changes += 1
elif ".br-wheel-rotor" in c and "transition:none" in c:
    print("[OK] Edit 2: already applied")
else:
    print("[WARN] Edit 2: unexpected state")

# --- EDIT 4: Rewrite onSpin body ---
fn_start_marker = "function onSpin(){{\n"
fn_idx = c.find(fn_start_marker)
if fn_idx < 0:
    fn_start_marker = "function onSpin(){\n"
    fn_idx = c.find(fn_start_marker)

if fn_idx < 0:
    print("[FAIL] Edit 4: onSpin function not found!")
else:
    body_start = fn_idx + len(fn_start_marker)
    depth = 1
    pos = body_start
    while pos < len(c) and depth > 0:
        ch = c[pos]
        if ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
        pos += 1
    fn_end = pos
    
    old_fn = c[fn_idx:fn_end]
    print("[DEBUG] Found onSpin at pos %d, length %d" % (fn_idx, fn_end - fn_idx))
    
    new_fn = 'function onSpin(){{\n'
    new_fn += '  if(spinning||won()||!disk||!spinBtn)return;\n'
    new_fn += '  spinning=true;\n'
    new_fn += '  spinBtn.disabled=true;\n'
    new_fn += '  disk.classList.add("is-spinning");\n'
    new_fn += '  if(resultEl)resultEl.textContent="Girando\u2026 boa sorte!";\n'
    new_fn += '\n'
    new_fn += '  /* === DRAMATIC SLOW-STOP: precise angle near 60% edge === */\n'
    new_fn += '  var DISK_DEG_PER_PCT=3.6;\n'
    new_fn += '  var SIXTY_SLICE_DEG=60*DISK_DEG_PER_PCT;\n'
    new_fn += '  var TARGET_SLICE_DEG=SIXTY_SLICE_DEG-4;\n'
    new_fn += '  var EXTRA_FULL_TURNS=7*360;\n'
    new_fn += '  var prevDeg=rotation;\n'
    new_fn += '  var endDeg=prevDeg+EXTRA_FULL_TURNS+TARGET_SLICE_DEG;\n'
    new_fn += '  var DUR_MS=4500;\n'
    new_fn += '  var startTime=-1;\n'
    new_fn += '\n'
    new_fn += '  function easeOutDramatic(t){{\n'
    new_fn += '    if(t<0.7){{return 1-Math.pow(1-t/0.7,3);}}\n'
    new_fn += '    var lt=(t-0.7)/0.3;\n'
    new_fn += '    return 1-Math.pow(1-lt,8)*0.06;\n'
    new_fn += '  }}\n'
    new_fn += '\n'
    new_fn += '  function tick(now){{\n'
    new_fn += '    if(startTime<0)startTime=now;\n'
    new_fn += '    var elapsed=now-startTime;\n'
    new_fn += '    var t=Math.min(elapsed/DUR_MS,1);\n'
    new_fn += '    var eased=easeOutDramatic(t);\n'
    new_fn += '    var currentDeg=prevDeg+(endDeg-prevDeg)*eased;\n'
    new_fn += '    disk.style.transform="rotate("+currentDeg+"deg)";\n'
    new_fn += '    if(t<1){{requestAnimationFrame(tick);return;}}\n'
    new_fn += '    rotation=endDeg;\n'
    new_fn += '    disk.style.transform="rotate("+rotation+"deg)";\n'
    new_fn += '    spinning=false;\n'
    new_fn += '    disk.classList.remove("is-spinning");\n'
    new_fn += '    createConfetti();\n'
    new_fn += '    setWon();\n'
    new_fn += '    applyWonUI();\n'
    new_fn += '    markCheckoutAnchors();\n'
    new_fn += '  }}\n'
    new_fn += '  requestAnimationFrame(tick);\n'
    new_fn += '}}'

    c = c[:fn_idx] + new_fn + c[fn_end:]
    print("[OK] Edit 4: onSpin rewritten")
    changes += 1

p.write_text(c, encoding="utf-8")
print("\n%d edit(s) saved." % changes)

# === FINAL VERIFICATION ===
c2 = p.read_text(encoding="utf-8")
onspin_region = ""
s_idx = c2.find("function onSpin()")
d_idx = c2.find("function onDocClick")
if s_idx >= 0 and d_idx > s_idx:
    onspin_region = c2[s_idx:d_idx]

checks = [
    ("confetti CSS keyframes", "@keyframes confettiFall" in c2),
    ("disk transition = none", ".br-wheel-rotor{position:absolute;inset:0;border-radius:50%;transition:none" in c2),
    ("createConfetti function", "function createConfetti()" in c2),
    ("rAF tick function", "function tick(now)" in c2),
    ("confetti on win", "createConfetti();" in c2),
    ("angle near 60% edge", "SIXTY_SLICE_DEG-4" in c2),
    ("dramatic easing", "easeOutDramatic" in c2),
    ("no old setTimeout 4200", "4200" not in onspin_region),
    ("DUR_MS 4500", "DUR_MS=4500" in c2),
]
print("\n=== Verification ===")
all_ok = True
for label, ok in checks:
    st = "OK" if ok else "FAIL"
    if not ok:
        all_ok = False
    print("  [%s] %s" % (st, label))
if all_ok:
    print("\nAll checks passed!")
else:
    print("\nSome checks FAILED!")
