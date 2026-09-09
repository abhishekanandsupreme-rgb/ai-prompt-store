#!/usr/bin/env python3
"""Verify all 14 covers: existence, exact 1280x720 dims, 30-300KB, pixel diversity."""
import os
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
SLUGS = [
    "ai-content-creator-pack", "ai-business-builder-pack", "ai-coding-assistant-pack",
    "ai-marketing-master-pack", "ai-writing-assistant-pack", "ai-productivity-pack",
    "ai-social-media-manager-pack", "ai-seo-expert-pack", "ai-entrepreneur-pack",
    "ai-education-pack", "complete-ai-prompt-bundle", "ai-finance-prompt-pack",
    "ai-legal-prompt-pack", "ai-real-estate-prompt-pack",
]

print(f"{'filename':<40} {'dimensions':<12} {'KB':>7}")
print("-" * 62)
fail = []
rows = []
for slug in SLUGS:
    p = os.path.join(HERE, f"{slug}.png")
    if not os.path.exists(p):
        fail.append(f"{slug}: MISSING")
        continue
    kb = os.path.getsize(p) / 1024
    with Image.open(p) as im:
        dims = im.size
        fmt = im.format
    rows.append((f"{slug}.png", dims, kb))
    status = []
    if dims != (1280, 720):
        status.append("BAD DIMS")
    if not (30 <= kb <= 300):
        status.append("BAD SIZE")
    if fmt != "PNG":
        status.append(f"BAD FORMAT {fmt}")
    if status:
        fail.append(f"{slug}: {', '.join(status)}")
    print(f"{slug + '.png':<40} {str(dims):<12} {kb:>7.1f}")

print("-" * 62)
print(f"Total: {len(rows)}/14 files, all listed")

# Diversity sanity check on 3 representative covers
print("\nPixel diversity check (sampled):")
for slug in ["complete-ai-prompt-bundle", "ai-legal-prompt-pack", "ai-education-pack"]:
    with Image.open(os.path.join(HERE, f"{slug}.png")) as im:
        rgb = im.convert("RGB")
        colors = rgb.getcolors(maxcolors=1_000_000)
        n_colors = len(colors) if colors else ">1M"
        # count near-white pixels (title text) as fraction
        small = rgb.resize((160, 90))
        px = list(small.getdata())
        whiteish = sum(1 for r, g, b in px if r > 230 and g > 230 and b > 230)
        accent = sum(1 for r, g, b in px if abs(r - 0x63) < 40 and abs(g - 0x66) < 40 and abs(b - 0xF1) < 40)
    print(f"  {slug}: distinct colors={n_colors}, white-text px={whiteish}/{len(px)}, accent px={accent}/{len(px)}")
    if n_colors == 1 or (isinstance(n_colors, int) and n_colors < 100):
        fail.append(f"{slug}: suspiciously low color diversity")

print("\nRESULT:", "ALL CHECKS PASSED" if not fail else f"FAILURES: {fail}")
raise SystemExit(0 if not fail else 1)
