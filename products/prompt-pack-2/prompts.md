# AI Coding Assistant Pack — 50 Expert Prompts
## Code Generation, Debugging, Testing, Architecture & DevOps

> Copy-paste ready. Replace [BRACKETS] with your details. Works with ChatGPT, Claude, Gemini, or any LLM.

---

## Code Generation (Prompts 1–8)

### 1. Production-Grade Function
```
You are a senior [LANGUAGE] engineer who writes code that survives 5 years of maintenance. Write a function that [TASK] taking input of type [INPUT] and returning [OUTPUT]. Requirements: full type hints, a Google-style docstring with one realistic usage example, explicit handling of [EDGE CASES], and no silent failures — every failure path either raises, returns a typed result, or logs with context. After the code, list the 3 most likely ways it fails in production, each with the monitoring signal that would catch it (error message pattern, metric, or log line) and the guard that prevents it.
```

### 2. The Behavior-Preserving Refactor
```
Act as a clean code specialist doing a pre-merge refactor. Refactor this [LANGUAGE] code to improve readability and maintainability WITHOUT changing behavior: [PASTE CODE]. Apply single-responsibility (no function over [N] lines or [M] indent levels), intention-revearing names, guard clauses instead of nested conditionals, and extraction of any block that needs a comment to be understood. Present a before/after summary of every change with a one-line rationale each. Flag with ⚠️ any change that could alter behavior — I will test those first. Do not introduce new abstractions beyond what the code already needs.
```

### 3. API Endpoint, Complete
```
You are an API developer who has shipped services handling millions of requests. Design and implement a [REST/GraphQL] endpoint for [RESOURCE] in [FRAMEWORK]: request validation with actionable error messages (field-level, not "invalid body"), an authentication/authorization check appropriate for [AUTH MODEL], error responses with correct status codes (400 vs 401 vs 403 vs 404 vs 422 vs 429), and cursor or offset pagination if the list can exceed 100 items. Show the complete route handler plus 2 example requests as curl — one success, one validation failure — with the exact JSON response body each returns. State your rate-limiting assumption in one line.
```

### 4. Database Schema with Query Verification
```
Act as a database engineer reviewing a schema before launch. Write a [SQL/MONGODB/OTHER] schema for [USE CASE — e.g., multi-tenant SaaS with organizations, users, and invoices]. Include indexes, foreign keys, and constraints with the reasoning for each index (what query it serves). Then show the 3 most frequent queries for this app and walk through why the schema executes them efficiently — which index each hits, and any that triggers a collection/table scan. Finally, flag the one write pattern (hot column updates, index churn on writes) that will hurt at [SCALE] and the mitigation.
```

### 5. Automation Script (Set-and-Forget)
```
You are an automation engineer who maintains unattended scripts in production. Write a [PYTHON/JS] script that [AUTOMATION TASK — e.g., monitors a page and emails on change, renames files by date, syncs a CSV to Sheets]. Requirements: idempotent (safe to rerun, no duplicate side effects), retries with exponential backoff and jitter, logs every failure to a file with timestamps and context, and a --dry-run flag that prints actions without executing. Include setup instructions for a non-expert (commands to run, env vars to set) and the one cron/scheduler line to deploy it. End with the 3 symptoms that mean the script is silently broken and how to check for each.
```

### 6. CLI Tool Done Right
```
Act as a CLI craftsman. Build a command-line tool in [LANGUAGE] that does [TASK]. Requirements: argument parsing with sensible defaults, a --help message that includes 2 realistic examples (not just flags), input validation with helpful errors (show the bad value and the expected format), and exit codes: 0 success, 1 user error, 2 system error — so it composes in shell scripts. Show the complete implementation, then 3 example invocations covering the most common use cases, and a note on how to distribute it ([PIP/NPM/BINARY]) with the exact publish commands.
```

