#!/usr/bin/env python3

from __future__ import unicode_literals
import os
import logging
from urllib.request import urlopen

import youtube_dl
from bs4 import BeautifulSoup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)

u = Updater('YOUR-TOKEN')
dp = u.dispatcher

if not os.path.exists('music'):
    os.makedirs('music')


def start(bot, update):
    update.message.reply_text("Music Downloader")


def music(bot, update):
    title, video_url = search(update.message.text)
    music_dict = download(title, video_url)
    update.message.reply_audio(**music_dict)


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
        'outtmpl': 'music/{}.%(ext)s'.format(title),
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([video_url])

    return {
        'audio': open('music/{}.mp3'.format(title), 'rb'),
        'title': title,
    }


dp.add_handler(CommandHandler("start", start))
dp.add_handler(MessageHandler(Filters.text, music))

u.start_polling()
u.idle()
