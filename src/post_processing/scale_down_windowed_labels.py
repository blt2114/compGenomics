#!/usr/bin/env python

# to scale down the read counts by the number of reads

import sys
import json

if len(sys.argv) < 2:
    sys.stderr.write("invalid usage: python scale_down_windowed_labels.py"+
            " <read_counts.json> <file_to_scale>\n")
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
                if not reads.has_key(k1):
                    # this is the case for exprmt E000
                    continue
                for k2 in site[k1].keys():
                    mark=k2.split("_")[0]
                    if reads[k1].has_key(mark):
                        # scale down for every value in the array
                        for i in range(0,len(site[k1][k2])):
                            site[k1][k2][i]/= (float(reads[k1][mark])/10000000)
        print json.dumps(site)
json_file.close()
