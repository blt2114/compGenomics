#!/usr/bin/env python

"""
This file converts a gtf file into a json dictionary of genes > transcripts > exons

Usage:
    python tss/gtf2dict.py files/gen10.long.gtf.genes files/gen10.long.gtf.transcripts files/gen10.long.gtf.exons > tss/genes.json

"""

__author__ = 'jeffrey'

import sys, json, collections
from src.utils import file_len, GTF

def main(argv):
    if len(sys.argv) is not 4:
        sys.stderr.write("invalid usage: python gtf2dict.py <gen10.long.gtf.genes> " +
                         "<gen10.long.gtf.transcripts> <gen10.long.gtf.exons>\n")
        sys.exit(2)

    # Initialize Variables
    genes_fn = sys.argv[1]
    transcripts_fn = sys.argv[2]
    exons_fn = sys.argv[3]
    strand_dict = {'+' : 1, '-' : -1}

    # Estimate compute time
    sys.stderr.write("Estimating compute time.\n")
    elen = file_len(exons_fn)
    tlen = file_len(transcripts_fn)
    glen = file_len(genes_fn)

    # Load genes
    sys.stderr.write("Starting to load genes.\n")
    count = 0
    prev = None
    gene_dict = {}
    genes_f = open(genes_fn, 'rb')
    for line in genes_f:
        gtf = GTF(line)
        gtf.transcripts = {}
        gene_dict[gtf.attribute['gene_id']] = gtf.__dict__

        # Update compute time
        count += 1
        percent = int(float(count) / float(glen) * 100)
        if prev != percent:
            sys.stderr.write("\rPart 1/3: %d%%" %percent)
            sys.stderr.flush()
        prev = percent

    # Load transcripts
    sys.stderr.write("\nStarting to load transcripts.\n")
    count = 0
    prev = None
    transcripts_f = open(transcripts_fn, 'rb')
    for line in transcripts_f:
        gtf = GTF(line)
        gtf.exons = []
        if gtf.attribute['gene_id'] in gene_dict:
            gene_dict[gtf.attribute['gene_id']]['transcripts'][gtf.attribute['transcript_id']] = gtf.__dict__
        else:
            sys.stderr.write("This transcript's gene cannot be found in the gene list!\n")

        # Update compute time
        count += 1
        percent = int(float(count) / float(tlen) * 100)
        if prev != percent:
            sys.stderr.write("\rPart 2/3: %d%%" %percent)
            sys.stderr.flush()
        prev = percent

    # Load exons
    sys.stderr.write("\nStarting to load exons.\n")
    count = 0
    prev = None
    exons_f = open(exons_fn, 'rb')
    for line in exons_f:
        gtf = GTF(line)
        if gtf.attribute['gene_id'] in gene_dict:
            gene = gene_dict[gtf.attribute['gene_id']]
            if gtf.attribute['transcript_id'] in gene['transcripts']:
                transcript = gene['transcripts'][gtf.attribute['transcript_id']]
                transcript['exons'].append(gtf.__dict__)
                transcript['exons'].sort(key=lambda x: (strand_dict[x['strand']])*int(x['start']))
            else:
                sys.stderr.write("This exon's transcript cannot be found in the gene list!\n")
        else:
            sys.stderr.write("This exon's gene cannot be found in the gene list!\n")

        # Update compute time
        count += 1
        percent = int(float(count) / float(elen) * 100)
        if prev != percent:
            sys.stderr.write("\rPart 3/3: %d%%" %percent)
            sys.stderr.flush()
        prev = percent

    # Print Everything
    sys.stderr.write("\nBeginning to print.\n")
    for gene in gene_dict:
        print json.dumps(gene_dict[gene])

    sys.stderr.write("\nProgram is complete.\n")

# Execute this module as a command line script
if __name__ == "__main__":
    main(sys.argv[1:])
