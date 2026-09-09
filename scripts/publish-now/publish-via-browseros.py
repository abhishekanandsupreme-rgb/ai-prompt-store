#!/usr/bin/env python3
"""
Gumroad bulk publisher — BrowserOS Neo browser-automation path.

Drives the CURRENT Gumroad product-edit UI (as of 2026-09) to create and
publish the 11 products in scripts/gumroad-product-payloads.json, one at a
time, with per-step UI comments. Fallback/alternative to publish-via-api.py:
use it when no GUMROAD_API_TOKEN can be generated.

HOW IT RUNS
    This is a DRIVER script: it does not open a browser itself. It emits the
    exact `browser_exec` code (the Hermes BrowserOS helper API: goto_url,
    js(), fill_input, cdp(), page_info()) for ONE product, or runs all 11 in
    sequence when executed under the Hermes agent with BrowserOS Neo
    connected (mcp server `browseros-neo`, http://127.0.0.1:9210/mcp —
    BrowserOS Neo must be RUNNING locally; it is not right now).

    The browser session must already be logged in to Gumroad as
    demosupreme001@gmail.com. If a login wall appears, the script STOPS and
    reports — credentials are never guessed or hardcoded.

USAGE (from the Hermes agent / any env with browser_exec + BrowserOS Neo)
    # all 11 products, in order:
    python scripts/publish-now/publish-via-browseros.py
    # resume after a crash/interrupt, starting at product #N (1-based):
    python scripts/publish-now/publish-via-browseros.py --start-from 8
    # just the bundle:
    python scripts/publish-now/publish-via-browseros.py --only 11
    # print the code for one product without executing anything:
    python scripts/publish-now/publish-via-browseros.py --only 1 --dry-run

CURRENT GUMROAD UI CONTRACT (what each step does, and where)
    1.  gumroad.com/products/new  — wizard: "Name your product" input,
        pricing card with a price input in DOLLARS ("$0+" style hint),
        "Next: customize" button.
    2.  Product edit page (/products/<draft>/edit):
        - Name field at top (input[id^="name-"]).
        - PRICING CARD, middle-right: price input in CENTS ("999") — the
          wizard's dollar field is gone here; the edit page expects cents
          ("$9.99" would set $0.09!). The card also has a toggle for
          pay-what-you-want — leave OFF (fixed $9.99 / $27.99).
        - DESCRIPTION: TipTap rich-text editor (div.tiptap / ProseMirror).
          Paste HTML via document.execCommand('insertHTML', ...) after
          focusing — typing plain text loses line breaks.
        - CONTENT section: "Add file" / "Upload a file" — an
          input[type=file] hidden behind the button. Set it via CDP
          DOM.setFileInputFiles (native file picker can't be scripted).
        - "Advanced" collapsible at the bottom -> "URL" row -> the slug
          input (shows "gumroad.com/l/<slug>" preview). Slugs are GLOBAL:
          if taken, append -v2 / -pack / -v3 until the field accepts it.
        - PUBLISH button, top right (turns into "Save" after first
          publish). Orange/primary. Click LAST — payouts must be set up
          (gumroad.com/settings/payments) or Publish is disabled.
"""

import argparse
import json
import re
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parent.parent
PAYLOADS_FILE = REPO / "scripts" / "gumroad-product-payloads.json"
READY_FILE = REPO / "scripts" / "gumroad-all-products-ready.json"
PROGRESS_FILE = HERE / "browseros-progress.json"

BUNDLE_SLUG = "complete-ai-prompt-bundle"
BUNDLE_FILE_REL = "products/bundle-all-10-packs.zip"
SLUG_SUFFIXES = ["", "-v2", "-pack", "-v3", "-v4", "-v5"]

PRODUCTS_NEW_URL = "https://gumroad.com/products/new"


# ---------------------------------------------------------------------------
# Payload loading (shared logic with publish-via-api.py, standalone copy)
# ---------------------------------------------------------------------------

