from urllib.request import urlopen

import youtube_dl
from bs4 import BeautifulSoup


def search(text):
    query = '+'.join(text.lower().split())
    url = 'https://www.youtube.com/results?search_query=' + query
    content = urlopen(url).read()
    soup = BeautifulSoup(content, 'lxml')
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
