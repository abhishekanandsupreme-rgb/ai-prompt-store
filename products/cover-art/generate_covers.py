#!/usr/bin/env python3
"""Generate 1280x720 Gumroad cover images for all 14 AI Prompt Store products.

Pure Pillow rendering — zero network calls. Output: <slug>.png next to this script.
"""

import os
import random
import sys

from PIL import Image, ImageChops, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))

W, H = 1280, 720
MARGIN_X = int(W * 0.05)          # 64px side margins (5%)
MARGIN_Y = int(H * 0.05)          # 36px top/bottom margins (5%)

# Brand palette
TOP_HEX = (0x0F, 0x17, 0x2A)      # 0f172a
BOTTOM_HEX = (0x31, 0x2E, 0x81)   # 312e81
ACCENT = (0x63, 0x66, 0xF1)       # 6366f1
WHITE = (255, 255, 255)
BADGE_TEXT = (0x0F, 0x17, 0x2A)   # dark text on bright badge
SOFT_WHITE = (199, 205, 254)      # indigo-tinted white for subtitle

# Imperceptible blocky dithering on the background: adds just enough PNG
# entropy to keep files in the 30-300KB band while looking like a clean
# gradient to the eye. Blocks are 4px; amplitude is +/-2 per channel.
NOISE_BLOCK = 4
NOISE_AMP = 2

PRODUCTS = [
    # slug, display name, subtitle, badge
    ("ai-content-creator-pack", "Content Creator", "YouTube • Social • Blogs • Email", "50 Expert Prompts"),
    ("ai-business-builder-pack", "Business Builder", "Strategy • Planning • Growth", "50 Expert Prompts"),
    ("ai-coding-assistant-pack", "Coding Assistant", "Debug • Test • Document", "50 Expert Prompts"),
    ("ai-marketing-master-pack", "Marketing Master", "Copy • Campaigns • Ads", "50 Expert Prompts"),
    ("ai-writing-assistant-pack", "Writing Assistant", "Fiction • Scripts • Poetry", "50 Expert Prompts"),
    ("ai-productivity-pack", "Productivity", "Time • Focus • Planning", "50 Expert Prompts"),
    ("ai-social-media-manager-pack", "Social Media Manager", "Calendars • Captions • Growth", "50 Expert Prompts"),
    ("ai-seo-expert-pack", "SEO Expert", "Keywords • Content • Rankings", "50 Expert Prompts"),
    ("ai-entrepreneur-pack", "Entrepreneur", "Ideas • MVPs • Growth", "50 Expert Prompts"),
    ("ai-education-pack", "Education", "Lessons • Courses • Quizzes", "50 Expert Prompts"),
    ("complete-ai-prompt-bundle", "Complete Bundle", "All 10 Packs — 500+ Prompts", "500+ Prompts"),
    ("ai-finance-prompt-pack", "Finance", "FP&A • Models • Analysis", "40 Expert Prompts"),
    ("ai-legal-prompt-pack", "Legal", "Contracts • Research • Drafts", "40 Expert Prompts"),
    ("ai-real-estate-prompt-pack", "Real Estate", "Listings • Marketing • Clients", "40 Expert Prompts"),
]

FONT_CANDIDATES = [
    "C:/Windows/Fonts/segoeuib.ttf",   # Segoe UI Bold (preferred)
    "C:/Windows/Fonts/arialbd.ttf",     # Arial Bold (fallback)
]


def find_font():
    """Return (path, used_fallback) for the first candidate that exists."""
    for path in FONT_CANDIDATES:
        if os.path.exists(path):
            return path, path != FONT_CANDIDATES[0]
    print("ERROR: no usable font found", file=sys.stderr)
    sys.exit(1)


def vertical_gradient():
    """1280x720 vertical gradient 0f172a -> 312e81 with subtle blocky dither."""
    grad = Image.new("RGB", (1, H))
    for y in range(H):
        t = y / (H - 1)
        color = tuple(int(a + (b - a) * t) for a, b in zip(TOP_HEX, BOTTOM_HEX))
        grad.putpixel((0, y), color)
    grad = grad.resize((W, H))

    # Tiny per-block offsets via ImageChops — fast, deterministic-ish, subtle.
    bw, bh = NOISE_BLOCK, NOISE_BLOCK
    small_w, small_h = W // bw, H // bh
    rng = random.Random(0x5170A5)  # fixed seed -> deterministic output
    noise = Image.new("RGB", (small_w, small_h))
    npx = noise.load()
    for y in range(small_h):
        for x in range(small_w):
            v = tuple(rng.randint(-NOISE_AMP, NOISE_AMP) for _ in range(3))
            # offset by 128 so ImageChops.subtract can't go negative
            npx[x, y] = tuple(c + 128 for c in v)
    noise = noise.resize((W, H), Image.NEAREST)
    # subtract: (grad - (128+delta)) + 128 == grad - delta
    return ImageChops.subtract(grad, noise, scale=1.0, offset=128)


