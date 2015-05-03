#!/usr/bin/env python

"""
The principle to this file is to add RPKM values to all transcripts in a config file

The input is a gene list, and the output is the gene RPKM.
"""

__author__ = 'jeffrey'

import sys, json, csv, collections
from src.utils import FileProgress, unix_sort

# Main Method
def main(argv):
    # parse args
    if len(sys.argv) is not 5:
        sys.stderr.write("invalid usage: python " + sys.argv[0] +
                " <all_tss.json> <57epigenomes.exon.RPKM.all> <chromosome_order.json> <granularity>\n")
        sys.exit(2)

    tss_fn = sys.argv[1]
    rna_fn = sys.argv[2]
    chromosomes_fn = sys.argv[3]
    granularity = int(sys.argv[4])
    progress1 = FileProgress(rna_fn, "Part 1/2: ")
    progress2 = FileProgress(rna_fn, "Part 2/2: ")

    # load expected chromosome order from json into a dictionary
    with open(chromosomes_fn) as chromosomes_file:
        chromosomes = json.load(chromosomes_file)

    # Sort RNA file by gene id, so they are confirmed to be in order
    rna_f = unix_sort(rna_fn, "-k2,2 -k1,1", header=True)

    # Load JSON GTF file into memory
    gene_dict = {}
    with open(tss_fn, 'rb') as json_file:
        for line in json_file:
            gene = json.loads(line)
            gene_dict[gene['gene_id']] = gene
    sys.stderr.write("Loaded " + str(len(gene_dict)) + " genes into memory.\n")

    # Read RNA-seq data into memory
    # The purpose of this entire section is calculate leading and cassette exons
    rna_data = []
    samples = []
    previous_gene = None
    rna_file = csv.reader(rna_f, delimiter='\t')
    for row in rna_file:
        if progress1.count == 0:
            samples = row
        else:
            gene = row[1]
            if gene in gene_dict:
                if previous_gene != gene:
                    if previous_gene is not None:
                        # The previous exon was the last exon of the previous gene
                        if gene_dict[previous_gene]['strand'] == '-':
                            rna_data[-1][2] = 'leading'
                    # The current exon is the first exon of this gene
                    if gene_dict[gene]['strand'] == '+':
                        row.insert(2, 'leading')
                    else:
                        row.insert(2, 'cassette')
                else:
                    row.insert(2, 'cassette')
                rna_data.append(row)
                previous_gene = gene
        progress1.update()

    # Now sort the RNA-seq data that is in memory
    sys.stderr.write("\nBeginning to sort loaded RNA-seq file\n")
    rna_data.sort(key=lambda row: (
        chromosomes[row[0].split(':')[0]], #chromosome, passed into chromosomes config dictionary
        (
            int(row[0].split(':')[1].split('-')[0]) #start
            if int(row[0].split('<')[1])==1 #if strand==1
            else int(row[0].split('-')[1].split('<')[0]) #else end
        )
    ))
    sys.stderr.write("Finished sorting loaded RNA-seq file\n")

    # Now print the exons that have transcript start sites
    for row in rna_data:
        gene = row[1]
        if gene in gene_dict:
            seqname = row[0].split(':')[0]
            start = int(row[0].split(':')[1].split('-')[0])
            end = int(row[0].split('-')[1].split('<')[0])
            strand = int(row[0].split('<')[1])
            tss = (start if strand==1 else end)

            # Assign all transcripts that map to this exon
            exon_transcripts = []
            splice_count = 0
            for transcript in gene_dict[gene]['transcripts'].itervalues():
                if transcript['tss'] > start - granularity and transcript['tss'] < end + granularity:
                    exon_transcripts.append(transcript)
                for intron in transcript['introns']:
                    if start > intron[1] or end < intron[0]:
                        # not spliced out
                        pass
                    else:
                        splice_count += 1

            # If a transcript mapped to one of the exons
            if len(exon_transcripts) > 0:

                # Print this transcript
                d = collections.OrderedDict()
                d['seqname'] = seqname
                d['tss'] = tss
                d['strand'] = ('+' if strand==1 else '-')
                d['gene_id'] = gene
                d['tss_type'] = row[2]
                d['splice_count'] = splice_count
                d['transcripts'] = exon_transcripts
                d['samples'] = {}
                for i in range(3, len(samples)):
                    sample_name = samples[i]
                    if sample_name not in d['samples']:
                        d['samples'][sample_name] = {}
                    d['samples'][sample_name]['rpkm'] = row[i]
                print json.dumps(d)
                break

        progress2.update()
    sys.stderr.write("\nAll done!\n")

# Execute this module as a command line script
if __name__ == "__main__":
    main(sys.argv[1:])





