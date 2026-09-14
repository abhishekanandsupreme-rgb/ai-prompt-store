# AI Finance Prompt Pack — 40 Expert Prompts
## Analysis, FP&A, Lending, Risk, Tax & Corporate Finance

> Copy-paste ready. Replace [BRACKETS] with your details. Works with ChatGPT, Claude, Gemini, or any LLM. For educational and drafting use — not individualized financial advice.

---

## Financial Analysis & Reporting (Prompts 1–5)

### 1. The Financial Statement Analysis
```
You are a senior financial analyst at a top-tier bank who writes analyses that actually get read by decision-makers. Analyze the financial statements for [COMPANY NAME] for [DATE RANGE]: [PASTE OR DESCRIBE STATEMENTS — revenues, costs, margins, debt, cash]. (1) Calculate and interpret: revenue growth, gross margin, operating margin, ROE, and current ratio — with the benchmark range for [INDUSTRY] and where this company sits, (2) identify 3 strengths — each tied to a specific number, (3) identify 3 risks — each with the trend that would confirm it's worsening. Format: a ratio table with a 2-year comparison column, then the findings as short narrative paragraphs. Rule: every claim points to a specific line item — no generic "strong liquidity" without the ratio behind it.
```

### 2. The Variance Analysis Report
```
Act as an FP&A manager presenting to a CFO who hates surprises. Write the variance analysis for [DEPARTMENT/PRODUCT] in [PERIOD]: actuals [PASTE ACTUALS] vs. budget [PASTE BUDGET]. (1) The summary table: top 5 variances by absolute dollar impact, each flagged favorable/unfavorable, (2) the narrative per variance: the driver — what actually caused it, not just "spending was higher", (3) the "so what" for next quarter: the corrective action, the leading indicator to watch, or the budget line to re-baseline. Format: table first, then one tight paragraph per variance. Tone: no spin — unfavorable variances explained with the same clarity as favorable ones. Under 600 words total.
```

### 3. The 12-Month Cash Flow Forecast
```
You are a cash flow forecaster who has kept real companies out of faux-insolvency. Create a 12-month cash flow forecast for [BUSINESS MODEL: SaaS, e-commerce, services] with current monthly inflows [REVENUE] and outflows [COSTS]. (1) Build the monthly cash table: operating, investing, and financing activities, with a running cash balance row, (2) model the timing realities for this business model: when customers actually pay — net-30/60 lag, seasonality, churn — not the accrual fantasy, (3) flag every month where the balance dips below the safety threshold [SAFETY THRESHOLD], (4) rank 3 mitigation levers by speed to cash: collections push, payment stretching, spend deferral — with the cost of each. Format: the monthly table, the shortfall flags, the lever ranking with honest tradeoffs.
```

### 4. The DCF Valuation Walkthrough
```
Act as a valuation analyst who builds models that survive an investor's spreadsheet audit. Build a DCF valuation for [COMPANY] with: revenue growth [GROWTH RATE], EBITDA margin [MARGIN], WACC [WACC]%, terminal growth [TERMINAL GROWTH]%. (1) State every assumption in a table with its source or reasoning — a number without a why is decoration, (2) build the 5-year projection: revenue → EBITDA → free cash flow, showing each step's formula, (3) the terminal value — both methods if relevant, and which fits this business, (4) the valuation bridge: from enterprise value to equity value — debt, cash, dilution, (5) the sensitivity matrix: ±10% on WACC and growth, showing the valuation range, and the honest comment on how wide it is. Format: assumptions table, projection table, sensitivity matrix, then a 3-sentence verdict on what the range means.
```

### 5. The Investment Committee Memo
```
You are an investment committee analyst whose memos get deals approved or killed — clearly. Write the investment memorandum for [PROJECT/ACQUISITION]: [DESCRIBE THE DEAL — target, price, thesis]. Cover: (1) the thesis — why this makes money, in 3 sentences a committee member could repeat, (2) market size and the gettable slice — not the TAM fantasy, the realistic capture, (3) financial projections with the 3 assumptions that swing the outcome flagged, (4) risks: the top 5, ranked by probability × impact, with the mitigations, (5) recommended allocation and the criteria that would trigger an exit. Length: 3 pages. Format: a one-page executive summary first — decision, ask, key numbers — then the supporting sections with tables. Rule: if the numbers only work in the base case, say that in the first paragraph.
```

---

## Budgeting & Forecasting (Prompts 6–10)

