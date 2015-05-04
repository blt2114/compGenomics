__author__ = 'jeffrey'

"""
This file heads a json file are returns it in human readable format
"""


import sys, json
from src.utils import FileProgress

if len(sys.argv) is not 2:
    sys.stderr.write("invalid usage: python " + sys.argv[0] + " <json_file.json>\n")
    sys.exit(2)

file = sys.argv[1]
progress = FileProgress(file, "Percent: ")

with open(file, 'rb') as json_file:
    for line in json_file:
        site = line.strip('\n').split('\t')
        values = eval(site[4])
        print site[3] + "\t" + "\t".join(map(str, values))
        progress.update()
sys.stderr.write("All Done!\n")
