#!/usr/bin/env python3
"""
Gumroad bulk publisher — REST API path (https://api.gumroad.com/v2).

Creates and publishes all 11 products defined in scripts/gumroad-product-payloads.json
(cross-checked against scripts/gumroad-all-products-ready.json).

AUTH
    The API token is read from the GUMROAD_API_TOKEN environment variable.
    It is NEVER hardcoded. Generate one at:
        https://gumroad.com/settings/developers
        (Settings -> Advanced -> Applications -> "Generate access token";
         pick scopes: edit_products, or the full "account" scope)
    Then export it:
        bash:   export GUMROAD_API_TOKEN=<token>
        cmd:    set GUMROAD_API_TOKEN=<token>

PER-PRODUCT FLOW (verified against https://gumroad.com/api):
    0. Idempotency: GET /products?scope=mine lists products already on the
       account. A payload whose url_slug (or exact name) already exists is
       SKIPPED; if it exists but is an unpublished draft left by a partial
       run, it is enabled (PUT /products/{id}/enable) so the run converges.
    1. File upload (S3 multipart "workflow_file" flow — 4 steps):
         a. POST /files/presign        -> upload_id, key, file_url, parts[]
         b. PUT  parts[i].presigned_url -> raw bytes; capture ETag header
         c. POST /files/complete       -> canonical file_url
            (single-use: NEVER retry /files/complete; restart at /files/presign.
             On failure: POST /files/abort with upload_id + key.)
    2. POST /products — creates a DRAFT (published: false) with:
       name, price (CENTS, e.g. 999 = $9.99), native_type=digital,
       and the uploaded file attached as files[][url].
    3. PUT /products/{id} — sets description (HTML), custom_permalink
       (URL slug; retried with -v2 / -pack / -v3 suffixes if the globally
       taken slug is rejected), custom_summary, tags, price (cents),
       category (best-effort, only if it resolves via GET /v2/categories).
    4. PUT /products/{id}/enable — flips published to true (POST /products
       always creates drafts, so this publish step is mandatory).
    5. Prints the live URL (product.short_url from the API response).

USAGE
    python scripts/publish-now/publish-via-api.py --check     # offline dry-run (no token, no network)
    python scripts/publish-now/publish-via-api.py             # publish all 11
    python scripts/publish-now/publish-via-api.py --only 11   # just the bundle
    python scripts/publish-now/publish-via-api.py --start-from 8
    python scripts/publish-now/publish-via-api.py --force     # re-push metadata even if product exists

Exit codes: 0 = ok, 1 = validation error or one or more products failed.
"""

import argparse
import json
import math
import os
import re
import sys
import time
from pathlib import Path

try:
    import requests
except ImportError:  # pragma: no cover
    sys.stderr.write(
        "ERROR: the 'requests' package is required. Install with: pip install requests\n"
    )
    sys.exit(1)

# ---------------------------------------------------------------------------
# Paths / constants
# ---------------------------------------------------------------------------

HERE = Path(__file__).resolve().parent          # scripts/publish-now/
REPO = HERE.parent.parent                       # ai-prompt-store/ (repo root)
PAYLOADS_FILE = REPO / "scripts" / "gumroad-product-payloads.json"
READY_FILE = REPO / "scripts" / "gumroad-all-products-ready.json"

API_BASE = "https://api.gumroad.com/v2"
EXPECTED_PRICE_CENTS = {"pack": 999, "bundle": 2799}   # $9.99 packs, $27.99 bundle
BUNDLE_SLUG = "complete-ai-prompt-bundle"
BUNDLE_FILE_REL = "products/bundle-all-10-packs.zip"

# Slug suffixes tried when a globally-taken custom_permalink is rejected.
# Gumroad slugs are GLOBAL (another seller may own yours) -> retry with these.
SLUG_SUFFIXES = ["", "-v2", "-pack", "-v3", "-v4", "-v5"]

SLUG_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


class ApiError(Exception):
    def __init__(self, status, message):
        super().__init__(f"HTTP {status}: {message}")
        self.status = status
        self.message = message or ""


# ---------------------------------------------------------------------------
# Payload loading / validation
# ---------------------------------------------------------------------------

