# dev.to Article — Outline + Draft Skeleton

**Angle:** the teach-first article. dev.to rewards genuinely useful tutorials and punishes marketing. The product appears once, at the end, clearly disclosed. This article stands 100% alone without it.

**Title:** "The Fill-in-the-Blank Method: 5 AI Prompt Templates I Actually Reuse (and How to Build Your Own)"

**Format notes:**
- 1,200–1,800 words. dev.to sweet spot.
- Code blocks for every template (dev.to audience expects copy-paste).
- Write it in first person, specific, no AI-marketing voice.
- Tags: `ai`, `productivity`, `chatgpt`, `promptengineering`, `beginners` (5 max).
- Posting window: Tue/Wed 9 AM US Eastern works well for dev.to.
- No numbers you can't defend: no "3x better output," no fake test results. First-person experience only.

---

## OUTLINE

### H2: Intro — the re-typing problem (150 words)
- Hook: "Every Monday I'd catch myself rebuilding the same prompts from scratch."
- The realization: the problem wasn't prompt knowledge, it was prompt *retention*.
- Promise of the article: 5 templates that survived a year of real use + the method for building your own.
- What this article is NOT: not advanced prompt engineering, no magic phrases, nothing you need a course for.

### H2: Why fill-in-the-blank templates work (250 words)
- The theory everyone knows: role, context, constraints, examples, output format.
- The practice nobody does: re-deriving that structure from scratch every time means you skip half of it when busy.
- The template fix: pre-bake the structure, leave holes for context.
- The [BRACKET] placeholder as a forcing function: you can't skip context that has a labeled hole.
- One paragraph on limits: templates are for *recurring* tasks; one-offs still need ad-hoc prompting.

### H2: Template 1 — The weekly review (200 words)
- Full template in a code block (from the productivity pack):

```
Act as my weekly review partner. I'll paste my notes from the week: [PASTE NOTES].
1. Summarize what moved forward vs. what stalled.
2. Identify the one decision I'm avoiding.
3. Draft next week's top 3 priorities based on the above.
```

- Why line 2 is the trick: to-do lists organize decided work; this surfaces the undecided work.
- Honest limitation: uncomfortable, not magic, 20 minutes.

### H2: Template 2 — The debugging prompt (200 words)
- Full template in a code block (from the coding pack):

```
Debug this code: [CODE + FULL ERROR MESSAGE].
Here's what I already tried: [LIST].
Expected behavior: [WHAT IT SHOULD DO].
```

- Why "what I already tried" matters: skips the obvious suggestions you ruled out; the model starts at the real diagnosis.
- Example follow-up: "now propose 3 hypotheses ranked by likelihood, and one test for each."

### H2: Template 3 — The script/content outline (200 words)
- Full template (from the content pack):

```
Write a 10-minute script about [TOPIC] with a hook, intro, 3 main points, and a call to action. Audience: [WHO]. Tone: [TONE].
```

- The upgrade follow-up: "give me 3 hook options for the first 15 seconds" → pick → "rewrite the intro around option 2."
- Why this generalizes: swap "script" for "blog post" / "webinar" and the structure holds.

### H2: Template 4 — The email welcome sequence (150 words)
- Full template:

```
Write a 5-email welcome sequence for [BUSINESS TYPE].
Product: [ONE-LINE DESCRIPTION].
Who it's for: [AUDIENCE].
Tone: match this: [PASTE 2-3 SENTENCES OF YOUR OWN WRITING].
```

- "Match this" beats every tone adjective — show, don't describe.

### H2: Template 5 — The decision matrix (150 words)
- Full template:

```
Create a decision matrix for [DECISION].
Options: [LIST THEM].
Criteria: [WHAT MATTERS, ROUGHLY WEIGHTED].
Present as a table and tell me which option wins — and where the weighting is doing all the work.
```

- The last clause is a built-in bias check: it exposes when you weighted criteria to get the answer you wanted.

### H2: How to build your own template (the actual method) (250 words)
- Step 1: Notice repetition — any prompt you've typed twice in a month.
- Step 2: Extract the stable part (structure) from the variable part (your context).
- Step 3: Bracket the variables. Name them descriptively ([AUDIENCE], not [X]).
- Step 4: The 4-week test — only prompts that survive a month graduate to the file.
- Step 5: Store them anywhere boring (a markdown file, a notes app). Boring storage is a feature.
- Where people fail: templating one-off tasks, and abandoning the rotation file after week 2.

### H2: Closing — the rotation is the asset (100 words)
- Templates compound; scattered prompts don't.
- One-line soft CTA, fully disclosed:
  > "I collected 500+ of these into 10 themed packs and sell them at https://abhishekanandsupreme-rgb.github.io/ai-prompt-store/ ($9.99 a pack, $27.99 for all 10) — but the five above and the method are the whole idea, and they're yours either way."
- Final line = a genuine question to drive comments: "What's the one prompt you've re-typed the most? I'll go first: the weekly review."

---

## Publication checklist

- [ ] Every template copy-pasteable in a code block (dev.to renders ``` fences).
- [ ] No invented metrics anywhere. First-person experience phrasing only ("I've", "in my rotation").
- [ ] Product mentioned once, in closing, disclosed.
- [ ] Answer every comment in first 24h — dev.to's comment culture is the growth engine.
- [ ] Add the canonical-series hook: "This is part of my build-in-public notes" if you plan a follow-up article (e.g., "The $0 Stack: Shipping a Product with No Software Budget").
- [ ] Cross-link from the article ONLY in this order: dev.to article → landing page. Do not link the article from Reddit posts (mods treat it as link-dodging).
