# Pricing Test Plan — 30-Day Experiment

**Store:** abhishekanand31.gumroad.com
**Catalog:** 10 packs @ $9.99 + Complete Bundle @ $27.99 (anchor $99.99)
**Constraint:** Gumroad has **no native A/B testing**. This plan is an honest workaround: fixed 7-day price blocks, alternating, with a decision protocol that doesn't pretend to more rigor than the method delivers.

---

## 1. The honest method (read this first)

**What we can do:** change the list price of every product at will, and track daily visitors/sales per product in Gumroad Analytics.

**What we cannot do:** show two prices simultaneously to two randomized audiences. Any "A/B" here is **sequential (time-blocked)**: week-blocks of price A alternating with week-blocks of price B. Confounds we accept and must control for:

1. **Day-of-week mix** — Sat/Sun traffic converts differently. Mitigation: every block is exactly 7 days, so every block contains the same weekday mix. Blocks start on a fixed weekday (pick Monday 00:00 IST).
2. **Traffic-source mix** — launch-week social spikes distort block 1. Mitigation: block 1 is *baseline-measurement*, not a comparison arm; the experiment proper starts when traffic sources have stabilized (Day 8). Comparisons use blocks 2–5.
3. **Novelty/announcement effects** — price drops announced publicly spike sales. Mitigation: **no public announcement of any mid-experiment price change.** Links keep flowing from the same channels at the same cadence.
4. **Sample size** — with low traffic, blocks may be underpowered (see §3). Then we decide by RPV with a stated confidence discount, not by pretending significance.

**Cadence: change prices every 7 days, Mondays 00:00 IST, via the product editor's price field.** Changes take effect immediately. (Alternative worth knowing: `Automatically apply discount code` shows a crossed-out price — visually similar to a price test but it *displays the original price*, which contaminates the perception; use actual price edits, not auto-applied codes, for the experiment blocks. Codes are for the launch and loyalty plans, not the pricing test.)

---

## 2. The 30-day schedule

| Block | Days | Dates (example, Mon-start) | Packs | Bundle | Notes |
|---|---|---|---|---|---|
| **Baseline A** | 1–7 | Mon–Sun wk 1 | **$9.99** | **$27.99** | Launch week. Also carries LAUNCH25 auto-applied at checkout (see DISCOUNT-LAUNCH-CODES.md). Distorted by launch noise — record, but don't compare. |
| **A (control)** | 8–14 | wk 2 | **$9.99** | **$27.99** | First clean baseline block. |
| **B (variant)** | 15–21 | wk 3 | **$7.99** | **$19.99** | First variant block. |
| **A (control)** | 22–28 | wk 4 | **$9.99** | **$27.99** | Second baseline block — captures the week-to-week trend line. |
| **B (variant)** | 29–35 | wk 5 | **$7.99** | **$19.99** | Second variant block. Decision at Day 36. |

*(If launch slips, re-anchor all Mondays to the actual launch date; keep the A-B-A-B order fixed. If a public holiday/online event falls inside a block, note it — that block gets flagged.)*

**Why A-B-A-B and not A-A-B-B:** an A-B-A-B (reversal) design lets you check that the *second* A block reproduces the *first* A block. If A₁ ≈ A₂ and B₁ ≉ A₁, the price effect is real; if A₁ ≉ A₂, something else (traffic, seasonality, Discover switching on) moved, and you distrust all blocks. Reversal is the cheapest defense against time trend.

**Discover timing:** the $100 threshold + ~3-week risk review means Discover traffic may switch on mid-experiment. **When the first Discover sale lands, add a "sales source" flag to that day's log row** (Analytics shows sales by source) — if Discover sales are >10% of a block's sales, tag the block "mixed-source" and treat cross-block comparison with caution. Ideally, exclude Discover-attributed sales from the price comparison and analyze direct traffic only (Discover buyers see the same price but the fee differs — comparing list-price conversion across fee regimes is fine, comparing *net revenue* needs the source split).

---

## 3. Decision metrics

Track per product per day in a simple sheet (template below):

- **Visitors** (product page views, from Gumroad Analytics)
- **Sales** (units)
- **Conversion rate** = sales ÷ visitors
- **Gross revenue** = units × current list price
- **Net revenue** = gross × 0.90 − $0.50 × units (direct sales) — or × 0.70 (Discover sales); log the source mix
- **RPV (revenue per visitor)** = gross ÷ visitors *(the primary decision metric — it folds price and conversion into one number)*

**Primary metric: RPV (gross, per-visitor, direct-traffic-attributed).** Conversion rate is secondary (it tells you *why* RPV moved), bundle share of sales is tertiary.

**The break-even math (exact, verified fees):**

| | List | Net direct | Net Discover |
|---|---|---|---|
| Pack A | $9.99 | $8.49 | $6.99 |
| Pack B | $7.99 | $6.69 | $5.59 |
| Bundle A | $27.99 | $24.69 | $19.59 |
| Bundle B | $19.99 | $17.49 | $13.99 |

- Variant B pack must lift units **+26.9%** (direct) / **+25.0%** (Discover) just to match baseline RPV.
- Variant B bundle must lift units **+41.2%** (direct) / **+40.0%** (Discover) to match.

