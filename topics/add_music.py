#!/usr/bin/env python3
import csv, os

new_lines = ""

seen = []


with open('news_topics_sru.csv', 'r') as fh:
    for line in fh.read().strip().split('\n'):
        if line.startswith('url'):
            new_lines += line + '\n'
            continue

        url = line.split(',')[0]
        line = line.replace(url + ",", '')

        if line.startswith('"'):
            line = line[1:]
            class_str = line.split('"')[0]
        else:
            class_str = line.split(',')[0].replace(',', '')

        line = line.replace(class_str, '')
        if line.startswith('",'):
            line = line[2:]

        if line.startswith(','):
            new_lines += '0' + line + '\n'
        else:
            new_lines += '0,' + line + '\n'

for fname in os.listdir('manual'):
    new_lines += '1,0,0,0,0,0,0,0,0,0,0,0,0,0,"'
    with open('manual/' + fname, 'r') as fh:
        new_lines += fh.read().replace('"', ' ') + '"\n'

with open('news_topics_music.csv', 'w') as fh:
    fh.write(new_lines)
