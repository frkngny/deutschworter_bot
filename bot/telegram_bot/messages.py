from telegram import Update
from telegram.ext import ContextTypes

from . import BOT_USERNAME

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