def _normalize_file_ref(raw):
    """Normalize a file reference to a repo-relative 'products/...' path."""
    raw = str(raw).strip().replace("\\", "/")
    m = re.search(r"(products/.+)$", raw)
    return m.group(1) if m else raw


def _is_placeholder_file_ref(raw):
    """True when file_upload_path is prose/a glob, not a real path
    (e.g. the bundle entry: 'All products/prompt-pack-*/prompts.md combined into one ZIP')."""
    raw = str(raw).strip()
    if not raw:
        return True
    return "*" in raw or not raw.lower().endswith((".md", ".zip", ".pdf", ".txt", ".epub"))


def load_payloads():
    """Load the 11 payloads; merge in file paths from the 'ready' JSON as fallback."""
    if not PAYLOADS_FILE.is_file():
        raise FileNotFoundError(f"Payload file not found: {PAYLOADS_FILE}")
    products = json.loads(PAYLOADS_FILE.read_text(encoding="utf-8"))
    if not isinstance(products, list) or not products:
        raise ValueError(f"No products in {PAYLOADS_FILE}")

    ready_by_name = {}
    if READY_FILE.is_file():
        for entry in json.loads(READY_FILE.read_text(encoding="utf-8")):
            if isinstance(entry, dict) and entry.get("name"):
                ready_by_name[entry["name"]] = entry

    for p in products:
        # Resolve the on-disk file for this product:
        #   1. payload's file_upload_path, if it is a real path
        #   2. the matching entry's file_path in gumroad-all-products-ready.json
        #   3. explicit remap for the bundle (its payload path is placeholder prose)
        raw = p.get("file_upload_path", "") or ""
        rel = None
        if not _is_placeholder_file_ref(raw):
            rel = _normalize_file_ref(raw)
        else:
            ready = ready_by_name.get(p.get("name", ""), {})
            if ready.get("file_path"):
                rel = _normalize_file_ref(ready["file_path"])
            if p.get("url_slug") == BUNDLE_SLUG or "bundle" in (p.get("name", "") or "").lower():
                rel = BUNDLE_FILE_REL  # explicit, known-good bundle path
        p["_file_rel"] = rel
        p["_file_abs"] = (REPO / rel).resolve() if rel else None
        p["_source_raw_file_ref"] = raw
        # Cross-check fields against the 'ready' JSON when available.
        p["_ready_match"] = ready_by_name.get(p.get("name", ""))
    return products


def description_to_html(text):
    """Convert the plain-text/markdown-ish payload description to the HTML
    the API's `description` (HTML) and the TipTap editor expect."""
    def esc(s):
        return (
            s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        )

    def inline(s):
        s = esc(s)
        s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
        return s

    blocks = [b.strip() for b in re.split(r"\n\s*\n", text or "") if b.strip()]
    out = []
    bullet_re = re.compile(r"^[-*\u2022]\s+(.*)$")
    for b in blocks:
        lines = [l.strip() for l in b.splitlines() if l.strip()]
        if lines and all(bullet_re.match(l) for l in lines):
            items = "".join(
                f"<li>{inline(bullet_re.match(l).group(1))}</li>" for l in lines
            )
            out.append(f"<ul>{items}</ul>")
        else:
            out.append("<p>" + "<br>".join(inline(l) for l in lines) + "</p>")
    return "\n".join(out) if out else "<p></p>"


def summary_from_description(text, limit=220):
    """custom_summary = first paragraph, plain text, trimmed."""
    text = re.sub(r"\*\*(.+?)\*\*", r"\1", text or "")
    first = re.split(r"\n\s*\n", text.strip())[0].strip() if text.strip() else ""
    first = " ".join(first.split())
    if len(first) > limit:
        cut = first[:limit]
        first = cut.rsplit(" ", 1)[0] + "..."
    return first


