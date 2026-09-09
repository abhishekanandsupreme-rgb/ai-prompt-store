# Cross-Sell Plan — Bundle Upsell + Post-Purchase Sequence

**Goal:** every pack buyer eventually sees the Complete AI Prompt Bundle ($27.99, anchor $99.99), and bundle buyers see nothing (they own everything — show them nothing but gratitude and ratings requests).

**All mechanics verified against Gumroad Help #331 (Creating an Upsell), #334 (Recommend related products / checkout recommendations), #131 (Workflows), #128 (Discount codes).**

---

## 1. The three surfaces (wired in this order)

### Surface 1 — Checkout upsell (fires immediately, highest intent)

Gumroad's upsell appears **after the buyer presses Pay** — the exact moment of maximum buying temperature.

**Setup (Checkout dashboard → Upsells tab → "New upsell"):**

| Setting | Value |
|---|---|
| Name | Pack → Bundle upgrade |
| Type | **"Replace the products in the cart"** — Gumroad's own docs call out this exact use case: "useful to upgrade a customer to a bundle that already contains the originally selected product(s)." Buyer's pack(s) are removed and the bundle is offered in its place. |
| Apply to these products | All 10 packs |
| Product to offer | Complete AI Prompt Bundle |
| Discount on the offer | Set the upsell's optional discount so the upgrade price is fair: buyer paid $7.49–$9.99 for one pack; offer the bundle for **$19.99** (≈ "you pay only the difference") — i.e. a ~29% discount inside the upsell. A buyer holding one $9.99 pack upgrading to a $19.99 bundle effectively pays $10 for the other 9 packs. That is the strongest deal in the store and it only exists at checkout. |

**Why replace-not-add:** adding the bundle on top of a pack sale double-charges for prompts the buyer just bought. Replacement makes the math honest for the buyer and still nets more for us ($17.49 net on a $19.99 bundle sale vs $8.49 on a pack).

**Guardrail:** one upsell rule store-wide. Multiple upsell rules competing at one checkout muddies which fires; keep exactly this one.

### Surface 2 — Checkout product recommendations (passive grid)

**Setup (Checkout dashboard → Checkout form tab):** select **"Recommend my products"** and save. A grid of your products shows on the checkout page — automatically excluding anything the buyer already owns or has in cart.

**Honest caveat from Gumroad's docs:** recommendations are driven by *co-purchase patterns* — "if the product has no purchasers in common with your other products, you won't get any recommendations." With zero sales, this grid will be empty at launch and populate organically as cross-buying emerges. It's a set-and-forget switch, not a launch lever. Do not recommend other creators' products (the alternative settings) — this is our own catalog's cross-sell surface.

**One deliberate note on the bundle:** the bundle should appear in every pack's checkout grid once co-purchases exist. Don't accelerate this with self-purchases — refunded sales don't count toward Discover eligibility and pollute co-purchase data. Surfaces 1 and 3 carry the bundle until the grid fills itself organically.

### Surface 3 — Post-purchase email workflow (the durable engine)

**Setup (Workflows → New workflow):**

- **Trigger:** Purchase
- **Filter "Has bought":** the 10 pack products (buyers of any pack)
- **Filter "Has not yet bought":** Complete AI Prompt Bundle — per Gumroad's docs, a buyer who purchases the bundle mid-sequence stops receiving the remaining emails automatically. This filter *is* the suppression logic.
- Emails scheduled 0h / 48h / 7d after purchase (below).

**Prerequisite:** workflows can't send until the account has **earned $100 after fees and received a payout**. Build and publish the workflow anyway on Day 1 so the trigger starts recording; emails begin flowing once the threshold clears (projected ~week 3–4). Until then the checkout upsell (Surface 1) is the only active cross-sell.

**Note:** workflow emails come from a @gumroad.com address in your name; replies route to your support email. One workflow per trigger-audience — don't build ten per-pack workflows; the "Has bought" filter accepts the pack list.

