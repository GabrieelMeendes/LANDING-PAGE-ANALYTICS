"""Patch berryup_wheel.py: confetti burst + dramatic slow-stop on 60%."""
import pathlib

p = pathlib.Path(r"C:\Users\CLIENTE\Desktop\LANDING-PAGE-BERRYUP\berryup_wheel.py")
c = p.read_text(encoding="utf-8")

# =========================================================================
# EDIT 1 — Add confetti CSS at the very end of WHEEL_CSS (before closing """)
# =========================================================================
marker1 = "@keyframes berryupRoletaPulse{0%,100%{box-shadow:inset 0 0 0 0 rgba(255,179,71,0)}50%{box-shadow:inset 0 0 0 4px rgba(255,179,71,.25)}}\n"

confetti_css = (
    "@keyframes berryupRoletaPulse{0%,100%{box-shadow:inset 0 0 0 0 rgba(255,179,71,0)}50%{box-shadow:inset 0 0 0 4px rgba(255,179,71,.25)}}\n"
    "\n"
    "/* === Confetti burst celebration on 60% win === */\n"
    "@keyframes confettiFall{\n"
    "  0%{opacity:1;transform:translate(var(--cx),var(--cy)) rotate(0deg) scale(1)}\n"
    "  100%{opacity:0;transform:translate(var(--ex),var(--ey)) rotate(var(--rot)) scale(.25)}\n"
    "}\n"
    ".berryup-confetti{position:fixed;top:0;left:0;width:100%;height:100%;pointer-events:none;z-index:99999;overflow:hidden}\n"
    ".berryup-confetti span{position:absolute;width:var(--w);height:var(--h);border-radius:var(--br);background:var(--bg);animation:confettiFall var(--dur) cubic-bezier(.25,.46,.45,.94) forwards}\n"
)

if marker1 in c:
    c = c.replace(marker1, confetti_css, 1)
    print("[OK] Edit 1: confetti CSS added")
else:
    print("[FAIL] Edit 1: marker not found")

# =========================================================================
# EDIT 2 — Remove CSS transition from disk (now JS-controlled)
# =========================================================================
marker2 = "transition:transform 4.2s cubic-bezier(.15,.85,.2,1)"
replacement2 = "transition:none  /* JS requestAnimationFrame slow-stop drama */"

if marker2 in c:
    c = c.replace(marker2, replacement2, 1)
    print("[OK] Edit 2: disk transition removed")
else:
    print("[FAIL] Edit 2: marker not found")

# =========================================================================
# EDIT 3 — Add createConfetti() function before onSpin()
# =========================================================================
marker3 = 'function onSpin(){{'

confetti_fn = """function createConfetti(){{
  var container=document.createElement("div");
  container.className="berryup-confetti";
  document.body.appendChild(container);
  var colors=["#ff6316","#FFD700","#FF1493","#00E5FF","#7CFC00","#FF6B6B","#a855f7","#FFF133"];
  var cx=window.innerWidth/2,cy=window.innerHeight/2;
  for(var i=0;i<120;i++){{
    var el=document.createElement("span");
    var angle=Math.random()*Math.PI*2;
    var dist=200+Math.random()*500;
    var ex=Math.cos(angle)*dist;
    var ey=Math.sin(angle)*dist-100;
    var w=6+Math.random()*8;
    var h=4+Math.random()*10;
    var rot=Math.random()*1080-540;
    var dur=1.2+Math.random()*1.8;
    var bg=colors[Math.floor(Math.random()*colors.length)];
    var br=Math.random()>.5?"50%":"2px";
    el.style.cssText="--cx:"+(-ex/2)+"px;--cy:"+(-ey/2)+"px;--ex:"+ex+"px;--ey:"+ey+"px;--rot:"+rot+"deg;--w:"+w+"px;--h:"+h+"px;--dur:"+dur+"s;--br:"+br+";--bg:"+bg+";left:"+cx+"px;top:"+cy+"px";
    container.appendChild(el);
  }}
  setTimeout(function(){{container.remove();}},4000);
}}

function onSpin(){{"""

