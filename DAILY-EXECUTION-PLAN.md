# AI Prompt Store — 7-Day Launch Execution Plan

> **Goal:** Go from "code complete" to first paying customer in 7 days.
> **Constraint:** $0 upfront spend. Use existing assets only.
> **Start date:** 2026-08-22

---

## Day 1 — Fix & Polish (Today)

**Morning (2 h)**
- [ ] Fix `products/prompt-pack-1/README.md` — add proper description matching the other 9 packs
- [ ] Replace placeholder URLs in `website/index.html` and `marketing/*`:
  - `ai-prompt-store.example.com` → your actual domain or GitHub Pages URL
  - `YOURDOMAIN.com` → your actual domain
  - `https://<dc>.list-manage.com/...` → remove or replace with real email form
  - `https://app.convertkit.com/forms/...` → remove or replace
  - `https://buttondown.email/api/emails/` → remove or replace
  - `https://gum.co/prompt-pack-*` → these are fine as placeholders until Gumroad live
- [ ] Expand root `README.md` with project description, install/run steps, and revenue model

**Afternoon (2 h)**
- [ ] Create Gumroad account (gumroad.com)
- [ ] Create all 10 products + 1 bundle using `scripts/gumroad-products.json` as the source of truth
- [ ] Upload `products/prompt-pack-*/prompts.md` and `products/bundle-all-10-packs.zip`
- [ ] Verify prices: $9.99 each, $27.99 bundle

