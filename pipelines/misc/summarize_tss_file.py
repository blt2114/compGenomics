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
results['exon_number'] = {}
results['exon_total'] = {}
results['splice_count'] = {}
results['splice_before'] = {}
results['coverage_count'] = {}
results['tss_mapped'] = {}
results['tss_total'] = {}
results['transcript_total'] = {}

gene_dict = {}

progress = FileProgress(file, "Percent: ")

counter = 0
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
        search = [
            'exon_number', 'exon_total', 'splice_count', 'splice_before', 'coverage_count', 'tss_mapped',
            'tss_total', 'transcript_total'
        ]
        for item in search:
            if str(site[item]) in results[item]:
                results[item][str(site[item])] += 1
            else:
                results[item][str(site[item])] = 1

        if not site['gene_id'] in gene_dict:
            gene_dict[site['gene_id']] = True

        progress.update()
        counter += 1

print json.dumps(results, indent=2)
print "Number of unique genes: " + str(len(gene_dict))
print "Number of tss sites: " + str(counter)
sys.stderr.write("\nAll Done!\n")
