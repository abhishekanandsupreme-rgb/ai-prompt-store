#!/usr/bin/env bash
# prepare-uploads.sh
# Validates all 11 product files exist and creates upload manifests.
# All paths are absolute Windows paths.

set -euo pipefail

BASE="C:/Users/asus/ai-prompt-store"
MANIFEST_DIR="$BASE/scripts/launch/manifests"
mkdir -p "$MANIFEST_DIR"

# 10 individual prompt packs
PACKS=(
  "products/prompt-pack-1/prompts.md"
  "products/prompt-pack-2/prompts.md"
  "products/prompt-pack-3/prompts.md"
  "products/prompt-pack-4/prompts.md"
  "products/prompt-pack-5/prompts.md"
  "products/prompt-pack-6/prompts.md"
  "products/prompt-pack-7/prompts.md"
  "products/prompt-pack-8/prompts.md"
  "products/prompt-pack-9/prompts.md"
  "products/prompt-pack-10/prompts.md"
)

BUNDLE="products/bundle-all-10-packs.zip"

echo "=== Gumroad Launch Upload Preparation ==="
echo "Base: $BASE"
echo ""

MISSING=0
ALL_FILES=("${PACKS[@]}")
ALL_FILES+=("$BUNDLE")

# Validate individual files
for REL in "${ALL_FILES[@]}"; do
  FULL="$BASE/$REL"
  if [ -f "$FULL" ]; then
    SIZE=$(stat -c%s "$FULL" 2>/dev/null || stat -f%z "$FULL" 2>/dev/null)
    echo "[OK] $FULL (${SIZE} bytes)"
  else
    echo "[MISSING] $FULL"
    MISSING=$((MISSING + 1))
  fi
done > "$MANIFEST_DIR/validation-report.txt"

if [ "$MISSING" -gt 0 ]; then
  echo ""
  echo "ERROR: $MISSING file(s) missing. Fix before uploading."
  cat "$MANIFEST_DIR/validation-report.txt"
  exit 1
fi

echo ""
echo "All 11 product files validated successfully."

# Create manifests for each product using a helper script
cat > "$MANIFEST_DIR/_gen_manifest.py" <<PY
import json, os, datetime

BASE = "C:/Users/asus/ai-prompt-store"
PAYLOADS = os.path.join(BASE, "scripts", "gumroad-product-payloads.json")

with open(PAYLOADS, "r", encoding="utf-8") as f:
    products = json.load(f)

manifests = []
for p in products:
    rel = p.get("file_upload_path") or p.get("files_upload") or ""
    if rel.startswith("All products/"):
        local_path = os.path.join(BASE, "products", "bundle-all-10-packs.zip")
    elif rel:
        local_path = os.path.join(BASE, rel.replace("/", os.sep))
    else:
        local_path = None

    entry = {
        "product_name": p["name"],
        "url_slug": p["url_slug"],
        "price": p["price"],
        "original_price": p.get("original_price"),
        "product_type": p["product_type"],
        "category": p["category"],
        "tags": p["tags"],
        "is_published": p.get("is_published", False),
        "upload_file": local_path,
        "file_exists": os.path.isfile(local_path) if local_path else False,
        "generated_at": datetime.datetime.utcnow().isoformat() + "Z"
    }
    manifests.append(entry)

with open(os.path.join("$MANIFEST_DIR", "upload-manifests.json"), "w", encoding="utf-8") as f:
    json.dump(manifests, f, indent=2)
PY

python "$MANIFEST_DIR/_gen_manifest.py"
rm -f "$MANIFEST_DIR/_gen_manifest.py"

echo ""
echo "Upload manifests written to: $MANIFEST_DIR/upload-manifests.json"
echo "Validation report written to: $MANIFEST_DIR/validation-report.txt"
echo ""
echo "Next: run publish-all-products.py to generate your checklist."
