---
title: "I Wrote 500+ AI Prompts — Here's the Anatomy of the Ones That Actually Work"
published: false
tags: [ai, chatgpt, programming, productivity, sideproject]
description: "I built a prompt pack store and had to write 500+ prompts to fill it. This is the anatomy of the ones that worked — plus 7 frameworks and 8 real prompts you can copy today."
---

Every prompt-writing guide gives the same advice: give the AI a role, add context, specify the format. Then most of us open ChatGPT anyway and type "fix this bug."

I know, because that was me — until I started writing prompts on purpose. I recently built a small store that sells themed packs of AI prompts, which meant sitting down and producing 500+ of them, testing each one, and keeping only the prompts that earned their place. The ones that made the cut weren't the cleverest or the longest. They were the ones with a specific, boring structure.

This article is that structure, taken apart: the anatomy of a prompt that works, the seven frameworks I kept reaching for, and eight real prompts from my packs — quoted exactly as they ship — that you can copy and steal today.

## The anatomy of a prompt that works

The most useful thing I learned from writing hundreds of prompts: a good prompt isn't a sentence, it's a specification. Every prompt that survived my testing had four parts — **role, context, task, format** — whether or not I'd set out to include them.

Here's one from my Content Creator pack, exactly as it ships:

```text
You are a professional YouTube scriptwriter. Write a [LENGTH]-minute script for a video about [TOPIC] aimed at [AUDIENCE]. Structure: 0-15s hook (the payoff, teased, no channel intro), intro (why watch to the end), 3 main points with a pattern-interrupt every 90 seconds, and a CTA that promises value ('subscribe because next week I'm covering X'). Write it in spoken language - short sentences, contractions, one idea per breath. Include B-roll and on-screen text cues in brackets.
```

Take it apart and the four parts are easy to see:

- **Role** — "You are a professional YouTube scriptwriter." This sets the vocabulary, the defaults, and the standard the model measures itself against. It's the difference between output written *about* scripts and output written *by* someone who writes them.
- **Context** — a `[LENGTH]`-minute video, about `[TOPIC]`, aimed at `[AUDIENCE]`. This is the part that's different every time you use the prompt — which is exactly why it's a bracketed hole instead of baked-in text.
- **Task** — "Write a script." One verb, one deliverable. Prompts that ask for three things at once get three mediocre things.
- **Format** — the structure spec (hook, intro, three points, CTA), the style rules (spoken language, short sentences, one idea per breath), and the bracketed B-roll cues. This is where most people stop early, and it's the part that does the most work.

The same skeleton shows up in the developer-focused prompts. Here's the code review prompt from my Coding Assistant pack, also verbatim:

```text
You are a staff engineer doing code review. Review this pull request: [PASTE DIFF]. Categorize findings as blocking, important, or nit. For each: line reference, reasoning grounded in maintainability or correctness, and a suggested fix. End with what the author did well - be specific.
```

Role: staff engineer. Context: the pasted diff. Task: review it. Format: three severity buckets, line references, reasoning, a suggested fix — and, the part most people never think to ask for, ending with what the author did well.

Notice what the format clause buys you in both cases. "Categorize findings as blocking, important, or nit" isn't decoration — it's a schema. It forces the model to make a judgment call per finding instead of listing everything with equal weight, which is what makes the output actually usable in a PR comment.

## The 7 prompt frameworks I kept reaching for

When you write prompts at scale, patterns get obvious fast. Seven structures showed up in almost everything that survived testing. None of them are inventions of mine — they're the standard frameworks — but here's the version of each I actually use:

### 1. Role-Context-Task

The base skeleton from the anatomy above, and the opening move of most prompts in my packs:

```text
Act as a [ROLE] with expertise in [DOMAIN].
Context: [BACKGROUND INFORMATION]
Task: [SPECIFIC ACTION YOU WANT]
```

### 2. Few-shot prompting

Paste two or three examples of the input and output you want, then your real input. This beats any tone adjective — "make it witty" is vague, one witty sample is a spec. It's the framework I reach for whenever tone matters more than information.

### 3. Chain-of-thought

