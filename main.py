#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This program is dedicated to the public domain under the CC0 license.
#
# THIS EXAMPLE HAS BEEN UPDATED TO WORK WITH THE BETA VERSION 12 OF PYTHON-TELEGRAM-BOT.
# If you're still using version 11.1.0, please see the examples at
# https://github.com/python-telegram-bot/python-telegram-bot/tree/v11.1.0/examples

"""
First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.
Usage:
Basic inline bot example. Applies different text transformations.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""
import os
import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Filters, Updater, MessageHandler, CommandHandler, CallbackQueryHandler
from random import shuffle

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text("Hello, I am the GateKeeper.")


def help(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Available commands:\n\n/id')


def id(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text(update.effective_chat.id)


def hodor(update, context):
    try:
        for new_member in update.message.new_chat_members:
            callback_id = str(new_member.id)
            context.bot.restrict_chat_member(
                int(os.environ['CHAT_ID']),
                new_member.id,
                can_send_messages=False,
                can_send_media_messages=False,
                can_send_other_messages=False,
                can_add_web_page_previews=False
            )

            keyboard_items = [
                InlineKeyboardButton("🥩", callback_data=callback_id + ',steak'),
                InlineKeyboardButton("🥝", callback_data=callback_id + ',kiwi'),
                InlineKeyboardButton("🥛", callback_data=callback_id + ',milk'),
                InlineKeyboardButton("🥓", callback_data=callback_id + ',bacon'),
                InlineKeyboardButton("🥥", callback_data=callback_id + ',coconut'),
                InlineKeyboardButton("🍩", callback_data=callback_id + ',donut'),
                InlineKeyboardButton("🌮", callback_data=callback_id + ',taco'),
                InlineKeyboardButton("🍺", callback_data=callback_id + ',beer'),
                InlineKeyboardButton("🥗", callback_data=callback_id + ',salad'),
                InlineKeyboardButton("🍌", callback_data=callback_id + ',banana'),
                InlineKeyboardButton("🌰", callback_data=callback_id + ',chestnut'),
                InlineKeyboardButton("🍵", callback_data=callback_id + ',tea'),
                InlineKeyboardButton("🥑", callback_data=callback_id + ',avocado'),
                InlineKeyboardButton("🍗", callback_data=callback_id + ',chicken'),
                InlineKeyboardButton("🥪", callback_data=callback_id + ',sandwich'),
                InlineKeyboardButton("🥒", callback_data=callback_id + ',cucumber')
            ]

            shuffle(keyboard_items)
            keyboard = []

            counter = 0
            for i in range(4):  # create a list with nested lists
                keyboard.append([])
                for n in range(4):
                    keyboard_item = keyboard_items[counter]
                    keyboard[i].append(keyboard_item)  # fills nested lists with data
                    counter += 1

            reply_markup = InlineKeyboardMarkup(keyboard)

            update.message.reply_text(
                'Hello, ' +
                new_member.first_name +
                ' and welcome to the group. Just a small formality before we start. Please prove that you are not a robot by grabbing a drink of your choice below.',
                reply_markup=reply_markup
            )
    except AttributeError:
        pass


def button(update, context):
    query = update.callback_query
    person_who_pushed_the_button = int(query.data.split(",")[0])

    if query.from_user.id == person_who_pushed_the_button:
        if 'milk' in query.data or 'beer' in query.data or 'tea' in query.data:
            query.edit_message_text(text="Cheers!")
            context.bot.restrict_chat_member(
                int(os.environ['CHAT_ID']),
                person_who_pushed_the_button,
                can_send_messages=True,
                can_send_media_messages=True,
                can_send_other_messages=True,
                can_add_web_page_previews=True
            )
        else:
            query.edit_message_text(text="So you are a robot after all? Shoo!")


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(str(os.environ['TOKEN']), use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("id", id))

    dp.add_handler(MessageHandler(Filters.chat(int(os.environ['CHAT_ID'])), hodor))

    updater.dispatcher.add_handler(CallbackQueryHandler(button))

    # on noncommand i.e message - echo the message on Telegram

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Block until the user presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