def validate(products):
    """Return (rows, blocking_issues, warnings) for the --check dry-run."""
    rows, blocking, warnings = [], [], []
    seen_slugs = {}

    for i, p in enumerate(products, start=1):
        name = p.get("name", "")
        slug = p.get("url_slug", "")
        price = p.get("price")
        is_bundle = (slug == BUNDLE_SLUG) or "bundle" in name.lower()
        expected = EXPECTED_PRICE_CENTS["bundle"] if is_bundle else EXPECTED_PRICE_CENTS["pack"]
        checks, notes = [], []

        # --- required fields ---
        if not name:
            blocking.append(f"#{i}: missing 'name'")
            checks.append("NAME:MISSING")
        if not slug:
            blocking.append(f"#{i} ({name}): missing 'url_slug'")
            checks.append("SLUG:MISSING")
        elif not SLUG_RE.match(slug):
            blocking.append(f"#{i}: url_slug '{slug}' is not lowercase alphanumeric+hyphens")
            checks.append("SLUG:BAD_FORMAT")
        elif slug in seen_slugs:
            blocking.append(f"#{i}: duplicate url_slug '{slug}' (also #{seen_slugs[slug]})")
            checks.append("SLUG:DUPLICATE")
        else:
            seen_slugs[slug] = i
            checks.append("slug:ok")

        # --- price: payload dollars -> API cents must equal expected ---
        if not isinstance(price, (int, float)):
            blocking.append(f"#{i} ({name}): price missing/not numeric")
            checks.append("PRICE:MISSING")
        else:
            cents = int(round(price * 100))
            if cents != expected:
                blocking.append(
                    f"#{i} ({name}): price ${price} -> {cents}c but expected "
                    f"${expected / 100:.2f} ({expected}c)"
                )
                checks.append(f"price:MISMATCH({cents}c!={expected}c)")
            else:
                checks.append(f"price:ok({cents}c)")

        # --- description ---
        desc = p.get("description", "") or ""
        # The bundle's description ends with an internal note ("**Files to upload:** ...")
        # that must not reach the buyer-facing page — strip it.
        internal_note = "Files to upload"
        if internal_note in desc and is_bundle:
            desc = desc.split(internal_note, 1)[0].rstrip().rstrip(",")
            p["_stripped_internal_note"] = True
        if len(desc) < 80:
            warnings.append(f"#{i} ({name}): description is very short ({len(desc)} chars)")
            checks.append("desc:SHORT")
        else:
            checks.append(f"desc:ok({len(desc)}ch)")

        # --- file on disk ---
        raw = p.get("_source_raw_file_ref", "")
        if p.get("_file_abs") and p["_file_abs"].is_file():
            size = p["_file_abs"].stat().st_size
            if size <= 0:
                blocking.append(f"#{i} ({name}): file exists but is empty: {p['_file_abs']}")
                checks.append("file:EMPTY")
            else:
                remapped = _is_placeholder_file_ref(raw) or str(raw).strip() != p["_file_rel"]
                tag = "file:ok" + ("(REMAPPED)" if remapped else "")
                if remapped:
                    warnings.append(
                        f"#{i} ({name}): file_upload_path in payloads JSON is placeholder "
                        f"prose ({raw!r}); remapped to {p['_file_rel']}"
                    )
                checks.append(f"{tag}({size}B)")
        else:
            blocking.append(f"#{i} ({name}): product file not found: {p.get('_file_rel')}")
            checks.append("file:MISSING")

        # --- zip sanity for the bundle ---
        if is_bundle and p.get("_file_abs") and p["_file_abs"].is_file():
            try:
                import zipfile
                with zipfile.ZipFile(p["_file_abs"]) as z:
                    n = len(z.namelist())
                    bad = z.testzip()
                checks.append(f"zip:ok({n} entries)" if bad is None else "zip:CORRUPT")
                if bad is not None:
                    blocking.append(f"#{i}: corrupt entry in bundle zip: {bad}")
                # Stale-zip guard: compare each bundled prompts.md against the
                # live file on disk so buyers don't get outdated copies.
                import zipfile as _zf
                with _zf.ZipFile(p["_file_abs"]) as z:
                    for zi in z.infolist():
                        rel = zi.filename.replace("\\", "/")
                        m = re.match(r"(products/)?(prompt-pack-\d+)/prompts\.md$", rel)
                        if not m:
                            continue
                        pack_dir = m.group(2)
                        disk_file = REPO / "products" / pack_dir / "prompts.md"
                        if not disk_file.is_file():
                            continue
                        zip_bytes = z.read(zi)
                        disk_bytes = disk_file.read_bytes()
                        if zip_bytes != disk_bytes:
                            checks.append(f"zip:STALE({pack_dir})")
                            warnings.append(
                                f"#{i}: {pack_dir}/prompts.md inside the bundle zip "
                                f"({len(zip_bytes)}B) is out of date vs disk "
                                f"({len(disk_bytes)}B) — re-zip before selling the bundle"
                            )
            except Exception as e:  # pragma: no cover
                warnings.append(f"#{i}: could not inspect bundle zip: {e}")

        # --- tags (comma string in JSON -> array for API) ---
        tags = [t.strip() for t in str(p.get("tags", "")).split(",") if t.strip()]
        checks.append(f"tags:ok({len(tags)})")

        # --- category is display-style, not an API path -> best-effort ---
        cat = p.get("category", "")
        if cat:
            warnings.append(
                f"#{i} ({name}): category {cat!r} is a display label, not an API "
                f"category path (like 'design/ui-and-web/figma' from GET /v2/categories); "
                f"script resolves it best-effort at publish time, else omits it"
            )
            checks.append("category:WARN(resolve-at-runtime)")
        else:
            checks.append("category:none")

        # --- original_price: no API param for strikethrough price ---
        if p.get("original_price"):
            warnings.append(
                f"#{i} ({name}): original_price {p.get('original_price')} has no direct "
                f"API parameter (strikethrough comparison price); set in the dashboard "
                f"if wanted — it is cosmetic"
            )

        # --- is_published in the payload is handled by PUT /products/{id}/enable ---
        if p.get("is_published"):
            notes.append("POST /products creates drafts; script publishes via PUT /products/{id}/enable")

        # --- cross-check with gumroad-all-products-ready.json ---
        # (compare against the ORIGINAL description, before the internal-note strip)
        orig_desc = p.get("description", "") or ""
        ready = p.get("_ready_match")
        if ready:
            mism = []
            if ready.get("price") is not None and int(round(float(ready["price"]) * 100)) != int(round(float(price or 0) * 100)):
                mism.append(f"price {ready['price']} vs {price}")
            if (ready.get("description") or "").strip() != orig_desc.strip():
                mism.append("description text differs")
            if mism:
                warnings.append(f"#{i} ({name}): payloads JSON vs ready JSON mismatch: " + "; ".join(mism))
                checks.append("xfile:MISMATCH")
            else:
                checks.append("xcheck:ok")
        else:
            warnings.append(f"#{i} ({name}): no matching entry in gumroad-all-products-ready.json")
            checks.append("xcheck:NO_ENTRY")

        rows.append(
            {
                "n": i,
                "name": name,
                "slug": slug,
                "price": price,
                "expected": expected / 100,
                "file": p.get("_file_rel") or "-",
                "size": (p["_file_abs"].stat().st_size if p.get("_file_abs") and p["_file_abs"].is_file() else None),
                "checks": checks,
            }
        )
    return rows, blocking, warnings