Ask the model to walk through its reasoning *before* giving the final answer. For anything high-stakes — architecture decisions, spending decisions — you want auditable logic, not just a confident conclusion.

### 4. Persona-Audience-Goal

The content-flavored sibling of Role-Context-Task: whose voice, which reader, and what that reader should do afterward. Three things generic prompts almost never specify.

### 5. Constraint + Format

Guardrails make output more usable, not less: length limits, what to avoid, and the exact shape of the result — table, list, diff, email. Nearly every prompt in my packs ends with a format clause for this reason.

### 6. Self-review

The cheapest quality upgrade there is: after the first draft, ask the model to critique its own output — what's missing, where it's vague, what a skeptical reader would push back on — then rewrite. One extra round-trip, noticeably better result.

### 7. Reverse prompting

When something works — a script that performed, a page that converted — paste it back in and ask the model to derive the reusable template: the role, the structure, the constraints that made it good. It's how a one-off success becomes a repeatable one.

Good prompts stack two or three of these. The YouTube prompt is Role-Context-Task plus Constraint + Format. The code review prompt is Role-Context-Task plus a schema. Self-review chains onto anything.

## Six more real prompts, verbatim

The two prompts above come from my packs. Here are six more, exactly as they ship, with the one detail I'd point out in each.

### The debugging diagnosis (AI Coding Assistant pack)

```text
You are a debugging specialist with 15 years of experience in [LANGUAGE]. I get this error: [PASTE ERROR/STACK TRACE] when running [PASTE CODE OR DESCRIBE]. List the 5 most likely root causes ranked by probability, the fastest diagnostic step for each, and the fix for the most likely one.
```

"Ranked by probability" is the whole trick. It converts the model's default behavior — one plausible guess, delivered confidently — into a differential diagnosis, and pairs each cause with the cheapest way to confirm or kill it.

### The edge cases you'd otherwise ship (AI Coding Assistant pack)

```text
Act as a QA edge case generator. For this feature: [DESCRIBE FEATURE], generate 20 test scenarios a junior QA would miss: unicode, timezones, concurrency, offline behavior, permission boundaries, and data volume. Prioritize the 5 that would cause the worst production incidents.
```

Asking for the scenarios "a junior QA would miss" aims the model directly at its strength — finding blind spots — and the prioritization clause keeps you from drowning in twenty equal test cases.

### Refactoring with a contract (AI Coding Assistant pack)

```text
Act as a clean code specialist. Refactor the following [LANGUAGE] code to improve readability and maintainability without changing behavior: [PASTE CODE]. Apply single-responsibility, meaningful names, and guard clauses. Present a before/after diff summary and explain each change in one line.
```

"Without changing behavior" is the contract. Refactor prompts that omit it will happily "improve" your code into different code.

### The welcome email sequence (AI Content Creator pack)

```text
You are an email marketing strategist. Write a 5-email welcome sequence for [BUSINESS TYPE] selling [PRODUCT] to new subscribers: email 1 (deliver the promise + origin story), 2 (best content), 3 (the pain and the shift), 4 (the offer with proof), 5 (the honest close). Each with subject line, preview text, 150-250 word body, one CTA. Warm, direct, zero hype.
```

The parenthetical arc per email is the format clause doing double duty: it specifies both the shape of each email and the emotional sequence across the five. "Zero hype" is a constraint that actually changes the output.

### The first-page edit (AI Writing Assistant pack)

```text
Act as a first-page doctor. Here is my opening: [PASTE FIRST 500 WORDS]. Evaluate against what agents check in the first page: character, voice, problem, world clarity, and promise. Cut anything before the first intriguing line, and offer 3 alternative first lines from later in my draft.
```

Borrowing a professional's checklist — what literary agents actually look at — gives the model a concrete rubric instead of a vague "make it better."

### Deciding between two options (AI Productivity pack)

```text
Act as a decision-making specialist. I'm torn between [OPTION A] and [OPTION B] for [DECISION CONTEXT]. Build my decision process: criteria that matter (weighted), score both options, list what would change my mind, and identify reversible vs. irreversible. If it's reversible, tell me the fast way to test it.
```

