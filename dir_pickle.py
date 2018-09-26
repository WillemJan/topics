#!/usr/bin/env python3

import pickle
import operator
import os
from pprint import pprint

c_list = []

for f in os.listdir('.'):
    if not f.endswith('.pkl'):
        continue

    with open(f, 'rb') as fh:
        data = pickle.load(fh, encoding='utf-8')
        data = sorted(data.items(), key=operator.itemgetter(1), reverse=True)

        for i,k in  enumerate(data):
            c_list.append(k)
            if i > 25:
                break


w = set()

for item in c_list:
    if len(item[0].split()) > 1:
        print(item[0])
