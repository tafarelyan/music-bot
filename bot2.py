#!/usr/bin/env python3

from __future__ import unicode_literals
import os
import logging

import requests
import youtube_dl
from bs4 import BeautifulSoup
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters,
                          ConversationHandler)


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)


def start(bot, update):
    update.message.reply_text("Music Downloader")


def music(bot, update):
    full_title, video_url = search(update.message.text)
    music_dict = download(full_title, video_url)
    update.message.reply_audio(**music_dict)


def search(text, user_data):
    url = 'https://www.youtube.com'
    payload = {'search_query': text}
    r = requests.get(url + '/results', params=payload)
    soup = BeautifulSoup(r.text, 'html.parser')

    results = soup.find('div', {'id': 'results'}).contents[1].ol.contents
    for i, a in enumerate((x.div.div.a for x in results if x != '\n')):
        print(a['href'])
        thumb = a.div.span.img['src']
        print(thumb)

    user_data['title'] = a.string
    user_data['url'] = url + a['href']


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

    u = Updater('344207483:AAGTWKuFIlvXVRGG45gsHsX7ISIiNwWWxHc')
    dp = u.dispatcher

    dp.add_handler(CommandHandler("start", start))
    conv_handler = ConversationHandler(
        entry_points=[MessageHandler(Filters.text, search, pass_user_data=True)],

        states={
        },

        fallbacks=[]
    )
    dp.add_handler(conv_handler)

    u.start_polling()
    u.idle()

if __name__ == '__main__':
    user_data = dict()
    search('shape of you', user_data)