### 6. Zero-Based Budget Template
```
You are a budgeting specialist who has rebuilt department budgets from zero and found 20% hiding every time. Create a zero-based budget template for a [DEPARTMENT: marketing, engineering, operations] team of [HEADCOUNT] with mandate [DEPARTMENT GOAL]. Structure: (1) headcount — roles, fully-loaded cost per head, (2) software — every tool with per-seat cost and the renewal date, (3) campaigns/programs — with the expected outcome per dollar, (4) contingency — the honest percentage for this department's volatility. Every line item gets two columns: cost driver and justification. Rule: nothing inherits from last year — each line re-earns its place with "what happens if this is zero". Format: the category table with a total row, then the 5 lines most likely to survive a CFO challenge, and the 5 most likely to be cut.
```

### 7. The 13-Week Rolling Cash Forecast
```
Act as a treasury analyst who has guided companies through tight quarters with this exact tool. Build a rolling 13-week cash flow forecast for [COMPANY]: current cash $[CASH], weekly payroll $[PAYROLL], A/R position [RECEIVABLES], A/P position [PAYABLES]. (1) Weeks 1–4 from actuals: what clears, when — collections, payroll dates, rent, debt service, (2) weeks 5–13 forecast: the assumptions per line, with the collection rate stated, (3) the running balance row with the minimum-cash alert line at [MINIMUM CASH], (4) the 3 weeks that decide the quarter — where the balance gets closest to the line and what levers exist that week: pull-forward collections, delay non-critical payables, draw on [FACILITY IF ANY]. Format: the week-by-week table, the alert flags, the lever plan per tight week.
```

### 8. The CapEx Request That Gets Approved
```
You are a capital planning analyst who knows the difference between a request that gets funded and one that gets nodded at and shelved. Draft the CapEx request for [PROJECT: new office, software platform, equipment] costing $[AMOUNT]. Include: (1) the problem — what breaks or stalls without this spend, in operational terms, (2) the ROI calculation: the benefits with their dollar-ization, conservative — shown line by line, (3) NPV at [DISCOUNT RATE]% and payback period — with the formula visible, (4) the alternatives: leasing vs. buying, phasing vs. full, doing nothing — each with its number, (5) the risks: what could make this underperform and the tripwire metrics. Format: a one-page request with a decision box at the top: approve/deny/defer with the three numbers that drive it. The approver reads the box; the page defends it.
```

### 9. Scenario Planning Model
```
Act as a scenario planning expert who preps leadership for the futures that actually happen, not the convenient ones. Create the scenario model for [BUSINESS] with base-case revenue [REVENUE] and EBITDA margin [MARGIN]: (1) the three cases — bear (-20% revenue), base, bull (+20%) — each with the full cascade: revenue → gross profit → opex (what flexes vs. what's fixed) → EBITDA → cash, (2) the trigger points: the specific indicators — pipeline, churn, macro signal — that say which world we're in, with thresholds, (3) the pre-decided responses: what we do in the first 30 days of recognizing each case, so we're executing, not deliberating. Format: the 3-column comparison table, the trigger dashboard spec, the response playbook. Include the trap: opex that looks variable but isn't — name the lines in my cost structure most likely to be fake-flexible.
```

### 10. The Board Financial Presentation
```
You are a CFO presentation writer whose decks survive board scrutiny. Write the board presentation summarizing Q[QUARTER]: [PASTE KEY FINANCIALS — revenue, margins, cash, headcount]. Structure, 8 slides, one message per slide: (1) the headline slide: the quarter in one sentence and one number, (2) performance vs. plan — the bridge, not the table dump, (3) the 3 metrics that matter with trend lines and the read on each, (4) highlights — the wins with why they matter, (5) lowlights — the misses with the corrective action, stated before they ask, (6) cash and runway slide — the one directors care most about, (7) forward guidance for Q[NEXT] — with the confidence level stated, (8) asks and decisions needed. Appendix: detailed tables. Format: slide-by-slide content with the speaker notes per slide — what you say vs. what's on screen.
```

---

## Lending & Credit (Prompts 11–15)

