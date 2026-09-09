# TRACKING.md — Live Launch Measurement & Decision Rules

Update this file daily during the 7-day blitz (see `7DAY-CALENDAR.md`). Fill the tables with REAL numbers only — never estimated, never projected. An empty cell is data ("no traction"); a made-up cell is poison.

---

## 1. What to measure (per channel)

| Channel | Views/Impressions | Clicks (to landing/Gumroad) | Sales | Free-value signal (engagement) | Where the data lives |
|---|---|---|---|---|---|
| Reddit (per sub) | Upvotes (proxy), post views (Reddit app) | Clicks via landing-page referrer | Sales with UTM tag | Comments, DM requests | Reddit app + referrer log + Gumroad |
| X/Twitter | Impressions, profile visits | Link clicks (X analytics) | Sales with UTM | Replies, reposts, bookmarks | X Analytics (needs a few days of history) |
| LinkedIn | Post impressions | Clicks (LinkedIn shows if link post) | Sales with UTM | Comments, reshares | LinkedIn analytics |
| Instagram | Reach | Bio-link taps | Sales with UTM | **Saves** (primary), comments, shares | IG Insights |
| Hacker News | Points, comments | Clicks via referrer | Sales with UTM | Comment quality | news.ycombinator.com thread |
| dev.to | Views, reactions | Clicks via referrer | Sales with UTM | Comments | dev.to dashboard |

**UTM tags — set these up on Day 0 (before the first post):** append to the landing URL so Gumroad/referrer data separates channels. e.g.:
- `https://abhishekanandsupreme-rgb.github.io/ai-prompt-store/?utm_source=reddit&utm_medium=r_chatgpt`
- `?utm_source=x&utm_medium=thread1` · `?utm_source=linkedin&utm_medium=post1` · `?utm_source=hn&utm_medium=show_hn` · `?utm_source=instagram&utm_medium=bio_link` · `?utm_source=devto&utm_medium=article`

If a platform forbids/uglifies links (Reddit r/productivity, r/SideHustle — no links allowed), that channel is measured by DM requests + word-of-mouth only. Note it; don't fake attribution.

**Gumroad dashboard:** Analytics → sales + views per product. Gumroad's own product-page views also tell you which pack people check after landing (e.g. bundle vs coding pack).

**Fallback if no analytics history exists:** use Gumroad "views" per product page as the click proxy, and ask buyers (Gumroad lets you email them) "where did you find us?" — 3 answers is enough signal at this scale.

---

## 2. Daily log (fill during the week)

| Day | Channel/asset | Views | Clicks | Sales | Engagement (upvotes/replies/saves) | Notes (mods, feedback, objections heard) |
|---|---|---|---|---|---|---|
| 1 | r/ChatGPT — `reddit/01` | | | | | |
| 1 | X Thread 1 — `social/01` | | | | | |
| 1 | IG Carousel 1 — `social/04` | | | | | |
| 2 | r/productivity — `reddit/05` | | | | | |
| 2 | LinkedIn Post 1 — `social/02` | | | | | |
| 3 | X Thread 2 | | | | | |
| 3 | r/sideproject — `reddit/02` | | | | | |
| 3 | IG Carousel 2 | | | | | |
| 4 | LinkedIn Post 2 | | | | | |
| 4 | X single (Friday prompt) | | | | | |
| 4 | dev.to article | | | | | |
| 5 | X Thread 3 ($0 stack) | | | | | |
| 5 | IG Carousel 3 | | | | | |
| 6 | HN Show HN — `social/hn` | | | | | |
| 6 | r/ArtificialInteligence — `reddit/03` | | | | | |
| 6 | LinkedIn Post 3 | | | | | |
| 7 | r/SideHustle — `reddit/04` | | | | | |
| 7 | X deep-dive (winner theme) | | | | | |

---

## 3. Unit economics (fixed — use for all ROI math)

- Pack price: $9.99 → Gumroad fee 10% + $0.50 ≈ $1.50 → **net ≈ $8.49/pack**
- Bundle: $27.99 → fee ≈ $3.30 → **net ≈ $24.69/bundle**
- Ad spend: $0 (organic only) → any sale is positive ROI; the real cost is time.

---

## 4. Decision rules — doubling down, Week 2

Apply at the Day-7 review. Ranked by strongest signal first; take the first rule that fires.

1. **Channel fires (double down):** any channel produces ≥1 sale OR ≥2 DM/purchase-intent signals (e.g., "where can I buy this", "what's the bundle link") with ≥500 views → double down: repeat the *winning content angle* on that channel in Week 2 (new body, same theme), and raise posting frequency there from 1x to 2–3x/week.
2. **Angle fires across channels (scale the angle):** one theme (Friday prompt / technique-vs-template / $0 stack) appears in ≥2 channels' top engagement slots → that theme becomes the Week-2 flagship everywhere + gets a dedicated landing-page section or new pack positioning.
3. **Views but no clicks (fix the CTA, not the content):** channel shows ≥1,000 views but <1% click-through → the value worked, the bridge didn't. Test a different CTA placement (e.g., pinned comment vs final tweet; landing-page hero copy) before spending more content there.
4. **Clicks but no sales (fix the page):** landing-page referrer shows ≥50 clicks but 0 purchases → problem is the landing page or offer, not distribution. Ship the r/sideproject feedback fixes first; re-run the same channel after.
5. **Dead channel (pause, don't kill):** <100 views after 2 quality posts on that channel → deprioritize for 2 weeks; don't delete accounts; note the cause (wrong audience vs bad timing vs rule-blocked).
6. **Mod removal / flag:** any removed post → never repost the same body; log which rule it hit; that sub waits ≥30 days and returns with a value-only, zero-link post.
7. **Zero sales anywhere after Day 7:** do not conclude "product is dead" — at this sample size, traffic is the bottleneck, not demand. Week 2 = new angles (SEO posts, YouTube from `marketing/06–07`, a second Show HN via Draft 2) before any pricing/packaging change.

**Weekly review questions (answer in writing, Day 7):**
1. Which single asset drove the most engagement, and was it the one we expected?
2. What objection came up most in comments (e.g., "prompts are free everywhere")? → that's the next content angle's opening line.
3. Which pack did people actually click on Gumroad (single pack vs bundle)? → Week 2 lead product.
4. What did we promise in posts that the landing page doesn't show? → fix the page, not the posts.

---

## 5. Honesty rules for this file

- No estimated numbers. If analytics aren't available yet, write "n/a (analytics lag)".
- Don't count DMs that were answered with "not interested."
- If a metric would make us look bad, it gets written down anyway — that's the whole point of tracking.
- Sales numbers here are internal; never quote them in marketing posts unless they're real and you'd show the Gumroad dashboard.