### 7. Regex with a Breakdown You Can Audit
```
You are a regex expert who has debugged catastrophic backtracking in production. Write a regular expression for [PATTERN DESCRIPTION — e.g., extract tracking numbers, validate phone numbers in multiple formats, parse log lines]. Deliverables: (1) the regex itself, optimized against ReDoS where relevant, (2) a plain-English breakdown of every component in a table (fragment → what it matches → why), (3) 5 test cases including 2 that must NOT match with an explanation of why they're excluded, and (4) a warning if any construct risks backtracking on adversarial input, with the safer alternative. Assume I will paste this into production without another review.
```

### 8. ETL Pipeline with a Run Manifest
```
Act as a data pipeline developer. Write [PYTHON] code that ingests [DATA SOURCE], cleans it (dedupe by [KEY], type coercion, null handling with explicit rules per column), and loads it into [DESTINATION]. Structure as separate extract/transform/load functions with a main entry point. At the end of every run, log a manifest: rows read, rows rejected with rejection reason counts, rows written, and runtime. Fail loudly on schema drift (unexpected columns) but tolerate bad rows per the rules. Include the 3 data quality checks you'd add next once this is stable, ranked by incident-prevention value.
```

---

## Debugging & Optimization (Prompts 9–16)

### 9. Root-Cause Diagnosis, Ranked
```
You are a debugging specialist with 15 years in [LANGUAGE] who ranks hypotheses before touching code. I get this error: [PASTE ERROR/STACK TRACE] when running [PASTE CODE OR DESCRIBE CONTEXT]. Give me: (1) the 5 most likely root causes ranked by probability with a one-line justification for each ranking, (2) the fastest diagnostic step per cause (the exact command, breakpoint, or log to check — cheapest test first), (3) the full fix for the most likely cause, and (4) the one log line or assertion I should add so that if it recurs, the next diagnosis takes one step instead of thirty.
```

### 10. Performance Surgery
```
Act as a performance engineer. This [LANGUAGE] function is slow: [PASTE CODE]. Analyze before touching it: (1) state the complexity class and the input size where it starts to hurt, (2) identify the top 3 bottlenecks in priority order, (3) rewrite with the single most impactful optimization, (4) show old vs. new side by side, and (5) state the expected speedup honestly with its tradeoffs (memory, readability, degraded behavior on small inputs). Close with the rule for when NOT to apply this optimization — the input sizes and contexts where the simpler version wins.
```

### 11. Memory Leak Hunt
```
You are a memory leak detective for [LANGUAGE/RUNTIME]. My [APPLICATION TYPE] grows in memory over [TIME PERIOD] in production. Give me: (1) a checklist of the 10 most common leak causes in this stack, grouped by category (references held, event listeners, caches, closures, native bindings), (2) for each cause, the confirmation method — the exact tool, heap-dump pattern, or log signature that proves or rules it out, and (3) the standard fix. Then design the canary: the metric or alert threshold that catches this class of leak before the OOM killer does. Assume I can take one heap dump and get 15 minutes of profiling.
```

### 12. Concurrency Correctness
```
Act as a concurrency expert. This [LANGUAGE] code sometimes produces wrong results under load: [PASTE CODE]. Identify every race condition, deadlock risk, and atomicity violation — name each one precisely (check-then-act, lost update, deadlock cycle, visibility issue). Rewrite using [THREADS/ASYNC/LOCKS] correctly and state exactly what guarantee the new version provides and what it does NOT (e.g., linearizable but not deadlock-proof under X). Then give me the stress test that would have caught the original bug: the parallelism pattern, iteration count, and assertion that fails deterministically on the old code.
```

### 13. Intermittent Failure Protocol
```
You are a reliability engineer who debugs flaky production issues for a living. My [SERVICE] fails intermittently with [SYMPTOM — e.g., timeouts after 30s, sporadic 502s]. Build a systematic debugging plan: (1) a hypothesis tree ordered most-likely to least-likely for this symptom class, (2) at each node, the evidence to collect — which logs, metrics, or traces confirm or kill it, and (3) a strategy to reproduce: the load profile, timing window, or environmental condition (clock skew, connection pool exhaustion, GC pause) most likely to trigger it deterministically. Include the temporary instrumentation to deploy if existing observability can't distinguish the top 2 hypotheses.
```

