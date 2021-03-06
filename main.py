from telegram_token import token
from config import reply_texts
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Updater, MessageHandler, Filters, CommandHandler, CallbackQueryHandler, ConversationHandler
import logging
import re
import requests

REQUEST_KWARGS = {
    'proxy_url': 'socks4://85.75.198.12:4145',
    # Optional, if you need authentication:
    # 'username': 'PROXY_USER',
    # 'password': 'PROXY_PASS',
}

# Stages
FIRST = 0
# Callback data
ONE, TWO, THREE, FOUR = range(4)

def start(bot, update):
    keyboard = [
        [InlineKeyboardButton("Обучение", callback_data=str(ONE)),
         InlineKeyboardButton("Адаптация", callback_data=str(TWO)),
         InlineKeyboardButton("О нас", callback_data=str(FOUR))]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text(reply_texts['start_message'])
    update.message.reply_text(reply_texts['start_message_2'], reply_markup=reply_markup)

    return FIRST

def learn(bot, update):
    query = update.callback_query
    query.answer()
    keyboard = [
        [InlineKeyboardButton("В начало", callback_data=str(THREE)),
         InlineKeyboardButton("Адаптация", callback_data=str(TWO)),
         InlineKeyboardButton("О нас", callback_data=str(FOUR))]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.message.reply_text(reply_texts['learn_message_1'])
    query.message.reply_text(reply_texts['learn_message_2'], reply_markup=reply_markup)
    #query.edit_message_text(
    #    text=reply_texts['learn_message_1'],
    #    reply_markup=reply_markup
    #)
    return FIRST

def adaptation(bot, update):
    query = update.callback_query
    query.answer()
    keyboard = [
        [InlineKeyboardButton("В начало", callback_data=str(THREE)),
         InlineKeyboardButton("Обучение", callback_data=str(ONE)),
         InlineKeyboardButton("О нас", callback_data=str(FOUR))]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.message.reply_text(reply_texts['adaptation_message_1'])
    query.message.reply_text(reply_texts['adaptation_message_2'], reply_markup=reply_markup)
    #query.edit_message_text(
    #    text=reply_texts['adaptation_message_1'],
    #    reply_markup=reply_markup
    #)
    return FIRST

def about(bot, update):
    query = update.callback_query
    query.answer()
    keyboard = [
        [InlineKeyboardButton("В начало", callback_data=str(THREE)),
         InlineKeyboardButton("Обучение", callback_data=str(ONE)),
         InlineKeyboardButton("Адаптация", callback_data=str(TWO))]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.message.reply_text(reply_texts['about_message_1'])
    query.message.reply_text(reply_texts['about_message_2'], reply_markup=reply_markup)
    #query.edit_message_text(
    #    text=reply_texts['a_message_1'],
    #    reply_markup=reply_markup
    #)
    return FIRST

def start_again(bot, update):
    query = update.callback_query
    query.answer()
    keyboard = [
        [InlineKeyboardButton("Обучение", callback_data=str(ONE)),
         InlineKeyboardButton("Адаптация", callback_data=str(TWO)),
         InlineKeyboardButton("О нас", callback_data=str(FOUR))]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.message.reply_text(reply_texts['start_again_message_1'])
    query.message.reply_text(reply_texts['start_again_message_2'], reply_markup=reply_markup)
    #query.edit_message_text(
    #    text=reply_texts['start_again_message'],
    #    reply_markup=reply_markup
    #)
    return FIRST

def main():
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO)
    # используем прокси, так как без него у меня ничего не работало(
    updater = Updater(token=token, request_kwargs=REQUEST_KWARGS)

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start),
                      CommandHandler('learn', learn),
                      CommandHandler('adaptation', adaptation),
                      CommandHandler('start_again', start_again),
                      CommandHandler('about', about)],
        states={
            FIRST: [CallbackQueryHandler(learn, pattern='^' + str(ONE) + '$'),
                    CallbackQueryHandler(adaptation, pattern='^' + str(TWO) + '$'),
                    CallbackQueryHandler(start_again, pattern='^' + str(THREE) + '$'),
                    CallbackQueryHandler(about, pattern='^' + str(FOUR) + '$')]
        },
        fallbacks=[CommandHandler('start', start)]
    )
    updater.dispatcher.add_handler(conv_handler)
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
