from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)

# ===== CONFIG =====
TOKEN = "telegram bot token"
ADMINS = [admin]  
PAID_CHANNEL_LINK = "channel link"
UPI_ID = "abhinavyaduvanshi100-1@oksbi"

# ===== START =====
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🔥 *Instagram Growth Premium*\n\n"
        "Daily milega:\n"
        "• Viral reel ideas\n"
        "• Trending audios\n"
        "• Hashtags\n"
        "• Best posting time\n\n"
        "💰 Price:\n"
        "₹199 → 7 Days\n"
        "₹399 → 30 Days\n\n"
        "👉 /buy likho to continue",
        parse_mode="Markdown"
    )

# ===== BUY =====
async def buy(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        f"💳 *Payment Details*\n\n"
        f"UPI ID: `{UPI_ID}`\n\n"
        "Payment ke baad *screenshot bhejo*.\n"
        "Admin verify karega aur channel access milega ✅",
        parse_mode="Markdown"
    )

# ===== PAYMENT PROOF =====
async def proof(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message.photo:
        await update.message.reply_text("❌ Screenshot bhejo payment ka")
        return

    for admin in ADMINS:
        await context.bot.send_photo(
            chat_id=admin,
            photo=update.message.photo[-1].file_id,
            caption=f"🧾 Payment proof from @{update.effective_user.username}\n\nApprove: /approve {update.effective_user.id}"
        )

    await update.message.reply_text("✅ Proof received. Verification pending.")

# ===== APPROVE (ADMIN) =====
async def approve(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id not in ADMINS:
        await update.message.reply_text("❌ Admin only")
        return

    if not context.args:
        await update.message.reply_text("Use: /approve user_id")
        return

    user_id = int(context.args[0])

    await context.bot.send_message(
        chat_id=user_id,
        text=f"🎉 Payment Approved!\n\nJoin Premium Channel:\n{PAID_CHANNEL_LINK}"
    )

    await update.message.reply_text("✅ User approved & link sent")

# ===== MAIN =====
def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("buy", buy))
    app.add_handler(CommandHandler("approve", approve))
    app.add_handler(MessageHandler(filters.PHOTO, proof))

    print("🔥 Paid Bot Running...")
    app.run_polling()

if __name__ == "__main__":
    main()

