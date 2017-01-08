#!/usr/bin/env python3

from __future__ import unicode_literals
import os
import logging
from urllib.request import urlopen

import youtube_dl
from bs4 import BeautifulSoup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from sqlalchemy.orm import Session

from credentials import ENGINE, TOKEN
from database import Backup


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)

u = Updater(TOKEN)
dp = u.dispatcher


def start(bot, update):
    bot.sendMessage(update.message.chat_id, text="Music Downloader")


def music(bot, update):
    title, video_url = search(update.message.text)
    session = Session(bind=ENGINE)
    session.add(Backup(title=title, video_url=video_url))
    session.commit()
    session.close()
    download(title, video_url)
    bot.sendAudio(update.message.chat_id,
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

u.start_polling()
u.idle()
