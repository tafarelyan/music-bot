#!/usr/bin/env python3

from __future__ import unicode_literals
import os
import logging
from uuid import uuid4
from urllib.request import urlopen

import youtube_dl
from bs4 import BeautifulSoup
from telegram import InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, \
    InlineQueryHandler
from telegram.ext.dispatcher import run_async
from pony.orm import db_session, select

from credentials import TOKEN
from database import db

from user import User


DB_NAME = 'db.sqlite'

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)

u = Updater(TOKEN, workers=10)
dp = u.dispatcher

db.bind('sqlite', DB_NAME, create_db=True)
db.generate_mapping(create_tables=True)


def start(bot, update):
    chat_id = update.message.chat_id

    bot.sendMessage(chat_id,
                    text="Hello, please type a song name to start downloading")


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


def search(text):
    query = '+'.join(text.lower().split())
    url = 'https://www.youtube.com/results?search_query=' + query
    content = urlopen(url).read()
    soup = BeautifulSoup(content, 'html.parser')
    tag = soup.find('a', {'rel': 'spf-prefetch'})
    title = tag.text
    video_url = 'https://www.youtube.com' + tag.get('href')
    return title, video_url


def download(title, video_url):
    ydl_opts = {
        'outtmpl': title + '.%(ext)s',
        'format': 'bestaudio/best', 'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([video_url])


dp.add_handler(CommandHandler("start", start))
dp.add_handler(MessageHandler([Filters.text], music))
dp.add_handler(InlineQueryHandler(inline_search))

u.start_polling()
u.idle()