### 11. The Commercial Credit Memo
```
You are a commercial credit analyst whose memos pass committee on the first read. Write the credit memo for a $[AMOUNT] [LOAN TYPE: term loan, line of credit, SBA] to [BORROWER — business, industry, years operating] for [PURPOSE]. Include: (1) borrower background — the 4 facts that matter: what they do, how long, who depends on them, why they need this, (2) financial analysis — the ratios that matter for this loan type: DSCR with the math shown, leverage, liquidity — with the covenant thresholds, (3) collateral description — what secures it, the LTV with a conservative valuation, the perfection steps, (4) repayment source — primary and secondary, honestly ranked, (5) risks and mitigants — the 3 things that go wrong and what protects the bank in each, (6) the recommendation with conditions. Format: standard credit memo with the approval box: amount, rate, term, conditions.
```

### 12. The Compliant Denial Letter
```
Act as a lending compliance officer who has kept institutions clean through fair-lending exams. Create the loan denial letter template for [INSTITUTION TYPE: bank, credit union, fintech lender], compliant with ECOA/Reg B. Include: (1) the adverse action notice structure: the specific principal reasons for denial — never "did not meet internal standards" — drawn from a defensible list, (2) the required disclosures: the credit score notice if used, the right to a statement of reasons, the ECOA anti-discrimination notice, the credit bureau contact block when a report was used, (3) what NOT to include: no encouragement to reapply soon without changed circumstances, no unverifiable reasons, (4) next steps for the applicant: the specific things that would change the decision. Format: the letter with each regulatory requirement labeled in brackets [ECOA], [FCRA] — so review can verify each element. Plain language throughout.
```

### 13. Venture Debt Term Sheet
```
You are a debt capital advisor who has negotiated venture debt from both sides. Draft the term sheet for a $[AMOUNT] venture debt facility: [INTEREST RATE]% interest, [TERM] months, to [BORROWER — stage, revenue]. Structure: (1) the deal table: amount, rate — cash vs. PIK, term, amortization — interest-only period then amort, (2) warrants: the coverage %, the strike mechanics, why this number, (3) covenants: the financial covenants — minimum cash, revenue milestones — with the headroom a founder should negotiate, (4) the definitions section that hides the leverage: what counts as EBITDA, what counts as cash — where these deals bite later, (5) events of default — including the ones founders don't read: the material adverse change clause. Format: term sheet with the deal table first, then covenant definitions, then the 5 terms most worth negotiating, ranked.
```

### 14. The Debt Schedule Build
```
Act as a debt schedule analyst who tracks every facility to the penny. Build the combined debt schedule for [COMPANY]: existing loans [PASTE: lender, amount, rate, maturity, monthly payment], proposed new facility [NEW FACILITY TERMS]. (1) The loan-by-loan table: balance, rate, payment, maturity, security, covenant summary — one row per facility, (2) the combined amortization schedule: monthly for 24 months, then quarterly to the longest maturity, with total debt service per period, (3) the coverage view: debt service vs. projected EBITDA/cash flow [PROJECTED CASH FLOW] per quarter — the times-covered ratio, (4) the covenant headroom dashboard: each financial covenant, the requirement, the projected level, the headroom — and the quarter where headroom thins most. Format: the three tables plus the 2 sentences a lender reads first.
```

### 15. The Mortgage Pre-Approval Package
```
You are a mortgage lending specialist who prepares packages that make agents take buyers seriously. Write the pre-approval package for [CLIENT NAME] seeking $[AMOUNT] at [INTEREST RATE]%: [INCOME, CREDIT RANGE, DOWN PAYMENT, ASSETS]. (1) The pre-approval letter — professional, specific: amount, the conditions it's subject to, the expiration date — written so a listing agent can rely on it, (2) the internal conditions checklist: the docs that must verify before closing — income, assets, appraisal — with the underwriting flags for [SITUATION: self-employed, gift funds, recent job change], (3) the buyer's next steps: what strengthens this pre-approval to underwritten-approval, in order of impact. Format: the letter, then the internal checklist, then the client-facing next steps. Compliance note: include the fair-lending-safe language and what must never appear in the letter.
```

---

## Risk & Compliance (Prompts 16–20)

### 16. The Financial Risk Register
```
You are an enterprise risk manager who builds registers that leadership actually reviews. Create the financial risk register for [COMPANY/INDUSTRY]. Cover the five categories: market, credit, liquidity, operational, regulatory. For each: (1) the top 3 risks for [INDUSTRY] specifically — named concretely: "interest rate rise repricing our floating facility", not "market risk", (2) likelihood and impact — scored 1–5 with the reasoning, (3) the mitigation: what reduces it, who owns it, the date, (4) the leading indicator: the metric that moves before the loss does. Format: one sortable table — risk, category, likelihood, impact, score, mitigation, owner, indicator — then a heat-map summary in text: the 5 risks in the red zone and why they cluster. End with the review cadence: what gets re-scored monthly vs. quarterly.
```

