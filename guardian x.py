import re
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# --- Configuration ---
BOT_TOKEN = "YOUR_BOT_TOKEN"  # 7684191272:AAHs9MuwkASMAmYPMPy6PiFqWvvoAVII3c8

# --- Scam Detection Patterns ---
SUSPICIOUS_KEYWORDS = [
    r"airdrop", r"giveaway", r"claim reward", r"free crypto", r"bonus", r"urgent", r"win", r"limited offer"
]
SHORTENED_DOMAINS = [
    r"bit\.ly", r"tinyurl\.com", r"t\.co", r"goo\.gl", r"ow\.ly", r"shorte\.st", r"cutt\.ly"
]
SUSPICIOUS_DOMAINS = [
    r"\.cn", r"\.tk", r"\.ml", r"\.ga", r"\.cf", r"\.gq"
]

# --- Scam Detection Function ---
def is_scam_message(text: str) -> bool:
    text_lower = text.lower()
    for kw in SUSPICIOUS_KEYWORDS:
        if re.search(kw, text_lower):
            return True
    for domain in SHORTENED_DOMAINS + SUSPICIOUS_DOMAINS:
        if re.search(domain, text_lower):
            return True
    return False

# --- Mock Wallet Activity Function ---
def get_wallet_activities(address: str):
    # Replace this with real API calls to a blockchain explorer
    # For now, return mock data
    return [
        {"type": "Received", "amount": "0.5 ETH", "from": "0xabc...123", "time": "2025-09-08 10:00"},
        {"type": "Sent", "amount": "0.2 ETH", "to": "0xdef...456", "time": "2025-09-07 18:30"},
        {"type": "Received", "amount": "1.0 ETH", "from": "0xghi...789", "time": "2025-09-06 14:15"},
    ]

# --- Handlers ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Welcome to Guardian X!\n"
        "I'm here to help keep your community safe from scams.\n"
        "Type /help to see what I can do."
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🛡️ *Guardian X - Security Bot*\n"
        "Features:\n"
        "1. Scam Detection\n"
        "2. Security Alerts\n"
        "3. Wallet Activity Lookup\n\n"
        "Basic Commands:\n"
        "/start - Welcome message\n"
        "/help - Show this help\n"
        "/about - About Guardian X\n"
        "/security - Get a security tip\n"
        "/wallet <address> - Show recent wallet activities\n"
        "/ping - Check if I'm online\n"
        "/commands - List all commands",
        parse_mode="Markdown"
    )

async def about_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 *Guardian X*\n"
        "A lightweight Telegram bot built with Python to help communities stay safe from scams.\n"
        "Focused on scam detection, security alerts, and wallet activity lookup.",
        parse_mode="Markdown"
    )

async def ping_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🏓 Pong! Guardian X is online.")

async def commands_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Available commands:\n"
        "/start\n"
        "/help\n"
        "/about\n"
        "/security\n"
        "/wallet <address>\n"
        "/ping"
    )

async def scan_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text or ""
    if is_scam_message(text):
        await update.message.reply_text(
            "🚨 *Scam Alert!*\n"
            "This message contains suspicious content. Please be cautious.",
            parse_mode="Markdown"
        )

async def security_alert(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🔒 *Security Tip:*\n"
        "Never click on suspicious links or share your private keys. "
        "Always verify official sources before taking action.",
        parse_mode="Markdown"
    )

async def wallet_activity(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Please provide a wallet address. Example: /wallet 0x1234...")
        return
    address = context.args[0]
    activities = get_wallet_activities(address)
    if not activities:
        await update.message.reply_text("No recent activities found for this wallet.")
        return
    msg = f"🧾 *Recent Activities for {address[:8]}...*:\n"
    for act in activities:
        if act["type"] == "Received":
            msg += f"✅ Received {act['amount']} from `{act['from']}` at {act['time']}\n"
        else:
            msg += f"⬆️ Sent {act['amount']} to `{act['to']}` at {act['time']}\n"
    await update.message.reply_text(msg, parse_mode="Markdown")

# --- Main Bot Setup ---
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("about", about_command))
    app.add_handler(CommandHandler("ping", ping_command))
    app.add_handler(CommandHandler("commands", commands_command))
    app.add_handler(CommandHandler("security", security_alert))
    app.add_handler(CommandHandler("wallet", wallet_activity))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), scan_message))

    print("Guardian X is running...")
    app.run_polling()

if __name__ == "__main__":
    main()