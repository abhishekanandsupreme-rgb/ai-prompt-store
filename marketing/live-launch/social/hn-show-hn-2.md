# Hacker News — 2 "Show HN" Drafts + Comment Strategy

## HN rules & norms (read before posting — HN is the harshest room you'll enter)

- **Show HN posts are for something people can try.** A paid product with a free landing page is acceptable *if the landing page itself demonstrates value* — HN hates paywalled "show me" posts. Lead with what's free and visible.
- **No promotional sockpuppeting, no voting rings.** Do not ask anyone to upvote. Ever. HN detects and hellbans for it.
- **Title rules:** Show HN titles must state what it is, plainly. No clickbait, no taglines in the title, no "revolutionary." Title ≤ 80 chars.
- **First comment is yours:** post a top-level comment immediately with build details/stack — HN expects the maker in the thread, and "why did you build this" answered fast buys goodwill.
- **Post Tue–Fri morning US Eastern (8–11 AM)**; weekends get less traffic but gentler crowds. Avoid Monday.
- **The product story must be verifiable.** No revenue claims unless you'll show receipts. The $0-stack story is safe because every element is checkable (the site is on github.io; Gumroad fees are public).
- Do not use the word "we" if you're one person. HN smells it instantly.

---

## DRAFT 1 — "Show HN: AI Prompt Store – 500+ fill-in-the-blank prompt templates"

**Title:**

> Show HN: AI Prompt Store – 500+ fill-in-the-blank prompt templates

**URL:** https://abhishekanandsupreme-rgb.github.io/ai-prompt-store/

**Your first comment (post within 2 minutes of submitting):**

> Maker here. What it is: 10 themed packs of fill-in-the-blank prompt templates (content, coding, marketing, productivity, SEO, business, writing, social, entrepreneurship, education) — ~50 per pack, sold as markdown files on Gumroad at $9.99/pack or $27.99 for the bundle.
>
> Why markdown: buyers of prompts want copy-paste, not a designed PDF. It's also version-controlled, so updates ship via Gumroad re-download.
>
> Landing page is hand-written HTML on GitHub Pages; Gumroad handles payments (their fee is 10% + $0.50/sale — so ~$1.50 on a pack). Total software spend $0.
>
> I know the objections: "prompts are free everywhere," "prompt packs are snake oil," "a template is just a prompt with brackets." Fair. My argument: the value isn't in any single prompt — it's in the rotation, the pre-baked structure that makes you hand over context you'd otherwise skip. I'll post three examples below in replies; judge the content, not the wrapper.
>
> Happy to answer anything about the build or the pricing.

**Anticipated objections → prepared answers (post as replies to each objection, calmly, no defensiveness):**

1. **"All prompts are free on the internet / you're selling what ChatGPT gives away"**
   → "True for any single prompt. What you're buying is curation and organization — 500 arranged by task, deduplicated, formatted consistently. Same reason people buy recipe books. If that's not worth $9.99 to you, genuinely fair — the three examples I posted are free and complete."

2. **"Prompt packs are the 2026 version of get-rich-quick ebooks"**
   → "Most are, and I can't prove mine isn't with a comment. The site shows exactly what each pack contains before purchase, and Gumroad refunds are a thing. If you buy and it feels thin, refund it — I'd rather that than a bad review."

3. **"Markdown is a lazy product format"**
   → "It was a deliberate choice — the only feature a prompt product needs is copy-paste, and .md does that natively. I'd take counterarguments on PDF, genuinely."

4. **"Why is the landing page on github.io instead of a real domain?"**
   → "$0 stack, and GitHub Pages is fast and HTTPS by default. A custom domain is on the list for after the product proves demand. This is the order I think more first products should follow."

5. **"Your examples are obvious/basic"**
   → "Some of the best ones are obvious — that's the point. The surprising ones are boring, like the weekly review prompt. Obvious-to-you is fine; the packs are for people who don't want to build the rotation themselves."

**Do NOT:**
- Reply to every negative comment in the first 30 minutes (looks desperate). Prioritize: substantive technical questions → objections with engagement → rest.
- Delete or downvote critics. HN users check comment histories; a maker who edits/deletes is dead on arrival.

**Success signal:** ~10 points and a real conversation = success for a first Show HN, even with zero sales. 2–5 points = normal. Getting flagged = learn from the thread's objections, fix, re-post as a different angle in 2+ weeks.

---

## DRAFT 2 — "Show HN: I shipped a digital product on a $0 stack (markdown + GitHub Pages + Gumroad)"

*Different angle: the build story, not the product. Post this only if Draft 1 stalled or got flagged — at least 1–2 weeks later. The product is the example in a process story, which HN tolerates far better.*

**Title:**

> Show HN: I shipped a digital product on a $0 stack (markdown + GitHub Pages + Gumroad)

*(HN allows text/self posts for Show HN when the interesting part is the story; if a link is required, link the landing page and put the process in the first comment.)*

**First comment (the actual content — this is the post):**

> Details of the $0 stack, since that's the interesting part:
>
> — Product: plain markdown files, one per pack. 500+ prompt templates across 10 themes.
> — Landing page: hand-written static HTML, one page, no framework, no build step.
> — Hosting: GitHub Pages. Free, fast, HTTPS by default, deploys are `git push`.
> — Payments + delivery + refunds: Gumroad. 10% + $0.50 per sale. On $9.99 that's ~$1.50; on the $27.99 bundle ~$3.30. No monthly fee = no burn while you find out what sells.
>
> What the stack deliberately does NOT have:
> — No email capture (no backend). This is the biggest gap; I'd fix it before scaling.
> — No upsell flow, no A/B tests, no analytics beyond basics.
>
> My claim isn't that this stack scales — it's that it validates. The failure mode I see in first-time builders is spending 3 weekends on infrastructure before anyone has said "I'd buy that."
>
> The landing page is here: https://abhishekanandsupreme-rgb.github.io/ai-prompt-store/ — judge the design honestly, that's the part I most want feedback on.
>
> Ask me anything about the stack. The stack is free forever; the prompts are what I sell.

**Objection prep specific to this angle:**

1. **"This isn't Show HN material, it's a blog post"**
   → "Fair. I read Show HN as 'something people can look at and discuss' — the site's live and that's what's up for discussion. If mods disagree I'll take it as a lesson."

2. **"You're using a 'process' post to sell a product — this is stealth marketing"**
   → "Guilty of selling a product, yes — disclosed in the first comment, and the process details are complete whether or not anyone buys. If the mods want the product mention removed I'd genuinely comply."

3. **"Gumroad's fees are too high / you should roll your own checkout"**
   → "10% + $0.50 is high vs. raw Stripe (~3% + $0.30), but Stripe means I'm building checkout, delivery, refunds, and PCI compliance instead of shipping. The fee is the cost of not building that yet. At this stage that trade is correct."

4. **"Prompts expire — model updates break them"**
   → "Fill-in-the-blank templates are more durable than magic-phrase prompts because they encode task structure, not incantations. But point taken — 'lifetime updates' in the listing needs me to actually maintain it."

**Same discipline as Draft 1:** answer calmly, never pile-on-reply, never ask for upvotes, disclose you're the maker in the first comment (not buried).

---

## Why two drafts

- Draft 1 (product-first) is honest and direct — the best chance at real feedback, the bigger flag risk.
- Draft 2 (process-first) is the fallback with higher survival odds — HN likes build stories more than products, and the $0-stack angle gives technical readers something to chew on.
- **Post at most one.** Never both. And never re-post the same draft if flagged — that's how accounts get hellbanned.