### 17. AML Policy Draft
```
Act as a compliance officer who has written AML programs that passed regulator examination. Draft the anti-money laundering (AML) policy for a [BANK/FINTECH/BROKERAGE]: [SIZE, CUSTOMER BASE, PRODUCT LINES]. Include: (1) the customer due diligence program: onboarding verification — the documents, the beneficial ownership for entities, the risk-rating criteria that tier customers, (2) the monitoring: the transaction patterns that trigger review for [PRODUCT LINES] — structuring, velocity, geography — and the rule tuning process, (3) the SAR process: who reviews, the escalation path, the confidentiality rules — tipping-off is the crime nobody thinks they'll commit, (4) record retention: what's kept, how long, retrievability, (5) training and the responsible officer. Format: policy document with numbered sections, then the responsibility matrix: role × duty. Regulatory note: this is a drafting framework — final policy requires legal review and jurisdiction-specific mapping.
```

### 18. Month-End Close Controls Checklist
```
You are a financial controls expert who has closed books in 5 days and watched others take 25. Write the month-end close controls checklist for [COMPANY TYPE/SIZE]. Sections: (1) segregation of duties — who prepares, who reviews, who approves — with the small-team workaround when one person is the accounting department, (2) reconciliations: bank, A/R, A/P, prepaid, accruals — each with the required evidence, (3) approval thresholds — the cutoffs that route spend for sign-off, (4) the GAAP checks: the misstatements this checklist exists to catch — cutoff errors, unrecorded liabilities, capitalization mistakes — with the test for each. Format: a checkbox checklist with owner, evidence, and day-of-close columns. Include the close calendar: day 1 through final sign-off, with the sequence that shaves days.
```

### 19. Vendor Financial Due Diligence Questionnaire
```
Act as a procurement risk specialist who has vetted hundreds of vendors and been burned by exactly one — which is why the questionnaire has each question it has. Create the vendor financial due diligence questionnaire for [VENDOR TYPE: SaaS provider, contract manufacturer, logistics]. Cover: (1) financial stability — years profitable, revenue trend, ownership/backing, the go-concern red flags, (2) insurance — the coverage types and limits required for this engagement, (3) capacity — references from similar-scale customers, the ones that will talk honestly, (4) conflict of interest — the disclosures that protect deal integrity, (5) continuity — what happens if they're acquired, fail, or lose their key staff. Format: scored questionnaire — each question weighted, pass/fail thresholds by category — plus the interview follow-ups for weak answers. Output includes the verdict logic: when a failing score ends the process vs. triggers mitigations.
```

### 20. The Fraud Response Playbook
```
You are a fraud response planner who knows the first 24 hours decide everything. Draft the financial fraud response plan for [COMPANY]: [SIZE, INDUSTRY]. Include: (1) detection signals: the red flags per fraud type for [INDUSTRY] — billing schemes, vendor fraud, payroll manipulation, expense abuse, cyber-enabled fraud — each with the control that surfaces it, (2) the escalation matrix: who is told in what order — and the rule about who is NOT told yet, including the suspect, (3) the first-24-hours checklist: preserve evidence — systems logs, documents, access records — freeze what's freezable, engage forensic accounting and counsel, in that order, (4) regulatory notification: the timelines that apply — and the clock that starts at discovery, not at convenience, (5) communication protocols: internal, customer, and public — the scripts approved in advance. Format: the playbook with the first-24-hours checklist as page one.
```

---

## Personal Finance & Wealth (Prompts 21–25)

### 21. The Financial Priority Ladder
```
You are a fiduciary financial planner writing in educational mode — frameworks, not individualized advice. Explain to a client earning $[INCOME]/year with $[SAVINGS] saved, debts [DEBT BREAKDOWN], and goals [GOALS: retirement at X, house in Y years] how to prioritize: (1) the emergency fund — the right size for their situation, the tiered build: starter fund first, then full, (2) the debt payoff order — the avalanche (rate-based) vs. snowball (balance-based) math on their actual debts, the interest difference, and the behavioral case for each, (3) retirement contributions — the employer match first: the free-money math shown, then the tax-advantaged order, (4) taxable investing — what comes after the above, and why. Format: the priority ladder — each rung with dollar allocations and the reasoning. Note: for educational purposes; individual circumstances vary and a licensed advisor should confirm specifics.
```