### 14. Security Code Audit
```
Act as an application security auditor doing a manual review before release. Review this code: [PASTE CODE]. Check specifically for: injection flaws (SQL, command, XSS), broken authentication/authorization, sensitive data exposure (logs, errors, responses), insecure deserialization, and vulnerable dependency usage. For each finding, output: severity on a CVSS-like scale with justification, the vulnerable line(s), a concrete exploitation scenario an attacker would follow, and the patched code. Rank findings by exploitability × impact. End with the single fix I should ship today if I can only ship one, and the test that would have caught it.
```

### 15. API Contract Mismatch
```
You are an API contract debugger mediating between my frontend and backend. My frontend calls [ENDPOINT] and gets [UNEXPECTED BEHAVIOR]; the backend team says it works. List 6 categories of mismatch to check: serialization (camelCase vs snake_case, number precision), timezones and timestamp formats, encodings, headers (content-type, auth tokens), pagination conventions, and error shape. For each, give a one-line curl command that isolates that hypothesis — so I can run all six in five minutes. Conclude with the contract test (schema assertion) that would have caught this class of mismatch in CI, written for [TEST FRAMEWORK].
```

### 16. Technical Debt Triage
```
Act as a technical debt assessor doing an honest audit. Review this module: [PASTE CODE OR FILE LISTING]. Identify the 5 worst debt items — coupling, missing tests on critical paths, dead code, fragile patterns, or knowledge trapped in one person's head. For each: what it costs today (bug risk, onboarding friction, velocity tax) in concrete terms, and the risk-to-effort ratio of fixing it. Then prescribe a 3-step incremental refactor plan where the app stays shippable after every step — each step scoped to under [N] hours, with the test to write BEFORE touching that step. Be honest about debt that's fine to leave: not everything needs fixing.
```

---

## Testing & Quality (Prompts 17–24)

### 17. Unit Test Suite from Scratch
```
You are a test automation architect. Write [UNIT TEST FRAMEWORK] tests for this function: [PASTE FUNCTION]. Cover: the happy path, boundary values (empty, zero, one, max, off-by-one), and 3 edge cases specific to this domain. Structure every test as arrange-act-assert with a descriptive name that states the expected behavior ("returns_empty_list_when_input_is_none", not "test_3"). Flag any case where the current code would FAIL the test — I want to know the bugs before they ship. Include the fixtures/mocks needed to run offline. Finish with one property-based test idea (invariant that should hold across random inputs) for this function.
```

### 18. TDD Walkthrough, 4 Iterations
```
Act as a TDD coach pair-programming with me. I need to build [FEATURE] in [LANGUAGE]. Walk me through red-green-refactor for 4 iterations: for each iteration show (1) the new failing test with a one-line reason it fails, (2) the MINIMAL implementation that passes it — resist doing more, (3) the refactor step with what improved and what behavior is guaranteed unchanged. At iteration 3, deliberately show a case where the minimal implementation is wrong and the next test forces the correction. End with the rule for when to break the cycle (integration points, exploratory code, throwaway scripts).
```

### 19. Integration Test Strategy
```
You are an integration testing specialist. Design a test suite for [SERVICE/FEATURE] that talks to [DEPENDENCIES — e.g., database, payment API, email]. Decide what to mock vs. run real: for each dependency, the decision with rationale (speed vs. fidelity vs. flakiness risk), and what contract tests cover the gap where you chose mocks. Set up test data (fixtures, factories, cleanup between runs) and write [FRAMEWORK] code for the 3 most critical cross-component scenarios — the ones whose failure would mean money or data loss. Include the test-ordering and isolation rules that prevent flaky suites from eroding trust.
```

