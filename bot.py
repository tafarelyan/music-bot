from __future__ import unicode_literals
import os
import logging
from urllib.request import urlopen

import youtube_dl
from bs4 import BeautifulSoup
from telegram import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardHide
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram.ext.dispatcher import run_async
from telegram.utils.botan import Botan

from credentials import TOKEN, BOTAN_TOKEN
from start_bot import start_bot
from admin import save, recent, users


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)

u = Updater(TOKEN)
dp = u.dispatcher

botan = False
if BOTAN_TOKEN:
    botan = Botan(BOTAN_TOKEN)


def start(bot, update):
    chat_id = update.message.chat_id
    bot.sendMessage(chat_id, 
                    text="Hello, please type a song name to start " \
                         "downloading")


def admin(bot, update):
    chat_id = update.message.chat_id
    username = update.message.chat.username
    if username == 'TafarelYan':
        bot.sendMessage(chat_id,
                        text='{} users registered.\n\n{}'.format(users, recent))


@run_async
def music(bot, update):
    user_id = update.message.from_user.id
    username = update.message.chat.username
    first_name = update.message.from_user.first_name
    last_name = update.message.from_user.last_name
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

    save(user_id, username, first_name, last_name, title, video_url)

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