if marker3 in c:
    c = c.replace(marker3, confetti_fn, 1)
    print("[OK] Edit 3: createConfetti function added")
else:
    print("[FAIL] Edit 3: marker not found")

# =========================================================================
# EDIT 4 — Rewrite onSpin body: requestAnimationFrame slow-stop + confetti
# =========================================================================
# Replace the body of onSpin: from "spinning=true;" through "}},4200);"
old_body = """spinning=true;
  spinBtn.disabled=true;
  disk.classList.add("is-spinning");
  if(resultEl)resultEl.textContent="Girando\\u2026 boa sorte!";
  var turns=7;
  rotation+=360*turns;
  disk.style.transform="rotate("+rotation+"deg)";
  setTimeout(function(){{
    spinning=false;
    setWon();
    applyWonUI();
    markCheckoutAnchors();
  }},4200);"""

new_body = """spinning=true;
  spinBtn.disabled=true;
  disk.classList.add("is-spinning");
  if(resultEl)resultEl.textContent="Girando\\u2026 boa sorte!";
  var DISK_DEG_PER_PCT=3.6;
  var SIXTY_SLICE_DEG=60*DISK_DEG_PER_PCT;
  var TARGET_SLICE_DEG=SIXTY_SLICE_DEG-4;
  var EXTRA_FULL_TURNS=7*360;
  var prevDeg=rotation;
  var endDeg=prevDeg+EXTRA_FULL_TURNS+TARGET_SLICE_DEG;
  var DUR_MS=4500;
  var startTime=-1;
  function easeOutDramatic(t){{
    if(t<.7)return 1-Math.pow(1-t/0.7,3);
    var lt=(t-.7)/.3;
    return 1-Math.pow(1-lt,8)*.06;
  }}
  function tick(now){{
    if(startTime<0)startTime=now;
    var elapsed=now-startTime;
    var t=Math.min(elapsed/DUR_MS,1);
    var eased=easeOutDramatic(t);
    var currentDeg=prevDeg+(endDeg-prevDeg)*eased;
    disk.style.transform="rotate("+currentDeg+"deg)";
    if(t<1){{requestAnimationFrame(tick);return}}
    rotation=endDeg;
    disk.style.transform="rotate("+rotation+"deg)";
    spinning=false;
    disk.classList.remove("is-spinning");
    createConfetti();
    setWon();
    applyWonUI();
    markCheckoutAnchors();
  }}
  requestAnimationFrame(tick);"""

if old_body in c:
    c = c.replace(old_body, new_body, 1)
    print("[OK] Edit 4: onSpin rewritten with rAF slow-stop + confetti")
else:
    print("[FAIL] Edit 4: old body not found — checking partial match...")
    idx = c.find("spinning=true;\n  spinBtn.disabled=true;")
    if idx >= 0:
        print(f"  Found 'spinning=true' at pos {idx}")
        snippet = c[idx:idx+60]
        print(f"  Snippet: {repr(snippet)}")
    else:
        print("  'spinning=true' not found at all!")

p.write_text(c, encoding="utf-8")

# Verification
c2 = p.read_text(encoding="utf-8")
checks = [
    ("confetti CSS keyframes", "confettiFall" in c2),
    ("disk transition = none", "transition:none" in c2 and "4.2s cubic" not in c2),
    ("createConfetti function", "function createConfetti()" in c2),
    ("requestAnimationFrame tick", "function tick(now)" in c2),
    ("confetti triggered on win", "createConfetti();" in c2),
    ("target 563 deg (near 60% edge)", "SIXTY_SLICE_DEG-4" in c2),
    ("dramatic easing", "easeOutDramatic" in c2),
]
print("\n=== Verification ===")
all_ok = True
for label, ok in checks:
    status = "OK" if ok else "FAIL"
    if not ok:
        all_ok = False
    print(f"  [{status}] {label}")
print(f"\n{'All checks passed!' if all_ok else 'Some checks FAILED!'}")