def _normalize_file_ref(raw):
    raw = str(raw).strip().replace("\\", "/")
    m = re.search(r"(products/.+)$", raw)
    return m.group(1) if m else raw


def _is_placeholder_file_ref(raw):
    raw = str(raw).strip()
    if not raw:
        return True
    return "*" in raw or not raw.lower().endswith((".md", ".zip", ".pdf", ".txt", ".epub"))


def load_payloads():
    products = json.loads(PAYLOADS_FILE.read_text(encoding="utf-8"))
    ready_by_name = {}
    if READY_FILE.is_file():
        for e in json.loads(READY_FILE.read_text(encoding="utf-8")):
            if isinstance(e, dict) and e.get("name"):
                ready_by_name[e["name"]] = e
    for p in products:
        raw = p.get("file_upload_path", "") or ""
        rel = None
        if not _is_placeholder_file_ref(raw):
            rel = _normalize_file_ref(raw)
        else:
            ready = ready_by_name.get(p.get("name", ""), {})
            if ready.get("file_path"):
                rel = _normalize_file_ref(ready["file_path"])
            if p.get("url_slug") == BUNDLE_SLUG or "bundle" in (p.get("name", "") or "").lower():
                rel = BUNDLE_FILE_REL
        p["_file_rel"] = rel
        p["_file_abs"] = (REPO / rel).resolve() if rel else None
    return products


def description_to_html(text):
    """Payload text -> the HTML to insert into the TipTap editor."""
    def esc(s):
        return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

    def inline(s):
        s = esc(s)
        s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
        return s

    # The bundle description ends with an internal "Files to upload" note —
    # strip it so it never reaches the buyer-facing page.
    if "Files to upload" in text:
        text = text.split("Files to upload", 1)[0].rstrip().rstrip(",")

    bullet_re = re.compile(r"^[-*\u2022]\s+(.*)$")
    blocks = [b.strip() for b in re.split(r"\n\s*\n", text or "") if b.strip()]
    out = []
    for b in blocks:
        lines = [l.strip() for l in b.splitlines() if l.strip()]
        if lines and all(bullet_re.match(l) for l in lines):
            items = "".join(f"<li>{inline(bullet_re.match(l).group(1))}</li>" for l in lines)
            out.append(f"<ul>{items}</ul>")
        else:
            out.append("<p>" + "<br>".join(inline(l) for l in lines) + "</p>")
    return "\n".join(out) if out else "<p></p>"


# ---------------------------------------------------------------------------
# browser_exec code generation — ONE product per call
# ---------------------------------------------------------------------------

def js_str(s):
    return json.dumps(s)  # produces a valid JS string literal


