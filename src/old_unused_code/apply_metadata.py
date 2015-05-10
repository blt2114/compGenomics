__author__ = 'jeffrey'

import json, sys, collections
from src.utils import FileProgress

if len(sys.argv) is not 3:
    sys.stderr.write("invalid usage: python " + sys.argv[0] + " <level1_tss_rna_chip.json> <level1_tss_rna.json>\n")
    sys.exit(2)

data = sys.argv[1]
meta = sys.argv[2]


progress1 = FileProgress(meta, "Percent: ")
progress2 = FileProgress(data, "Percent: ")

# Load metadata into memory. It's going to be big.
chrom = {}
with open(meta, 'rb') as json_file:
    for line in json_file:
        site = json.loads(line)
        seqname = site.pop('seqname')
        tss = site.pop('tss')
        site.pop('strand')
        site.pop('gene_id')
        site.pop('transcripts')
        if seqname in chrom:
            chrom[seqname][tss] = site
        else:
            chrom[seqname] = { tss : site}
        progress1.update()

# Now go through data file and update
sys.stderr.write("\nNow working through data file!\n")
with open(data) as json_file:
    for line in json_file:
        site = json.loads(line)
        meta = chrom[site['seqname']][site['tss']]

        # Site-level features
        features = ['exon_number', 'exon_total', 'splice_count', 'coverage_count', 'tss_mapped',
                    'tss_total', 'transcript_total']
        for feature in features:
            site[feature] = meta[feature]

        # Sample-level features
        features = ['delta_rpkm', 'rpkm', 'max_rpkm', 'gene_rpkm']
        for sample_name, sample_dict in site['samples'].iteritems():
            for feature in features:
                sample_dict[feature] = meta['samples'][sample_name][feature]

        chrom[site['seqname']].pop(site['tss'])
        print json.dumps(site)
        progress2.update()

sys.stderr.write("\nAll done!\n")