#!/usr/bin/env python3
"""
Gumroad Auto-Setup Assistant
Parses GUMROAD-LISTINGS.md into structured JSON and generates
pre-filled product payloads for rapid Gumroad account creation.
"""

import json
import re
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
LISTINGS_FILE = BASE_DIR / "GUMROAD-LISTINGS.md"
OUTPUT_FILE = BASE_DIR / "scripts" / "gumroad-products.json"
PAYLOAD_FILE = BASE_DIR / "scripts" / "gumroad-product-payloads.json"


def parse_listings(text: str) -> list:
    products = []
    blocks = re.split(r"\n---\n", text)

    for block in blocks:
        if not block.strip():
            continue

        product = {}

        name_match = re.search(r"\*\*Product Name:\*\* (.+)", block)
        if name_match:
            product["name"] = name_match.group(1).strip()

        slug_match = re.search(r"\*\*URL Slug:\*\* (.+)", block)
        if slug_match:
            product["slug"] = slug_match.group(1).strip()

        price_match = re.search(r"\*\*Price:\*\* \$(\d+\.\d+)", block)
        if price_match:
            product["price"] = float(price_match.group(1))

        orig_price_match = re.search(r"\*\*Original Price:\*\* \$(\d+\.\d+)", block)
        if orig_price_match:
            product["original_price"] = float(orig_price_match.group(1))

        type_match = re.search(r"\*\*Product Type:\*\* (.+)", block)
        if type_match:
            product["product_type"] = type_match.group(1).strip()

        category_match = re.search(r"\*\*Category:\*\* (.+)", block)
        if category_match:
            product["category"] = category_match.group(1).strip()

        tags_match = re.search(r"\*\*Tags:\*\* (.+)", block)
        if tags_match:
            product["tags"] = [t.strip() for t in tags_match.group(1).split(",")]

        # Description: everything between Description and first ** after it
        desc_match = re.search(
            r"\*\*Description:\*\*\n(.+?)(?=\n\*\*File to upload|\n\*\*Tags:|\Z)",
            block,
            re.DOTALL,
        )
        if desc_match:
            product["description"] = desc_match.group(1).strip()

        # File uploads
        file_upload = re.search(r"\*\*File to upload:\*\* (.+)", block)
        files_upload = re.search(r"\*\*Files to upload:\*\* (.+)", block)
        if file_upload:
            product["file_upload"] = file_upload.group(1).strip()
        if files_upload:
            product["files_upload"] = files_upload.group(1).strip()

        if product:
            products.append(product)

    return products


def build_gumroad_payload(product: dict) -> dict:
    """
    Build a form-ready payload matching Gumroad's product creation fields.
    This is a best-guess mapping based on typical Gumroad create-product form.
    """
    payload = {
        "name": product.get("name", ""),
        "url_slug": product.get("slug", ""),
        "price": product.get("price", 999),
        "original_price": product.get("original_price"),
        "product_type": product.get("product_type", "Digital Product"),
        "description": product.get("description", ""),
        "category": product.get("category", ""),
        "tags": ", ".join(product.get("tags", [])),
        "file_upload_path": product.get("file_upload") or product.get("files_upload", ""),
        "is_pay_what_you_want": False,
        "require_shipping": False,
        "is_published": True,
    }
    return payload


def main():
    if not LISTINGS_FILE.exists():
        print(f"ERROR: {LISTINGS_FILE} not found.")
        return 1

    text = LISTINGS_FILE.read_text(encoding="utf-8")
    products = parse_listings(text)
    payloads = [build_gumroad_payload(p) for p in products]

    OUTPUT_FILE.write_text(json.dumps(products, indent=2), encoding="utf-8")
    PAYLOAD_FILE.write_text(json.dumps(payloads, indent=2), encoding="utf-8")

    print(f"Parsed {len(products)} products.")
    print(f"Structured JSON: {OUTPUT_FILE}")
    print(f"Form payloads:   {PAYLOAD_FILE}")
    print("\n=== Pre-filled Payloads (copy/paste ready) ===\n")
    for i, p in enumerate(payloads, 1):
        print(f"--- Product {i}: {p['name']} ---")
        print(json.dumps(p, indent=2))
        print()

    return 0


if __name__ == "__main__":
    exit(main())