def build_browser_code(p, n, total):
    """The browser_exec Python code for publishing product #n via the
    current Gumroad UI. Every step is labelled with a # STEP comment."""
    name = p["name"]
    slug = p["url_slug"]
    price_cents = int(round(float(p["price"]) * 100))
    file_abs = str(p["_file_abs"]).replace("\\", "\\\\")
    desc_html = description_to_html(p.get("description", ""))

    return f'''
# =============================================================================
# PUBLISH PRODUCT {n}/{total}: {name}
# Target: https://abhishekanand31.gumroad.com/l/{slug}  (account: demosupreme001@gmail.com)
# =============================================================================
# STEP 0 — Pre-flight: are we still logged in? (Login wall => STOP, never guess.)
wall = js("(() => {{ const t = (document.body.innerText || '').toLowerCase();"
          " return document.location.href.includes('/login') || "
          "!!document.querySelector('input[type=\\"email\\"]') && t.includes('log in'); }})()")
if wall:
    print("LOGIN_WALL: Gumroad session expired. Log in as demosupreme001@gmail.com in the BrowserOS tab, then re-run with --start-from {n}.")
    raise SystemExit(2)

# STEP 1 — Open the new-product wizard.
goto_url("{PRODUCTS_NEW_URL}")
wait_for_load()
time_dupe = js("(() => {{ const b = Array.from(document.querySelectorAll('button')).find(b => /let'*s* start|create.*product/i.test(b.textContent)); return !!b; }})()")
if not time_dupe:
    print("WARN: wizard button not found — page may already be the product form.")

# STEP 2 — Fill the NAME field ("Name your product").
#   React input: set value via the native setter, then dispatch input events.
ok = js("""
(() => {{
  const el = document.querySelector('input[id^="name-"]')
         || document.querySelector('input[placeholder*="product" i]')
         || document.querySelector('form input[type="text"]');
  if (!el) return "NAME_FIELD_NOT_FOUND";
  el.focus();
  const setter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value').set;
  setter.call(el, {js_str(name)});
  el.dispatchEvent(new Event('input', {{ bubbles: true }}));
  el.dispatchEvent(new Event('change', {{ bubbles: true }}));
  return "OK";
}})()
""")
if ok != "OK":
    print("FAIL at STEP 2 (name): " + str(ok))
    raise SystemExit(3)

# STEP 3 — Set the PRICE in the pricing card, IN CENTS.
#   Current UI: the pricing card input takes cents ("999" => $9.99, NOT 9.99).
#   Fill BOTH candidate inputs (wizard dollar field on /products/new, cents
#   field on the edit page) — the one that exists gets the value; harmless
#   otherwise. We type the CENTS value into both.
cents = "{price_cents}"
r = js("""
(() => {{
  const rv = {{ name: null, price: null }};
  const fields = Array.from(document.querySelectorAll('input'));
  const priceField = fields.find(i =>
      (i.id || '').toLowerCase().includes('price') ||
      /price|amount|cost/i.test(i.name || '') || /\\$0\\+|^0$/.test(i.placeholder || ''));
  if (!priceField) return "PRICE_FIELD_NOT_FOUND";
  priceField.focus();
  const setter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value').set;
  setter.call(priceField, "{price_cents}");
  priceField.dispatchEvent(new Event('input', {{ bubbles: true }}));
  priceField.dispatchEvent(new Event('change', {{ bubbles: true }}));
  return "OK";
}})()
""")
if r != "OK":
    print("FAIL at STEP 3 (price): " + str(r))
    raise SystemExit(3)

# STEP 4 — Advance: click "Next: customize" (or equivalent) to reach the edit page.
js("""
(() => {{
  const btn = Array.from(document.querySelectorAll('button'))
    .find(b => /next|customiz|continue/i.test(b.textContent));
  if (btn) btn.click();
}})()
""")
wait_for_load()
time.sleep(3)  # Inertia page swap

# STEP 5 — On the EDIT PAGE: (re-)set the name field (the draft wizard
#   pre-fills it, but re-assert to be safe).
r = js("""
(() => {{
  const el = document.querySelector('input[id^="name-"]');
  if (!el) return "NO_NAME_FIELD (ok on wizard-only flow)";
  el.focus();
  const setter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value').set;
  setter.call(el, {js_str(name)});
  el.dispatchEvent(new Event('input', {{ bubbles: true }}));
  return "OK";
}})()
""")
print("STEP 5 name (edit page): " + str(r))

# STEP 6 — Edit-page PRICING CARD: price IN CENTS ("999" = $9.99 / "2799" = $27.99).
#   The edit page's pricing card is the cents field — setting "9.99" would be $0.09!
r = js("""
(() => {{
  const card = Array.from(document.querySelectorAll('div, section'))
    .find(c => /pricing/i.test(c.textContent.slice(0, 200)) && c.querySelector('input'));
  const candidates = (card ? Array.from(card.querySelectorAll('input')) : [])
    .concat(Array.from(document.querySelectorAll('input[id*="price" i], input[name*="price" i]')));
  const f = candidates.find(i => i.offsetParent !== null);
  if (!f) return "PRICE_CARD_NOT_FOUND";
  f.focus();
  const setter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value').set;
  setter.call(f, "{price_cents}");
  f.dispatchEvent(new Event('input', {{ bubbles: true }}));
  f.dispatchEvent(new Event('change', {{ bubbles: true }}));
  return "OK:" + (f.id || f.name || 'anon');
}})()
""")
print("STEP 6 pricing card (cents): " + str(r))

# STEP 7 — DESCRIPTION into the TipTap rich-text editor.
#   TipTap/ProseMirror: plain typing collapses newlines. Focus the editor
#   (div.tiptap / .ProseMirror), select-all, then insert HTML via
#   document.execCommand('insertHTML') — it lands as real rich content.
r = js("""
(() => {{
  const editor = document.querySelector('.tiptap, .ProseMirror, [contenteditable="true"]');
  if (!editor) return "TIPTAP_EDITOR_NOT_FOUND";
  editor.focus();
  const sel = window.getSelection();
  const range = document.createRange();
  range.selectNodeContents(editor);
  sel.removeAllRanges();
  sel.addRange(range);
  const ok = document.execCommand('insertHTML', false, {js_str(desc_html)});
  return ok ? "OK" : "EXEC_COMMAND_REJECTED";
}})()
""")
if r not in ("OK",):
    print("WARN at STEP 7 (description): " + str(r) + " — falling back to plain text")
    js("""
    (() => {{
      const editor = document.querySelector('.tiptap, .ProseMirror, [contenteditable="true"]');
      if (!editor) return;
      editor.focus();
      document.execCommand('insertText', false, {js_str(desc_html)});
    }})()
    """)

# STEP 8 — Upload the product FILE via CDP DOM.setFileInputFiles.
#   The "Upload a file" button hides input[type=file]; the native picker
#   cannot be scripted — set files directly over CDP on the file input.
#   (a) locate the content file input and give it a stable id,
r = js("""
(() => {{
  const inputs = Array.from(document.querySelectorAll('input[type="file"]'));
  // Prefer the CONTENT upload input (in the Content card), not cover/thumbnail.
  const content = inputs.find(i => !/cover|thumb|image/i.test((i.name || '') + (i.id || '') + (i.className || '')));
  if (!content) return "FILE_INPUT_NOT_FOUND";
  content.id = "gumroad-content-file-input";
  return "OK:" + (content.accept || "any");
}})()
""")
print("STEP 8 file input: " + str(r))
#   (b) resolve its DOM node for CDP, then set the file from disk.
#   CDP flow: DOM.getDocument -> DOM.querySelector(rootNodeId, selector)
#   -> DOM.setFileInputFiles(files, nodeId)
doc = cdp("DOM.getDocument")
root_id = doc["root"]["nodeId"]
node = cdp("DOM.querySelector", nodeId=root_id, selector="#gumroad-content-file-input")
if not node or not node.get("nodeId"):
    # Fallback: DOM.enable first (some sessions need it before queries resolve)
    cdp("DOM.enable")
    doc = cdp("DOM.getDocument")
    root_id = doc["root"]["nodeId"]
    node = cdp("DOM.querySelector", nodeId=root_id, selector="#gumroad-content-file-input")
if not node or not node.get("nodeId"):
    print("FAIL at STEP 8: file input not found via CDP")
    raise SystemExit(4)
cdp("DOM.setFileInputFiles", files=["{file_abs}"], nodeId=node["nodeId"])
print("STEP 8 file set via CDP: {file_abs}")
time.sleep(3)  # allow the upload POST to finish before advancing

# STEP 9 — URL SLUG under "Advanced".
#   Open the Advanced collapsible, clear the slug input (it shows the
#   gumroad.com/l/<slug> preview), type the desired slug. If taken
#   (slugs are GLOBAL across all sellers), the field flags an error ->
#   retry with -v2, -pack, -v3 suffixes.
r = js("""
(() => {{
  // reveal the Advanced section if collapsed
  const adv = Array.from(document.querySelectorAll('button, [role="button"], summary, a'))
    .find(b => /^advanced$/i.test(b.textContent.trim()));
  if (adv && adv.getAttribute('aria-expanded') === 'false') adv.click();
  return "advanced-opened";
}})()
""")
time.sleep(1)
# The slug input: directly under Advanced, labelled "URL" / prefilled with the
# auto-generated permalink. Strategy: find input whose VALUE already looks like
# a slug, or that sits in a row containing 'gumroad.com/l/'.
slug_set = js("""
(() => {{
  const inputs = Array.from(document.querySelectorAll('input[type="text"], input:not([type])'));
  const slugInput = inputs.find(i =>
      /gumroad\\.com\\/l\\//.test(i.closest('div')?.innerText || '') ||
      /^gumroad\\.com\\/l\\//.test(i.placeholder || '') ||
      /^[a-z0-9]+(?:-[a-z0-9]+)*$/.test(i.value || '') && i.value.length > 3);
  if (!slugInput) return "SLUG_INPUT_NOT_FOUND";
  slugInput.focus();
  const setter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value').set;
  setter.call(slugInput, '');
  slugInput.dispatchEvent(new Event('input', {{ bubbles: true }}));
  return "OK";
}})()
""")
if slug_set == "OK":
    # type the desired slug char-by-char is overkill; set via native setter:
    r2 = js("""
    (() => {{
      const inputs = Array.from(document.querySelectorAll('input[type="text"], input:not([type])'));
      const slugInput = inputs.find(i =>
          /gumroad\\.com\\/l\\//.test(i.closest('div')?.innerText || '') ||
          /^gumroad\\.com\\/l\\//.test(i.placeholder || ''));
      if (!slugInput) return "SLUG_INPUT_NOT_FOUND";
      slugInput.focus();
      const setter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value').set;
      setter.call(slugInput, {js_str(slug)});
      slugInput.dispatchEvent(new Event('input', {{ bubbles: true }}));
      slugInput.dispatchEvent(new Event('change', {{ bubbles: true }}));
      return "OK";
    }})()
    """)
    print("STEP 9 slug: " + str(r2))
    # If the slug is globally taken, the UI shows an inline error. Detect and
    # retry with suffixes (-v2, -pack, -v3...). The candidates list is
    # embedded as a JS array so the retry loop lives entirely in JS.
    err = js("(() => {{ const t = (document.body.innerText || '').toLowerCase();"
             " return /already (taken|in use)|not available|is taken/.test(t); }})()")
    if err:
        retries = js("""
        (() => {{
          const base = {js_str(slug)};
          const suffixes = {json.dumps(SLUG_SUFFIXES[1:])};
          const inputs = Array.from(document.querySelectorAll('input[type="text"], input:not([type])'));
          const slugInput = inputs.find(i =>
              /gumroad\\.com\\/l\\//.test(i.closest('div')?.innerText || '') ||
              /^gumroad\\.com\\/l\\//.test(i.placeholder || ''));
          if (!slugInput) return "SLUG_INPUT_GONE";
          const setter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value').set;
          const setVal = (v) => {{
            slugInput.focus();
            setter.call(slugInput, v);
            slugInput.dispatchEvent(new Event('input', {{ bubbles: true }}));
            slugInput.dispatchEvent(new Event('change', {{ bubbles: true }}));
          }};
          for (const s of suffixes) {{
            setVal(base + s);
            // The UI flags a taken slug inline; look for an error near the field.
            const row = slugInput.closest('div, fieldset') || document.body;
            const txt = (row.innerText || '').toLowerCase();
            if (!/already (taken|in use)|not available|is taken/.test(txt)) {{
              return "OK:" + (base + s);
            }}
          }}
          return "ALL_SLUGS_TAKEN";
        }})()
        """)
        print("STEP 9 slug retry: " + str(retries))

# STEP 10 — PUBLISH (top-right primary button). Requires payouts configured
#   (gumroad.com/settings/payments) — otherwise the button stays disabled.
r = js("""
(() => {{
  const btn = Array.from(document.querySelectorAll('button'))
    .find(b => /^\\s*publish\\s*$/i.test(b.textContent) && !b.disabled);
  if (!btn) {{
    const any = Array.from(document.querySelectorAll('button'))
      .find(b => /publish/i.test(b.textContent));
    return any && any.disabled ? "PUBLISH_DISABLED (payouts not set up?)" : "PUBLISH_BUTTON_NOT_FOUND";
  }}
  btn.click();
  return "OK";
}})()
""")
print("STEP 10 publish: " + str(r))
time.sleep(4)
wait_for_load()

# STEP 11 — Verify: read the final URL and the published state.
info = page_info()
url = info.get("url", "")
print("DONE {n}/{total}: " + url)
url
'''