The last two clauses are the adults-in-the-room part: "what would change my mind" exposes a decision you've already made in disguise, and reversible-vs-irreversible tells you whether you should be deliberating at all.

## How to build your own

The method, if you'd rather make your own than steal mine:

1. **Notice repetition.** Any prompt you've typed twice in a month is a candidate.
2. **Split the stable from the variable.** The structure stays the same every time; your situation is the part that changes.
3. **Bracket the variables, descriptively.** `[AUDIENCE]`, not `[X]` — a labeled hole forces you to supply the context you'd otherwise skip.
4. **Run the four-week test.** Only prompts that survive a month of real use graduate to your permanent file. Most won't.
5. **Store them somewhere boring.** A markdown file, a notes app. Boring storage is a feature: it's searchable, and it never locks you in.

## What writing 500+ prompts taught me

- **Fill-in-the-blank beats clever phrasing.** The value isn't in the words — it's in the holes that force you to fill in role, context, and format every single time.
- **Constraints make output better, not narrower.** Every "under 60 characters," "without changing behavior," and "zero hype" clause sharpened the results in a way no amount of polite asking did.
- **The survivors share structure, not cleverness.** When I looked at what made the final cut across ten packs, the pattern wasn't a secret phrase or a trick. It was the four-part skeleton, applied without exception.

## The honest closing

Everything above is the method. You never need to buy anything from me to use any of it. That said, full disclosure: I compiled 500+ of these into 10 packs and I do sell them — $9.99 per pack, $27.99 for the bundle. If you'd rather judge the quality first, the **[free 15-prompt sampler is here](https://abhishekanandsupreme-rgb.github.io/ai-prompt-store/free-teaser.md)**, and the **[full store is here](https://abhishekanandsupreme-rgb.github.io/ai-prompt-store/)**. The eight prompts in this article, the anatomy, and the frameworks are the whole idea — they're yours either way.

This is one of my build-in-public notes; if a follow-up on shipping this entire store with a $0 software budget would be useful, say so in the comments.

What's the one prompt you've re-typed the most? I'll go first: the debugging one — five likely root causes, ranked.

<!-- ================================================================
EDITOR NOTES — DELETE THIS BLOCK BEFORE PUBLISHING TO DEV.TO
================================================================

1. COVER IMAGE (1000x420, dev.to cover ratio)
   Concept: split-frame, dark terminal/editor aesthetic to match dev.to's UI.
   - LEFT half: a plain gray one-line prompt ("fix this bug") with a red strike-through.
   - RIGHT half: the same intent rebuilt as a structured prompt block with four
     color-coded labeled sections: ROLE / CONTEXT / TASK / FORMAT.
   - Arrow connecting the two halves. Indigo/violet accents (matches the store brand).
   - Keep on-image text under 6 words (e.g. "same question, better prompt").
   - Avoid stock clichés: no robots, no brains, no handshakes, no sparkles.
   1000x420 PNG; readable at 50% zoom (it appears small in the feed).

2. PUBLISHING
   - Window: Tue or Wed, ~9 AM US Eastern (dev.to peak traffic).
   - Front matter above is dev.to-ready: title, tags, description (description shows
     in meta previews; keep under 200 chars — it is).
   - Leave published: false until the cover image is uploaded and links are
     clicked through once (sampler + store both resolve).
   - Do NOT set canonical_url unless the article is republished elsewhere first.

3. AFTER PUBLISHING
   - Answer every comment in the first 24 hours — dev.to's comment culture is
     the growth engine.
   - Do not link the article from Reddit posts (mods read it as link-dodging);
     link only dev.to article -> store, as done here.

4. HONESTY CHECK (already enforced in the draft)
   - No user counts, no revenue claims, no testimonials — the store is brand new.
   - The only numbers in the article: prompt counts (500+, 10 packs, 50/pack),
     prices ($9.99 / $27.99), and prompt-internal numbers quoted from the packs.
   - All 8 quoted prompts are verbatim from the pack files (verified programmatically).
================================================================ -->
