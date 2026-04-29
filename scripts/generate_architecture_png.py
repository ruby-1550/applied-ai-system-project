from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "architecture.png"


def _font(size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    try:
        return ImageFont.truetype("DejaVuSans.ttf", size=size)
    except Exception:
        return ImageFont.load_default()


def box(draw: ImageDraw.ImageDraw, xy: tuple[int, int, int, int], title: str) -> None:
    draw.rounded_rectangle(xy, radius=16, outline=(30, 41, 59), width=3, fill=(248, 250, 252))
    x0, y0, x1, y1 = xy
    draw.text((x0 + 18, y0 + 14), title, font=_font(18), fill=(15, 23, 42))


def arrow(draw: ImageDraw.ImageDraw, start: tuple[int, int], end: tuple[int, int]) -> None:
    draw.line([start, end], fill=(51, 65, 85), width=4)
    ex, ey = end
    draw.polygon([(ex, ey), (ex - 10, ey - 6), (ex - 10, ey + 6)], fill=(51, 65, 85))


def main() -> None:
    (ROOT / "assets").mkdir(exist_ok=True)
    img = Image.new("RGB", (1400, 720), (241, 245, 249))
    draw = ImageDraw.Draw(img)

    draw.text((40, 30), "VibeCraft System Architecture", font=_font(28), fill=(2, 6, 23))
    draw.text(
        (40, 70),
        "Retrieval-Augmented + Agentic playlist building with a self-check loop",
        font=_font(18),
        fill=(51, 65, 85),
    )

    box(draw, (60, 160, 360, 270), "User Request (NL)")
    box(draw, (430, 130, 820, 260), "Retriever (TF-IDF)\nTop-N candidates")
    box(draw, (430, 300, 820, 470), "Scorer + Diversifier\nRule-based rank + constraints")
    box(draw, (890, 210, 1330, 360), "Self-check + Debug Trace\nLogs, reasons, constraints")
    box(draw, (890, 400, 1330, 540), "Outputs\nPlaylist + explanations")
    box(draw, (60, 360, 360, 520), "Eval Harness\nPredefined scenarios")

    arrow(draw, (360, 215), (430, 205))
    arrow(draw, (625, 260), (625, 300))
    arrow(draw, (820, 240), (890, 270))
    arrow(draw, (820, 385), (890, 450))
    arrow(draw, (360, 440), (430, 385))

    img.save(OUT)
    print(f"Wrote {OUT}")


if __name__ == "__main__":
    main()

