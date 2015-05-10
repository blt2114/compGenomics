#!/usr/bin/env python

# to scale down the read counts by the number of reads

import sys
import json
from json import encoder
encoder.FLOAT_REPR = lambda o: format(o, '.2f')

if len(sys.argv) < 1:
    sys.stderr.write("invalid usage: python change_float_precision.py"+
            "<file_to_reformat>\n")
    sys.exit(2)

file_to_reformat = sys.argv[1]

dicts = []
with open(file_to_reformat) as json_file:
    for line in json_file:
        site=json.loads(line)
        for k1 in site.keys():
            if type(site[k1]) is dict:
                for k2 in site[k1].keys():
                    if not type(site[k1][k2]) is list: 
                        continue
                    my_list = site[k1][k2]
                    for i in range(0,len(my_list)):
                        my_list[i]=float("%.3f" % my_list[i])
                    site[k1][k2]=my_list;
        print json.dumps(site)
json_file.close()