### 20. The 20 Edge Cases QA Misses
```
Act as a senior QA engineer who has filed the incident reports. For this feature: [DESCRIBE FEATURE], generate 20 test scenarios a junior QA would miss — covering unicode and emoji input, timezones and DST transitions, concurrency and double-clicks, offline/intermittent connectivity, permission boundaries, data volume (empty state, 10k rows), clock skew, and session expiry mid-action. For each scenario, one line: the setup, the action, the expected behavior. Then prioritize the 5 that would cause the worst production incidents, each mapped to the environment it can only be caught in (unit, integration, staging, production monitoring).
```

### 21. Load Test with Pass/Fail Thresholds
```
You are a load testing engineer. Write a [K6/LOCUST/JMETER] script simulating [N] virtual users hitting [ENDPOINTS] for [DURATION], with a ramp profile that reveals the breaking point (gradual ramp, not instant slam). Define pass/fail thresholds for: latency p95 and p99, error rate, and throughput — with the actual numbers you'd set for a [NICHE] service and where those benchmarks come from. After the script, explain in plain English what each metric tells me about scaling: what a p99 blowout with healthy p95 means, what rising error rate at flat throughput means, and the 3 things to check in the app before blaming the infrastructure.
```

### 22. Mutation Testing, Practical
```
Act as a mutation testing advocate who cares about test suites that actually catch bugs. Explain mutation testing on this [LANGUAGE] module in practical terms: [PASTE MODULE]. List 6 mutations a tool would try (boundary flips, boolean negation, return-value removal, arithmetic tweaks), and for each, which of my current tests would catch it — be honest about misses. Then write the 2 tests that would raise my mutation score the most, and explain the score threshold where adding more tests stops paying off (diminishing returns and slow CI). Recommend whether to run mutation checks per-PR or nightly for a team of [SIZE].
```

### 23. CI Quality Gates
```
You are a DevOps lead configuring CI for a [LANGUAGE] repo. Configure [CI SYSTEM — GitHub Actions/GitLab CI] checks: linting, type checking, unit tests, coverage threshold of [PERCENT]%, and build. Provide the YAML with every step commented on what it protects against. Make the blocking decision explicit: which gates BLOCK a merge vs. WARN only, with reasoning — e.g., lint blocks on errors but not style warnings; coverage blocks on decrease, not absolute. Include the flaky-test policy: quarantine workflow, retry rules, and the maximum tolerated failure rate before a suite is quarantined. Total CI time must stay under [MINUTES] — say what to cut if it exceeds it.
```

### 24. Regression Bisect Procedure
```
Act as a regression detective. A feature worked in version [X] and broke in version [Y]; my repo has [COMMITS] between them. Give me: (1) the bisect procedure with the exact git commands at each step, including how to define "good" and "bad" in one sentence each and what to do when the bug is intermittent (bisect on a repro script, not vibes), (2) how to write the regression test once the commit is found — naming it after the bug, not the feature, and (3) the prevention layer: the feature flag, canary deploy, or contract test that would have caught this before users did. Include the total expected bisect steps for my commit count.
```

---

## APIs, Data & Architecture (Prompts 25–32)

### 25. OpenAPI Spec, Complete
```
You are an API designer who reads specs like a consumer. Write an OpenAPI 3.0 specification for [SERVICE — e.g., a booking system] with endpoints for [OPERATIONS]. Include: full schemas with required fields and format constraints, error responses with error bodies (not just status codes — define the error schema once and reuse it), and auth via [METHOD]. Then generate one example request/response pair for EVERY endpoint — realistic values, not "string". Finish with the API style review: naming consistency, pagination convention, versioning strategy, and the 2 endpoints most likely to need redesign once real consumers arrive.
```

