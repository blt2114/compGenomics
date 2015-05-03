__author__ = 'jeffrey'

"""
This file heads a json file are returns it in human readable format
"""


import sys, json

if len(sys.argv) is not 3:
    sys.stderr.write("invalid usage: python " + sys.argv[0] + " <number_lines> <json_file.json>\n")
    sys.exit(2)

num = int(sys.argv[1])
file = sys.argv[2]

count = 0
with open(file, 'rb') as json_file:
    for line in json_file:
        if count < num:
            site = json.loads(line)
            print json.dumps(site, indent=2)
        else:
            break
        count += 1
sys.stderr.write("All Done!\n")