def accent_geometry(img):
    """Subtle geometric accents in 6366f1: rounded frame + diagonal bands.

    Drawn on an RGBA overlay at low opacity, composited over the gradient.
    """
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(overlay)

    # Rounded-rectangle frame just inside the canvas edge
    inset = 28
    d.rounded_rectangle(
        [inset, inset, W - inset, H - inset],
        radius=36,
        outline=ACCENT + (110,),
        width=4,
    )

    # Diagonal band from the upper area toward the top-right corner (thin, subtle)
    d.polygon([(W * 0.62, 0), (W, 0), (W, H * 0.42)], fill=ACCENT + (34,))
    # Second diagonal echo, lower-left, even subtler
    d.polygon([(0, H * 0.68), (W * 0.38, H), (0, H)], fill=ACCENT + (22,))

    out = img.convert("RGBA")
    out.alpha_composite(overlay)
    return out.convert("RGB")


def wrap_to_2_lines(draw, text, font, max_width):
    """Split text into at most 2 balanced lines that each fit max_width."""
    if draw.textlength(text, font=font) <= max_width:
        return [text]
    words = text.split()
    if len(words) < 2:
        return [text]  # single long word: no wrap possible
    best = None
    for i in range(1, len(words)):
        l1, l2 = " ".join(words[:i]), " ".join(words[i:])
        w1, w2 = draw.textlength(l1, font=font), draw.textlength(l2, font=font)
        if w1 <= max_width and w2 <= max_width:
            spread = abs(w1 - w2)
            if best is None or spread < best[0]:
                best = (spread, [l1, l2])
    return best[1] if best else [text]


def rounded_badge(draw, cx, cy, text, font, fill, text_color, pad_x=22, pad_y=10):
    """Pill-shaped badge centered at (cx, cy) with centered text."""
    tw = draw.textlength(text, font=font)
    bbox = draw.textbbox((0, 0), text, font=font)
    th = bbox[3] - bbox[1]
    x0, x1 = cx - tw / 2 - pad_x, cx + tw / 2 + pad_x
    y0, y1 = cy - th / 2 - pad_y, cy + th / 2 + pad_y
    draw.rounded_rectangle([x0, y0, x1, y1], radius=int((y1 - y0) / 2), fill=fill)
    ty = cy - th / 2 - bbox[1]
    draw.text((cx - tw / 2, ty), text, font=font, fill=text_color)


def render_cover(font_path, display, subtitle, badge, out_path):
    img = vertical_gradient()
    img = accent_geometry(img)
    draw = ImageDraw.Draw(img)

    max_w = W - 2 * MARGIN_X          # usable width inside 5% side margins
    cx = W / 2

    f_badge = ImageFont.truetype(font_path, 26)
    f_title = ImageFont.truetype(font_path, 92)
    f_sub = ImageFont.truetype(font_path, 38)
    f_word = ImageFont.truetype(font_path, 28)

    lines = wrap_to_2_lines(draw, display, f_title, max_w)
    line_h = 108                      # line height for the 92px title
    sub_h = 48

    # --- vertical layout: badge zone, title, subtitle (block roughly centered)
    badge_zone = 90                   # pill is ~46px tall, centered in this zone
    gap_badge_title = 28
    gap_title_sub = 16
    block_h = badge_zone + gap_badge_title + line_h * len(lines) + gap_title_sub + sub_h
    top = max((H - block_h) / 2, MARGIN_Y)

    # Badge (top-center, above the title)
    rounded_badge(draw, cx, top + badge_zone / 2, badge.upper(), f_badge, ACCENT, BADGE_TEXT)

    # Title (big bold, centered, at most 2 lines)
    y = top + badge_zone + gap_badge_title
    for line in lines:
        tw = draw.textlength(line, font=f_title)
        draw.text((cx - tw / 2, y), line, font=f_title, fill=WHITE)
        y += line_h

    # Subtitle (smaller, below the title)
    y += gap_title_sub - (line_h - 100)   # 100px ≈ visual glyph height of a title line
    sw = draw.textlength(subtitle, font=f_sub)
    draw.text((cx - sw / 2, y), subtitle, font=f_sub, fill=SOFT_WHITE)

    # Wordmark at the bottom, ending exactly at the 5% bottom margin (y=684)
    wm = "AI Prompt Store"
    wbbox = draw.textbbox((0, 0), wm, font=f_word)
    wm_h = wbbox[3] - wbbox[1]
    ww = draw.textlength(wm, font=f_word)
    draw.text((cx - ww / 2, H - MARGIN_Y - wm_h - wbbox[1] - 2), wm, font=f_word, fill=SOFT_WHITE)

    img.save(out_path, "PNG", optimize=True)


def main():
    font_path, used_fallback = find_font()
    print(f"Font: {font_path} (fallback used: {used_fallback})")

    for slug, display, subtitle, badge in PRODUCTS:
        out = os.path.join(HERE, f"{slug}.png")
        render_cover(font_path, display, subtitle, badge, out)
        print(f"  wrote {slug}.png  {os.path.getsize(out) / 1024:.1f} KB")
    print(f"Done: {len(PRODUCTS)} covers generated in {HERE}")


if __name__ == "__main__":
    main()
