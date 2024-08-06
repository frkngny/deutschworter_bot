from telegram import Update
from telegram.ext import ContextTypes

import requests

# Commands
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    start_text = """
    \tHello! Welcome to Deutsch Wörter Bot!
    
    You can get your daily German word and an example sentence with its translation to your preferred language. (Default 'en')

    Commands:
    /start - This is the starting point.
    /help
    /dailyword - Get a words which you did not get previously.
    /reset_previous_words - You may get previous words after resetting.
    """
    
    if update.effective_user.username:
        params = {'username': update.effective_user.username}
        requests.post('http://127.0.0.1:5000/api/user', data=params)
    else:
        await update.message.reply_text('You don\'t have your username set. Please go to settings and set your username.')
    
    await update.message.reply_text(start_text)
   
    
async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Can\'t help right now :/')

async def daily_word(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.username:
        params = {'username': update.effective_user.username}
        resp = requests.get('http://127.0.0.1:5000/api/get_word', data=params)
        
        if resp.status_code < 400:
            word = resp.json()
            
            # set info per word type
            info = ""
            if word['Type'] == 'Verb':
                info = "<i>Verbs are inflected according to pronouns. (e.g.: haben -> Ich habe, du hast, ..)</i>"
            if word['Type'] == 'Noun':
                info = "<i>The artikel (der, die, das) may depend on the preposition.</i>"
                
            reply_text = f"""Here is your daily word:
            + <b>{word['Word']}</b>
            - {word['Sentence'].replace(word['Word'], "<u>"+word['Word']+"</u>")}
            
            + {word['Translation']}
            - {word['SentenceTranslation']}
            
            {word['Word']} is a/an {word['Type']}
            {info}
            """
        else:
            reply_text = "Sorry! I'm having issues right now :("
        await update.message.reply_html(reply_text)
    else:
        await update.message.reply_text('You don\'t have your username set. Please go to settings and set your username.')


async def reset_words(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.username:
        params = {'username': update.effective_user.username}
        resp = requests.post('http://127.0.0.1:5000/api/reset_words', data=params)
        if resp.status_code < 400:
            await update.message.reply_text('All seen words storage is removed. You can now get previous words.')
        else:
            await update.message.reply_text(resp.json()['error'])
    else:
        await update.message.reply_text('You don\'t have your username set. Please go to settings and set your username.')