from __future__ import unicode_literals
import os
import csv
import logging
from urllib.request import urlopen
from os.path import join, expanduser

import youtube_dl
from bs4 import BeautifulSoup
from telegram import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardHide
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram.utils.botan import Botan

from credentials import TOKEN, BOTAN_TOKEN
from start_bot import start_bot


path_to = join(expanduser('~'), 'workspace/musicbot')

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)

u = Updater(TOKEN)
dp = u.dispatcher

botan = False
if BOTAN_TOKEN:
    botan = Botan(BOTAN_TOKEN)


def start(bot, update):
    bot.sendMessage(update.message.chat_id, 
                    text="Hello, please type a song name to start downloading")


def down(bot, update, args):
    if update.message.chat.type == 'group':
        query = ' '.join(args)
        title, url = get_url(query)
        song_down(url, title)
        bot.sendAudio(chat_id=update.message.chat_id, 
                      audio=open(title + '.mp3', 'rb'), 
                      title=title)
        os.remove(title + '.mp3')

    else:
        bot.sendMessage(update.message.chat_id, 
                        text="Only use /down in group")


def music(bot, update):
    username = update.message.chat.username
    title, url = get_url(update.message.text)

    with open(join(path_to, 'database.csv'), 'a') as csvfile:
        new = csv.writer(csvfile, delimiter=' ')
        new.writerow([username, title])

    bot.sendMessage(update.message.chat_id, 
                    text="Request received\nDownloading now...")
    song_down(url, title)
    bot.sendAudio(update.message.chat_id, 
                  audio=open('{}.mp3'.format(title), 'rb'), 
                  title=title)
    os.remove('{}.mp3'.format(title))
    print("Deleted .mp3 file too")


def suggest(bot, update):
    pass


def get_url(query):
    query = query.lower().split()
    query = "+".join(query)
    url = "https://www.youtube.com/results?search_query=" + query
    content = urlopen(url).read()
    soup = BeautifulSoup(content, "lxml")
    tag = soup.find('a', {'rel': 'spf-prefetch'})
    title = tag.text
    video_url = "https://www.youtube.com" + tag.get('href')
    return title, video_url


def song_down(video_url, title):
    ydl_opts = {
        'outtmpl': '{}.%(ext)s'.format(title),
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([video_url])


dp.add_handler(CommandHandler("start", start))
dp.add_handler(CommandHandler("down", down, pass_args=True))
dp.add_handler(CommandHandler("suggest", suggest, pass_args=True))
dp.add_handler(MessageHandler([Filters.text], music))

start_bot(u)
u.idle()
