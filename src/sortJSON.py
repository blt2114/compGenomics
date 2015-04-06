#!/usr/bin/env python

# to sort by list of json dictionaries in a file by keys

import sys
import json

if len(sys.argv) < 3:
    sys.stderr.write("invalid usage: python sortJSON.py <config.json> <file_to_sort.json>\n")
    sys.exit(2)

config_fn = sys.argv[1]
# load config info from json into a dictionary
with open(config_fn) as config_file:
    config = json.load(config_file)
    config_file.close()

# load expected chromosome order from json into a dictionary
chromosomes_fn = config["chromosome_order_fn"] 
with open(chromosomes_fn) as chromosomes_file:
    chromosomes = json.load(chromosomes_file)
chromosomes_file.close()

file_to_sort = sys.argv[2]

dicts = []
with open(file_to_sort) as json_file:
    for line in json_file:
        dicts.append(json.loads(line))
json_file.close()

# Lambda expression for sort taken from stack overflow:
# http://stackoverflow.com/questions/18761776/sort-list-of-dictionaries-by-multiple-keys-with-different-ordering
dicts.sort(key=lambda x: (chromosomes[x['chrom']],x['location']))
for site in dicts:
    print json.dumps(site)


