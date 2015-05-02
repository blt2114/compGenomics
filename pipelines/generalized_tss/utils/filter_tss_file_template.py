__author__ = 'jeffrey'

import json, sys, collections
from src.utils import FileProgress

if len(sys.argv) is not 2:
    sys.stderr.write("invalid usage: python " + sys.argv[0] + " <all_tss_rna.json>\n")
    sys.exit(2)

file = sys.argv[1]

progress = FileProgress(file, "Percent: ")

with open(file, 'rb') as json_file:
    for line in json_file:
        site = json.loads(line, object_pairs_hook=collections.OrderedDict)
        for transcript in site['transcripts']:
            if transcript['attribute']['level'] == "1":
                print json.dumps(site)
                break
        progress.update()

sys.stderr.write("\nAll done!\n")