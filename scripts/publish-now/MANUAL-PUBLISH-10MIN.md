# Publish All 11 Products — 10-Minute Guide

**Fastest path first.** Three options, in order of speed: **A) the script**
(2 min of your time), B) manual CLI commands, C) manual browser clicking.

**Account:** `demosupreme001@gmail.com` · Profile: `abhishekanand31.gumroad.com`
**Catalog:** 10 packs @ **$9.99** + 1 bundle @ **$27.99**

---

## Step 0 (one-time, REQUIRED for all paths) — Payouts

Publish is blocked until payouts are configured. Do this first:

1. Go to **https://gumroad.com/settings/payments** (log in as
   `demosupreme001@gmail.com`).
2. Connect **Stripe** (or PayPal): country, bank details, verification.
   Takes ~3–5 minutes. Have your PAN/bank IFSC (India) or tax ID ready.
3. Complete the tax information prompt if one appears — payouts are
   blocked without it.

---

## Path A — The script (recommended, ~2 minutes of attention)

### A1. Log the CLI in (one-time)

The official Gumroad CLI is already installed at
`C:/Users/asus/.local/bin/gumroad.exe` (v2026.09.07).

**Device flow (no token needed):**

```
C:/Users/asus/.local/bin/gumroad.exe auth login
```

It prints a URL + a code. Open the URL in a browser where you're logged
in to Gumroad, enter the code, approve. Done — the CLI stores the session.

**Alternative — token:** at https://gumroad.com/settings/developers
(Settings → Advanced → Applications → "Generate access token", scopes:
`edit_products` or `account`), then either:

```
# save the token to a file and:
bash scripts/publish-now/auth-with-token.sh token.txt
# or set the env var the CLI reads:
export GUMROAD_ACCESS_TOKEN=<token>
```

Check with: `C:/Users/asus/.local/bin/gumroad.exe auth status`

### A2. Run the publish script

From the repo root (`C:\Users\asus\ai-prompt-store`), in git-bash:

```
cd scripts/publish-now
bash publish-all.sh --dry-run     # preview: validates + echoes all 11 CLI calls
bash publish-all.sh               # LIVE: creates + publishes all 11
```

What it does per product: `gumroad products create` (name, price, file,
description HTML, custom permalink, summary, tags — the CLI uploads the
file itself) → captures the product id from `--json` → `gumroad products
publish <id>` → `gumroad products url <id>` for the live link. Results
are logged to `scripts/publish-now/publish-results.tsv` (slug, id, URL).

**Resume / idempotency:**

```
bash publish-all.sh --start-from 8    # resume after a crash, from product #8
bash publish-all.sh --only 11         # just the bundle
bash publish-all.sh                   # safe to re-run: skips slugs already live
                                      # (via gumroad products list --all --json)
```

**Note:** slugs are GLOBAL across Gumroad. If a `--custom-permalink` is
taken, the create call fails for that product; the script reports it, and
you re-run that one with a different slug (edit `url_slug` in
`scripts/gumroad-product-payloads.json`, e.g. append `-v2`).

### A3. Verify

Open 2–3 of the URLs from `publish-results.tsv` in an incognito window —
they should load the product page with price + file + description.

---

## Path B — Manual CLI (same commands, typed by hand)

Per product (values from the cheat-sheet below):

```
GUM=C:/Users/asus/.local/bin/gumroad.exe

# 1. create draft (file upload handled by the CLI):
$GUM products create --non-interactive \
  --name "AI Content Creator Pack - 50 Expert Prompts for YouTube, Social Media, Blogs & Email" \
  --price 9.99 \
  --file ../products/prompt-pack-1/prompts.md \
  --custom-permalink ai-content-creator-pack \
  --custom-summary "Get 50+ expertly crafted AI prompts for content creators." \
  --description "<p>...description HTML...</p>" \
  --tag AI --tag ChatGPT --tag prompts

# 2. copy the product id from the JSON output, then:
$GUM products publish <id>
$GUM products url <id>
```

The description HTML is generated from the payload text — the script's
python helper converts it; by hand, wrap paragraphs in `<p>…</p>`,
bullets in `<ul><li>…</li></ul>`, and skip the bundle's last line
(`**Files to upload:** …` — internal note, not buyer-facing).

---

## Path C — Manual browser (fallback, ~10 minutes)

1. **https://gumroad.com/products/new** — log in first if asked.
2. **Name**: paste `name` from `scripts/gumroad-product-payloads.json`.
   Pick "Digital product" when the type chooser appears.
