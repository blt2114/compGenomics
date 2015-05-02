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
results['tss_number'] = {}
results['tss_type'] = {}
gene_dict = {}

progress = FileProgress(file, "Percent: ")

with open(file, 'rb') as json_file:
    prev = (None, 0)
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
        if site['tss_type'] in results['tss_type']:
            results['tss_type'][site['tss_type']] += 1
        else:
            results['tss_type'][site['tss_type']] = 1

        if not site['gene_id'] in gene_dict:
            gene_dict[site['gene_id']] = True

        if prev[0] != site['gene_id'] and prev[0] is not None:
            label = str(prev[1]) + "_tss"
            if label in results['tss_number']:
                results['tss_number'][label] += 1
            else:
                results['tss_number'][label] = 1
            prev = (site['gene_id'], 1)
        else:
            prev = (site['gene_id'], prev[1] + 1)
        progress.update()

print json.dumps(results, indent=2)
print str(len(gene_dict))