### 22. Retirement Readiness Model
```
Act as a retirement projection specialist who shows people their number without flinching. Model retirement readiness: age [AGE], current balance $[CURRENT BALANCE], contributing $[MONTHLY]/month, target retirement age [AGE], desired income [DESIRED ANNUAL INCOME]. (1) The 4% rule check: the target nest egg — 25× desired income — and the gap, (2) the projection: the balance at retirement under three return assumptions — conservative [4-5]%, moderate [6-7]%, historical-equity [8-10]% — with the compounding math visible, (3) the honest caveats: sequence-of-returns risk for near-retirees, inflation's bite on a fixed number, (4) the 3 levers that most change the outcome, ranked by impact: contribution increase — the per-dollar effect of $100 more per month, delay — the per-year effect of working one more year, and withdrawal rate flexibility. Format: the projection table with scenarios, then the levers. Educational framing, not individualized advice.
```

### 23. The Debt Payoff Plan
```
You are a debt strategist who has walked hundreds of households out of five-figure debt. My situation: $[DEBT BREAKDOWN: credit card $X at Y%, student loan, auto, mortgage] with $[MONTHLY AVAILABLE] available monthly. Build the payoff plan: (1) the order — the avalanche math: rate-ranked, total interest paid; the snowball: balance-ranked, the behavioral win — show both totals on my actual numbers and the tradeoff in dollars and months, (2) the payment schedule: month-by-month until the first debt dies — the momentum moment — then the snowball reallocation, (3) total interest saved vs. minimum payments — the headline number, (4) consolidation analysis: the balance-transfer and personal-loan options — when the math favors it, the fees and the risk — the same-balance-new-card trap — and when it's cosmetic. Format: the comparison table, the payoff timeline, the verdict. Educational framing.
```

### 24. Tax-Aware Investing Explained
```
Act as a tax-aware investing explainer who makes this genuinely clear, not simplified-to-wrong. Explain to an investor in the [TAX BRACKET] bracket: (1) the account priority order — 401(k) to the match: why leaving the match is a guaranteed instant loss, HSA: the triple advantage and its conditions, then IRA — traditional vs. Roth for this bracket, then taxable — with the reasoning for each step in order, (2) the difference between tax-deferred, Roth, and taxable — where each dollar is taxed, at what point, with a worked example of the same $1,000 through all three, (3) tax-loss harvesting in plain English: the mechanics, the wash-sale rule, and when it's worth the complexity, (4) the 3 mistakes that trigger avoidable bills: high-turnover funds in taxable accounts, holding the wrong asset type in the wrong account, and missing the backdoor mechanics when income phases out direct contributions. Format: the decision tree, then the one-page summary. Educational framing.
```

### 25. The 90-Day Money Reset
```
You are a personal finance educator who designs programs people actually finish — because week 2 is where programs die, and it's designed for that. Create the 90-day money reset for someone [SITUATION: living paycheck to paycheck, first job out of school, post-divorce, starting over]. Week by week: (1) track spending — the method that takes 10 minutes weekly, not the app that gets abandoned, (2) build the $1,000 starter fund — the fast version: what gets sold, what gets paused, the side income that's realistic, (3) the bill audit — the negotiation scripts: internet, insurance, phone — the actual words, (4) automate — the split that happens before willpower gets involved, (5) start investing — the boring correct first account. Each week: the specific actions, the time required, and the metric that proves progress. Format: the weekly checklist with the escalation note: what to do when life derails week 4 — because it will. Educational framing.
```

---

## Fintech, Payments & Financial Products (Prompts 26–30)

### 26. Payments Pricing Model Design
```
You are a payments product manager who has priced interchange economics and lived with the margin consequences. Design the pricing model for a [PAYMENT PRODUCT: P2P app, merchant processor, BNPL]: [TARGET USER, VOLUME ASSUMPTIONS]. (1) The unit economics: the interchange/network fee stack per transaction — the fixed and percentage components — and what's left for us at [AVERAGE TICKET], (2) the free tier vs. premium split: what's free to drive adoption — the loss-leader math stated — and what's paid, (3) the fee structure options: flat, percentage, hybrid, subscription-plus — with the break-even volume of each, (4) competitor pricing: how [COMPETITORS] price and the positioning that implies — under-cutting, premium, or bundle. Format: the pricing table with the per-transaction margin math at 3 volume levels, then the recommendation with the risk: the pricing that wins share now and bleeds later.
```

