#!/usr/bin/env python

# to filter out samples in exon entries that do not have every dimension

import sys
import json

if len(sys.argv) < 3:
    sys.stderr.write("invalid usage: python"+
            " filter_exons_samples_by_dimension"+
            " <exons_fn> <num_dimensions>\n")
    sys.exit(2)

exons_fn = sys.argv[1]
num_dimensions= int(sys.argv[2])

with open(exons_fn) as json_file:
    for line in json_file:
        new_dict={}
        site=json.loads(line)
        for key in site:
            if type(site[key])==dict:
                if len(site[key])!=num_dimensions:
                    continue
            new_dict[key]=site[key]
        print json.dumps(new_dict)
json_file.close()
