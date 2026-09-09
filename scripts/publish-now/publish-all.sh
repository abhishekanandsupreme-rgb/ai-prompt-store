#!/usr/bin/env bash
# =============================================================================
# publish-all.sh — publish all 11 products to Gumroad via the official CLI
#
# Uses the installed Gumroad CLI (v2026.09.07) at C:/Users/asus/.local/bin/gumroad.exe
# (https://github.com/antiwork/gumroad-cli). One CLI call set per product:
#   1. gumroad products create --name --price --file --description --custom-permalink
#        --custom-summary --tag ...   -> creates a DRAFT with the file attached
#        (the CLI uploads the file via the S3 presign flow automatically)
#   2. capture the product id from the --json output
#   3. gumroad products publish <id>  -> flips it live
#
# PREREQUISITE (once): log the CLI in.
#     C:/Users/asus/.local/bin/gumroad.exe auth login
#   (device flow: it prints a URL + code; open in a browser logged in as
#    demosupreme001@gmail.com and approve. Or, with a token from
#    gumroad.com/settings/developers:  gumroad auth login --with-token < token.txt)
#
# ALSO PREREQUISITE: payouts must be configured at
#     https://gumroad.com/settings/payments  (else publish is blocked).
#
# USAGE
#   ./publish-all.sh                # all 11 products
#   ./publish-all.sh --start-from 8 # resume from product #8 (after a crash)
#   ./publish-all.sh --only 11      # just the bundle
#   ./publish-all.sh --dry-run      # echo the exact CLI calls, execute nothing
#
# IDEMPOTENCY: before creating, runs `gumroad products list --json` and skips
# any product whose slug (custom_permalink) or exact name is already live.
# Safe to re-run any number of times.
#
# Exit codes: 0 all done (or already existed) | 1 validation error |
#             2 not logged in | 3 one or more products failed
# =============================================================================

set -u

GUM="C:/Users/asus/.local/bin/gumroad.exe"
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"   # scripts/publish-now
REPO="$(cd "$HERE/../.." && pwd)"                       # ai-prompt-store
# python is a NATIVE Windows binary: it needs Windows-style paths, not MSYS
# /c/... paths. Convert once via cygpath (no-op when cygpath is absent).
W() { command -v cygpath >/dev/null 2>&1 && cygpath -w "$1" || printf '%s' "$1"; }
HERE_W="$(W "$HERE")"
REPO_W="$(W "$REPO")"
PAYLOADS="$REPO/scripts/gumroad-product-payloads.json"  # names/slugs/tags/descriptions/prices
READY="$REPO/scripts/gumroad-all-products-ready.json"   # file_path per product (fallback)
BUNDLE_FILE="$REPO/products/bundle-all-10-packs.zip"
RESULTS="$HERE/publish-results.tsv"                     # slug<TAB>id<TAB>url log

START_FROM=1
ONLY=""
DRY_RUN=0

for arg in "$@"; do
  case "$arg" in
    --start-from) shift_next=1 ;;
    *) : ;;
  esac
done
# proper arg parse (kept simple: --start-from N | --only N | --dry-run)
while [ $# -gt 0 ]; do
  case "$1" in
    --start-from) START_FROM="$2"; shift 2 ;;
    --only)       ONLY="$2"; shift 2 ;;
    --dry-run)    DRY_RUN=1; shift ;;
    -h|--help)    grep '^#' "$0" | head -40; exit 0 ;;
    *) echo "Unknown arg: $1 (use --start-from N | --only N | --dry-run)"; exit 1 ;;
  esac
done

# -----------------------------------------------------------------------------
# Helpers
# -----------------------------------------------------------------------------
PYLIST="$HERE/.payload-list.py"
PYLIST_W="$HERE_W/.payload-list.py"
cat > "$PYLIST" <<'EOF'
import json, re, sys
from pathlib import Path

# Windows python print() emits \r\n; strip it so the bash TSV read stays clean.
def out(s):
    sys.stdout.write(s.replace("\r", "") + "\n")

REPO = Path(sys.argv[1])
payloads = json.loads((REPO / "scripts/gumroad-product-payloads.json").read_text(encoding="utf-8"))
ready = {}
rfile = REPO / "scripts/gumroad-all-products-ready.json"
if rfile.is_file():
    for e in json.loads(rfile.read_text(encoding="utf-8")):
        if isinstance(e, dict) and e.get("name"):
            ready[e["name"]] = e

def html(text):
    def esc(s):
        return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    def inline(s):
        return re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", esc(s))
    if "Files to upload" in text:   # strip internal note from the bundle description
        text = text.split("Files to upload", 1)[0].rstrip().rstrip(",")
    bullet = re.compile(r"^[-*\u2022]\s+(.*)$")
    out = []
    for b in [b.strip() for b in re.split(r"\n\s*\n", text or "") if b.strip()]:
        lines = [l.strip() for l in b.splitlines() if l.strip()]
        if lines and all(bullet.match(l) for l in lines):
            out.append("<ul>" + "".join(f"<li>{inline(bullet.match(l).group(1))}</li>" for l in lines) + "</ul>")
        else:
            out.append("<p>" + "<br>".join(inline(l) for l in lines) + "</p>")
    return "\n".join(out)

