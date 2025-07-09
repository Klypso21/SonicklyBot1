import os
from flask import Flask
from keep_alive import keep_alive
from telegram import Bot, Update
from telegram.ext import CommandHandler, Updater, CallbackContext

BOT_TOKEN = os.getenv("BOT_TOKEN")
OWNER_ID = int(os.getenv("OWNER_ID"))

app = Flask(__name__)
keep_alive()

def start(update: Update, context: CallbackContext):
    if update.effective_user.id != OWNER_ID:
        return
    context.bot.send_message(chat_id=update.effective_chat.id, text="🎧 Welcome to SonicklyBot!")

def session(update: Update, context: CallbackContext):
    if update.effective_user.id != OWNER_ID:
        return
    with open("session.flac", "rb") as audio:
        context.bot.send_audio(chat_id=update.effective_chat.id, audio=audio, caption="🎶 Your session is here.")

def main():
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("session", session))
    updater.start_polling()
    print("✅ Klipso Bot is running and listening...")

if __name__ == "__main__":
    main()