### 26. System Architecture Design
```
Act as a system architect who has built this exact system at scale. Design [SYSTEM — e.g., real-time chat, food delivery, analytics dashboard] for [EXPECTED SCALE — e.g., 10k DAU, 500 RPS]. Cover: components and their responsibilities, data flow (who calls whom, sync vs. async), database choice with reasoning (read/write ratio, consistency needs), caching strategy, and the failure modes — what happens when each critical component dies, and what the user experiences. Present as a text-described diagram (you can't draw, so be precise with arrows in words) plus a tradeoff table for the 3 biggest decisions. Name the scaling assumption most likely to break first at 10× traffic.
```

### 27. Spreadsheet to Relational Model
```
You are a data modeling expert untangling a spreadsheet-era schema. Normalize this data into relational tables: [PASTE COLUMNS/SAMPLE ROWS]. Show the 1NF → 2NF → 3NF steps with what each step eliminates (no skipping), final table definitions with primary and foreign keys, and the query with joins that reconstructs the original flat view — verify it against the sample rows. Then argue the other side: the one reporting or read-heavy case where a denormalized column or materialized view is justified, and the trigger condition that should flip the decision. Flag any column that is actually two facts in disguise.
```

### 28. Integration Between Two Systems
```
Act as an integration engineer making two systems behave. Connect [SYSTEM A] to [SYSTEM B] via [WEBHOOK/REST API]. Write the integration plan: auth setup with credential rotation, retry policy with backoff and the failure classification (retry vs. dead-letter vs. alert), idempotency key design (what makes an event unique, and what happens on duplicates), and the [LANGUAGE] code for the sync worker — including the reconciliation job that detects drift between systems and the backfill procedure for initial sync. State the consistency model honestly: eventual means eventual — quantify the expected lag and what breaks if it doubles.
```

### 29. Rough Idea to Build-Ready Spec
```
You are a technical spec writer who turns fuzzy ideas into shippable tickets. Take this rough feature idea: [DESCRIBE FEATURE] — and produce a build-ready spec: (1) user stories with acceptance criteria in Given/When/Then form, (2) API changes with request/response shapes, (3) data model changes with migrations, (4) error handling for the 4 most likely failure paths, (5) rollout plan (flag, percentage, or big bang — justify), and (6) open questions ranked by blocking severity — what must be answered before a line of code, and what can be decided mid-build. Assume a senior engineer picks this up without you available to ask.
```

### 30. Zero-Downtime Migration Plan
```
Act as a migration planner whose migrations have never caused an outage. I need to move from [OLD SYSTEM — e.g., monolith, MySQL, Heroku] to [NEW SYSTEM] with zero downtime. Write the plan in phases where every phase ends in a fully working system: dual-write/read fallback strategy, backfill of historical data, verification step per phase (the exact counts and diffs to compare), and a rollback procedure per phase that takes under [MINUTES]. Include the metrics that say each phase succeeded and the total riskiest hour — the moment of maximum irreversibility — with the pre-flight checklist for that hour. Name the thing most teams forget to migrate (scheduled jobs, triggers, permissions, DNS TTLs).
```

### 31. Caching Strategy Table
```
You are a caching strategist who has debugged both stale-data incidents and stampedes. For this [APPLICATION TYPE] with [TRAFFIC PATTERN — e.g., read-heavy, bursty mornings], decide what to cache, where (CDN, application, database), the invalidation strategy, and TTL reasoning. Output a table: data type | cache layer | TTL | invalidation trigger | staleness risk (what the user sees if it goes stale). Then design the stampede protection for the top cache key (lock, probabilistic early expiry, or request coalescing — pick and justify). Close with the debugging playbook: the 3 symptoms of a caching bug and the cache-vs-origin test for each.
```

### 32. Schema Evolution, Backward Compatible
```
Act as a schema evolution expert protecting [CONSUMERS — e.g., 3 services and a nightly job] from my database changes. I must change a production [DATABASE] table: [CHANGE — e.g., rename a column, split a table, change a type]. Design a backward-compatible migration using expand-and-contract: (1) the sequence of DDL steps in order, (2) the deployment order — which app versions must ship before which DDL, and why, (3) the verification between steps that proves old and new code coexist safely (dual-read check, shadow writes), and (4) the cleanup contract phase — when it's safe, and who signs off. Include the revert path at every step.
```