**Evening (1 h)**
- [ ] Deploy `website/` to Netlify / Vercel / GitHub Pages
- [ ] Test all buy buttons load (they will 404 until Gumroad is live — that's expected)
- [ ] Share draft link with 2-3 friends for quick feedback

**Deliverable:** Live website + Gumroad products created (not yet published)

---

## Day 2 — Publish & Seed Traffic

**Morning (1 h)**
- [ ] Publish all 11 Gumroad products (set to "public")
- [ ] Update website links if Gumroad assigns different URLs
- [ ] Enable Gumroad email notifications for new sales

**Afternoon (2 h)**
- [ ] Post in r/ChatGPT using `DAY-1-TRAFFIC.md` template
- [ ] Post in r/sideproject using `DAY-1-TRAFFIC.md` template
- [ ] Post in r/productivity using `DAY-1-TRAFFIC.md` template
- [ ] Submit Hacker News Show HN post

**Evening (1 h)**
- [ ] Publish LinkedIn post from `DAY-1-TRAFFIC.md`
- [ ] Post Twitter/X thread from `DAY-1-TRAFFIC.md`
- [ ] Post 3 Instagram captions from `DAY-1-TRAFFIC.md`

**Deliverable:** 6+ community posts live, products publicly purchasable

---

## Day 3 — Content & Social Proof

**Morning (2 h)**
- [ ] Record a 2-minute Loom/desktop demo showing the prompt packs in use
- [ ] Write a short case study: "How I used these prompts to write a YouTube script in 10 minutes"
- [ ] Add testimonial section to `website/index.html` (even if self-authored initially)

**Afternoon (2 h)**
- [ ] Publish first SEO blog post from `marketing/01-seo-blog-how-to-write-ai-prompts.md`
- [ ] Publish second SEO blog post from `marketing/02-seo-blog-50-chatgpt-prompts-content-creators.md`
- [ ] Set up a free GitHub Pages blog or publish on Medium/Dev.to

**Evening (1 h)**
- [ ] Engage with every comment on Day 2 posts (reply within 1 hour of any notification)
- [ ] Identify which post got the most clicks; note the channel

**Deliverable:** 2 blog posts published, demo video recorded, social proof section added

---

## Day 4 — Double Down on Best Channel

**Morning (1 h)**
- [ ] Check Gumroad analytics: which product got the most views?
- [ ] Check website analytics (if any): which traffic source converted?

**Afternoon (2 h)**
- [ ] Post in 5 additional subreddits relevant to the best-performing niche
- [ ] Post in 3 Facebook/Discord groups for AI creators
- [ ] Create a short-form video (TikTok/Reels/Shorts) from `marketing/21-tiktok-video-concepts.md`

**Evening (1 h)**
- [ ] Write and publish email-capture landing page (`marketing/22-email-capture-landing-page.md`)
- [ ] Add email capture form to website header

**Deliverable:** Best channel amplified, email list building started

---

## Day 5 — Outreach & Partnerships

**Morning (2 h)**
- [ ] Identify 10 micro-influencers in AI/creator space (1k-50k followers)
- [ ] Draft personalized outreach offering free bundle for honest review
- [ ] Send 5 outreach emails/DMs

**Afternoon (2 h)**
- [ ] Reach out to 3 AI newsletter writers with a free pack + exclusive discount for their readers
- [ ] Post the influencer outreach template in `marketing/customer-testimonial-template-pack.md` as a ready-to-use asset

**Evening (1 h)**
- [ ] Create a simple affiliate landing page or Google Sheet to track referrals
- [ ] Respond to any inbound interest from Day 1-4 posts

**Deliverable:** 5 influencer outreaches sent, 3 newsletter pitches sent

---

## Day 6 — Paid Boost (Optional, $50)

**Morning (1 h)**
- [ ] If you have $50 to spend, run a Reddit promoted post in r/ChatGPT or r/productivity
- [ ] Target: people interested in AI, ChatGPT, productivity tools
- [ ] Budget: $25 Reddit + $25 Facebook/Instagram

**Afternoon (2 h)**
- [ ] A/B test landing page headline: try "500+ Expert AI Prompts" vs "Supercharge Your AI Workflow"
- [ ] Update `website/index.html` with winner after 4 hours of data

**Evening (1 h)**
- [ ] Analyze all traffic sources from the past 6 days
- [ ] Document top 3 converting channels in a new `marketing/traffic-analysis-day-6.md`

**Deliverable:** Paid campaign live (if budget allows), landing page optimized

---

## Day 7 — Review, Optimize & Scale

**Morning (1 h)**
- [ ] Review all metrics: visits, conversion rate, revenue, email signups
- [ ] Calculate cost per acquisition (CPA) and lifetime value (LTV)

**Afternoon (2 h)**
- [ ] Update product descriptions on Gumroad based on customer questions/feedback
- [ ] Add 5-10 new prompts to the most popular pack based on user requests
- [ ] Publish a "Week 1 Recap" blog post or Twitter thread showing early results

**Evening (1 h)**
- [ ] Plan Week 2 priorities:
  1. Launch affiliate program (30% commission)
  2. Create 3 more YouTube short-form videos
  3. Build email sequence for new subscribers
- [ ] Celebrate the first sale (if any). If none, adjust pricing or messaging for Week 2.

**Deliverable:** Week 1 metrics documented, Week 2 plan locked, first optimizations shipped

---

## Success Metrics

| Metric | Target | Stretch |
|--------|--------|---------|
| Website visits (Day 7) | 100+ | 500+ |
| Sales (Day 7) | 1-2 | 5+ |
| Revenue (Day 7) | $10-$20 | $50+ |
| Email subscribers | 10+ | 50+ |
| Community posts published | 6+ | 10+ |
| Blog posts published | 2+ | 4+ |

---

## Risk Register

| Risk | Mitigation |
|------|-----------|
| No sales by Day 3 | Drop price to $4.99 for 24 hours, post in more communities |
| Gumroad approval delay | Have GitHub + PayPal fallback ready |
| Website breaks on mobile | Test on iPhone/Android before Day 2 posts go live |
| Placeholder links confuse buyers | Fix all YOURDOMAIN.com links on Day 1 before publishing |
| Burnout | Time-box every block to 2h max; protect evenings |

---

## Files Referenced

- `DAY-1-TRAFFIC.md` — Ready-to-post copy for Reddit, HN, LinkedIn, Twitter, Instagram
- `LAUNCH-GUIDE.md` — 15-day strategic overview
- `GUMROAD-SETUP.md` — Step-by-step Gumroad product creation
- `scripts/gumroad-products.json` — Source of truth for all 11 products
- `marketing/` — 27 marketing assets (blogs, scripts, carousels, templates)
- `products/` — 10 prompt packs + bundle ZIP
