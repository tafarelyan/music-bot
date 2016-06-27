#!//usr/bin/env python3
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import logging

from telegram import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardHide
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram.ext.dispatcher import run_async

from credentials import TOKEN
from start_bot import start_bot
from custom import search, download, save, user, recent


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)

u = Updater(TOKEN)
dp = u.dispatcher


def start(bot, update):
    chat_id = update.message.chat_id
    bot.sendMessage(chat_id, 
                    text="Hello, please type a song name to start " \
                         "downloading")


def admin(bot, update):
    chat_id = update.message.chat_id
    username = update.message.chat.username

    usernumbers = user()
    last_songs = recent()
    if username == 'TafarelYan':
        bot.sendMessage(chat_id,
                        text='{} users registered.\n\n{}'.format(usernumber, last_songs))


@run_async
def music(bot, update):
    user_id = update.message.from_user.id
    username = update.message.chat.username
    first_name = update.message.from_user.first_name
    last_name = update.message.from_user.last_name
    chat_id = update.message.chat_id
    text = update.message.text

    title, video_url = search(text)
    save(user_id, username, first_name, last_name, title, video_url)
    bot.sendMessage(chat_id, 
                    text="Request received\nDownloading now...")

    download(video_url)
    bot.sendAudio(chat_id, 
                  audio=open(title + '.mp3', 'rb'), 
                  title=title)


dp.add_handler(CommandHandler("start", start))
dp.add_handler(CommandHandler("admin", admin))
dp.add_handler(MessageHandler([Filters.text], music))

start_bot(u)
u.idle()
