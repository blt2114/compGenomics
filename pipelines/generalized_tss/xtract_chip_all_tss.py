#!/usr/bin/env python

"""
The principle to this file is to add chip read counts to all transcripts in a config file
"""

__author__ = 'jeffrey'

import sys, json, csv, collections
from src.utils import FileProgress

# Main Method
def main(argv):
    # parse args
    if len(sys.argv) is not 4:
        sys.stderr.write("invalid usage: python " + sys.argv[0] +
                " <all_tss_rna.json> <E003-H2A.Z.tagAlign> <chromosome_order.json>\n")
        sys.exit(2)
    rna_fn = sys.argv[1]
    chip_fn = sys.argv[2]
    chromosomes_fn = sys.argv[3]
    progress = FileProgress(chip_fn, "Percent Complete: ")

    # load expected chromosome order from json into a dictionary
    with open(chromosomes_fn) as chromosomes_file:
        chromosomes = json.load(chromosomes_file)

    # Main loop
    with open(chip_fn) as csv_file:
        chip_file = csv.reader(csv_file, delimiter='\t')
        prev = None
        for row in chip_file:
            if prev != row[0] and prev is not None:
                print prev
            prev = row[0]
            progress.update()
        print prev


    # Sort RNA file by gene id, so they are confirmed to be in order
    #rna_f = unix_sort(rna_fn, "-2,2", header=True)

"""
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
"""

# Execute this module as a command line script
if __name__ == "__main__":
    main(sys.argv[1:])