def print_check_table(rows, warnings, blocking):
    print("=" * 118)
    print("GUMROAD PUBLISH DRY-RUN (--check) — no network calls, no token needed")
    print("=" * 118)
    hdr = f"{'#':>2}  {'slug':<30} {'price':>6} {'file':<34} {'size':>8}  checks"
    print(hdr)
    print("-" * len(hdr))
    for r in rows:
        size = f"{r['size']}B" if r["size"] is not None else "N/A"
        checks = ", ".join(r["checks"])
        bad = [c for c in r["checks"] if "MISSING" in c or "MISMATCH" in c or "DUPLICATE" in c or "BAD" in c or "EMPTY" in c or "CORRUPT" in c]
        price_str = f"${r['price']:.2f}" if isinstance(r["price"], (int, float)) else str(r["price"])
        flag = "FAIL " if bad else "OK   "
        print(f"{flag}{r['n']:>2}  {r['slug']:<30} {price_str:>6} {r['file']:<34} {size:>8}")
        print(f"     {'':2}  {checks}")
    print("-" * len(hdr))
    print(f"Products validated : {len(rows)} (expected 11)")
    print(f"Files on disk       : {sum(1 for r in rows if r['size'] is not None)}/{len(rows)} present")
    total = sum(r["size"] or 0 for r in rows)
    print(f"Total upload size   : {total} bytes ({total / 1024:.1f} KB)")

    if warnings:
        print(f"\nWARNINGS ({len(warnings)}):")
        for w in warnings:
            print(f"  - {w}")
    if blocking:
        print(f"\nBLOCKING ISSUES ({len(blocking)}):")
        for b in blocking:
            print(f"  ! {b}")
        print("\nRESULT: FAIL — fix the issues above before publishing.")
    else:
        print("\nRESULT: PASS — all 11 payloads validated; files present; safe to publish.")
        print("Next: set GUMROAD_API_TOKEN (https://gumroad.com/settings/developers) and re-run without --check.")
    return 1 if blocking else 0