**Interpretation rule:** only claim "B wins" if variant blocks' combined RPV ≥ baseline blocks' combined RPV × 1.10 (a 10% confidence buffer). Between 0.9× and 1.1× = inconclusive → keep A (higher price loses less to fees). Below 0.9× → A clearly.

**Statistical honesty:** a two-proportion z-test needs ~6,700 visitors per arm to detect 4%→5% CR at 80% power. With 11 products × ~30 days, aggregate visitors may reach a few thousand *per product* at best if marketing is working. At realistic small-sample numbers:
- Compare **aggregated RPV across all 10 packs** (pooling 10 products multiplies the sample ~10×) rather than per-product.
- Treat a single variant win as directional, not significant; require the win in *both* B blocks (B₁ and B₂) before switching.
- If total visitors across the test < 2,000, declare the test underpowered and default to A (fees punish the lower price; the burden of proof is on B).

---

## 4. Decision rules — when to switch

At **Day 36** (after the second B block), compute for the pack tier and the bundle tier separately:

| Outcome (pooled RPV, B₁+B₂ vs A₁+A₂) | Decision |
|---|---|
| B ≥ 1.10 × A, and B₁, B₂ both individually ≥ A | **Switch to B permanently** ($7.99 / $19.99). Log the win. |
| 0.90 × A ≤ B < 1.10 × A | **Keep A** ($9.99 / $27.99). Inconclusive → higher price wins the fee argument. |
| B < 0.90 × A | **Keep A**, and record that lower price does not lift volume for this audience. |
| A₁ and A₂ differ by > 25% from each other | **Distrust all blocks.** Extend the test 4 more weeks (B-A-B-A) before deciding. |
| Total visitors < 2,000 across the test | **Keep A** by default; the test was underpowered. Focus energy on traffic, not price. |

Mid-test kill-switches:
- If either B block produces **zero sales across all products** while A blocks sold, halt the experiment, restore A prices, and investigate (listing broke? payment issue? traffic died?).
- If a refund spike appears (>15% of units), flag that block.

**Separate pack-tier and bundle-tier decisions:** the bundle can move to B while packs stay A, or vice versa. The bundle has the higher unit-lift hurdle (+40%), so the prior is "bundle stays at A ($27.99) unless the data is emphatic."

---

## 5. Measurement protocol (daily, 5 minutes)

Log one row per product per day into `marketing/gumroad-discover/pricing-log.csv`:

```csv
date,product,price,visitors,sales,cr,gross,net_direct,discover_sales,discover_gross,block,notes
2026-09-14,ai-coding-assistant-pack,9.99,34,1,2.9%,9.99,8.49,0,0,A1,launch day spike from reddit post
```

- Pull visitors + sales from **Gumroad Analytics → Products** (last 7 days view, daily granularity).
- Pull Discover-vs-direct split from **Analytics → Sales** by source where available.
- End-of-block ritual (each Monday): sum each block's rows, compute pooled RPV per tier, append to a running `BLOCK-SUMMARY` section at the bottom of this file (don't create a new doc per block).

**Attribution honesty:** Gumroad doesn't give referrer-level detail per sale; the protocol above is what its analytics support. Don't invent attribution.

---

## 6. Interaction with the launch codes

- **Week 1 (Days 1–7):** LAUNCH25 auto-applies at checkout. List prices show $9.99/$27.99 with the discount applied at checkout; the crossed-out display is a *promotional* crossed price, fine for launch week. This block is baseline-measurement only.
- **Days 8–35 (the experiment):** no active codes on any product (except the LOYALTY20 mechanics in CROSS-SELL-PLAN.md, which are gated by "Limit to existing customers" — they only fire for prior buyers, so they don't contaminate the cold-visitor price test... with one caveat: workflow emails carry the code link to existing buyers mid-test. Their purchases are a small fraction; log bundle sales via loyalty link in the notes column).
- **Day 36+:** winner prices revert/settle; flash codes may resume per the discount plan.

**Why auto-applied codes are not a valid A/B mechanism:** Gumroad applies the *larger* of stacked discounts and shows the original price crossed out — every visitor sees the same thing, so it randomizes nothing; it's a promo, not a test.

---

## 7. Pre-mortem — ways this test silently fails

1. **Price changed but checkout still shows old price** — always spot-check a product page in an incognito window after every Monday change.
2. **Discover switches on mid-block** — source mix shifts; flag and analyze direct-only.
3. **Marketing post goes viral on a B week** — B looks great for the wrong reason; check visitors in the block summary; if a block's visitors are >2× the adjacent block's, discount that block's evidence.
4. **Weekday drift from sloppy block boundaries** — always change price Monday 00:00 IST; if you're 12h late, note it and keep going, don't shift the whole calendar.
5. **Comparing gross instead of net on mixed sources** — direct sales keep 90%−$0.50; Discover keeps 70%. RPV comparisons use gross (same price shown either way); *net* comparisons only within one source.
6. **Bundle cannibalization misread as price effect** — if bundle share of units jumps in a B block, the bundle is eating pack sales; check pack-only RPV separately before concluding packs "won."
