from telegram_bot import create_bot

if __name__ == "__main__":
    bot = create_bot()
    bot.run_polling(poll_interval=5)