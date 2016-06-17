import csv
from os.path import join, expanduser

path = join(expanduser('~'), 'workspace/musicbot')

def save(*args):
    with open(join(path, 'database.csv'), 'a') as csvfile:
        new = 
    line = [arg for arg in args]
    print(line)


def user_number():
    with open(join(path, 'database.csv'), 'r', encoding='utf-8') as csvfile:
        data = csv.reader([line.replace('\0','') for line in csvfile], 
                          delimiter=' ')
        userbase = list(set([row[0] for row in data if row[0] != '']))
    return len(userbase)


def lasts_songs():
    with open(join(path, 'database.csv'), 'r', encoding='utf-8') as csvfile:
        data = csv.reader([line.replace('\0','') for line in csvfile], 
                          delimiter=' ')
        lasts_songs = '\n'.join([row[1] for row in data][-5:])
    return lasts_songs