---

## DevOps, CI/CD & Deployment (Prompts 33–40)

### 33. Dockerfile, Small and Secure
```
You are a DevOps engineer who treats image size and CVE count as features. Write a Dockerfile for a [LANGUAGE/FRAMEWORK] app: multi-stage build, non-root user, pinned base image (full digest, not :latest), minimal layers, and a HEALTHCHECK. Then show the docker-compose.yml wiring it to [DEPENDENCY — e.g., Postgres, Redis] with volumes and healthcheck-based startup ordering. Comment each instruction on what it protects against. Finish with: expected final image size for this stack, the CVE scan command to run before shipping, and the 2 things that commonly bloat images for [LANGUAGE] builds and how to verify you avoided them.
```

### 34. CI/CD Pipeline with Guardrails
```
Act as a CI/CD pipeline designer. Create a [GITHUB ACTIONS/GITLAB CI] workflow for a [LANGUAGE] monorepo: lint, test, build, and deploy to [ENVIRONMENT] with environment protections (required reviewers for prod, no secrets in logs, least-privilege tokens) and secrets handled via the platform's secret store — never inline. Provide the YAML, with each step commented on what it protects against. Include: concurrency cancellation (kill superseded runs), path filters (don't deploy when docs change), and a manual approval gate for production. State the pipeline's total expected runtime and the first thing to cache to cut it by 30%.
```

### 35. Monitoring That Wakes You for Real Reasons
```
You are an observability engineer who has been paged for nothing too many times. Design monitoring for a [APPLICATION TYPE]: the 4 golden signals (latency, traffic, errors, saturation) per service, which alerts deserve to wake a human at 3am — with the actual thresholds and the reasoning (symptom-based, not cause-based; page on user pain, not CPU), and which dashboards to build first for on-call triage. Include the [PROMQL/QUERY] for the 2 most important alerts. Then do the subtraction: name one alert most teams configure that's pure noise, and the check that should replace it.
```

### 36. Incident Runbook
```
Act as an incident response planner. Write the runbook for [FAILURE SCENARIO — e.g., database failover, payment provider outage, region loss] in my [STACK]: (1) detection — what fires and who gets it, (2) severity classification with concrete definitions (SEV1 = money stopped, not feelings), (3) immediate actions as a numbered checklist — including the DO NOT list (restarts that destroy evidence), (4) comms templates: status page update, customer email, team channel message — each under 100 words, honest, with a next-update time, and (5) the post-incident review agenda. Assign roles by name-slot (commander, comms, investigator) so the runbook works when the usual person is on vacation.
```

### 37. Cloud Bill Attack
```
You are a cloud cost optimizer. My [AWS/GCP/AZURE] bill grew [PERCENT]% this quarter for a [APPLICATION TYPE]. List the 8 most common causes for this pattern (idle resources, oversized instances, chatty cross-AZ traffic, snapshot hoarding, forgotten load balancers, NAT gateway games, orphaned volumes, log retention), with for each: the exact console page or CLI command that confirms it in under 5 minutes, the expected savings, and the fix. Sort the final list by savings-per-hour-of-effort. Include the budget alert I should set today (threshold, email/action) and the one cost metric to review weekly so this never surprises me again.
```

### 38. Config & Secrets Audit
```
Act as an environment configuration auditor. Review how my app manages config across [ENVIRONMENTS]: what's in .env files, what's duplicated per environment, and what differs without a reason. Propose a secrets management approach for [STACK] — [VAULT/AWS SECRETS MANAGER/DOPPLER] — with: least-privilege access design (which service reads which secret, nothing more), a rotation policy with realistic intervals by secret type, and a step-by-step migration path away from .env files that doesn't require a big-bang deploy. Include the example tool config and the pre-deploy check that fails the build if a secret appears in code, logs, or the image layer.
```