# ---------------------------------------------------------------------------
# API client
# ---------------------------------------------------------------------------

def get_token():
    tok = (os.environ.get("GUMROAD_API_TOKEN") or "").strip()
    if not tok:
        sys.stderr.write(
            "ERROR: GUMROAD_API_TOKEN is not set.\n"
            "Generate a token at https://gumroad.com/settings/developers "
            "(Settings -> Advanced -> Applications -> Generate access token;\n"
            "scopes: edit_products or account), then:\n"
            "  bash: export GUMROAD_API_TOKEN=<token>\n"
            "  cmd : set GUMROAD_API_TOKEN=<token>\n"
            "(--check mode works without a token.)\n"
        )
        sys.exit(2)
    return tok


def api(token, method, path, data=None, params=None, timeout=90):
    """Call the Gumroad v2 API. Auth: Bearer header + access_token form/query param."""
    url = f"{API_BASE}{path}"
    headers = {"Authorization": f"Bearer {token}"}
    kwargs = {"headers": headers, "timeout": timeout}
    if data is not None:
        # form-encoded body (list of tuples preserves order for parts[][...] etc.)
        items = list(data.items()) if isinstance(data, dict) else list(data)
        items.append(("access_token", token))
        kwargs["data"] = items
    else:
        q = dict(params or {})
        q["access_token"] = token
        kwargs["params"] = q

    for attempt in range(4):
        try:
            resp = requests.request(method, url, **kwargs)
        except requests.RequestException as e:
            if attempt == 3:
                raise ApiError(0, f"network error: {e}")
            time.sleep(2 ** attempt)
            continue
        if resp.status_code == 429:  # rate limited — back off and retry
            time.sleep(5 * (attempt + 1))
            continue
        break

    try:
        body = resp.json()
    except ValueError:
        body = {"raw": resp.text[:500]}
    if not resp.ok:
        raise ApiError(resp.status_code, body.get("message") or body.get("raw") or resp.text[:300])
    return body


def list_existing_products(token):
    """GET /products?scope=mine — every product on the account (paginated).
    Falls back to GET /products if the scope param is rejected."""
    products, page_key, first = [], None, True
    while True:
        params = {"scope": "mine"}
        if page_key:
            params["page_key"] = page_key
        try:
            body = api(token, "GET", "/products", params=params)
        except ApiError:
            if first:
                body = api(token, "GET", "/products", params={"page_key": page_key} if page_key else {})
            else:
                raise
        first = False
        products.extend(body.get("products", []))
        page_key = body.get("next_page_key")
        if not page_key or len(products) > 500:
            break
    return products


def upload_file(token, file_path):
    """workflow_file S3 multipart flow: presign -> PUT parts -> complete.
    Returns the canonical file_url to attach via files[][url]."""
    size = file_path.stat().st_size
    # Step 1: presign
    body = api(token, "POST", "/files/presign",
               data={"filename": file_path.name, "file_size": size})
    upload_id = body["upload_id"]
    key = body["key"]
    parts = body.get("parts", [])
    if not parts:
        raise ApiError(500, "presign returned no parts")

    # Step 2: PUT each part's bytes to its presigned URL (no auth headers),
    #         capturing the ETag response header per part.
    part_size = max(1, math.ceil(size / len(parts)))
    etags = []
    with open(file_path, "rb") as fh:
        for part in parts:
            pn = part["part_number"]
            fh.seek((pn - 1) * part_size)
            chunk = fh.read(part_size)
            r = requests.put(part["presigned_url"], data=chunk, timeout=600)
            if r.status_code not in (200, 201):
                _abort_quietly(token, upload_id, key)
                raise ApiError(r.status_code, f"part {pn} upload failed: {r.text[:200]}")
            etag = r.headers.get("ETag")
            if not etag:
                _abort_quietly(token, upload_id, key)
                raise ApiError(500, f"part {pn} returned no ETag header")
            etags.append(("parts[][part_number]", str(pn)))
            etags.append(("parts[][etag]", etag))

    # Step 3: complete — SINGLE-USE: never retry this call on failure;
    # restart the whole flow with a fresh /files/presign instead.
    try:
        done = api(token, "POST", "/files/complete", data=etags)
    except Exception:
        _abort_quietly(token, upload_id, key)
        raise
    return done["file_url"]


