from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# Apne channel ka username ya ID yahan dalein
CHANNEL_USERNAME = "@Nexonbio" 

async def check_subscription(user_id, context):
    try:
        member = await context.bot.get_chat_member(CHANNEL_USERNAME, user_id)
        return member.status in ['member', 'administrator', 'creator']
    except:
        return False

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    
    # Check if user joined channel
    if not await check_subscription(user.id, context):
        keyboard = [[InlineKeyboardButton("Join Channel", url=f"https://t.me/{CHANNEL_USERNAME.replace('@', '')}")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(
            f"Namaste {user.first_name}! 🙏\n\nIs bot ko use karne ke liye pehle hamara channel join karein:",
            reply_markup=reply_markup
        )
    else:
        await update.message.reply_text(f"Welcome {user.first_name}! Main ek Instagram Reels Downloader hoon. Link bhejein!")

# Reels logic yahan pehle ki tarah rahega
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await check_subscription(update.effective_user.id, context):
        await update.message.reply_text("❌ Pehle channel join karein!")
        return
    
    # Yahan apna Reels downloader ka code call karein
    await update.message.reply_text("Downloading start ho rahi hai...")

if __name__ == '__main__':
    app = ApplicationBuilder().token("8643380281:AAGayVXrlD40NSVLcG4qPkweCUpL50F62AQ").build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    app.run_polling()