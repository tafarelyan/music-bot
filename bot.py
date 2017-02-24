#!/usr/bin/env python3

from __future__ import unicode_literals
import os
import logging

import requests
import youtube_dl
from bs4 import BeautifulSoup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)


def start(bot, update):
    update.message.reply_text("Music Downloader")


def music(bot, update):
    full_title, video_url = search(update.message.text)
    music_dict = download(full_title, video_url)
    update.message.reply_audio(**music_dict)


def search(text):
    url = 'https://www.youtube.com/results'
    r = requests.get(url, params={'search_query': text})
    soup = BeautifulSoup(r.content, 'html.parser')
    tag = soup.find('a', {'rel': 'spf-prefetch'})
    full_title = tag.text
    video_url = 'https://www.youtube.com' + tag.get('href')
    return full_title, video_url


def download(full_title, video_url):
    try:
        author, title = full_title.split('-')
        title = title.strip()
        author = author.strip()
    except:
        title = full_title

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

    music_dict = {
        'audio': open('music/{}.mp3'.format(title), 'rb'),
        'title': title,
    }

    try:
        music_dict['performer'] = author
    except:
        pass

    return music_dict


def main():
    if not os.path.exists('music'):
        os.makedirs('music')

    u = Updater('YOUR-TOKEN')
    dp = u.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text, music))

    u.start_polling()
    u.idle()

if __name__ == '__main__':
    main()