3. **Price** (pricing card): `9.99` (packs) / `27.99` (bundle) — dollars
   on the wizard.
4. **Next: customize** → product edit page.
5. **Content** card → **Upload a file** → pick:
   - packs 1–10: `C:\Users\asus\ai-prompt-store\products\prompt-pack-N\prompts.md`
   - bundle: `C:\Users\asus\ai-prompt-store\products\bundle-all-10-packs.zip`
6. **Description**: click into the rich-text box, paste `description`
   (paste preserves line breaks).
7. **Advanced** → **URL** → paste `url_slug`. Taken (slugs are global)?
   Append `-v2`, then `-pack`, then `-v3`.
8. **Tags**: paste the comma list from `tags`.
9. **Publish** (top right, orange).
10. Verify: `https://abhishekanand31.gumroad.com/l/<slug>` in incognito.
11. Repeat. Publish the 10 packs first, the bundle last.

**Why this order:** payouts first (Step 0) or Publish is disabled; file
upload before description (missing file is the #1 publish blocker); slug
before Publish (changing it after breaks the gum.co short link).

---

## Product cheat-sheet (all 11)

| # | name | slug | price | file |
|---|---|---|---|---|
| 1 | AI Content Creator Pack - 50 Expert Prompts for YouTube, Social Media, Blogs & Email | `ai-content-creator-pack` | 9.99 | `products/prompt-pack-1/prompts.md` |
| 2 | AI Business Builder Pack - 50 Prompts for Strategy, Planning & Growth | `ai-business-builder-pack` | 9.99 | `products/prompt-pack-2/prompts.md` |
| 3 | AI Coding Assistant Pack - 50 Prompts for Developers | `ai-coding-assistant-pack` | 9.99 | `products/prompt-pack-3/prompts.md` |
| 4 | AI Marketing Master Pack - 50 Prompts for Copywriting & Campaigns | `ai-marketing-master-pack` | 9.99 | `products/prompt-pack-4/prompts.md` |
| 5 | AI Writing Assistant Pack - 50 Prompts for Fiction & Creative Writing | `ai-writing-assistant-pack` | 9.99 | `products/prompt-pack-5/prompts.md` |
| 6 | AI Productivity Pack - 50 Prompts for Time Management & Planning | `ai-productivity-pack` | 9.99 | `products/prompt-pack-6/prompts.md` |
| 7 | AI Social Media Manager Pack - 50 Prompts for Strategy & Content | `ai-social-media-manager-pack` | 9.99 | `products/prompt-pack-7/prompts.md` |
| 8 | AI SEO Expert Pack - 50 Prompts for Search Engine Optimization | `ai-seo-expert-pack` | 9.99 | `products/prompt-pack-8/prompts.md` |
| 9 | AI Entrepreneur Pack - 50 Prompts for Startups & Growth Hacking | `ai-entrepreneur-pack` | 9.99 | `products/prompt-pack-9/prompts.md` |
| 10 | AI Education Pack - 50 Prompts for Teaching & Course Creation | `ai-education-pack` | 9.99 | `products/prompt-pack-10/prompts.md` |
| 11 | Complete AI Prompt Bundle - All 10 Packs (500+ Prompts) | `complete-ai-prompt-bundle` | 27.99 | `products/bundle-all-10-packs.zip` |

> **Payload quirks:** the bundle's `file_upload_path` in the payloads JSON
> is placeholder prose — the real file is `products/bundle-all-10-packs.zip`
> (the script resolves this automatically). And skip the bundle
> description's last line when pasting manually.

---

## Common blockers

| Symptom | Fix |
|---|---|
| Publish button greyed out / publish fails | Payouts not set up — do Step 0. |
| "URL already in use" / permalink rejected | Slugs are global; retry with `-v2`/`-pack`/`-v3`. |
| `auth_error` / `not authenticated` | Re-run `gumroad auth login`. |
| Uploaded .md previews as text | Fine — Gumroad serves .md as a downloadable file. |
| Script create fails on one product | Note which #, fix its payload, re-run `--start-from N` (already-done slugs are skipped). |

---

## After publishing

1. Verify each URL from `publish-results.tsv` loads (incognito).
2. Sanity-buy one pack with a 100%-off offer code to test checkout + email.
3. Optional: set the bundle's comparison price ($99.99 strikethrough) on
   its pricing card in the dashboard — there's no API/CLI field for it.
