# Discount & Launch Code Plan

**Store:** abhishekanand31.gumroad.com — launch week for 11 products.
**All mechanics below verified against Gumroad Help #128 (Discount codes), #331 (Upsells), and live product URLs.**

---

## 1. Verified code mechanics (what Gumroad actually supports)

1. **Create codes at** Checkout dashboard → Discounts tab → "New discount". Name is auto-generated; replace with your custom code. **Codes can contain only numbers and letters** (so `LAUNCH25`, `FLASH50`, `LOYALTY20` — no dashes/underscores).
2. **A code applies to chosen product(s) or "All products"** (with optional per-product exclusions).
3. **Max one code per product per checkout** — "Only one code can be used per product." Stacking is impossible; plan codes as mutually exclusive per product.
4. **URL embedding:** append the code as a path segment: `https://username.gumroad.com/l/{ProductID}/{DiscountCode}`. The product page then shows the original price crossed out with the discounted price next to it. (Legacy `?offer_code=NAME` parameter form also auto-applies; the path-segment form is the one Gumroad's own docs now show.)
5. **Validity period, quantity limits, minimum amount/quantity** are all settable per code. Quantity limit = total uses, and each item in a cart uses one redemption.
6. **"Limit to existing customers"** gates a code on prior ownership of a chosen product — this powers the loyalty discount in CROSS-SELL-PLAN.md.
7. **"Automatically apply discount code"** (product editor → pricing section) applies a code to every visitor without a link — the page shows the crossed-out price. Pick one code; it must apply to that product and be unexpired.
8. If a customer arrives with a different code link, **Gumroad applies the larger discount** — never stacked.
9. Codes work on custom domains the same way (`/{YourCustomDomain}/{ProductID}/{DiscountCode}`), and can be combined with affiliate links: `.../{ProductID}/{DiscountCode}?affiliate_id={Affiliate_ID}`.

---

## 2. The launch code set (the exact plan)

| Code | Discount | Applies to | Window | Limit | Mechanics note |
|---|---|---|---|---|---|
| **LAUNCH25** | 25% off | **All 11 products** (10 packs + bundle) | Launch week, Days 1–7 | Unlimited uses; validity period set to the 7 launch days | One code covers the whole catalog — Gumroad allows a code scoped to "All products", which keeps us inside the "max 1 code per product" rule with zero conflicts. |
| **FLASH50** | 50% off | **Bundle ONLY** | One 24h window mid-launch (Day 4, 00:00–23:59 IST) | Unlimited uses during its 24h validity | Scoped to the bundle product only. Because only one code applies per product, a FLASH50 link on Day 4 simply replaces LAUNCH25 for the bundle that day — no stacking conflict. |
| **LOYALTY20** | 20% off | Bundle only | From Day 8 onward (post-purchase emails) | Gated by **Limit to existing customers → must have purchased any pack** | Never public. Only fires for verified prior buyers via the workflow email. See CROSS-SELL-PLAN.md. |

**Resulting prices (verified math):**

| Product | List | LAUNCH25 (−25%) | FLASH50 (bundle, 24h) | LOYALTY20 (−20%) |
|---|---|---|---|---|
| Each of 10 packs ($9.99) | $9.99 | **$7.49** | — | — |
| Complete Bundle ($27.99) | $27.99 | **$20.99** | **$13.99** | **$22.39** |

Net per sale after fees (10% + $0.50 direct; 30% Discover): LAUNCH25 pack → $6.24 net direct / $5.24 Discover; LAUNCH25 bundle → $18.39 / $14.69; FLASH50 bundle → $12.10 / $9.80; LOYALTY20 bundle → $19.65 / $15.67.

**Fee note for launch week:** LAUNCH25 on a pack nets $6.24 on a direct sale. Ten pack sales ≈ $62 net — under the $100 payout threshold, so launch week alone won't trigger payout. Expect first payout once bundle + full-price sales accumulate in weeks 2–4.

---

## 3. Link formats — copy-paste ready

Canonical product URL: `https://abhishekanand31.gumroad.com/l/{product-slug}` (confirm each actual Gumroad product ID from the Share tab after publish — slugs in the repo, e.g. `ai-coding-assistant-pack`, may differ from the final Gumroad URL ID; **verify before blasting links**).

**Path-segment auto-apply (recommended, Gumroad's documented form):**

```
https://abhishekanand31.gumroad.com/l/{ProductID}/LAUNCH25
https://abhishekanand31.gumroad.com/l/{ProductID}/FLASH50     (bundle, Day 4 only)
```

**URL-parameter form (also auto-applies):**

```
https://abhishekanand31.gumroad.com/l/{ProductID}?offer_code=LAUNCH25
https://abhishekanand31.gumroad.com/l/{ProductID}?offer_code=FLASH50
```

Both show the crossed-out price pre-checkout. Use one form consistently across all channels (path-segment recommended — it's shorter in bios and survives link truncation better).

**Important: URL parameters in query strings can be stripped by some social platforms' link scrapers — the path-segment form can't be.** For Twitter/X bios, Instagram link-in-bio, and YouTube descriptions, use path-segment links.

---

##  4. Launch-week timeline

| Day | Action | Code state |
|---|---|---|
| **Pre-launch (Day 0)** | Create LAUNCH25 (validity: Day 1 00:00 → Day 7 23:59 IST, all products) and FLASH50 (validity: Day 4 00:00 → Day 4 23:59 IST, bundle only). Create LOYALTY20 (validity: Day 8 → 90 days, bundle only, Limit to existing customers = any pack). Turn ON "Automatically apply discount code → LAUNCH25" on all 11 products so even bare product URLs get the launch price. | Codes live but not yet valid |
| **Day 1** | Publish all 11 products. Announce: "All 11 packs live — 25% off launch week" + store link. | LAUNCH25 active (auto-applied) |
| **Day 2–3** | Daily posts per 15-DAY-CALENDAR.md; every link path-segment form `/LAUNCH25`. | LAUNCH25 |
| **Day 4** | 24h bundle flash: post/email "Bundle at 50% off for 24 hours only — $13.99" with `/FLASH50` bundle link. Since FLASH50 > LAUNCH25 on the bundle, Gumroad auto-applies the larger one — customers clicking old LAUNCH25 bundle links still get 50% if it's Day 4. | LAUNCH25 (packs) + FLASH50 (bundle) |
| **Day 5–6** | Continue LAUNCH25 push on individual packs ("last days of launch pricing"). | LAUNCH25 |
| **Day 7** | "Final hours" posts at 6h and 2h before expiry. | LAUNCH25 ends 23:59 |
| **Day 8** | Turn OFF auto-apply on all products (edit each product → pricing section). List prices ($9.99/$27.99) now show clean — pricing test Block A1 begins (see PRICING-TEST-PLAN.md). LOYALTY20 becomes active for existing buyers via workflows. | No public codes; LOYALTY20 live (gated) |

**Why auto-apply for launch week:** every share, including bare store links from other people, carries the discount — no lost code-entry at checkout. Remember the auto-applied code blocks edits that would stop it applying; turn it off before any code edits on Day 8.

---

## 5. Guardrails

1. **One code per product is a hard limit** — the plan respects it: LAUNCH25 covers all products; FLASH50 is bundle-only and time-boxed to a day when it simply overrides LAUNCH25 via the "larger discount wins" rule; LOYALTY20 is bundle-only and buyer-gated.
2. **Don't create overlapping public codes on the same product.** A hypothetical "SAVE10" alongside LAUNCH25 would never stack and only splits your attribution.
3. **Set validity periods, not manual deletion.** Scheduled expiry means the codes die cleanly at 23:59 without you touching them, and usage stats persist for post-launch analysis.
4. **FLASH50 is bundle-only, deliberately:** 50% off a pack ($4.99) triggers Gumroad's per-sale fee floor problem (10% + $0.50 = 12% effective fee at $4.99, and only $3.99 net direct) — the bundle at $13.99 still nets $12.10.
5. **After Day 7, codes are a scalpel, not a habit.** The next public code should be a purposeful event (e.g., a 48h Black Friday code), not a weekly drip — frequent codes train buyers to wait.
6. **Track redemptions:** Discounts tab shows uses + revenue per code. Log daily into `pricing-log.csv` notes.

---

## 6. Launch-week revenue model (expectations, not promises)

Assume (from nothing — zero live data, so these are planning placeholders): ~40 store visitors/day from owned channels in week 1, pack CR ~3%, bundle attach ~10% of buyers.

- ~280 visitors → ~8 pack sales @ $7.49 = $59.92 gross → ~$50 net direct
- ~1 bundle sale @ $20.99 (or $13.99 on Day 4) → $18.39 (or $12.10) net
- **Week-1 realistic net: $60–75** — under the $100 threshold. The launch week's true goal is (a) first sale on every product (unlocks Discover eligibility per product) and (b) verified pipeline, not revenue.

These numbers are placeholders until Day 1 data exists; replace them in the Day 8 block summary.