### 27. The Regulatory Surface Map
```
Act as a fintech compliance strategist who maps regulation before product — because retrofitting compliance costs 10×. My product [PRODUCT: budgeting app, lending platform, investing app] handles [DATA TYPE] for [CUSTOMER TYPE]. Map the regulatory surface: (1) the applicability verdicts, rule by rule: Reg E — electronic transfers and error resolution: applies if [CONDITION], Reg Z — lending disclosures, KYC/BSA — the onboarding obligations, PCI DSS — if cards are touched at what level, GLBA — the privacy and safeguarding duties, state licensing — the money transmission/lending license triggers by activity, (2) the compliance MVP: what's required at launch vs. what scale triggers — with the user-count and volume thresholds where obligations expand, (3) the cost picture: the build cost of each requirement — engineering, process, personnel — rated low/medium/high. Format: the regulation table with verdicts and trigger conditions, then the phased roadmap: launch-ready vs. later.
```

### 28. Behavioral Financial Product Design
```
You are a financial product designer who builds for how people actually behave, not how they should. Design a [PRODUCT: savings app, credit builder, robo-advisor feature] for [AUDIENCE: gig workers, teens, immigrants, retirees]: [THEIR SPECIFIC FINANCIAL CONTEXT]. For each feature: (1) the behavioral principle — default: the auto-save that works because opting out beats opting in; friction: the delay that blocks impulse; reward: the immediate vs. delayed payoff — and the research it rests on, (2) the engagement loop: the trigger, action, reward, investment cycle — what brings them back, ethically, (3) the alignment check: does the business model want what the user's outcome needs — where the incentives diverge, and the design choice that closes the gap. Format: the feature spec with user stories, the loop diagram in text, and the alignment audit. Include the dark-pattern boundary: the engagement tactics that cross the line — named.
```

### 29. The Bank Partnership Evaluation
```
Act as a banking partnership advisor who has sat on both the fintech and the bank side of these deals. My fintech needs [BANK PARTNER TYPE: sponsor bank, BaaS provider] for [FUNCTION: deposits, lending, cards]. (1) The landscape: the models — sponsor bank, BaaS platform, direct charter — and what each gives and takes, (2) the diligence questions: the compliance burden split — who owns KYC, monitoring, reporting; the fee structure — the per-account and transaction costs, the minimums; the SLAs — uptime, dispute timelines, change-request turnaround, (3) the red flags: banks exiting fintech sponsorship under regulatory pressure, concentration risk — one partner, one point of failure, (4) the 6-month onboarding timeline: the integration phases, the testing, the pilot — and what slips. Format: the evaluation scorecard — weighted criteria, pass thresholds — plus the reference-check questions for their existing fintech clients.
```

### 30. Open Banking API Monetization
```
You are an open banking / API strategist who has watched API programs make money and watch them become expensive giveaways. Plan the API monetization for [FINANCIAL INSTITUTION]: [SIZE, EXISTING API STATE]. (1) The endpoint portfolio: which APIs to open — accounts, payments, data — and the value of each: the data uniqueness, the transaction capability, (2) the developer tiering: free — the sandbox and rate limits that seed an ecosystem, paid — the volume and SLA tiers, enterprise — the dedicated support and compliance packaging, with the pricing logic per tier, (3) the security requirements: OAuth flows, consent management — the customer-permission model that regulation and trust both demand, (4) the roadmap: what opens year 1 vs. year 2, sequenced by revenue potential ÷ build cost. Format: the tier table, then the API roadmap. Include the honest failure mode: APIs launched with no developer experience investment — the program that has endpoints and no customers.
```

---

## Tax & Accounting (Prompts 31–35)

### 31. The Small Business Deduction Audit
```
You are a small business tax strategist who finds deductions without crossing lines. My [BUSINESS TYPE: LLC, S-corp, sole prop] earned $[REVENUE] with $[EXPENSES] in expenses: [DESCRIBE BUSINESS ACTIVITY]. (1) The deductions I'm likely missing for this business type: the industry-specific ones — the categories [ACTIVITY] businesses routinely leave on the table — with the documentation each requires, (2) the home office calculation: both methods shown on my numbers — simplified and actual — with the better answer and its audit-posture note, (3) the retirement account options that reduce taxable income: SEP, Solo 401(k), defined-benefit for high earners — the limits and the fit by income level, (4) the quarterly estimated tax math: the safe-harbor calculation and the payment schedule. Format: checklist with dollar-impact estimates per item. Note: verify with a CPA before filing — this is the thinking framework, not the filing position.
```

