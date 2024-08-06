import os
import dotenv

from telegram import Update
from telegram.ext import CommandHandler, MessageHandler, filters, ContextTypes, ApplicationBuilder

dotenv.load_dotenv()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

ENV_NAME = '.env'
env_path = os.path.join(os.path.dirname(BASE_DIR), ENV_NAME)

TOKEN = dotenv.get_key(env_path, "TOKEN")
BOT_USERNAME = dotenv.get_key(env_path, "USERNAME")


def create_bot():
    app = ApplicationBuilder().token(TOKEN).build()

    from . import commands, messages, errors
    
    # Commands
    app.add_handler(CommandHandler("start", commands.start))
    app.add_handler(CommandHandler("help", commands.help))
    app.add_handler(CommandHandler("dailyword", commands.daily_word))
    app.add_handler(CommandHandler("reset_previous_words", commands.reset_words))

    # Messages
    app.add_handler(MessageHandler(filters.TEXT, messages.handle_message))

    # Errors
    app.add_error_handler(errors.error_handler)
    
    return app