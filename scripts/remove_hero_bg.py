"""Remove o fundo do hero e salva PNG com alpha."""
from pathlib import Path

import cv2
import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "assets" / "hero-berry-up.png"
OUT = ROOT / "assets" / "hero-berry-up.png"


def main() -> None:
    bgr = cv2.imread(str(SRC))
    if bgr is None:
        raise SystemExit(f"Nao foi possivel ler {SRC}")

    h, w = bgr.shape[:2]
    hsv = cv2.cvtColor(bgr, cv2.COLOR_BGR2HSV)
    mask = np.full((h, w), cv2.GC_PR_BGD, np.uint8)

    border = max(18, int(min(h, w) * 0.035))
    mask[:border, :] = cv2.GC_BGD
    mask[-border:, :] = cv2.GC_BGD
    mask[:, :border] = cv2.GC_BGD
    mask[:, -border:] = cv2.GC_BGD

    # Fundo laranja saturado. A faixa de saturacao evita comer pele/cabelo.
    orange_bg = cv2.inRange(hsv, (6, 125, 145), (24, 255, 255))
    skin_hair_guard = cv2.inRange(hsv, (0, 25, 45), (24, 150, 245))
    orange_bg = cv2.bitwise_and(orange_bg, cv2.bitwise_not(skin_hair_guard))
    mask[orange_bg > 0] = cv2.GC_PR_BGD

    probable_fg = np.zeros((h, w), np.uint8)
    cv2.rectangle(
        probable_fg,
        (int(w * 0.04), int(h * 0.04)),
        (int(w * 0.96), int(h * 0.96)),
        255,
        -1,
    )
    mask[probable_fg > 0] = cv2.GC_PR_FGD
    mask[orange_bg > 0] = cv2.GC_PR_BGD

    # Regioes centrais de pessoa/objetos que precisam permanecer no recorte.
    sure_fg = np.zeros((h, w), np.uint8)
    cv2.ellipse(sure_fg, (int(w * 0.53), int(h * 0.31)), (int(w * 0.24), int(h * 0.24)), 0, 0, 360, 255, -1)
    torso = np.array(
        [
            (int(w * 0.16), int(h * 0.58)),
            (int(w * 0.34), int(h * 0.43)),
            (int(w * 0.70), int(h * 0.47)),
            (int(w * 0.86), int(h * 0.94)),
            (int(w * 0.09), int(h * 0.94)),
        ],
        dtype=np.int32,
    )
    cv2.fillPoly(sure_fg, [torso], 255)
    cv2.ellipse(sure_fg, (int(w * 0.15), int(h * 0.59)), (int(w * 0.09), int(h * 0.28)), -5, 0, 360, 255, -1)
    cv2.ellipse(sure_fg, (int(w * 0.17), int(h * 0.37)), (int(w * 0.11), int(h * 0.11)), 0, 0, 360, 255, -1)
    cv2.ellipse(sure_fg, (int(w * 0.46), int(h * 0.78)), (int(w * 0.17), int(h * 0.12)), 0, 0, 360, 255, -1)
    paper = np.array(
        [
            (int(w * 0.63), int(h * 0.49)),
            (int(w * 0.96), int(h * 0.54)),
            (int(w * 0.89), int(h * 0.90)),
            (int(w * 0.56), int(h * 0.84)),
        ],
        dtype=np.int32,
    )
    cv2.fillPoly(sure_fg, [paper], 255)
    mask[sure_fg > 0] = cv2.GC_FGD

    bgd_model = np.zeros((1, 65), np.float64)
    fgd_model = np.zeros((1, 65), np.float64)
    cv2.grabCut(bgr, mask, None, bgd_model, fgd_model, 6, cv2.GC_INIT_WITH_MASK)

    fg = np.where((mask == cv2.GC_FGD) | (mask == cv2.GC_PR_FGD), 255, 0).astype("uint8")
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    fg = cv2.morphologyEx(fg, cv2.MORPH_CLOSE, kernel, iterations=2)
    fg = cv2.morphologyEx(fg, cv2.MORPH_OPEN, kernel, iterations=1)

    n, labels, stats, _ = cv2.connectedComponentsWithStats(fg, 8)
    keep = np.zeros_like(fg)
    min_area = int(w * h * 0.004)
    for i in range(1, n):
        if stats[i, cv2.CC_STAT_AREA] >= min_area:
            keep[labels == i] = 255
    fg = keep

    fg = cv2.GaussianBlur(fg, (0, 0), 1.1)
    fg[fg < 8] = 0
    fg[fg > 245] = 255

    rgba = cv2.cvtColor(bgr, cv2.COLOR_BGR2BGRA)
    rgba[:, :, 3] = fg

    Image.fromarray(cv2.cvtColor(rgba, cv2.COLOR_BGRA2RGBA)).save(OUT, optimize=True)
    print(f"Salvo: {OUT} ({OUT.stat().st_size:,} bytes)")


if __name__ == "__main__":
    main()