def _abort_quietly(token, upload_id, key):
    """POST /files/abort — loop while status == 'accepted', stop on 'already_gone'."""
    for _ in range(5):
        try:
            body = api(token, "POST", "/files/abort",
                       data={"upload_id": upload_id, "key": key})
            if body.get("status") == "already_gone":
                return
        except Exception:
            return
        time.sleep(2)


def resolve_category(token, label, cache={}):
    """Map the payload's display-style category ('Education / Productivity')
    to an API category path from GET /v2/categories. Best-effort; returns
    None when nothing matches (category is optional)."""
    if "tree" not in cache:
        try:
            cache["tree"] = api(token, "GET", "/categories").get("categories", [])
        except Exception:
            cache["tree"] = []

    def walk(nodes, trail):
        for node in nodes or []:
            path = "/".join(trail + [str(node.get("name", "")).lower().replace(" ", "-")])
            yield path, node
            yield from walk(node.get("children") or node.get("sub_categories") or [], trail + [str(node.get("name", ""))])

    words = {w.strip().lower() for w in re.split(r"[/,]", label or "") if w.strip()}
    best = None
    for path, node in walk(cache["tree"], []):
        segs = [s for s in path.split("/") if s]
        if segs and any(w in segs[-1] or segs[-1] in w for w in words):
            best = best or path
    return best


def slug_retry(token, product_id, desired_slug, update_payload_fn):
    """PUT /products/{id} with custom_permalink=desired_slug; if the global slug
    is taken, retry with -v2/-pack/-v3... suffixes. Returns the accepted slug."""
    last_err = None
    for suffix in SLUG_SUFFIXES:
        candidate = desired_slug + suffix
        try:
            update_payload_fn(candidate)
            return candidate
        except ApiError as e:
            last_err = e
            msg = (e.message or "").lower()
            if any(k in msg for k in ("url", "permalink", "slug", "taken", "in use", "already")):
                print(f"    slug '{candidate}' taken globally, retrying...")
                continue
            raise
    raise ApiError(last_err.status if last_err else 0,
                   f"all slug candidates rejected for '{desired_slug}': {last_err}")


