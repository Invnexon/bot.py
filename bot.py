import os
import yt_dlp
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes

TOKEN = os.environ.get("8643380281:AAGayVXrlD40NSVLcG4qPkweCUpL50F62AQ")
# Agar aapka channel Public hai toh username use karein (Example: "@yourchannel")
# Agar aapka channel Private hai, toh code mein channel ID use karni padti hai.
CHANNEL_LINK = "https://t.me/+V8X-WAWXHn45Y2Y1" 

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📢 Join Channel", url=CHANNEL_LINK)],
        [InlineKeyboardButton("✅ Verify", callback_data="verify_join")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Welcome Please Join Channel To Continue Using Bot:", reply_markup=reply_markup)

async def verify_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer("Checking... please wait!", show_alert=False)
    # Note: Private invite link se check karne ke liye bot ka us channel/group mein hona aur admin hona zaruri hai
    await query.edit_message_text("✅ Verified! Send Link Here.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text
    if "instagram.com" in url:
        status = await update.message.reply_text("⏳ Downloading...")
        try:
            ydl_opts = {'format': 'best'}
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                video_url = info['url']
            await update.message.reply_video(video=video_url)
            await status.delete()
        except Exception as e:
            await update.message.reply_text(f"❌ Error: {e}")
    else:
        await update.message.reply_text("⚠️ Please send a valid Instagram link.")

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(verify_button, pattern="verify_join"))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    app.run_polling()