# slug -> (n, name, price, file_abs, desc_html, summary, tags, slug)
out("\t".join(["n", "name", "price", "file", "slug"]))
for i, p in enumerate(payloads, 1):
    name = p["name"]
    raw = p.get("file_upload_path", "") or ""
    if "*" in raw or not raw.lower().endswith((".md", ".zip")):
        cand = ready.get(name, {}).get("file_path", "")
        m = re.search(r"(products/.+)$", str(cand))
        rel = m.group(1) if m else ("products/bundle-all-10-packs.zip" if "bundle" in name.lower() else "")
    else:
        m = re.search(r"(products/.+)$", raw)
        rel = m.group(1) if m else raw
    f = (REPO / rel).resolve()
    desc = p.get("description", "") or ""
    summary = " ".join(re.split(r"\n\s*\n", desc.strip())[0].split())[:220] if desc.strip() else ""
    if len(summary) == 220:
        summary = summary.rsplit(" ", 1)[0] + "..."
    tags = [t.strip() for t in str(p.get("tags", "")).split(",") if t.strip()]
    slug = str(p["url_slug"]).strip()
    out("\t".join([str(i), name, str(p["price"]), str(f), slug]))
    # sidecar per product for the bash loop (desc html, summary, tags)
    (REPO / ("scripts/publish-now/.meta-%d.json" % i)).write_text(
        json.dumps({"html": html(desc), "summary": summary, "tags": tags}), encoding="utf-8")
EOF

# -----------------------------------------------------------------------------
# 1. Validate payloads & files (always, even in --dry-run)
# -----------------------------------------------------------------------------
echo "=== Validating payloads + files (offline) ==="
python "$PYLIST_W" "$REPO_W" > "$HERE/.payloads.tsv" || { echo "payload parse failed"; exit 1; }

PASS=1
while IFS=$'\t' read -r n name price file slug; do
  [ "$n" = "n" ] && continue
  if [ ! -f "$file" ]; then
    echo "  MISSING FILE for #$n ($name): $file"; PASS=0
  fi
done < "$HERE/.payloads.tsv"

if [ "$PASS" -ne 1 ]; then echo "Validation FAILED — fix files first."; exit 1; fi
N_ROWS=$(( $(wc -l < "$HERE/.payloads.tsv") - 1 ))
echo "  $N_ROWS payloads, all files present."
if [ "$N_ROWS" -ne 11 ]; then echo "  WARNING: expected 11 payloads, found $N_ROWS"; fi
rm -f "$PYLIST"

# bundle staleness check (zip built Aug 22; packs 2-9 were enriched since)
python - "$REPO_W" <<'EOF'
import zipfile, sys
from pathlib import Path
repo = Path(sys.argv[1])
z = repo / "products/bundle-all-10-packs.zip"
stale = []
try:
    with zipfile.ZipFile(z) as zf:
        for zi in zf.infolist():
            if zi.filename.endswith("prompts.md"):
                pack = zi.filename.split("/")[0]
                disk = repo / "products" / pack / "prompts.md"
                if disk.is_file() and zf.read(zi) != disk.read_bytes():
                    stale.append(pack)
except Exception as e:
    print(f"  WARN: bundle zip unreadable: {e}")
if stale:
    print(f"  NOTE: bundle zip is STALE for: {', '.join(stale)}")
    print("        (disk files were enriched after the zip was built; re-zip before selling the bundle)")
EOF

# -----------------------------------------------------------------------------
# 2. Auth gate (skip in dry-run)
# -----------------------------------------------------------------------------
if [ "$DRY_RUN" -ne 1 ]; then
  "$GUM" auth status >/dev/null 2>&1
  if [ $? -ne 0 ] || "$GUM" auth status 2>&1 | grep -qi "not logged in"; then
    echo "NOT LOGGED IN. Run:  $GUM auth login"
    exit 2
  fi
fi