---

## 2. The 3-email post-purchase sequence (full copy)

Trigger: purchase of any pack. Suppression: bought the bundle (auto via "Has not yet bought" filter).

---

### Email 1 — Deliver + orient (0 hours after purchase)

**Subject:** Your AI prompts are inside (plus how to use them tonight)
**Preview text:** Download link + the one prompt to try first.

> Hey [first name],
>
> Your **[Product Name]** is ready — download it here:
> **[Download link]**
>
> One request before you dive in: open the file, find **Prompt #1**, paste it into ChatGPT (or Claude/Gemini), and swap in your own context — your niche, your product, your week. That's the whole trick. These are fill-in-the-blank systems, not quotes to admire.
>
> Works with ChatGPT, Claude, Gemini, and any AI tool. Lifetime access. Free updates forever — when we improve the pack, you get the new version at no cost.
>
> Quick question while you have this open: reply and tell me what you're working on. I read every reply, and it shapes what gets added next.
>
> — Abhishek

*Purpose: instant delivery, first-use instruction (fights buyer's remorse / refund impulse), opens a reply channel that improves deliverability. No pitch.*

---

### Email 2 — Thank + rate (48 hours after purchase)

**Subject:** Did Prompt #1 work? (2-minute favor)
**Preview text:** A rating helps other creators find this pack.

> Hey [first name],
>
> Two days with [Product Name] — how's it going?
>
> If you've gotten value, would you leave a quick rating? It takes ~2 minutes on your Gumroad library page: **[rate link]** — it's the single biggest thing that helps other creators find the pack. (Ratings also decide whether these products surface in Gumroad Discover, so it genuinely matters.)
>
> If something *didn't* work — a prompt that fell flat, a section that's missing — reply and tell me. I'll fix it and you'll get the update free.
>
> Thanks for being an early buyer,
> — Abhishek

*Purpose: ratings are a hard Discover-listing requirement and every rating compounds visibility. Reply-handles complaints before they become refunds. Still no pitch.*

---

### Email 3 — Bundle upsell + LOYALTY20 (7 days after purchase)

**Subject:** You own 1 of 10 packs — here's the other 9 for $22.39
**Preview text:** 20% loyalty discount on the Complete Bundle, just for early buyers.

> Hey [first name],
>
> You've had [Product Name] for a week. If it's earning its keep, here's the math worth 60 seconds:
>
> You paid $9.99 for 50 prompts. The **Complete AI Prompt Bundle** is all **10 packs — 500+ prompts** — covering content, business, coding, marketing, writing, productivity, social media, SEO, entrepreneurship, and education.
>
> Bought separately: **$99.90**. Bundle list price: **$27.99**.
>
> As a thank-you for being an early buyer, use code **LOYALTY20** and the bundle is **$22.39** — and since you already own [Product Name], think of it as paying $12.40 for the other 9 packs. That's $1.38 per pack.
>
> **[Get the Complete Bundle — $22.39 with LOYALTY20 →]**
> *(link: `https://abhishekanand31.gumroad.com/l/{BundleID}/LOYALTY20` — the discount auto-applies; no code-typing)*
>
> The code works for the next 14 days and is exclusive to people who already own a pack.
>
> Either way — thanks for the support. Reply anytime.
>
> — Abhishek

*Purpose: the loyalty upsell. Explicit fairness math ("$12.40 for the other 9") does the selling; the auto-apply link removes friction; 14-day window creates action without being sleazy.*

**LOYALTY20 code settings (Checkout → Discounts):** 20% off, bundle only, **Limit to existing customers → must have purchased any one pack**, validity Day 8 → Day 90. The existing-customer gate means even if the link leaks publicly, non-buyers can't redeem it — Gumroad checks ownership at checkout (guest checkouts count if the email matches a confirmed Gumroad account).

---

## 3. Who sees what (routing summary)

| Buyer type | Checkout upsell | Checkout recommendations | Emails |
|---|---|---|---|
| Cold visitor, pack page | — | — | — |
| Pack in cart → checkout | Bundle replace-upsell at $19.99 | Grid of other products (excl. in-cart) | — |
| Pack buyer, post-purchase | — | — | E1 (0h) → E2 (48h) → E3 (7d, LOYALTY20) |
| Pack buyer who grabs the checkout upsell or buys the bundle at any point | — | Grid (excl. owned) | Workflow auto-stops remaining emails |
| Bundle buyer | No upsell (rule applies to packs only) | Grid of packs (they own none individually... but they own the *content* — see guardrail 2) | None — build no workflow for bundle buyers beyond delivery |

**Guardrails:**

1. **Never offer the bundle to a bundle buyer.** The "Has not yet bought" filter and the cart-exclusion in recommendations both handle this automatically — verify with a test purchase.
2. **Don't market individual packs to bundle buyers.** They already own the content of all 10 packs. Selling them Pack #4 at $9.99 is a refund waiting to happen. Recommendations exclude owned products but NOT "content-equivalent" ones — the bundle is one product, the packs are ten. Until Gumroad's grid gets smart about this, the single-workflow design (packs only) is our protection: bundle buyers simply receive no sequence. Their only emails: delivery + (later) new-pack announcements framed as free updates where applicable.
3. **One upsell rule, one workflow, one recommendations switch** — three surfaces, no overlap conflicts.
4. **Test before launch:** make a real test purchase of one pack at full price ($9.99 — the cheapest possible QA) and walk the entire flow: upsell presentation, receipt, workflow enrollment. Refunded test sales don't count toward Discover eligibility, so don't plan on refunding it. Verify the LOYALTY20 gate with a second Gumroad account that owns nothing (it must NOT redeem).

---

## 4. Metrics & targets

Track weekly (Gumroad Analytics + Discounts tab usage stats):

| Metric | Source | Launch target (30 days) |
|---|---|---|
| Checkout upsell take-rate (bundle upgrades ÷ pack sales) | Upsell stats / order inspection | ≥ 8% (industry-ish placeholder — replace with real data at Day 30) |
| LOYALTY20 redemptions | Discounts tab | ≥ 5% of pack buyers within 14 days of Email 3 |
| Email 3 click-rate on bundle link | Workflow email stats (available once workflows send) | ≥ 6% |
| Rating submissions (Email 2) | Product ratings counts | ≥ 25% of buyers rating |
| Refund rate | Analytics | < 5% — if above, stop cross-sell and fix the product |

**Revenue stack potential per 100 pack buyers (illustrative, at targets):** 8 checkout upgrades × $17.49 net + 5 loyalty redemptions × $19.65 net ≈ **$236 net incremental** on top of ~$849 direct pack net — a ~28% cross-sell lift. Placeholders until data exists; recompute at Day 30.

---

## 5. Build order (one sitting, ~60 minutes)

1. Checkout → Upsells → New upsell (Surface 1) — packs → bundle, replace, $19.99-equivalent discount.
2. Checkout → Checkout form → "Recommend my products" (Surface 2) — one radio button.
3. Workflows → New workflow: Purchase trigger, Has bought = 10 packs, Has not yet bought = bundle (Surface 3). Add E1 (0h), E2 (48h), E3 (7d). Preview each to your own email. **Publish** — remember: settings (not content) lock after first publish; get the filters right before publishing. Emails themselves remain editable.
4. Discounts → create LOYALTY20 (existing-customers-gated, bundle-only, Day 8–90) if not already created in the launch plan.
5. Test purchase → verify upsell fires, receipt lands, workflow enrolls, recommendations grid behaves.
6. Note in `pricing-log.csv` when workflows begin actually sending (post-$100 threshold) so cross-sell metrics get an honest start date.
