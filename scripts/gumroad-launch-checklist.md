# Gumroad Post-Creation Checklist & Traffic-Ready Link Templates

> **Status:** Pre-launch template  
> **Last updated:** 2026-08-22  
> **Goal:** Verify account, configure payouts, upload products in the right order, and have traffic-ready links ready before launch.

---

## 1. Account Verification Steps

Complete these inside your Gumroad dashboard (`Settings → Account`):

- [ ] **Confirm email address** — check inbox for verification link; mark as primary if multiple emails exist.
- [ ] **Enable two-factor authentication (2FA)** — use an authenticator app (Google Authenticator / Authy). Screenshot backup codes and store them offline.
- [ ] **Verify phone number** — required for payouts and fraud prevention in many regions.
- [ ] **Confirm identity / KYC (if prompted)** — upload government-issued ID and proof of address if Gumroad flags your account.
- [ ] **Review connected apps** — disconnect any unused third-party integrations to reduce attack surface.
- [ ] **Set timezone correctly** — ensures sales timestamps and payout schedules align with your local time.

---

## 2. Payout Setup

Payouts are configured under `Settings → Payouts`:

- [ ] **Link payment method**
  - PayPal (available in most countries) or
  - Bank transfer (direct deposit) or
  - Payoneer (where PayPal is restricted)
- [ ] **Add payout email / account** — ensure it matches the name on your Gumroad account to avoid holds.
- [ ] **Set payout threshold** — default is $10; raise it if you prefer fewer, larger transfers.
- [ ] **Review payout schedule** — Gumroad pays daily (Mon–Fri) once balance exceeds threshold, or weekly/monthly depending on region.
- [ ] **Test a sale** (optional but recommended) — buy your own product with a different payment method to confirm funds route correctly.
- [ ] **Save payout method as default** — avoid accidental splits or new-payment-method prompts during a live launch.

---

## 3. Tax Info

Configure under `Settings → Tax info`:

- [ ] **Complete W-8BEN (non-US creators) or W-9 (US creators)** — required for tax reporting; upload through Gumroad's tax wizard.
- [ ] **Provide VAT number if applicable (EU/UK)** — necessary if registered for VAT; otherwise Gumroad handles reverse-charge.
- [ ] **Set tax rate per product** — decide if you collect sales tax / VAT from buyers or if Gumroad handles it at checkout.
- [ ] **Download a copy of submitted tax form** — save PDF locally for your records.
- [ ] **Note: Gumroad does not withhold tax automatically in most jurisdictions** — consult a local tax advisor for your specific obligations.

---

## 4. Product Upload Order

Upload products in this sequence to ensure preview and checkout links work before announcing:

1. **Create the free lead magnet first**
   - Use it as the "free download" on your landing page to build your email list.
   - Example: `your-product-free-preview.pdf`

2. **Upload the paid flagship product second**
   - Enable "I want buyers to enter their email" to capture leads.
   - Set the final price after testing.
   - Add a clear title, description, and at least one cover image (recommended: 1280×720 px).

3. **Add a "bundle" or upsell third (optional)**
   - If offering a premium tier, create it after the base product so the upgrade path is clear.

4. **Enable product visibility settings**
   - [ ] Toggle product to **Public** (unlisted works too if you control the link).
   - [ ] Set "Notify existing customers" to **Off** during setup.
   - [ ] Disable "Allow sharing on Gumroad discovery" if you want zero Gumroad-driven traffic initially.

---

## 5. Traffic-Ready Link Templates

### Core Product Link
```
https://gumroad.com/l/your-product-handle
```

### Shortened / Tracking Variant
```
https://gumroad.com/l/your-product-handle?wanted=true
```

> Replace `your-product-handle` with your actual product slug. The `?wanted=true` query parameter can be appended to any link for basic UTM-like tracking in Gumroad's analytics.

### Social Post Templates

> **Instructions:** Copy the block below into each post. Fill in `{{product_name}}`, `{{short_description}}`, and `{{gumroad_link}}`. Do **not** publish these yet — save as drafts or store here for copy-paste.

---

#### Twitter / X Post

```
🚀 {{product_name}} is almost here.

{{short_description}}

Get early access → {{gumroad_link}}

#{{topic}} #AI #DigitalProducts
```

---

#### LinkedIn Post

