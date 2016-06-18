import csv
from os.path import join, expanduser

path = join(expanduser('~'), 'workspace/musicbot')

def save(*args):
    line = [arg for arg in args]
    with open(join(path, 'database.csv'), 'a') as csvfile:
        new = csv.writer(csvfile, delimiter=' ')
        new.writerow(line)


with open(join(path, 'database.csv'), 'r', encoding='utf-8') as csvfile:
    data = csv.reader([line.replace('\0','') for line in csvfile], 
                      delimiter=' ')
    users = len(set([row[0] for row in data]))

with open(join(path, 'database.csv'), 'r', encoding='utf-8') as csvfile:
    data = csv.reader([line.replace('\0','') for line in csvfile], 
                      delimiter=' ')
    recent = '\n'.join([row[4] for row in data][-5:])
