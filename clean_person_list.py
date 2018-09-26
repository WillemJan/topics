#!/usr/bin/env python3

from pprint import pprint

import requests
import Levenshtein
import json

person_list = []
with open('persons_of_intrest.txt', 'r') as fh:
    for line in fh.read().split('\n'):
        if line.strip():
            person_list.append(line)
wanted = []

for person in person_list:
    data = requests.get('http://linksolr1.kbresearch.nl/dbpedia/select/?q=label:"%s"&wt=json&rows=1&fl=pref_label_str' % person)
    r = False
    try:
        r = data.json().get('response').get('docs')
        #print(len(r))
        low = 0


        res = []
        for d in r:
            ld = Levenshtein.distance(d.get('pref_label_str'), person)
            res.append([ld, d.get('pref_label_str')])

    except:
        r = False
    if res and res[0][0] < 4:
        wanted.append(person)

with open('wanted_persons.json', 'w', encoding='utf-8') as fh:
    fh.write(json.dumps(wanted))
