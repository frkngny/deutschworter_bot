import os
import dotenv

from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, ApplicationBuilder

dotenv.load_dotenv()

TOKEN = os.getenv("TOKEN")
BOT_USERNAME = os.getenv("USERNAME")


### Handler methods

# Commands
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Hello! Thanks for chatting with me.')
    
async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Can\'t help right now :/')
    
    
# Responses from user
def handle_response(response_text: str) -> str:
    processed: str = response_text.lower()
    
    if 'hello' in processed:
        return 'Hey there!'
    
    if 'how are you' in processed:
        return 'I am good.'
    
    return 'Please try again.'

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_type: str = update.message.chat.type
    text: str = update.message.text
    user: str = update.effective_user.full_name
    
    print(f'User {user} in {chat_type}')
    
    if chat_type == 'group':
        if BOT_USERNAME in text:
            text = text.replace(BOT_USERNAME, '').strip()
            response: str = handle_response(text)
        else:
            return
    else:
        response: str = handle_response(text)
    await update.message.reply_text(response)

# Error
async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused error {context.error}')


### BUILD

app = ApplicationBuilder().token(TOKEN).build()

# Commands
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("help", help))

# Messages
app.add_handler(MessageHandler(filters.TEXT, handle_message))

# Errors
app.add_error_handler(error_handler)
