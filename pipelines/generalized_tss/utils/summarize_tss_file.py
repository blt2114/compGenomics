__author__ = 'jeffrey'

import sys, json
from src.utils import FileProgress

if len(sys.argv) is not 2:
    sys.stderr.write("invalid usage: python " + sys.argv[0] + " <all_tss_rna.json>\n")
    sys.exit(2)

file = sys.argv[1]

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
            if transcript['attribute']['transcript_status'] in results['transcript_status']:
                results['transcript_status'][transcript['attribute']['transcript_status']] += 1
            else:
                results['transcript_status'][transcript['attribute']['transcript_status']] = 1
            if transcript['attribute']['level'] in results['level']:
                results['level'][transcript['attribute']['level']] += 1
            else:
                results['level'][transcript['attribute']['level']] = 1
            if transcript['attribute']['transcript_type'] in results['transcript_type']:
                results['transcript_type'][transcript['attribute']['transcript_type']] += 1
            else:
                results['transcript_type'][transcript['attribute']['transcript_type']] = 1
            if transcript['source'] in results['source']:
                results['source'][transcript['source']] +=1
            else:
                results['source'][transcript['source']] = 1
        progress.update()

print json.dumps(results, indent=2)