### 32. Chart of Accounts Design
```
Act as an accountant specializing in [INDUSTRY: e-commerce, SaaS, restaurants] who has rebuilt messy charts into ones that answer questions. Design the chart of accounts for my [BUSINESS TYPE]: [REVENUE STREAMS, SIZE]. Structure: (1) revenue by stream — the accounts that make revenue mix visible, (2) COGS — matched to how [INDUSTRY] actually incurs cost of sale, (3) the expense buckets: the 5-8 categories that survive — payroll, occupancy, marketing, software, professional — with the sub-accounts that matter for [INDUSTRY], (4) the design rules: the account set that makes tax time a export, not a project; the lender-ready view — what a bank asks for and which accounts answer it; the parent/child numbering that scales without a rewrite. Format: the numbered COA with a description column — plus the 3 reports this structure enables that my current one can't produce.
```

### 33. Revenue Recognition Under ASC 606
```
You are a revenue recognition expert who has untangled ASC 606 for companies that got it wrong — expensively. My [BUSINESS MODEL: subscriptions, multi-year contracts, usage-based]: [DESCRIBE THE BILLING AND DELIVERY MODEL]. (1) Walk the 5-step model on my case: identify the contract, the performance obligations — the deliverables that are distinct vs. bundled, the transaction price — including the variable pieces: usage, refunds, credits, allocate, recognize — over time or point in time, with which and why, (2) apply to [SPECIFIC SCENARIO: e.g., annual subscription billed monthly, setup fee + recurring, credits rolling over] — when revenue actually recognizes, with the journal entries, (3) the mistakes that require restatement: the 3 most common for this model — recognizing on billing instead of delivery, mishandled contract modifications, deferred cost capitalization errors. Format: step-by-step with example journal entries. Educational framework — confirm specifics with the auditor.
```

### 34. The Audit Response Binder
```
Act as a tax controversy preparer who has sat through audits — as preparer, not defendant. My [BUSINESS/PERSONAL] return is being audited for [ISSUE]: [NOTICE DETAILS]. Build the response: (1) the document checklist: every line item in question mapped to its supporting evidence — the specific document, where it lives, what it proves — with the IRS substantiation standards noted per item, (2) the gaps: what I can't substantiate and the honest options — reconstructing records, secondary evidence, and what the burden shifting means, (3) the representation decision: CPA, attorney, or self — the cost and stakes analysis, and when attorney-client privilege actually matters: when it looks like more than an audit, (4) the narrative: the explanation that resolves the issue cleanly — factual, chronological, no editorializing — organized to make the examiner's job easy, which is the whole strategy. Format: the audit binder outline with tabs. Note: this prepares; a licensed representative confirms the position.
```

### 35. The Bookkeeping System Rebuild
```
You are a bookkeeping systems designer who has rescued the shoebox, the spreadsheet, and the 6-months-behind. My [BUSINESS TYPE] currently: [CURRENT STATE — shoebox, spreadsheet, behind by MONTHS]. Design the catch-up and the go-forward system: (1) The catch-up plan: the steps in order — gather statements, reconcile the bank — the source of truth, the categorization triage: what matters vs. what's noise, the deadline structure, (2) the go-forward system: bank feed rules — the auto-categorization that removes 80% of the work, with the rule examples for [BUSINESS TYPE], (3) the weekly 30-minute routine: the exact agenda — what gets reviewed, what gets reconciled, the dashboard glance, (4) the month-end close checklist: the 5 items, in order, with the evidence, (5) the reports I actually need monthly — P&L, balance sheet, the cash view — and the rest to skip. Format: the process doc with checklists. Include the realistic time estimate: month 1 vs. steady state.
```

---

## Investor Relations & Corporate Finance (Prompts 36–40)

### 36. The Earnings Announcement Kit
```
You are an IR communications director who has written earnings materials for companies where every word moved the stock. Write the earnings kit for [COMPANY], Q[QUARTER]: [HEADLINE RESULTS — revenue, EPS vs. expectations, key drivers]. (1) The press release: the results with narrative — numbers first, the why second, the guidance third — no burying the bad number; investors find it anyway, and candor is priced in as credibility, (2) the CEO quote: 2-3 sentences that say something — the operational read, not the victory lap, (3) the 3 key messages for the call — the message discipline that keeps the narrative from fracturing, (4) the FAQ anticipating the tough questions about [SENSITIVE TOPIC]: the honest answers prepared in advance — the questions you'd rather never hear are exactly the ones that get asked. Format: press release, quote, message discipline sheet, FAQ. Include the disclosure discipline note: what can never be said — material information outside proper channels.
```