def publish_one(token, payload, existing, force=False):
    """Create + update + enable one product. Returns dict with status/url."""
    name = payload["name"]
    slug = payload["url_slug"]
    cents = int(round(float(payload["price"]) * 100))
    file_abs = payload["_file_abs"]
    desc = payload.get("description", "") or ""
    # Strip the internal "Files to upload" note so it never reaches the product page.
    if "Files to upload" in desc:
        desc = desc.split("Files to upload", 1)[0].rstrip().rstrip(",")
    desc_html = description_to_html(desc)
    summary = summary_from_description(desc)
    tags = [t.strip() for t in str(payload.get("tags", "")).split(",") if t.strip()]

    # ---- Step 0: idempotency — already on the account? ----
    match = next(
        (p for p in existing
         if (p.get("custom_permalink") or "") == slug
         or p.get("name", "").strip() == name.strip()),
        None,
    )
    if match and not force:
        if match.get("published"):
            print(f"  SKIP (already published): {match.get('short_url')}")
            return {"slug": slug, "status": "skipped", "url": match.get("short_url")}
        # draft left by a partial run -> publish it so the run converges
        api(token, "PUT", f"/products/{match['id']}/enable")
        print(f"  SKIP (existed as draft, now enabled): {match.get('short_url')}")
        return {"slug": slug, "status": "enabled-existing", "url": match.get("short_url")}

    # ---- Step 1: upload the product file (presign -> PUT -> complete) ----
    print(f"  uploading file: {file_abs.name} ({file_abs.stat().st_size} bytes)")
    file_url = upload_file(token, file_abs)

    # ---- Step 2: POST /products — draft with name/price/file ----
    print(f"  POST /products (draft) ...")
    created = api(token, "POST", "/products", data=[
        ("name", name),
        ("price", cents),                       # CENTS: 999 = $9.99, 2799 = $27.99
        ("native_type", "digital"),             # immutable after creation
        ("price_currency_type", "usd"),
        ("files[][url]", file_url),
    ])["product"]
    pid = created["id"]
    print(f"  created draft id={pid}")

    # ---- Step 3: PUT /products/{id} — description/summary/tags/category/slug ----
    category = resolve_category(token, payload.get("category", ""))
    if category:
        print(f"  category resolved: {category}")

    def do_update(candidate_slug):
        data = [
            ("description", desc_html),          # HTML
            ("custom_summary", summary),
            ("price", cents),                    # cents again (idempotent metadata push)
        ]
        data += [("tags[]", t) for t in tags]
        if category:
            data.append(("category", category))
        data.append(("custom_permalink", candidate_slug))  # the URL slug
        api(token, "PUT", f"/products/{pid}", data=data)

    accepted_slug = slug_retry(token, pid, slug, do_update)
    if accepted_slug != slug:
        print(f"  NOTE: slug taken; live slug is '{accepted_slug}'")
    print(f"  PUT /products/{pid} done (slug={accepted_slug})")

    # ---- Step 4: PUT /products/{id}/enable — publish ----
    api(token, "PUT", f"/products/{pid}/enable")
    final = api(token, "GET", f"/products/{pid}")["product"]
    if not final.get("published"):
        raise ApiError(409, f"enable returned success but published is still false for {pid}")
    url = final.get("short_url") or f"https://abhishekanand31.gumroad.com/l/{accepted_slug}"
    return {"slug": accepted_slug, "status": "published", "url": url, "id": pid}


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser(description="Publish all 11 products to Gumroad via the v2 REST API.")
    ap.add_argument("--check", action="store_true",
                    help="offline dry-run: validate payloads + files, print a table, touch nothing")
    ap.add_argument("--only", type=int, metavar="N", help="publish only product #N (1-based)")
    ap.add_argument("--start-from", type=int, metavar="N", help="skip products before #N (1-based)")
    ap.add_argument("--force", action="store_true",
                    help="re-push metadata even if the product already exists")
    args = ap.parse_args()

    try:
        products = load_payloads()
    except Exception as e:
        print(f"ERROR loading payloads: {e}")
        return 1

    if args.check:
        rows, blocking, warnings = validate(products)
        return print_check_table(rows, warnings, blocking)

    if len(products) != 11:
        print(f"WARNING: expected 11 payloads, found {len(products)}")

    token = get_token()
    start = args.start_from or 1
    results, failed = [], []

    # Idempotency: what already exists on the account?
    existing = list_existing_products(token)
    print(f"Account already has {len(existing)} product(s); their slugs: "
          f"{[p.get('custom_permalink') for p in existing]}")

    for i, p in enumerate(products, start=1):
        if i < start:
            continue
        if args.only and i != args.only:
            continue
        print(f"\n[{i}/{len(products)}] {p['name']}")
        try:
            res = publish_one(token, p, existing, force=args.force)
            results.append(res)
            print(f"  LIVE: {res['url']}")
            existing.append({"id": res.get("id", ""), "custom_permalink": res["slug"],
                             "name": p["name"], "published": True,
                             "short_url": res["url"]})
        except ApiError as e:
            failed.append((i, p["name"], str(e)))
            print(f"  FAILED: {e}")

    # Persist results so a re-run can resume / the parent agent can read them.
    out = HERE / "publish-results.json"
    out.write_text(json.dumps(results, indent=2), encoding="utf-8")

    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    for r in results:
        print(f"  {r['status']:<18} {r['slug']:<30} {r['url']}")
    print(f"\nResults written to {out}")
    if failed:
        print(f"\nFAILED ({len(failed)}):")
        for i, name, err in failed:
            print(f"  #{i} {name}: {err}")
        print("Re-run — already-published products are skipped automatically.")
        return 1
    print(f"\nDone: {len(results)} processed, {len(failed)} failed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
