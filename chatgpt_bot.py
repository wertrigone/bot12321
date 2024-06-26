from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import openai
import sqlite3
import os

# Получаем токен и ключ API из переменных окружения
TELEGRAM_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# Инициализация клиента OpenAI
openai.api_key = OPENAI_API_KEY

# Подключение к SQLite базе данных
conn = sqlite3.connect('chat_history.db', check_same_thread=False)
c = conn.cursor()

# Создание таблицы для истории сообщений, если она не существует
c.execute('''
    CREATE TABLE IF NOT EXISTS chat_history (
        user_id INTEGER,
        message TEXT,
        response TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
''')
conn.commit()

def start(update: Update, context: CallbackContext):
    update.message.reply_text('Привет! Я бот, созданный на базе ChatGPT. Отправь мне что-нибудь, и я отвечу.')

def echo(update: Update, context: CallbackContext):
    user_text = update.message.text  # текст полученный от пользователя
    user_id = update.message.from_user.id

    # Сохраняем сообщение пользователя в базу данных
    c.execute('INSERT INTO chat_history (user_id, message) VALUES (?, ?)', (user_id, user_text))
    conn.commit()

    # Генерация ответа через OpenAI GPT
    gpt_response = openai.Completion.create(
        engine="text-davinci-002",  # Можете выбрать другой движок
        prompt=user_text,
        max_tokens=150
    )
    response_text = gpt_response.choices[0].text.strip()

    # Сохраняем ответ бота в базу данных
    c.execute('UPDATE chat_history SET response = ? WHERE user_id = ? AND message = ?',
              (response_text, user_id, user_text))
    conn.commit()

    # Отправляем ответ пользователю
    update.message.reply_text(response_text)

def main():
    # Инициализация бота
    updater = Updater(TELEGRAM_TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    # Обработчики команд
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    # Начало приема сообщений
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
