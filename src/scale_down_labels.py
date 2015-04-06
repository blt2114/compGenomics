#!/usr/bin/env python

# to scale down the read counts by the number of reads

import sys
import json

if len(sys.argv) < 3:
    sys.stderr.write("invalid usage: python scale_down_labels.py"+
            +"<read_counts.json> <features.txt>\n")
    sys.exit(2)

read_counts_fn = sys.argv[1]
# load config info from json into a dictionary
with open(read_counts_fn) as reads_file:
    print read_counts_fn
    reads = json.load(reads_file)
    reads_file.close()


file_to_scale_down = sys.argv[2]

dicts = []
with open(file_to_scale_down) as json_file:
    for line in json_file:
        site=json.loads(line)
        for k1 in site.keys():
            if type(site[k1]) is dict:
                for k2 in site[k1].keys():
                    site[k1][k2]["num_reads"]/= float(reads[k1][k2])
        print json.dumps(site)
json_file.close()