### 37. Capital Structure Optimization
```
Act as a capital structure advisor who has recapitalized companies in both directions. My [COMPANY] at [STAGE]: revenue $[REVENUE], current mix [DEBT/EQUITY MIX], planned raise $[AMOUNT] for [USE]. Analyze: (1) debt capacity: the leverage this business can carry — cash flow stability is the real input — with the coverage math at 3 debt levels, (2) the WACC impact of the alternatives: more debt — the tax shield math, the risk premium the market charges — vs. more equity: dilution now vs. flexibility, (3) covenant tradeoffs: what each structure restricts — the operating freedom given away at each leverage level, (4) the sequencing: the raise timed against milestones — raise after the proof, at the valuation the proof creates, with the 6-month window logic. Format: the alternatives table with the recommendation and the reasoning. Include the stress note: what the structure looks like in a downturn scenario — the covenant headroom under -20% revenue.
```

### 38. M&A Target Screen
```
You are an M&A analyst who has built screens that surfaced real deals, not listicles. Build the acquisition screen for [ACQUIRER TYPE — strategic, PE, size] targeting [INDUSTRY] with criteria [SIZE, GEOGRAPHY, CAPABILITY SOUGHT]. (1) The 10 screening criteria: the must-haves vs. nice-to-haves — with the disqualifiers: customer concentration, founder dependence, the messy cap table — and the scoring weights, (2) where to find candidates: the sources that actually surface sellers — industry association lists, the "for sale" signals in public data: aging ownership, succession gaps, the brokers and bankers who cover this size, (3) the valuation multiples for [INDUSTRY]: the range — EBITDA or revenue-based — by size tier, with what moves a target within the range, (4) the outreach logic: the first-10 list rationale — why these, the angle per target, the approach that doesn't signal desperation. Format: the criteria matrix, then the screen methodology, then the target list structure.
```

### 39. The Capital Return Decision
```
Act as a dividend/capital return strategist who has designed return policies that the market read correctly. My company generates $[FREE CASH FLOW] annually: [STAGE, GROWTH PROFILE, CURRENT BALANCE SHEET]. Analyze the options: (1) reinvestment first: the ROI threshold — the hurdle new projects must clear to beat returning cash, and the honest capacity: how much capital the pipeline can actually absorb, (2) buybacks vs. dividends: signaling — what each says and how the market reads it, tax efficiency for the shareholder base, flexibility — buybacks can pause quietly, dividends can't be cut without damage, (3) the payout policy for [STAGE]: growth-stage, cash-generative, mature — with the percentage ranges each supports, (4) what the market reads into each choice: the undisciplined buyback that says nothing about conviction, the dividend as a discipline device that constrains bad empire-building. Format: the decision framework with the recommendation and the policy language to announce it.
```

### 40. Financial Storytelling for Tough Rooms
```
You are a financial storytelling coach who has prepped founders for boards, down-round investors, and skeptical lenders — the rooms that matter. My [STARTUP] presents financials to [AUDIENCE: board, investors, lender]: the numbers are [SITUATION: early, complex, negative — pick and describe]. Teach me the narrative structure: (1) lead with the operating story — the metrics that show the machine working: pipeline, retention, unit economics improving — before the P&L that hasn't caught up yet, (2) connect every metric to a driver — never present a number without the operational cause: "cash burn down 15% — because churn fell from X to Y", (3) pre-empt the obvious concern: state it before they raise it — the credibility move that changes the room's posture, (4) end with the capital logic: the ask, the milestones it funds, the next data point that de-risks. Format: an annotated example presentation — slide content plus the speaker's note — built on my situation. Include the Q&A prep: the 5 questions this room will ask and the one-line answers.
```

---

## How to Use This Pack

1. **Match the prompt to the job** — analysis, budgeting, credit, risk, tax, or corporate finance. Don't read linearly.
2. **Fill the [BRACKETS]** — the more specific your inputs, the better the output. Vague in, vague out.
3. **Iterate** — when the first output is 80% right, reply with what to change instead of regenerating from scratch.
4. **Professional review** — these prompts produce professional drafts; regulated outputs (filings, policies, advice) still require a licensed professional's sign-off.

*License: single user. Resale or redistribution of this pack is not permitted. Questions: [CONTACT].*
