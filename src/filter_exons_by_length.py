#!/usr/bin/env python

# to scale down the read counts by the number of reads

import sys
import json

if len(sys.argv) < 4:
    sys.stderr.write("invalid usage: python filter_exons_by_length.py"+
            "<exons_fn> <min_length> <max_length>\n")
    sys.exit(2)

exons_fn = sys.argv[1]
min_length= int(sys.argv[2])
max_length= int(sys.argv[3])


file_to_scale_down = sys.argv[2]

with open(exons_fn) as json_file:
    for line in json_file:
        site=json.loads(line)
        length=abs(int(site["five_p_loc"])-int(site["three_p_loc"]))
        if length>min_length and length<max_length:
            print json.dumps(site)
json_file.close()