```
I'm launching {{product_name}} — {{short_description}}.

If you've been looking for a way to [primary benefit], this is for you.

Early access link (limited slots): {{gumroad_link}}

Drop a 🔥 if you want me to send you a reminder.
```

---

#### Instagram / Threads Caption

```
✨ something new is coming...

{{product_name}} → {{short_description}}

Tap the link in bio to get early access 👉 {{gumroad_link}}

#{{topic}} #CreatorEconomy #AITools
```

---

#### Facebook Post

```
Hey everyone — just a heads up that {{product_name}} is now available.

{{short_description}}

Grab it here: {{gumroad_link}}

Share with someone who needs this.
```

---

#### Reddit Post (text post, no direct link spam — follow sub rules)

```
Title: [Resource] {{product_name}} — {{short_description}}

Body:
I built this because [one-sentence motivation].

It covers:
- [bullet 1]
- [bullet 2]
- [bullet 3]

Happy to answer questions in the comments. If it looks useful, the link is in my profile / first comment per sub rules.
```

> ⚠️ **Reddit warning:** Do not paste the Gumroad link in the post body unless the sub allows it. Link from your profile or a pinned comment instead.

---

#### YouTube Community Post

```
{{product_name}} is live on Gumroad 👇

{{short_description}}

{{gumroad_link}}
```

---

#### Email Announcement (for your list)

```
Subject: {{product_name}} — now available

Hi {{first_name}},

{{short_description}}

Grab your copy here: {{gumroad_link}}

Questions? Hit reply.

— {{your_name}}
```

---

## 6. 24-Hour Launch Timeline

Use this checklist on launch day to stay on schedule without scrambling.

| Time | Task | Done |
|------|------|------|
| **-24h** | Finalize product files; double-check pricing and description. | [ ] |
| **-24h** | Test purchase flow (buy your own product); confirm email delivery works. | [ ] |
| **-24h** | Verify payout method is active and tax forms are submitted. | [ ] |
| **-24h** | Schedule or save-draft all social posts with correct `{{gumroad_link}}`. | [ ] |
| **-24h** | Prepare any visual assets (cover image, preview GIF, tweet image). | [ ] |
| **-12h** | Send reminder to email list ("launching tomorrow"). | [ ] |
| **-1h** | Do final screenshot of dashboard sales count at zero (for "from 0 to X" social proof later). | [ ] |
| **T-0 (Launch)** | Flip product from Unlisted → Public (if not already). | [ ] |
| **T+15m** | Post to Twitter / X. | [ ] |
| **T+30m** | Post to LinkedIn. | [ ] |
| **T+45m** | Post to Instagram / Threads. | [ ] |
| **T+1h** | Post to Facebook group/page. | [ ] |
| **T+1.5h** | Submit to relevant subreddits (follow rules). | [ ] |
| **T+2h** | Post YouTube community update (if channel is live). | [ ] |
| **T+3h** | Send launch email to list. | [ ] |
| **T+4h** | Respond to every comment / DM within 15 minutes. | [ ] |
| **T+6h** | Share a testimonial or early-feedback screenshot (if any sales). | [ ] |
| **T+8h** | Post "still live" reminder with a different hook or benefit. | [ ] |
| **T+12h** | Update link-in-bio to point directly to product (if using link-in-bio services). | [ ] |
| **T+18h** | Share a behind-the-scenes or BTS story about why you built the product. | [ ] |
| **T+24h** | Review analytics: clicks, conversion rate, top traffic source. Document learnings. | [ ] |

---

## Quick Reference: What NOT to Do

- ❌ Do **not** publish real posts yet — use the templates above and save them as drafts.
- ❌ Do **not** lower the price impulsively within the first 24 hours.
- ❌ Do **not** ignore the email list — they are your highest-converting audience.
- ❌ Do **not** post affiliate links before confirming your payout / tax setup is complete.
- ❌ Do **not** forget to turn off "Notify existing customers" until you are ready to announce.

---

## Next Steps

1. Fill in all `{{placeholder}}` values above with your real product details.
2. Save this file as `scripts/gumroad-launch-checklist.md`.
3. Complete every checkbox in Sections 1–4.
4. Draft (but do not publish) all social posts from Section 5.
5. Run through the 24-hour timeline once as a dry run before launch day.

---

*End of checklist.*
