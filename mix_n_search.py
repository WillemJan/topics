#!/usr/bin/env python3


# JSON_solr_delpher
# JSON_solr_research

import requests
from lxml import etree
import json
from pprint import pprint


SRU_QUERY_p = 'http://jsru.kb.nl/sru/sru?query='
SRU_QUERY_p += '"%s"'
SRU_QUERY_p += '&x-collection=DDD_artikel'
SRU_QUERY_p += '&startRecord=%s'

SRU_QUERY_r = 'http://jsru.kb.nl/sru/sru?query='
SRU_QUERY_r += '"%s"'
SRU_QUERY_r += '&x-collection=DDD_artikel_research'
SRU_QUERY_r += '&startRecord=%s'

with open('mix_n_match_no_null.json', 'r') as fh:
    data = json.loads(fh.read())


records_associated = {}
records_associated['by_string'] = {}
records_associated['by_id'] = {}

for line in data:
    name = line.get('name')
    sru = SRU_QUERY_p % (name, "0")
    data = requests.get(sru)
    data = etree.fromstring(data.content)

    if not name in records_associated['by_string']:
        records_associated['by_string'][name] = set()

    total_nr_of_records = 0

    for l in data.iter():
        if l.tag.endswith('numberOfRecords'):
            total_nr_of_records = int(l.text)
        if l.tag.endswith('identifier'):
            val = l.text.split('=')[1]
            records_associated['by_string'][name].add(val)


   
    if records_associated['by_string'][name]:
        one_loop = len(records_associated['by_string'][name])
    else:
        one_loop = 0
   
    if one_loop < total_nr_of_records:
        #for i in range(0, int(total_nr_of_records / one_loop)):
            print('start', i* one_loop)
            sru = SRU_QUERY_p % (name, str(i * one_loop))
            data = requests.get(sru)
            data = etree.fromstring(data.content)

            for l in data.iter():
                if l.tag.endswith('identifier'):
                    name = line.get('name')
                    val = l.text.split('=')[1]
                    records_associated['by_string'][name].add(val)

            print(name, len(records_associated['by_string'][name]), total_nr_of_records)