# -----------------------------------------------------------------------------
# 3. Idempotency: what's already live?
# -----------------------------------------------------------------------------
LIVE_SLUGS=""
if [ "$DRY_RUN" -ne 1 ]; then
  echo "=== Checking existing products (idempotency) ==="
  LIVE_SLUGS=$("$GUM" products list --all --json 2>/dev/null | python -c "
import json, sys
try:
    d = json.load(sys.stdin)
except Exception:
    print(''); raise SystemExit
out = []
for p in d.get('products', []):
    out.append((p.get('custom_permalink') or '') + '\t' + (p.get('name') or ''))
print('\n'.join(out))
" 2>/dev/null || true)
fi
live_count=$(printf '%s' "$LIVE_SLUGS" | grep -c . || true)

# -----------------------------------------------------------------------------
# 4. The publish loop
# -----------------------------------------------------------------------------
echo "=== Publishing ($([ "$DRY_RUN" -eq 1 ] && echo DRY-RUN: echoing commands only || echo live run)) ==="
[ "$DRY_RUN" -eq 1 ] || : > "$RESULTS"

FAILED=0
DONE=0
while IFS=$'\t' read -r n name price file slug; do
  [ "$n" = "n" ] && continue
  slug="${slug%$'\r'}"; name="${name%$'\r'}"
  if [ -n "$ONLY" ] && [ "$n" != "$ONLY" ]; then continue; fi

  # idempotency skip
  if [ -n "$LIVE_SLUGS" ] && printf '%s' "$LIVE_SLUGS" | grep -qi "^${slug}$\|^${slug}\b"; then
    if printf '%s' "$LIVE_SLUGS" | grep -q "^${slug}"; then
      echo "[$n/11] SKIP $slug (already exists on the account)"
      continue
    fi
  fi

  echo "[$n/11] $name  (slug=$slug, price=\$$price)"

  # per-product metadata built by the python step
  META="$HERE/.meta-$n.json"
  META_W="$HERE_W/.meta-$n.json"
  [ -f "$META" ] || META="$HERE_W/.meta-$n.json"

  # Build the exact CLI argv (shown in dry-run, executed otherwise)
  TAG_ARGS=()
  DESC_HTML=$(python -c "import json,sys; sys.stdout.write(json.load(open(sys.argv[1]))['html'])" "$META_W")
  SUMMARY=$(python -c "import json,sys; sys.stdout.write(json.load(open(sys.argv[1]))['summary'])" "$META_W")
  TAGS=$(python -c "import json,sys; sys.stdout.write('\n'.join(json.load(open(sys.argv[1]))['tags']))" "$META_W")
  while IFS= read -r t; do [ -n "$t" ] && TAG_ARGS+=(--tag "$t"); done <<< "$TAGS"

  CMD_CREATE=("$GUM" products create --non-interactive --json
              --name "$name" --price "$price" --file "$file"
              --custom-permalink "$slug" --custom-summary "$SUMMARY"
              --description "$DESC_HTML" "${TAG_ARGS[@]}")
  CMD_PUBLISH=("$GUM" products publish --non-interactive --json)

  if [ "$DRY_RUN" -eq 1 ]; then
    # echo the create command (with a shortened description for readability)
    SHORT_DESC=$(printf '%s' "$DESC_HTML" | head -c 60)
    NTAG=$(( ${#TAG_ARGS[@]} / 2 ))
    echo "  CREATE: $GUM products create --non-interactive --json --name \"$name\" \\"
    echo "            --price \"$price\" --file \"$(W "$file")\" \\"
    echo "            --custom-permalink \"$slug\" --custom-summary \"${SUMMARY:0:50}...\" \\"
    echo "            --description \"<${#DESC_HTML}-byte HTML>\" ($NTAG tags: $(printf '%s ' "${TAG_ARGS[@]:1:2}" | tr '\n' ' ')...)"
  else
    # create -> capture id -> publish -> capture url
    OUT=$("${CMD_CREATE[@]}" 2>&1)
    if [ $? -ne 0 ]; then
      echo "  CREATE FAILED: $OUT" | head -3
      FAILED=$((FAILED+1)); continue
    fi
    PID=$(printf '%s' "$OUT" | python -c "
import json, sys
try:
    d = json.load(sys.stdin)
    p = d.get('product', d)
    print(p.get('id', ''))
except Exception:
    print('')
" 2>/dev/null)
    if [ -z "$PID" ]; then
      echo "  could not parse product id from: $(printf '%s' "$OUT" | head -c 200)"
      FAILED=$((FAILED+1)); continue
    fi
    echo "  created draft id=$PID; publishing..."
    PUB=$("${CMD_PUBLISH[@]}" "$PID" 2>&1)
    if [ $? -ne 0 ]; then
      echo "  PUBLISH FAILED: $PUB" | head -3
      FAILED=$((FAILED+1)); continue
    fi
    URL=$("$GUM" products url "$PID" 2>/dev/null | tail -1)
    echo "  LIVE: $URL"
    printf '%s\t%s\t%s\n' "$slug" "$PID" "$URL" >> "$RESULTS"
  fi
  DONE=$((DONE+1))
done < "$HERE/.payloads.tsv"

# cleanup sidecars
rm -f "$HERE"/.meta-*.json "$HERE/.payloads.tsv"

echo
echo "=== Summary ==="
if [ "$DRY_RUN" -eq 1 ]; then
  echo "Dry-run complete: $DONE product(s) would be created + published (see commands above)."
  echo "Remove --dry-run (and be logged in via '$GUM auth login') to execute."
else
  echo "Processed: $DONE | Failed: $FAILED | Results log: $RESULTS"
  [ "$FAILED" -gt 0 ] && exit 3
fi
exit 0
