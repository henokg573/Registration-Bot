import telebot
API_KEY = '7759515826:AAEjjGhr8pM7WAJBWP8JG1F-wu85nJck338'
bot = telebot.TeleBot(API_KEY)
webhook_info = bot.get_webhook_info()
print(webhook_info)
