__author__ = 'jeffrey'

import json, sys
from src.utils import FileProgress

file = "../files/all_tss_rna.json"

results = {}
results['transcript_status'] = {}
results['level'] = {}
results['transcript_type'] = {}
results['source'] = {}

progress = FileProgress(file, "Percent: ")

with open(file, 'rb') as json_file:
    for line in json_file:
        site = json.loads(line)
        for transcript in site['transcripts']:
            if transcript['attribute']['level'] == "1":
                print json.dumps(site)
                break
        progress.update()

sys.stderr.write("\nAll done!\n")