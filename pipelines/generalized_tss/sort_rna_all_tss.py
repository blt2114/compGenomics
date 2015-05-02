#!/usr/bin/env python

"""
This file sorts the all_tss_rna.json to match the chromosome order of the chip file
"""

__author__ = 'jeffrey'

import sys, json, csv, collections
from src.utils import FileProgress

# Main Method
def main(argv):
    # parse args
    if len(sys.argv) is not 3:
        sys.stderr.write("invalid usage: python " + sys.argv[0] +
                " <all_tss.json> <57epigenomes.exons.RPKM.all>\n")
        sys.exit(2)

    tss_fn = sys.argv[1]
    rna_fn = sys.argv[2]
    progress = FileProgress(rna_fn, "Percent Complete: ")

    # Sort RNA file by gene id, so they are confirmed to be in order
    #rna_f = unix_sort(rna_fn, "-2,2", header=True)

    # Load JSON file into memory
    gene_dict = {}
    with open(tss_fn, 'rb') as json_file:
        for line in json_file:
            gene = json.loads(line)
            gene_dict[gene['gene_id']] = gene
    sys.stderr.write("Loaded " + str(len(gene_dict)) + " genes into memory.\n")

    # For each match, generate a json_file for all the TSS+RNA+Sample data
    samples = []
    with open(rna_fn) as csv_file:
        rna_file = csv.reader(csv_file, delimiter='\t')
        for row in rna_file:
            if progress.count == 0:
                samples = row
            else:
                gene = row[1]
                if gene in gene_dict:
                    seqname = row[0].split(':')[0]
                    start = int(row[0].split(':')[1].split('-')[0])
                    end = int(row[0].split('-')[1].split('<')[0])
                    strand = int(row[0].split('<')[1])
                    tss = (start if strand==1 else end)

                    # Assign all transcripts that map to this exon
                    exon_transcripts = []
                    for transcript in gene_dict[gene]['transcripts'].itervalues():
                        if transcript['tss'] > start and transcript['tss'] < end:
                            exon_transcripts.append(transcript)

                    # If a transcript mapped, print it
                    if len(exon_transcripts) > 0:
                        d = collections.OrderedDict()
                        d['seqname'] = seqname
                        d['tss'] = tss
                        d['strand'] = ('+' if strand==1 else '-')
                        d['gene_id'] = gene
                        d['transcripts'] = exon_transcripts
                        d['samples'] = {}
                        for i in range(2, len(samples)):
                             sample_name = samples[i]
                             if sample_name not in d['samples']:
                                 d['samples'][sample_name] = {}
                             d['samples'][sample_name]['rpkm'] = row[i]
                        print json.dumps(d)
                else:
                    pass
            progress.update()
    sys.stderr.write("\nAll done!\n")

# Execute this module as a command line script
if __name__ == "__main__":
    main(sys.argv[1:])





