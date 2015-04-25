#!/usr/bin/env python

# to sort lines in tsv by second field alphanumerically

import sys

if len(sys.argv) < 2:
    sys.stderr.write("invalid usage: python sortJSON.py <file_to_sort.tsv>\n")
    sys.exit(2)

file_to_sort_fn = sys.argv[1]
# load config info from json into a dictionary
with open(file_to_sort_fn) as exons_file:
    lines= list(exons_file)

#print first line
print lines[0].strip("\n")

lines = lines[1:]

lines.sort(key=lambda x: x.split("\t")[1])
for line in lines:
    print line.strip("\n")
