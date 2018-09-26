#!/usr/bin/env python3

import requests
import lxml.etree
from pprint import pprint

import json

with open('wanted_persons.json', 'r', encoding='utf-8') as fh:
    data = json.loads(fh.read())

#resp = requests.get('')
#pprint(resp.json())

QUERY = 'http://jsru.kb.nl/sru/sru?query=%s&x-collection=DDD_artikel&startRecord=%s'


q = 'type="artikel" AND '
for item in data:
    q += '"' + item + '"' + " OR "


wanted = []

s = 0
while len(wanted) < 1000:
    resp = requests.get(QUERY % (q[:-4], s))
    records = lxml.etree.fromstring(resp.content)

    for item in records.iter():
        if item.tag.endswith('identifier'):
            wanted.append(item.text)
    s+=len(wanted)

print(wanted, len(wanted))


articles = {}

all_txt = ""

avg = []

for article in wanted:
    try:
        data = lxml.etree.fromstring(requests.get(article).content)
        txt = u""
        fname = 'out/' + article.replace('http://resolver.kb.nl/resolve?urn=','')
        with open(fname, 'w', encoding='utf-8') as fh:
            for i in data.iter():
                if i.text.strip():
                    txt += i.text.strip() + " "

                    all_txt += " " + i.text.strip()
                    if not article in articles:
                        articles[article] = i.text
                    else:
                        articles[article] += " " + i.text
            #print(len(txt.strip()))
            #avg.append(len(txt.strip()))
            if len(txt.strip()) > 1270:
                fh.write(txt.strip())
        if len(txt.strip()) < 1270:
            os.unlink(fname)
    except:
        pass

print('AVG', sum(avg) / len(avg))
#seen = {}
#for word in all_txt.split(' '):
#    if len(word) > 4:
#        if not word in seen:
#            seen[word] = 0
#        else:
#            seen[word] += 1
#
#for word in seen:
#    if seen[word] > 10:
#        print(word)
