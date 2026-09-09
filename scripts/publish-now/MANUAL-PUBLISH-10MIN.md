# Manual Publish — 10 Minutes for All 11 Products

Fastest zero-automation path. No token, no BrowserOS, no scripts. Paste fields
from the JSON files you already have. One product takes ~50 seconds once
you've done the first.

**Account:** `demosupreme001@gmail.com` · Profile: `abhishekanand31.gumroad.com`
**Products:** 10 packs @ **$9.99** + 1 bundle @ **$27.99**

---

## Where your data lives (what to paste from where)

| Product page field | Copy from | File |
|---|---|---|
| Name | `name` | `scripts/gumroad-product-payloads.json` |
| Price | `price` (dollars) | `scripts/gumroad-product-payloads.json` |
| Description | `description` | `scripts/gumroad-product-payloads.json` |
| Summary (checkout) | first sentence of `description` | `scripts/gumroad-product-payloads.json` |
| Tags | `tags` (comma list) | `scripts/gumroad-product-payloads.json` |
| Content file | `file_path` (row 1–10) / the ZIP (row 11) | `scripts/gumroad-all-products-ready.json` |

Tip: run `python scripts/publish-now/publish-via-api.py --check` first — it
prints every product's name/price/slug/file in one table to copy from.

> **Payload quirk you'll hit:** the bundle's `file_upload_path` in the
> payloads JSON is placeholder prose ("All products/prompt-pack-*/prompts.md
> combined into one ZIP"). The real file is **`products/bundle-all-10-packs.zip`**
> — that's the one you upload. For rows 1–10 upload
> `products/prompt-pack-N/prompts.md` directly.

> **Skip the last line of the bundle description** (`**Files to upload:** ...`)
> when pasting — that's an internal note, not buyer-facing copy.

---

## Step 0 (one-time, REQUIRED) — Payouts setup

Publish is **disabled** until payouts are configured. Do this first:

1. Go to **https://gumroad.com/settings/payments**
2. Connect **Stripe** (or PayPal): country, bank details, verification.
   Takes ~3–5 minutes. Have your PAN/bank IFSC (India) or tax ID ready.
3. Don't skip tax info if prompted — Gumroad blocks payout without it.

Optional, once, for the bundle's "$99.99 → $27.99" look: on the bundle's
pricing card, toggle **"Show original price"** / comparison price and enter
`$99.99`. (There is no API field for this — dashboard-only.)

---

## The 10-minute loop (per product)

1. **https://gumroad.com/products/new** — log in first if asked.
2. **Name**: paste `name` from the payloads JSON. (Choose "Digital product"
   when the type picker appears.)
3. **Price** (pricing card): paste `price` — `9.99` (packs) / `27.99` (bundle).
   Type it as dollars here; the wizard expects `$9.99`-style input.
4. Click **Next: Customize** → lands on the product edit page.
5. **Content** card → **Add file / Upload a file** → pick:
   - packs 1–10: `C:\Users\asus\ai-prompt-store\products\prompt-pack-N\prompts.md`
   - bundle: `C:\Users\asus\ai-prompt-store\products\bundle-all-10-packs.zip`
   Wait for the upload progress to finish (~1s, files are 3–16 KB).
6. **Description**: click into the rich-text box, paste `description`.
   Line breaks survive paste; bullets stay bullets. (If pasting looks flat,
   the editor mangled it — select-all, delete, re-paste.)
7. **Advanced** (bottom of page) → **URL** row → paste `url_slug`.
   If Gumroad flags it taken (slugs are GLOBAL across all sellers), append
   `-v2` (e.g. `ai-content-creator-pack-v2`), then `-pack`, then `-v3`.
   Note the final slug you used.
8. **Tags** (sidebar/summary card): paste the comma list from `tags`.
9. **Summary** (if you want it): first line of the description.
10. **Publish** (top right, orange). It flips to "Saved/Published" — done.
11. Verify live: `https://abhishekanand31.gumroad.com/l/<slug>` (your profile
    domain), or the `gum.co/<short>` link on the confirmation screen.
12. Back to step 1 for the next product. Publish the 10 packs first, the
    bundle last (its page can link to all of them).

### Order of operations (why this order)

- Payouts first — otherwise step 10 is a disabled button and you'll redo steps 1–9.
- File upload BEFORE description — the upload card is at the top; if the
  page validates on Publish, a missing file is the #1 publish blocker.
- Slug BEFORE Publish — after publishing, changing the URL breaks the `gum.co` link.

---

## Product cheat-sheet (copy targets)

| # | slug | price | file |
|---|---|---|---|
| 1 | `ai-content-creator-pack` | 9.99 | `products/prompt-pack-1/prompts.md` |
| 2 | `ai-business-builder-pack` | 9.99 | `products/prompt-pack-2/prompts.md` |
| 3 | `ai-coding-assistant-pack` | 9.99 | `products/prompt-pack-3/prompts.md` |
| 4 | `ai-marketing-master-pack` | 9.99 | `products/prompt-pack-4/prompts.md` |
| 5 | `ai-writing-assistant-pack` | 9.99 | `products/prompt-pack-5/prompts.md` |
| 6 | `ai-productivity-pack` | 9.99 | `products/prompt-pack-6/prompts.md` |
| 7 | `ai-social-media-manager-pack` | 9.99 | `products/prompt-pack-7/prompts.md` |
| 8 | `ai-seo-expert-pack` | 9.99 | `products/prompt-pack-8/prompts.md` |
| 9 | `ai-entrepreneur-pack` | 9.99 | `products/prompt-pack-9/prompts.md` |
| 10 | `ai-education-pack` | 9.99 | `products/prompt-pack-10/prompts.md` |
| 11 | `complete-ai-prompt-bundle` | 27.99 | `products/bundle-all-10-packs.zip` |

⚠️ **Before selling the bundle**: the ZIP was built Aug 22 and several
`prompts.md` files inside it have since been updated on disk (packs 2–9 were
enriched to ~16 KB). The ZIP still contains the old ~3 KB copies. Re-zip
`products/prompt-pack-*/` before buyers get stale content, or publish the
bundle after re-zipping. The 10 individual packs are unaffected.

---

## Common blockers

| Symptom | Fix |
|---|---|
| Publish button greyed out | Payouts not set up — do Step 0 (settings/payments). |
| "URL already in use" on slug | Slugs are global; retry with `-v2`/`-pack`/`-v3`. |
| Uploaded .md shows as text preview | Fine — Gumroad serves .md as a downloadable file. |
| File upload spins forever | Files are tiny; it's the network. Cancel and re-add. |
| Login loop | Log in once at gumroad.com in the same browser before `/products/new`. |

---

## After publishing all 11

1. Verify each URL from the cheat-sheet loads (logged out / incognito).
2. Sanity-buy one $9.99 pack with a discount code (`100off` = free) to test
   checkout + delivery email.
3. Set up the bundle's "original price" comparison (`$99.99`) on its pricing card.

Automation alternatives, when you'd rather not click 11 times:

```
# API path (preferred; needs a token from gumroad.com/settings/developers)
python scripts/publish-now/publish-via-api.py --check    # dry-run validate
export GUMROAD_API_TOKEN=<token>                        # setx GUMROAD_API_TOKEN <token> on cmd
python scripts/publish-now/publish-via-api.py           # publish all 11

# Browser path (needs BrowserOS Neo running on 127.0.0.1:9210)
python scripts/publish-now/publish-via-browseros.py --start-from 5
```