### 39. Zero-Downtime Deployment
```
You are a deployment engineer who has never taken a planned outage. My [APPLICATION TYPE] currently deploys via [CURRENT METHOD — e.g., manual ssh, 5-minute outage]. Design a blue-green or rolling deployment for my [INFRA]: traffic switching strategy, database migration coordination (expand phase before deploy, contract after), automated smoke tests post-switch (the 5 checks that prove the app serves real users), and instant rollback that doesn't require a rebuild. Include the deploy drill to run in staging before trusting it in production, and the 3 signs mid-deploy that say abort and roll back rather than push through.
```

### 40. Git Workflow, Right-Sized
```
Act as a Git workflow consultant for a team of [SIZE] that keeps breaking [BRANCHING MODEL]. Design a right-sized strategy: branch naming that a stranger could parse, commit message convention with examples (one good, one bad), PR review rules (who must approve, max size before splitting, stale-after-N-days), and merge checks enforced by the platform — with the exact repo settings or branch protection rules to configure. Include when trunk-based development IS wrong for this team (deployment cadence, test discipline) and the escape hatch: the hotfix path that works when production is burning. The whole strategy must fit on one page a new hire reads on day one.
```

---

## Code Review, Docs & Developer Experience (Prompts 41–50)

### 41. Staff-Level Code Review
```
You are a staff engineer doing code review with a reputation for making PRs better, not bigger. Review this pull request: [PASTE DIFF]. Categorize findings as: BLOCKING (correctness, security, data loss), IMPORTANT (maintainability, performance, missing test), or NIT (style — bundled together at the end, never mixed with real findings). For each: the line reference, the reasoning grounded in what breaks later (not taste), and a suggested fix in code. End by naming what the author did well — be specific about the good decisions so they're repeated. If the PR is over [LINES], say what to review first rather than rubber-stamping.
```

### 42. README That Onboards
```
Act as a documentation engineer. Write a README for [PROJECT] following this outline: what it is (2 sentences, no marketing), quickstart in under 5 commands (copy-pasteable, tested order, with expected output), configuration table (variable | required | default | what it does), common errors with fixes (the 4 errors a newcomer hits, including the install/env one), and a contribution guide (dev setup, test command, PR expectations). Audience: [AUDIENCE — new hires, open-source users]. Rules: no orphan links, every command must work verbatim, assume zero context. Include the one diagram-slot where a picture would replace 200 words.
```

### 43. API Reference Docs, Stripe-Grade
```
You are an API documentation writer matching the tone of Stripe docs: precise, complete, quietly confident. Turn this endpoint code into reference docs: [PASTE CODE]. Include: a one-paragraph description covering what it's for and when NOT to use it, a parameters table (name, type, required, constraints, notes), auth requirements and scopes, request/response examples for success AND each error code — with realistic values, rate limits, and a complete curl example I could run with only a token. Note in one line each: the parameter most commonly confused, and the error that new integrators hit first.
```

### 44. First-Week Onboarding Plan
```
Act as an onboarding guide author who has watched [N] new hires fail and fixed the causes. Create a first-week plan for a new [ROLE] joining a [STACK] codebase: Day 1 — environment setup with the exact commands in order, including the 3 setup steps that break on new machines and their fixes; Day 2 — code walkthrough order (which modules first and why, what to skip until week 2); Day 3 — their first good-first-issue with acceptance criteria, plus the person to ask; Day 4-5 — the first small PR and what a good one looks like here. Include a glossary of our 10 internal terms: [LIST TERMS — or ask me to supply them].
```

### 45. User-Facing Release Notes
```
You are a changelog writer whose notes users actually read. Turn these commits into user-facing release notes for version [X.Y.Z]: [PASTE COMMITS]. Group by Added/Changed/Fixed; write from the user's perspective — what changed FOR THEM, not what we did (kill refactors and internal cleanup from the visible list unless behavior changed). Each entry: one sentence, plain language, the benefit or impact visible. Add an upgrade note for breaking changes with the exact migration step. Top it with a one-line TL;DR for the skimmers. Flag any commit too vague to translate and tell me what to ask the author.
```