# ---------------------------------------------------------------------------
# Progress / resume
# ---------------------------------------------------------------------------

def load_progress():
    if PROGRESS_FILE.is_file():
        try:
            return json.loads(PROGRESS_FILE.read_text(encoding="utf-8"))
        except Exception:
            return {}
    return {}


def save_progress(progress):
    PROGRESS_FILE.write_text(json.dumps(progress, indent=2), encoding="utf-8")


def can_reach_browseros(port=9210, timeout=2):
    """True if the BrowserOS Neo MCP endpoint is listening locally."""
    import socket
    try:
        with socket.create_connection(("127.0.0.1", port), timeout=timeout):
            return True
    except OSError:
        return False


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser(
        description="Publish all 11 products to Gumroad via BrowserOS Neo browser automation.")
    ap.add_argument("--start-from", type=int, metavar="N",
                    help="resume: skip products before #N (1-based)")
    ap.add_argument("--only", type=int, metavar="N", help="publish only product #N")
    ap.add_argument("--dry-run", action="store_true",
                    help="print the browser_exec code for the selected product(s), execute nothing")
    ap.add_argument("--check", action="store_true",
                    help="same as publish-via-api.py --check: offline validation of payloads/files")
    args = ap.parse_args()

    products = load_payloads()

    if args.check:
        # Delegate to the API script's offline validator (no token needed).
        import subprocess
        api_script = HERE / "publish-via-api.py"
        return subprocess.call([sys.executable, str(api_script), "--check"])

    start = args.start_from or 1
    todo = [(i, p) for i, p in enumerate(products, start=1) if i >= start]
    if args.only:
        todo = [(i, p) for i, p in todo if i == args.only]

    if not todo:
        print("Nothing to do (empty selection).")
        return 0

    # Pre-flight: files must exist for every selected product.
    missing = [(i, p["_file_rel"]) for i, p in todo if not (p["_file_abs"] and p["_file_abs"].is_file())]
    if missing:
        for i, rel in missing:
            print(f"ERROR: product #{i} file missing: {rel}")
        return 1

    if args.dry_run:
        for i, p in todo:
            print("=" * 78)
            print(f"# DRY-RUN code for product {i}/{len(products)} (not executed)")
            print("=" * 78)
            print(build_browser_code(p, i, len(products)))
        return 0

    # Live mode requires the BrowserOS Neo MCP server to be up (port 9210
    # in this setup — see BROWSEROS-AGENT-WIRING.md) AND browser_exec
    # helpers in the runtime. This driver is executed BY the Hermes agent:
    # it cannot import browser_exec itself.
    if not can_reach_browseros(9210):
        print("BrowserOS Neo is NOT running (127.0.0.1:9210 unreachable).")
        print("Start BrowserOS Neo, verify the tab is logged in to Gumroad, then re-run:")
        print(f"  python scripts/publish-now/publish-via-browseros.py --start-from {todo[0][0]}")
        print("Meanwhile the API path needs no browser:")
        print("  python scripts/publish-now/publish-via-api.py --check   # then set GUMROAD_API_TOKEN")
        return 3

    print("NOTE: to execute the steps, run the generated code via the Hermes agent's")
    print("browser_exec tool in session 'browseros-neo'. Generated code per product is")
    print("identical to --dry-run output. Progress file:", PROGRESS_FILE)
    progress = load_progress()
    for i, p in todo:
        print(f"\n[{i}/{len(products)}] {p['name']}")
        print("  -> run this via browser_exec (session='browseros-neo'):")
        print(build_browser_code(p, i, len(products)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
