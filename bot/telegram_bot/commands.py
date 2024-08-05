from telegram import Update
from telegram.ext import ContextTypes

# Commands
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    start_text = """
    \tHello! Welcome to Deutsch Wörter Bot!
    
    You can get your daily German word and an example sentence with its translation to your preferred language. (Default 'en')

    Commands:
    /start
    /help
    /configure
    /dailyword
    """
    await update.message.reply_text(start_text)
    
async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Can\'t help right now :/')
    