#!/usr/bin/env python3
"""
publish-all-products.py
Reads C:/Users/asus/ai-prompt-store/scripts/gumroad-product-payloads.json
and generates a step-by-step publishing checklist with exact Gumroad form
values for each of the 11 products.
"""

import json
import os
from datetime import datetime

BASE = "C:/Users/asus/ai-prompt-store"
PAYLOAD_PATH = os.path.join(BASE, "scripts", "gumroad-product-payloads.json")
OUTPUT_PATH = os.path.join(BASE, "scripts", "launch", "PUBLISHING-CHECKLIST.md")


def load_products():
    with open(PAYLOAD_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def generate_checklist(products):
    lines = []
    lines.append("# Gumroad Publishing Checklist")
    lines.append("")
    lines.append(f"Generated: {datetime.utcnow().isoformat()}Z")
    lines.append(f"Source: {PAYLOAD_PATH}")
    lines.append(f"Total products: {len(products)}")
    lines.append("")
    lines.append("---")
    lines.append("")

    for idx, p in enumerate(products, start=1):
        slug = p.get("url_slug", "")
        name = p.get("name", "")
        price = p.get("price", "")
        orig = p.get("original_price")
        ptype = p.get("product_type", "Digital Product")
        desc = p.get("description", "")
        cat = p.get("category", "")
        tags = p.get("tags", "")
        upload = p.get("file_upload_path") or p.get("files_upload", "")
        pay_what = p.get("is_pay_what_you_want", False)
        ship = p.get("require_shipping", False)

        lines.append(f"## Step {idx}: {name}")
        lines.append("")
        lines.append("| Gumroad Field | Value to Enter |")
        lines.append("| --- | --- |")
        lines.append(f"| **Product Name** | {name} |")
        lines.append(f"| **URL Slug** | {slug} |")
        lines.append(f"| **Price** | ${price} |")
        if orig:
            lines.append(f"| **Original Price** | ${orig} |")
        lines.append(f"| **Product Type** | {ptype} |")
        lines.append(f"| **Category** | {cat} |")
        lines.append(f"| **Tags** | {tags} |")
        lines.append(f"| **Pay What You Want** | {'Yes' if pay_what else 'No'} |")
        lines.append(f"| **Require Shipping** | {'Yes' if ship else 'No'} |")
        lines.append(f"| **File Upload** | {upload} |")
        lines.append("")
        lines.append("### Description (copy/paste)")
        lines.append("")
        lines.append("```")
        lines.append(desc)
        lines.append("```")
        lines.append("")
        lines.append("### Verification")
        lines.append(f"- [ ] Live URL loads at `https://gumroad.com/l/{slug}`")
        lines.append(f"- [ ] Price shows as **${price}**")
        lines.append(f"- [ ] Download link works after purchase")
        lines.append("")
        lines.append("---")
        lines.append("")

    return "\n".join(lines)


def main():
    if not os.path.isfile(PAYLOAD_PATH):
        raise SystemExit(f"Payload file not found: {PAYLOAD_PATH}")

    products = load_products()
    if not isinstance(products, list) or len(products) == 0:
        raise SystemExit("No products found in payload file.")

    checklist = generate_checklist(products)

    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        f.write(checklist)

    print(f"Checklist written to: {OUTPUT_PATH}")
    print(f"Products processed: {len(products)}")


if __name__ == "__main__":
    main()
