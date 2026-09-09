import json, re, sys
from pathlib import Path

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
print("\t".join(["n", "name", "price", "file", "slug"]))
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
    print("\t".join([str(i), name, str(p["price"]), str(f), p["url_slug"]]))
    # sidecar per product for the bash loop (desc html, summary, tags)
    (REPO / "scripts/publish-now/.meta-%d.json" % i).write_text(
        json.dumps({"html": html(desc), "summary": summary, "tags": tags}), encoding="utf-8")
