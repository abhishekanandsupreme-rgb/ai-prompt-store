# Telegram Delivery Setup — AI Prompt Store

> **Current state:** Telegram user **Abhishek** (`id: 8545318720`) is already connected to this Hermes session (confirmed in `C:\Users\asus\AppData\Local\hermes\channel_directory.json`).  
> This guide turns that connection into a full digital-product delivery pipeline: direct file sends, auto-replies, a public storefront channel, and Gumroad webhook integration.

---

## Table of Contents

1. [What We're Building](#1-what-were-building)
2. [Prerequisites](#2-prerequisites)
3. [Option A — Manual Delivery (Fastest)](#3-option-a--manual-delivery-fastest)
4. [Option B — Bot Auto-Delivery (Recommended)](#4-option-b--bot-auto-delivery-recommended)
5. [Option C — Gumroad Webhook → Telegram](#5-option-c--gumroad-webhook--telegram)
6. [Create a Telegram Channel / Storefront](#6-create-a-telegram-channel--storefront)
7. [Auto-Reply Templates](#7-auto-reply-templates)
8. [Commands Cheat-Sheet](#8-commands-cheat-sheet)
9. [Troubleshooting](#9-troubleshooting)
10. [Security & Best Practices](#10-security--best-practices)

---

## 1. What We're Building

| Component | Purpose |
|-----------|---------|
| **Direct DM delivery** | Send prompt ZIPs / Markdown files to buyers in Telegram |
| **Auto-reply bot** | Respond to keywords (`/buy`, `/bundle`, `/help`) instantly |
| **Storefront channel** | Public channel where new products are announced |
| **Gumroad webhook bridge** | When Gumroad fires a sale event, auto-deliver the file on Telegram |

---

## 2. Prerequisites

### 2.1 Confirm Abhishek Connection

```powershell
# Verify the channel directory entry
Get-Content "C:\Users\asus\AppData\Local\hermes\channel_directory.json"
```

Expected output:
```json
{
  "platforms": {
    "telegram": [
      {
        "id": "8545318720",
        "name": "Abhishek",
        "type": "dm"
      }
    ]
  }
}
```

### 2.2 Product Files Ready

All deliverable files live in `C:\Users\asus\ai-prompt-store\products\`:

| Product | Path |
|---------|------|
| Individual Pack 1 | `products/prompt-pack-1/prompts.md` |
| … Pack 10 | `products/prompt-pack-10/prompts.md` |
| Bundle | `products/bundle-all-10-packs.zip` |

### 2.3 Create a Telegram Bot (if you don't have one)

1. Open Telegram, search for **@BotFather**
2. Send `/newbot`
3. Name it: `AI Prompt Store Delivery`
4. Username: `ai_prompt_store_bot` (must end in `bot`)
5. **Copy the API token** — it looks like `123456789:ABCdefGhIJKlmNoPQRstUvWxYz123456`
6. Save it securely (you'll need it in the scripts below)

### 2.4 Get Your Chat ID

```powershell
# Send any message to @ai_prompt_store_bot first, then run:
curl -s "https://api.telegram.org/bot<YOUR_TOKEN>/getUpdates" | Select-String "chat"
```

Look for:
```json
"id": 8545318720,
"first_name": "Abhishek",
"username": "..." 
```

If you want a **group / channel ID**, add the bot to the group, send a message, and check `getUpdates` again. Channel IDs are negative numbers (e.g., `-1001234567890`).

---

## 3. Option A — Manual Delivery (Fastest)

Use this when you want to send files to specific buyers one-off without writing code.

### 3.1 Send a File via curl

```powershell
# Variables
$BOT_TOKEN = "123456789:ABCdefGhIJKlmNoPQRstUvWxYz123456"
$CHAT_ID = "8545318720"
$PRODUCT_ZIP = "C:\Users\asus\ai-prompt-store\products\bundle-all-10-packs.zip"

# Send the bundle ZIP
curl -F "chat_id=$CHAT_ID" `
     -F "document=@$PRODUCT_ZIP;filename=bundle-all-10-packs.zip" `
     -F "caption=🎉 Here's your Complete AI Prompt Bundle! 500+ prompts inside." `
     "https://api.telegram.org/bot$BOT_TOKEN/sendDocument"
```

### 3.2 Send a Single Pack

```powershell
$PRODUCT = "C:\Users\asus\ai-prompt-store\products\prompt-pack-3\prompts.md"
curl -F "chat_id=$CHAT_ID" `
     -F "document=@$PRODUCT;filename=ai-coding-assistant-pack.md" `
     -F "caption=💻 Your AI Coding Assistant Pack (50 prompts)" `
     "https://api.telegram.org/bot$BOT_TOKEN/sendDocument"
```

### 3.3 Send a Text Message

```powershell
curl -X POST "https://api.telegram.org/bot$BOT_TOKEN/sendMessage" `
     -H "Content-Type: application/json" `
     -d '{"chat_id":"8545318720","text":"Thanks for purchasing! Your download is below."}'
```

---

## 4. Option B — Bot Auto-Delivery (Recommended)

This creates a Python Telegram bot that auto-responds to commands and delivers files from the `products/` folder.

### 4.1 Install Dependencies

```powershell
# From the project root
cd C:\Users\asus\ai-prompt-store

# Create a virtual environment
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# Install the Telegram bot library
pip install python-telegram-bot==20.7
```

> **Note:** `python-telegram-bot` v20 uses `async`/`await`. The script below is tested against v20.7.

### 4.2 Create `telegram-delivery-bot.py`

Create the file at `C:\Users\asus\ai-prompt-store\telegram-delivery-bot.py`:

```python
"""
AI Prompt Store — Telegram Delivery Bot
Delivers digital products and handles auto-replies.
"""
import os
import logging
from pathlib import Path
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters,
    ContextTypes,
)

# --------------------------- CONFIG ---------------------------
PROJECT_ROOT = Path(r"C:\Users\asus\ai-prompt-store")
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "YOUR_BOT_TOKEN_HERE")

# Product catalog
PRODUCTS = {
    "bundle": {
        "name": "Complete AI Prompt Bundle (500+ Prompts)",
        "price": "$27.99",
        "file": PROJECT_ROOT / "products" / "bundle-all-10-packs.zip",
        "description": "All 10 packs at 72% off. Instant download.",
        "tags": ["bundle", "all", "complete"],
    },
    "pack1": {
        "name": "AI Content Creator Pack",
        "price": "$9.99",
        "file": PROJECT_ROOT / "products" / "prompt-pack-1" / "prompts.md",
        "description": "50 prompts for YouTube, social media, blogs & email.",
        "tags": ["content", "social", "youtube", "blog"],
    },
    "pack2": {
        "name": "AI Business Builder Pack",
        "price": "$9.99",
        "file": PROJECT_ROOT / "products" / "prompt-pack-2" / "prompts.md",
        "description": "50 prompts for strategy, planning & growth.",
        "tags": ["business", "strategy", "startup"],
    },
    "pack3": {
        "name": "AI Coding Assistant Pack",
        "price": "$9.99",
        "file": PROJECT_ROOT / "products" / "prompt-pack-3" / "prompts.md",
        "description": "50 prompts for developers — debug, code, document.",
        "tags": ["coding", "developer", "programming"],
    },
    # Add pack4-10 here following the same pattern
}

# Approved chat IDs (Abhishek + any staff)
ALLOWED_USERS = {int(os.getenv("ALLOWED_USER_ID", "8545318720"))}

# --------------------------- HELPERS ---------------------------
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


def is_authorized(user_id: int) -> bool:
    return user_id in ALLOWED_USERS


async def safe_reply(update: Update, text: str):
    """Reply to the user, falling back to direct chat send if no message context."""
    try:
        if update.message:
            await update.message.reply_text(text)
        else:
            await update.effective_chat.send_message(text)
    except Exception as e:
        logger.error(f"Failed to send message: {e}")


# --------------------------- COMMANDS ---------------------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_authorized(update.effective_user.id):
        await safe_reply(update, "⛔ Unauthorized. Contact the store owner.")
        return

    await safe_reply(
        update,
        "👋 Welcome to the AI Prompt Store!\n\n"
        "Commands:\n"
        "/browse — See all products\n"
        "/buy <pack_id> — Get a download link (Gumroad)\n"
        "/deliver <pack_id> — Direct file delivery (staff only)\n"
        "/help — Show this menu",
    )


async def browse(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_authorized(update.effective_user.id):
        await safe_reply(update, "⛔ Unauthorized.")
        return

    lines = ["📦 *Available Products:*\n"]
    for pid, prod in PRODUCTS.items():
        lines.append(f"• `{pid}` — {prod['name']} ({prod['price']})\n  _{prod['description']}_\n")

    await safe_reply(update, "\n".join(lines))


async def buy(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a Gumroad purchase link."""
    if not is_authorized(update.effective_user.id):
        await safe_reply(update, "⛔ Unauthorized.")
        return

    if not context.args:
        await safe_reply(update, "Usage: /buy <pack_id>\nExample: /buy bundle")
        return

    pid = context.args[0].lower()
    if pid not in PRODUCTS:
        await safe_reply(update, f"❌ Unknown product `{pid}`. Use /browse to see options.")
        return

    gumroad_slug = {
        "bundle": "complete-ai-prompt-bundle",
        "pack1": "ai-content-creator-pack",
        "pack2": "ai-business-builder-pack",
        "pack3": "ai-coding-assistant-pack",
        # extend for pack4-10
    }.get(pid, pid)

    url = f"https://ai-prompt-store.gumroad.com/l/{gumroad_slug}"
    prod = PRODUCTS[pid]
    await safe_reply(
        update,
        f"🛒 *{prod['name']}* — {prod['price']}\n\n"
        f"Buy here: {url}\n\n"
        f"After purchase, you will receive the file automatically here.",
    )


async def deliver(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Staff-only: send the actual file directly."""
    if not is_authorized(update.effective_user.id):
        await safe_reply(update, "⛔ Unauthorized. This is a staff-only command.")
        return

    if not context.args:
        await safe_reply(update, "Usage: /deliver <pack_id>")
        return

    pid = context.args[0].lower()
    if pid not in PRODUCTS:
        await safe_reply(update, f"❌ Unknown product `{pid}`.")
        return

    prod = PRODUCTS[pid]
    file_path = prod["file"]

    if not file_path.exists():
        await safe_reply(update, f"⚠️ File not found: `{file_path}`")
        return

    await safe_reply(update, f"📤 Sending *{prod['name']}*...")
    try:
        await context.bot.send_document(
            chat_id=update.effective_chat.id,
            document=open(file_path, "rb"),
            filename=file_path.name,
            caption=f"✅ {prod['name']}\n\n{prod['description']}\n\nThanks for your purchase!",
        )
    except Exception as e:
        logger.error(f"Delivery failed: {e}")
        await safe_reply(update, f"❌ Failed to send file: {e}")


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await start(update, context)


# --------------------------- AUTO-REPLIES ---------------------------
async def auto_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Keyword-based auto-replies for common questions."""
    if not is_authorized(update.effective_user.id):
        return

    text = (update.message.text or "").lower().strip()

    responses = {
        "price": "Individual packs are $9.99. The complete bundle is $27.99 (72% off). Use /buy to purchase.",
        "payment": "We use Gumroad for secure payments. Credit card, PayPal, and Apple Pay are accepted.",
        "refund": "We offer a 14-day no-questions-asked refund policy. Contact us here.",
        "format": "All products are delivered as .md (Markdown) or .zip files. They work on any device.",
        "hello": "Hey! 👋 Use /browse to see our prompt packs or /buy to get started.",
        "hi": "Hi there! Use /browse to see our prompt packs or /buy to get started.",
        "help": "Use /browse to see products, /buy <id> to purchase, or /deliver <id> for direct file access.",
    }

    for keyword, reply in responses.items():
        if keyword in text:
            await safe_reply(update, reply)
            return


# --------------------------- MAIN ---------------------------
def main():
    if BOT_TOKEN == "YOUR_BOT_TOKEN_HERE":
        raise ValueError("Set TELEGRAM_BOT_TOKEN env var or edit BOT_TOKEN in the script.")

    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("browse", browse))
    app.add_handler(CommandHandler("buy", buy))
    app.add_handler(CommandHandler("deliver", deliver))
    app.add_handler(CommandHandler("help", help_command))

    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, auto_reply))

    logger.info("Bot started. Press Ctrl+C to stop.")
    app.run_polling()


if __name__ == "__main__":
    main()
```

### 4.3 Run the Bot

```powershell
# From the project root
cd C:\Users\asus\ai-prompt-store
.\.venv\Scripts\Activate.ps1

# Set your bot token as an environment variable (Windows PowerShell)
$env:TELEGRAM_BOT_TOKEN = "123456789:ABCdefGhIJKlmNoPQRstUvWxYz123456"

# Run the bot
python telegram-delivery-bot.py
```

Keep this terminal open — the bot polls Telegram for updates.

### 4.4 Keep the Bot Running in Background (Windows)

```powershell
# Start as a background job (PowerShell)
Start-Job -ScriptBlock {
    Set-Location C:\Users\asus\ai-prompt-store
    .\.venv\Scripts\Activate.ps1
    python telegram-delivery-bot.py
}
```

Or use **Windows Task Scheduler** to run at startup:
- Trigger: At log on
- Action: `C:\Users\asus\ai-prompt-store\.venv\Scripts\python.exe`
- Arguments: `C:\Users\asus\ai-prompt-store\telegram-delivery-bot.py`
- Start in: `C:\Users\asus\ai-prompt-store`

---

## 5. Option C — Gumroad Webhook → Telegram

Gumroad can POST sale events to your server. We'll build a tiny Flask receiver that forwards the event to Telegram.

### 5.1 Why This Works

Gumroad doesn't have a native "send to Telegram" button, but it has **webhooks**. When someone buys a product, Gumroad sends a JSON payload to your URL. Your server reads the buyer's email / ID and delivers the file on Telegram.

### 5.2 Install Dependencies

```powershell
cd C:\Users\asus\ai-prompt-store
.\.venv\Scripts\Activate.ps1
pip install flask python-telegram-bot==20.7 requests
```

### 5.3 Create `gumroad-telegram-bridge.py`

```python
"""
Gumroad Webhook → Telegram Delivery Bridge
Receives Gumroad sale events and auto-delivers files on Telegram.
"""
import os
import hmac
import hashlib
import logging
from pathlib import Path
from flask import Flask, request, jsonify
from telegram import Bot
from telegram.constants import ParseMode

# --------------------------- CONFIG ---------------------------
PROJECT_ROOT = Path(r"C:\Users\asus\ai-prompt-store")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "YOUR_BOT_TOKEN")
ALLOWED_USER_ID = int(os.getenv("ALLOWED_USER_ID", "8545318720"))
GUMROAD_WEBHOOK_SECRET = os.getenv("GUMROAD_WEBHOOK_SECRET", "")  # Optional but recommended

# Map Gumroad product IDs to local files
PRODUCT_MAP = {
    "ai-content-creator-pack": PROJECT_ROOT / "products" / "prompt-pack-1" / "prompts.md",
    "ai-business-builder-pack": PROJECT_ROOT / "products" / "prompt-pack-2" / "prompts.md",
    "ai-coding-assistant-pack": PROJECT_ROOT / "products" / "prompt-pack-3" / "prompts.md",
    "complete-ai-prompt-bundle": PROJECT_ROOT / "products" / "bundle-all-10-packs.zip",
    # Extend with all 10 pack slugs
}

app = Flask(__name__)
bot = Bot(token=TELEGRAM_BOT_TOKEN)
logger = logging.getLogger(__name__)


def verify_gumroad_signature(payload: bytes, signature: str) -> bool:
    """Optional: verify Gumroad webhook signature."""
    if not GUMROAD_WEBHOOK_SECRET:
        return True
    expected = hmac.new(
        GUMROAD_WEBHOOK_SECRET.encode(), payload, hashlib.sha256
    ).hexdigest()
    return hmac.compare_digest(expected, signature)


@app.route("/webhook/gumroad", methods=["POST"])
def gumroad_webhook():
    # 1. Verify signature (if configured)
    signature = request.headers.get("X-Gumroad-Signature", "")
    if not verify_gumroad_signature(request.data, signature):
        logger.warning("Invalid Gumroad signature")
        return jsonify({"status": "error", "reason": "bad_signature"}), 403

    event = request.json
    logger.info(f"Gumroad event: {event.get('event_name', 'unknown')}")

    # 2. Only process successful sale events
    if event.get("event_name") not in ("sale", "purchase"):
        return jsonify({"status": "ignored"}), 200

    # 3. Extract buyer info
    buyer_email = event.get("email", "")
    product_id = event.get("product_id", "")
    product_name = event.get("product_name", "Unknown Product")

    # 4. Find the file
    file_path = PRODUCT_MAP.get(product_id)
    if not file_path or not file_path.exists():
        logger.error(f"No file mapped for product {product_id}")
        return jsonify({"status": "error", "reason": "no_file"}), 404

    # 5. Deliver via Telegram
    try:
        caption = (
            f"🎉 Thanks for purchasing *{product_name}*!\n\n"
            f"Your download is attached. If you have any issues, reply here.\n\n"
            f"Buyer: {buyer_email}"
        )
        with open(file_path, "rb") as f:
            bot.send_document(
                chat_id=ALLOWED_USER_ID,
                document=f,
                filename=file_path.name,
                caption=caption,
                parse_mode=ParseMode.MARKDOWN,
            )
        logger.info(f"Delivered {file_path.name} to Telegram user {ALLOWED_USER_ID}")
    except Exception as e:
        logger.error(f"Telegram delivery failed: {e}")
        return jsonify({"status": "error", "reason": str(e)}), 500

    return jsonify({"status": "delivered"}), 200


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"}), 200


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
```

### 5.4 Run the Bridge

```powershell
# From the project root
cd C:\Users\asus\ai-prompt-store
.\.venv\Scripts\Activate.ps1

$env:TELEGRAM_BOT_TOKEN = "123456789:ABCdefGhIJKlmNoPQRstUvWxYz123456"
$env:ALLOWED_USER_ID = "8545318720"

python gumroad-telegram-bridge.py
```

### 5.5 Expose to the Internet (for Gumroad to reach you)

Gumroad needs a public HTTPS URL. On Windows, use **ngrok**:

1. Download ngrok from https://ngrok.com/download
2. Sign up (free) and run:

```powershell
# Expose local port 5000
ngrok http 5000
```

You'll get a URL like `https://abc1-23-45-67-89.ngrok-free.app`.

### 5.6 Configure Gumroad Webhook

1. Log in to Gumroad → **Settings** → **Advanced** → **Webhooks**
2. Paste your ngrok URL: `https://abc1-23-45-67-89.ngrok-free.app/webhook/gumroad`
3. (Optional but recommended) Set a **Webhook Secret** — copy it into `GUMROAD_WEBHOOK_SECRET` env var
4. Save

Now every sale will auto-deliver the file to Telegram user 8545318720.

> **Caveat:** Free ngrok URLs change every time you restart. For production, host this on Render, Fly.io, or a VPS with a static domain.

---

## 6. Create a Telegram Channel / Storefront

A public channel lets you broadcast new products, promos, and announcements.

### 6.1 Create the Channel

1. Open Telegram → **New Channel**
2. Name: `AI Prompt Store`
3. Username: `@ai_prompt_store` (or similar)
4. Set as **Public**
5. Invite your bot (`@ai_prompt_store_bot`) as an **Administrator** (it needs permission to post)

### 6.2 Post Your First Announcement

```powershell
$BOT_TOKEN = "123456789:ABCdefGhIJKlmNoPQRstUvWxYz123456"
$CHANNEL_ID = "@ai_prompt_store"

$body = @{
    chat_id = $CHANNEL_ID
    text = "🚀 Welcome to AI Prompt Store!
We drop 50+ expert AI prompts every week.
👇 Browse our collection:"
    reply_markup = '{
        "inline_keyboard": [
            [
                {"text": "🎁 Complete Bundle ($27.99)", "url": "https://ai-prompt-store.gumroad.com/l/complete-ai-prompt-bundle"},
                {"text": "📦 All Products", "url": "https://ai-prompt-store.gumroad.com"}
            ]
        ]
    }'
} | ConvertTo-Json

Invoke-RestMethod -Uri "https://api.telegram.org/bot$BOT_TOKEN/sendMessage" `
    -Method Post `
    -ContentType "application/json" `
    -Body $body
```

### 6.3 Auto-Post New Products to Channel

Add this to `telegram-delivery-bot.py`:

```python
async def announce_to_channel(context: ContextTypes.DEFAULT_TYPE, text: str):
    channel_id = os.getenv("TELEGRAM_CHANNEL_ID", "@ai_prompt_store")
    try:
        await context.bot.send_message(chat_id=channel_id, text=text)
    except Exception as e:
        logger.error(f"Channel post failed: {e}")
```

Call it whenever you add a new product.

---

## 7. Auto-Reply Templates

Store these in `telegram-replies.md` (or embed them in the bot) for consistent responses:

### 7.1 Welcome Message

```
👋 Hey! Welcome to AI Prompt Store.

I sell battle-tested AI prompts that save you hours of work.

🔥 Hot deal: Complete Bundle — 500+ prompts for $27.99 (normally $99.99).

Type /buy bundle to get it, or /browse to see all 10 packs.
```

### 7.2 Delivery Confirmation

```
✅ Your file is attached!

📦 Product: AI Coding Assistant Pack
💵 Price: $9.99

Need help? Just reply to this message.
Want the full bundle? Use /buy bundle
```

### 7.3 Support / Refund

```
📩 Support request received.

We'll get back to you within 24 hours.

In the meantime, check our FAQ:
• Files are .md and .zip — open on any device
• Refunds: 14-day no-questions-asked
• Updates: Free for life
```

---

## 8. Commands Cheat-Sheet

| Action | Command / Script |
|--------|------------------|
| Send bundle to Abhishek | `curl -F "chat_id=8545318720" -F "document=@C:\Users\asus\ai-prompt-store\products\bundle-all-10-packs.zip" "https://api.telegram.org/bot<TOKEN>/sendDocument"` |
| Start bot locally | `python telegram-delivery-bot.py` |
| Run bridge locally | `python gumroad-telegram-bridge.py` |
| Expose bridge (ngrok) | `ngrok http 5000` |
| Get bot updates | `curl "https://api.telegram.org/bot<TOKEN>/getUpdates"` |
| Post to channel | Use the PowerShell snippet in §6.2 |
| Test webhook locally | `curl -X POST http://localhost:5000/webhook/gumroad -H "Content-Type: application/json" -d '{"event_name":"sale","email":"test@test.com","product_id":"complete-ai-prompt-bundle","product_name":"Bundle"}'` |

---

## 9. Troubleshooting

### 9.1 Bot Not Responding

| Symptom | Fix |
|---------|-----|
| `/start` returns nothing | Ensure bot is running (`python telegram-delivery-bot.py`). Check for `Unauthorized` error — token may be wrong. |
| `401 Unauthorized` | Bot token is invalid or revoked. Re-create bot via @BotFather. |
| `403 Forbidden` | User blocked the bot, or chat ID is wrong. Verify with `/getUpdates`. |
| No updates arriving | Make sure you sent a message to the bot **after** starting it. Telegram only sends updates that occur after the bot connects. |

### 9.2 File Delivery Fails

| Symptom | Fix |
|---------|-----|
| `File too large` | Telegram document limit is 50 MB. Your ZIP is ~8 KB — fine. If you ever hit the limit, split the ZIP or host on Google Drive and send a link. |
| `File not found` | Double-check the path in `PRODUCTS`. Use absolute paths (the script already does this). |
| `Bad Request: wrong file identifier` | Don't send a URL as `document`. Use `sendDocument` with a file path, or `sendMessage` with a link. |

### 9.3 Gumroad Webhook Not Firing

| Symptom | Fix |
|---------|-----|
| Gumroad shows "Webhook URL is invalid" | Your ngrok/VPS URL must be HTTPS. Gumroad rejects HTTP. |
| No events received | Gumroad only fires webhooks for **new** sales. Re-test with a $0.01 purchase if possible. |
| `Invalid signature` | Copy the exact secret from Gumroad into `GUMROAD_WEBHOOK_SECRET`. No extra spaces. |
| Events arrive but file not sent | Check `PRODUCT_MAP` — the `product_id` from Gumroad must match your dictionary key exactly. |

### 9.4 Channel Posts Not Showing

| Symptom | Fix |
|---------|-----|
| `Chat not found` | Bot must be an **admin** in the channel. Re-invite with admin rights. |
| Messages silently fail | Channels can't receive messages from users — only admins/bots. Make sure you're posting as the bot, not your user account. |

### 9.5 Windows-Specific Issues

| Symptom | Fix |
|---------|-----|
| `Activate.ps1` blocked | Run PowerShell as Admin: `Set-ExecutionPolicy RemoteSigned -Scope CurrentUser` |
| `python` not found | Use `py` or the full path `C:\Users\asus\ai-prompt-store\.venv\Scripts\python.exe` |
| Port 5000 already in use | Change `port=5000` in `gumroad-telegram-bridge.py` to `5001` and update ngrok accordingly |

---

## 10. Security & Best Practices

1. **Never commit bot tokens** to git. Use environment variables (`TELEGRAM_BOT_TOKEN`, `GUMROAD_WEBHOOK_SECRET`).
2. **Restrict `ALLOWED_USERS`** in the bot — don't let strangers trigger `/deliver`.
3. **Use HTTPS** for the webhook receiver. Ngrok is fine for testing; Render/Fly/VPS for production.
4. **Verify Gumroad signatures** — set a webhook secret to prevent spoofed requests.
5. **Rate-limit** the `/deliver` command if you expose the bot publicly.
6. **Log everything** — the scripts already use `logging`. Pipe logs to a file in production:
   ```powershell
   python telegram-delivery-bot.py >> delivery-bot.log 2>&1
   ```
7. **Back up product files** — keep `products/` in git. If a file is lost, delivery breaks.
8. **Test before sharing** — send one test delivery to your own Telegram ID before announcing the bot publicly.

---

## Quick Start (Copy-Paste)

```powershell
# 1. Create bot via @BotFather, copy token
# 2. Install
cd C:\Users\asus\ai-prompt-store
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install python-telegram-bot==20.7 flask requests

# 3. Save telegram-delivery-bot.py (from §4.2)
# 4. Save gumroad-telegram-bridge.py (from §5.3)

# 5. Run bot
$env:TELEGRAM_BOT_TOKEN = "YOUR_TOKEN"
python telegram-delivery-bot.py

# 6. In another terminal, run bridge (optional)
python gumroad-telegram-bridge.py

# 7. Test in Telegram: /start /browse /buy bundle
```

---

*Guide generated for AI Prompt Store. Last updated: 2026-08-22.*
