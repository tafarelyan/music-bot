#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import csv
from urllib.request import urlopen

import youtube_dl
from bs4 import BeautifulSoup


def search(text):
    query = text.lower().split()
    query = '+'.join(query)
    url = 'https://www.youtube.com/results?search_query=' + query
    content = urlopen(url).read()
    soup = BeautifulSoup(content, 'lxml')
    tag = soup.find('a', {'rel': 'spf-prefetch'})
    title = tag.text
    video_url = 'https://www.youtube.com' + tag.get('href')

    return title, video_url


def download(video_url):
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

    os.remove(title + '.mp3')


def save(*args):
    line = [arg for arg in args]
    with open('database.csv', 'a') as csvfile:
        new = csv.writer(csvfile, delimiter=',')
        new.writerow(line)


def user():
    with open('database.csv', 'r') as csvfile:
        data = csv.reader([line.replace('\0','') for line in csvfile], 
                          delimiter=',')
        users = len(set([row[0] for row in data]))
    return users


def recent():
    with open('database.csv', 'r') as csvfile:
        data = csv.reader([line.replace('\0','') for line in csvfile], 
                          delimiter=',')
        recent = '\n'.join([row[4] for row in data][-5:])
    return recent
