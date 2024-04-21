from telegram import Update, Bot
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import openai

# Токен, который вы получили от BotFather
TELEGRAM_TOKEN = '7113631749:AAGHS58e3uGMUw6KXlkLkzEAVVeRl7fVYdQ'
# Ключ API OpenAI
OPENAI_API_KEY = 'sk-proj-B1m9C6AfnYjNl7D2u7zmT3BlbkFJ98fudud8ZiVAAbFu2fFa'

# Инициализация клиента OpenAI
openai.api_key = OPENAI_API_KEY

def start(update: Update, context: CallbackContext):
    update.message.reply_text('Привет! Я бот, созданный на базе ChatGPT. Отправь мне что-нибудь, и я отвечу.')

def echo(update: Update, context: CallbackContext):
    user_text = update.message.text  # текст полученный от пользователя
    # Генерация ответа через OpenAI GPT
    gpt_response = openai.Completion.create(
        engine="text-davinci-002",  # Можете выбрать другой движок
        prompt=user_text,
        max_tokens=150
    )
    # Отправляем ответ пользователю
    update.message.reply_text(gpt_response.choices[0].text.strip())

def main():
    # Инициализация бота
    updater = Updater(TELEGRAM_TOKEN)
    dispatcher = updater.dispatcher

    # Обработчики команд
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    # Начало приема сообщений
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
