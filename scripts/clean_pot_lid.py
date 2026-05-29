"""Remove brand text from the product jar lid."""
from pathlib import Path

import cv2
import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "assets" / "pot-original.webp"
OUT_PNG = ROOT / "assets" / "pot-sem-texto.png"
OUT_WEBP = ROOT / "assets" / "pot-sem-texto.webp"

img = np.array(Image.open(SRC).convert("RGBA"))
rgb = img[:, :, :3].copy()
alpha = img[:, :, 3]
bgr = cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR)
h, w = bgr.shape[:2]
hsv = cv2.cvtColor(bgr, cv2.COLOR_BGR2HSV)

text_mask = np.zeros((h, w), dtype=np.uint8)

# --- Pink logo + signature ---
pink = cv2.inRange(hsv, (130, 28, 70), (180, 255, 255))
lid = np.zeros((h, w), dtype=np.uint8)
lid[: int(h * 0.58), :] = 255
pink_lid = cv2.bitwise_and(pink, lid)
n, labels, stats, _ = cv2.connectedComponentsWithStats(pink_lid, 8)
for i in range(1, n):
    if stats[i, cv2.CC_STAT_AREA] >= 150:
        text_mask[labels == i] = 255

# --- Flat top of lid ---
top = np.zeros((h, w), dtype=np.uint8)
cv2.ellipse(top, (w // 2, int(h * 0.13)), (int(w * 0.32), int(h * 0.10)), 0, 0, 360, 255, -1)
text_mask = cv2.bitwise_or(text_mask, cv2.bitwise_and(pink, top))
text_mask = cv2.bitwise_or(
    text_mask,
    cv2.bitwise_and(cv2.inRange(hsv, (0, 0, 100), (180, 42, 240)), top),
)

# --- Front/side label band (grey + pink text) ---
front_band = np.zeros((h, w), dtype=np.uint8)
cv2.rectangle(
    front_band,
    (int(w * 0.22), int(h * 0.17)),
    (int(w * 0.78), int(h * 0.42)),
    255,
    -1,
)
# Sample clean white from dot zones on lid sides
dot_zones = np.zeros((h, w), dtype=np.uint8)
cv2.rectangle(dot_zones, (0, int(h * 0.18)), (int(w * 0.16), int(h * 0.41)), 255, -1)
cv2.rectangle(dot_zones, (int(w * 0.84), int(h * 0.18)), (w - 1, int(h * 0.41)), 255, -1)
white_dots = cv2.bitwise_and(
    dot_zones, cv2.inRange(hsv, (0, 0, 200), (180, 80, 255))
)
white_dots = cv2.bitwise_and(white_dots, cv2.bitwise_not(pink))

kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (9, 9))
inpaint_mask = cv2.dilate(text_mask, kernel, 2)
# Grey/pink lettering in central front band only
front_ink = cv2.bitwise_and(
    front_band,
    cv2.bitwise_or(
        pink_lid,
        cv2.inRange(hsv, (0, 0, 105), (180, 45, 238)),
    ),
)
inpaint_mask = cv2.bitwise_or(inpaint_mask, front_ink)

clean_bgr = cv2.inpaint(bgr, inpaint_mask, 11, cv2.INPAINT_TELEA)
# Second pass for faint ghost text on front rim
h2, w2 = clean_bgr.shape[:2]
hsv2 = cv2.cvtColor(clean_bgr, cv2.COLOR_BGR2HSV)
ghost = cv2.bitwise_and(
    front_band,
    cv2.inRange(hsv2, (0, 0, 108), (180, 48, 242)),
)
ghost = cv2.bitwise_and(ghost, cv2.bitwise_not(cv2.inRange(hsv2, (130, 35, 80), (180, 255, 255))))
ghost = cv2.dilate(ghost, kernel, 1)
clean_bgr = cv2.inpaint(clean_bgr, ghost, 9, cv2.INPAINT_TELEA)

clean_rgb = cv2.cvtColor(clean_bgr, cv2.COLOR_BGR2RGB)
out = np.dstack([clean_rgb, alpha])
Image.fromarray(out, "RGBA").save(OUT_PNG, optimize=True)
Image.fromarray(out, "RGBA").save(OUT_WEBP, quality=92, method=6)
print("OK", OUT_WEBP.stat().st_size)
