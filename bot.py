import os
import asyncio
from telegram import Update
from telegram.ext import Application, MessageHandler, CommandHandler, filters, ContextTypes
from yt_dlp import YoutubeDL

TOKEN = os.getenv("8469554752:AAF1PoFLddzsgDHpB6LvvuiuidmpZULE1BE")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Send me any YouTube link, I will upload the video.")

async def handle_url(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text.strip()
    await update.message.reply_text("Downloading...")

    ydl_opts = {"outtmpl": "video.%(ext)s"}
    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info)

    await update.message.reply_video(video=open(filename, "rb"))
    os.remove(filename)

async def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_url))
    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())

