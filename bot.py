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
from telegram.ext.dispatcher import run_async
from telegram.utils.botan import Botan

from credentials import TOKEN, BOTAN_TOKEN
from start_bot import start_bot


path = join(expanduser('~'), 'workspace/musicbot')

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)

u = Updater(TOKEN)
dp = u.dispatcher

botan = False
if BOTAN_TOKEN:
    botan = Botan(BOTAN_TOKEN)


def user_number():
    with open(join(path, 'database.csv'), 'r', encoding='utf-8') as csvfile:
        data = csv.reader([line.replace('\0','') for line in csvfile], 
                          delimiter=' ')
        userbase = list(set([row[0] for row in data if row[0] != '']))
    return len(userbase)


def start(bot, update):
    chat_id = update.message.chat_id
    bot.sendMessage(chat_id, 
                    text="Hello, please type a song name to start " \
                         "downloading")


def admin(bot, update):
    chat_id = update.message.chat_id
    username = update.message.chat.username
    if username == 'TafarelYan':
        users = user_number()
        bot.sendMessage(chat_id,
                        text='This bot has {} users registered.'.format(users))


@run_async
def music(bot, update):
    username = update.message.chat.username
    chat_id = update.message.chat_id
    text = update.message.text

    query = text.lower().split()
    query = "+".join(query)
    url = "https://www.youtube.com/results?search_query=" + query
    content = urlopen(url).read()
    soup = BeautifulSoup(content, "lxml")
    tag = soup.find('a', {'rel': 'spf-prefetch'})
    title = tag.text
    video_url = "https://www.youtube.com" + tag.get('href')

    with open(join(path, 'database.csv'), 'a') as csvfile:
        new = csv.writer(csvfile, delimiter=' ')
        new.writerow([username, title])

    bot.sendMessage(chat_id, 
                    text="Request received\nDownloading now...")

    ydl_opts = {
        'outtmpl': title + '.%(ext)s',
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([video_url])

    bot.sendAudio(chat_id, 
                  audio=open(title + '.mp3', 'rb'), 
                  title=title)

    os.remove(title+'.mp3')


dp.add_handler(CommandHandler("start", start))
dp.add_handler(CommandHandler("admin", admin))
dp.add_handler(MessageHandler([Filters.text], music))

start_bot(u)
u.idle()
