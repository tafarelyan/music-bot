#!/usr/bin/env python3

from __future__ import unicode_literals
import os
import logging

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram.ext.dispatcher import run_async
from pony.orm import db_session, select

from credentials import TOKEN
from custom import search, download
from database import db

from user import User


DB_NAME = 'bot.sqlite'

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)

u = Updater(TOKEN)
dp = u.dispatcher

db.bind('sqlite', DB_NAME, create_db=True)
db.generate_mapping(create_tables=True)



def start(bot, update):
    chat_id = update.message.chat_id

    bot.sendMessage(chat_id, 
                    text="Hello, please type a song name to start " \
                         "downloading")


def admin(bot, update):
    chat_id = update.message.chat_id
    username = update.message.chat.username

    with db_session:
        users = len(select(p.user_id for p in User)[:])
        last5 = '\n'.join(select(p.title for p in User)[:][-5:])

    if username == 'TafarelYan':
        bot.sendMessage(chat_id,
                        text="{} users registered.\n\n{}".format(users, last5))


@run_async
def music(bot, update):
    user_id = update.message.from_user.id
    username = update.message.chat.username
    first_name = update.message.from_user.first_name
    last_name = update.message.from_user.last_name

    chat_id = update.message.chat_id
    text = update.message.text

    title, video_url = search(text)
    with db_session:
        User(user_id=user_id,
             username=username,
             first_name=first_name,
             last_name=last_name,
             title=title,
             video_url=video_url)

    bot.sendMessage(chat_id, 
                    text="Request received\nDownloading now...")

    download(title, video_url)
    bot.sendAudio(chat_id, 
                  audio=open(title + '.mp3', 'rb'), 
                  title=title)
    os.remove(title + '.mp3')


dp.add_handler(CommandHandler("start", start))
dp.add_handler(CommandHandler("admin", admin))
dp.add_handler(MessageHandler([Filters.text], music))

u.start_polling()
u.idle()