### 46. Architecture Decision Record (ADR)
```
Act as a technical decision record facilitator. We are deciding between [OPTION A] and [OPTION B] for [DECISION — e.g., queue technology, frontend framework, monorepo vs polyrepo]. Write an ADR: (1) context — the forces at play, the constraints that are real vs. assumed, (2) considered options with a tradeoff table (at least 3 options including "do nothing"), (3) decision criteria weighted by what this team actually optimizes for, (4) the chosen option stated plainly, (5) consequences — including what we're giving up, and (6) the revisit triggers: the specific conditions under which this decision should be reopened. Written so a new engineer in 2 years understands why without asking anyone.
```

### 47. Developer Experience Audit
```
You are a developer experience auditor. My team complains: [COMPLAINTS — e.g., slow tests, flaky builds, unclear errors]. Diagnose the 5 most common DX killers in a [STACK] repo (slow feedback loops, flaky tests eroding trust, unclear error messages, mystery builds, missing context). For each: the measurement — a metric with a number (test duration p95, flake rate, time-to-first-green-build for a new hire) so this isn't vibes, the 30-day improvement plan with before/after targets, and the quick win for week 1. Order by trust-erosion severity. Include the one DX fix that backfired at most companies and how to avoid it.
```

### 48. Lint & Format Setup That Ends Debates
```
Act as a code style arbiter whose setups end style arguments permanently. Design a linting and formatting setup for [LANGUAGE]: tool choices with one-line justifications, the 10 rules that matter most (each with a one-line rationale tied to a real bug class it prevents — not taste), the config that applies them, and the CI enforcement (fix automatically where possible, block where necessary). Then state what to leave UNLINTED and why — the places where rules do more harm than good. Include the migration path for a legacy codebase: how to adopt without a 10,000-line PR that destroys git blame.
```

### 49. The Refactoring Business Case
```
You are a refactoring storyteller who gets engineering time approved by speaking business. I need [TIME — e.g., 2 weeks of the team] to refactor [MODULE]. Write the one-page case: (1) current cost in numbers — bug rate attributable to this module, onboarding time tax, velocity decline, incident hours this quarter (use my placeholders: [METRICS] and mark clearly which need real data before presenting), (2) proposed target design in 5 sentences, (3) a phased plan that ships user-visible value every week (never a dark-month rewrite), and (4) the risks of doing nothing, stated as next-quarter consequences. Frame for [AUDIENCE — e.g., a non-technical founder]: outcome language, not architecture language.
```

### 50. Legacy Code Translator
```
Act as a legacy code translator — the engineer they call in when the last person who understood a system left. Explain this legacy [LANGUAGE] code: [PASTE CODE]. Provide: (1) what it does in plain English, step by step, (2) the implicit business rules it encodes — the rules that live only in this code, marked with ⚠️ because they'll need to be re-implemented anywhere it's ported, (3) landmines: side effects, global state, ordering dependencies, and the input that makes it behave differently than it looks, and (4) a safe modernization path in 3 steps — starting with the characterization test to write first that locks in current behavior before anyone changes a line.
```

---

## How to Use This Pack

1. **Match the prompt to the job** — pick the section you need; don't read linearly.
2. **Fill the [BRACKETS]** — the more specific your inputs (real code, real errors, real scale numbers), the better the output. Vague in, vague out.
3. **Iterate** — when the first output is 80% right, reply with what to change ("keep the plan, add the rollback steps, drop the tool recommendations") instead of regenerating from scratch.
4. **Own the result** — the prompts encode senior-engineer structures, but you review the code before it ships.

*License: single user. Resale or redistribution of this pack is not permitted. Questions: [CONTACT].*
