#!/usr/bin/env python3
"""
Gumroad BrowserOS Neo Automation Script
Uploads products to Gumroad using browser_exec with session='browseros-neo-team1'.
Reads product data from scripts/gumroad-product-payloads.json.

IMPORTANT:
- Do not hardcode credentials. If Gumroad shows a login wall, STOP and report.
- browser_exec requires Chrome's remote debugging permission. If blocked,
  click "Allow" on Chrome's "Allow remote debugging?" popup and retry.
- This script targets Product 1 only by default.
"""

import json
import os
from pathlib import Path

# Resolve paths relative to the scripts directory
BASE_DIR = Path(__file__).resolve().parent
PAYLOAD_FILE = BASE_DIR / "gumroad-product-payloads.json"


def load_product_payloads():
    """Load product payloads from JSON file."""
    if not PAYLOAD_FILE.exists():
        raise FileNotFoundError(f"Payload file not found: {PAYLOAD_FILE}")
    with open(PAYLOAD_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def get_abs_file_path(product):
    """Resolve the product file upload path to an absolute Windows path."""
    rel_path = product.get("file_upload_path", "")
    if not rel_path:
        raise ValueError("No file_upload_path specified in payload")
    # Resolve relative to the ai-prompt-store root (parent of scripts/)
    abs_path = (BASE_DIR.parent / rel_path).resolve()
    if not abs_path.exists():
        raise FileNotFoundError(f"Product file not found: {abs_path}")
    return str(abs_path)


def check_login_wall():
    """Return True if Gumroad is showing a login wall."""
    return js(
        "document.body.innerText.toLowerCase().includes('log in') "
        "|| document.querySelector('input[type=\"email\"]') !== null"
    )


def build_browser_code(product, abs_file_path):
    """Build the browser_exec Python code string for a single product."""
    name = product["name"]
    price = str(product["price"])
    url_slug = product.get("url_slug", "")
    description = product.get("description", "").replace("\\", "\\\\").replace('"', '\\"')

    code = """
# Check for login wall before proceeding
if check_login_wall():
    print("LOGIN_WALL: Gumroad requires login. Please log in manually and retry.")
    exit(1)

goto_url("https://gumroad.com/products/new")
wait_for_load()

# Step 1: Fill name and price on the wizard page
# Use type_text after focusing because fill_input does not trigger React onChange
js(\"""
(() => {
  const nameInput = document.querySelector('input[id^="name-"]');
  if (nameInput) nameInput.focus();
})()
\""")
type_text("__NAME__")

js(\"""
(() => {
  const priceInput = document.querySelector('input[id^="price-"]');
  if (priceInput) priceInput.focus();
})()
\""")
type_text("__PRICE__")

# Click Next: Customize
js(\"""
(() => {
  const btn = Array.from(document.querySelectorAll('button'))
    .find(b => b.textContent.includes('Next: Customize'));
  if (btn) btn.click();
})()
\""")
wait_for_load()

# Step 2: On the edit page, set URL slug
js(\"""
(() => {
  const inputs = Array.from(document.querySelectorAll('input[type="text"]'));
  const slugInput = inputs.find(i => i.placeholder === 'bosfjm' || i.id.startsWith(':rh:'));
  if (slugInput) {
    slugInput.focus();
    slugInput.value = '';
    slugInput.dispatchEvent(new Event('input', { bubbles: true }));
  }
})()
\""")
type_text("__URL_SLUG__")

# Step 3: Fill description using the TipTap editor
js(\"""
(() => {
  const editor = document.querySelector('.tiptap');
  if (editor) {
    editor.focus();
    editor.innerHTML = '';
  }
})()
\""")
type_text("__DESCRIPTION__")

# Step 4: Upload product file via CDP
# First find the file input intended for product content
js(\"""
(() => {
  const inputs = Array.from(document.querySelectorAll('input[type="file"]'));
  const contentInput = inputs.find(i => !i.accept || i.accept === '');
  if (contentInput) {
    contentInput.id = 'gumroad-product-file-input';
  }
})()
\""")
# Upload via CDP DOM.setFileInputFiles
cdp('DOM.setFileInputFiles', nodeId=0, files=["__ABS_FILE_PATH__"])

# Step 5: Click Publish
js(\"""
(() => {
  const btn = Array.from(document.querySelectorAll('button'))
    .find(b => b.textContent.includes('Publish'));
  if (btn) btn.click();
})()
\""")
wait_for_load()

# Return the final URL
result = page_info()
print(result.get("url", "UNKNOWN"))
"""
    code = code.replace("__NAME__", name)
    code = code.replace("__PRICE__", price)
    code = code.replace("__URL_SLUG__", url_slug)
    code = code.replace("__DESCRIPTION__", description)
    code = code.replace("__ABS_FILE_PATH__", abs_file_path)
    return code


def main():
    print("Loading product payloads...")
    products = load_product_payloads()
    if not products:
        print("No products found in payload file.")
        return 1

    product = products[0]  # Product 1 only
    print(f"Processing Product 1: {product['name']}")

    abs_file_path = get_abs_file_path(product)
    print(f"Product file: {abs_file_path}")

    code = build_browser_code(product, abs_file_path)
    print("=" * 60)
    print("Browser automation code built. Execute via browser_exec:")
    print("=" * 60)
    print(code)
    print("=" * 60)
    return 0


if __name__ == "__main__":
    exit(main())
