#!/usr/bin/env python3
"""
generate-product-covers.py
Generates simple product cover images using PIL for all 11 products
defined in C:/Users/asus/ai-prompt-store/scripts/gumroad-product-payloads.json.
Covers are saved to C:/Users/asus/ai-prompt-store/scripts/launch/covers/.
"""

import json
import os
from PIL import Image, ImageDraw, ImageFont

BASE = "C:/Users/asus/ai-prompt-store"
PAYLOAD_PATH = os.path.join(BASE, "scripts", "gumroad-product-payloads.json")
COVERS_DIR = os.path.join(BASE, "scripts", "launch", "covers")
os.makedirs(COVERS_DIR, exist_ok=True)

# Cover dimensions (Gumroad recommended)
WIDTH, HEIGHT = 1280, 720
BG_COLORS = [
    (30, 60, 114),   # deep blue
    (42, 157, 143),  # teal
    (233, 196, 106), # gold
    (244, 162, 97),  # orange
    (159, 96, 177),  # purple
    (38, 70, 83),    # dark teal
    (231, 111, 81),  # coral
    (57, 62, 6),     # forest
    (156, 78, 85),   # mauve
    (44, 62, 80),    # navy
    (192, 57, 43),   # red
]

FALLBACK_FONT = None
FONT_PATH = None

# Try to locate a usable TrueType font on Windows
WINDOWS_FONTS = [
    "C:/Windows/Fonts/arial.ttf",
    "C:/Windows/Fonts/arialbd.ttf",
    "C:/Windows/Fonts/calibri.ttf",
    "C:/Windows/Fonts/calibrib.ttf",
    "C:/Windows/Fonts/segoeui.ttf",
    "C:/Windows/Fonts/segoeuib.ttf",
]
for fp in WINDOWS_FONTS:
    if os.path.isfile(fp):
        FONT_PATH = fp
        break


def wrap_text(text, font, max_width, draw):
    """Simple word wrap for PIL."""
    words = text.split()
    lines = []
    current = []
    for word in words:
        test = " ".join(current + [word])
        bbox = draw.textbbox((0, 0), test, font=font)
        if bbox[2] - bbox[0] <= max_width:
            current.append(word)
        else:
            if current:
                lines.append(" ".join(current))
            current = [word]
    if current:
        lines.append(" ".join(current))
    return lines


def draw_centered_text(draw, text, font, y, width, fill="white"):
    bbox = draw.textbbox((0, 0), text, font=font)
    text_w = bbox[2] - bbox[0]
    x = (width - text_w) // 2
    draw.text((x, y), text, font=font, fill=fill)


def generate_cover(product, index):
    color = BG_COLORS[index % len(BG_COLORS)]
    img = Image.new("RGB", (WIDTH, HEIGHT), color)
    draw = ImageDraw.Draw(img)

    # Fonts
    title_font = ImageFont.truetype(FONT_PATH, 52) if FONT_PATH else ImageFont.load_default()
    sub_font = ImageFont.truetype(FONT_PATH, 32) if FONT_PATH else ImageFont.load_default()
    tag_font = ImageFont.truetype(FONT_PATH, 24) if FONT_PATH else ImageFont.load_default()

    name = product.get("name", "Untitled Product")
    price = product.get("price", "")
    slug = product.get("url_slug", "")

    # Decorative band
    band_color = tuple(min(c + 40, 255) for c in color)
    draw.rectangle([0, HEIGHT - 120, WIDTH, HEIGHT], fill=band_color)

    # Title wrap
    max_text_w = WIDTH - 120
    lines = wrap_text(name, title_font, max_text_w, draw)
    y = 140
    for line in lines[:4]:  # max 4 lines
        draw_centered_text(draw, line, title_font, y, WIDTH)
        y += 70

    # Price
    price_text = f"${price}" if price else ""
    draw_centered_text(draw, price_text, sub_font, y + 20, WIDTH, fill=(255, 255, 255))

    # Slug at bottom
    draw_centered_text(draw, f"gumroad.com/l/{slug}", tag_font, HEIGHT - 80, WIDTH, fill=(220, 220, 220))

    out_path = os.path.join(COVERS_DIR, f"{slug}.png")
    img.save(out_path, "PNG")
    return out_path


def main():
    if not os.path.isfile(PAYLOAD_PATH):
        raise SystemExit(f"Payload file not found: {PAYLOAD_PATH}")

    with open(PAYLOAD_PATH, "r", encoding="utf-8") as f:
        products = json.load(f)

    if not isinstance(products, list):
        raise SystemExit("Invalid payload format: expected a list.")

    generated = []
    for idx, p in enumerate(products):
        path = generate_cover(p, idx)
        generated.append(path)
        print(f"[OK] {path}")

    print(f"\nGenerated {len(generated)} cover images in: {COVERS_DIR}")


if __name__ == "__main__":
    main()
