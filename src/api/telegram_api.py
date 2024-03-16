import telebot
from genta import GentaAPI

def run_telegram_bot(telegram_token:str, prompt:str, genta_token:str, model_name:str):
    """_summary_

    Args:
        telegram_token (str): token from telegram, got from https://t.me/BotFather 
        prompt (str): prompt engineering to user
        genta_token (str): token from genta API
        model_name (str): name of model
    """
    # Replace with your actual token 
    GENTA_API = GentaAPI(token=genta_token)
    bot = telebot.TeleBot(telegram_token)
    chats = [{"role": "system", "content":prompt}]
    @bot.message_handler(commands=['start']) # Start the message
    def send_welcome(message):
        bot.reply_to(message, "Hi there, I am a simple Telegram bot. How can I help you?")
        chats.append({"role": "user", "content": "Hi there, I am a simple Telegram bot. How can I help you?"})

    @bot.message_handler(commands=['help']) # give help to the user
    def send_help(message):
        bot.reply_to(message,
    """Hi, this is a telegram bot integrated with Genta API.

    You can control me by sending these commands:

    /start - restart your chats from the beginning
    /clear - clear all chats
    """)
        
    @bot.message_handler(commands=['clear']) # Clear all of chat
    def send_help(message):
        chats = []
        bot.reply_to(message, "chat cleared, you could restart your messages")

    @bot.message_handler(func=lambda message: True)  # Respond to all other messages
    def echo_all(message):
        user_response = {"role": "user", "content": message.text}
        chats.append(user_response)
        response = GENTA_API.ChatCompletion(chats,model_name=model_name)
        response_txt = response[0][0][0]['generated_text']
        chat = {"role": "assistant", "content": response_txt}
        chats.append(chat)
        bot.reply_to(message, response_txt)

    bot.infinity_polling()