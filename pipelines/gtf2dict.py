#!/usr/bin/env python

"""
This file converts a gtf file into a json dictionary of genes > transcripts > exons

Usage:

"""

__author__ = 'jeffrey'

import sys, json
from src.utils import GTF, file_len

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

    """
    # Load exons
    sys.stderr.write("Starting to load exons.\n")
    count = 0
    prev = None
    exon_list = []
    exons_f = open(exons_fn, 'rb')
    for line in exons_f:
        gtf = GTF(line)
        exon_list.append(gtf)

        # Update compute time
        count += 1
        percent = int(float(count) / float(elen) * 100)
        if prev != percent:
            sys.stderr.write("\rPart 1/3: %d%%" %percent)
            sys.stderr.flush()
        prev = percent

    # Load transcripts
    sys.stderr.write("\nStarting to load transcripts.\n")
    count = 0
    prev = None
    transcript_list = []
    transcripts_f = open(transcripts_fn, 'rb')
    for line in transcripts_f:
        gtf = GTF(line)

        # Update compute time
        count += 1
        percent = int(float(count) / float(tlen) * 100)
        if prev != percent:
            sys.stderr.write("\rPart 2/3: %d%% - 0" %percent)
            sys.stderr.flush()
        prev = percent

        # Find all exons for this transcript
        icount = 0
        iprev = None
        transcript_exon_list = []
        for exon in exon_list:
            if exon.attribute['transcript_id'] ==  gtf.attribute['transcript_id']:
                transcript_exon_list.append(exon)

            # Update compute time
            icount += 1
            ipercent = int(float(icount) / float(elen) * 100)
            if iprev != ipercent:
                sys.stderr.write("\rPart 2/3: " + str(percent) + "% - " + str(ipercent) + "%")
                sys.stderr.flush()
            iprev = ipercent

        if len(transcript_exon_list) == 0:
            sys.stderr.write("ERROR! No exons matched to this transcript!")
        transcript_exon_list.sort(key=lambda x: (strand_dict[x.strand])*int(x.start))
        gtf.exons = transcript_exon_list

    # Load genes
    sys.stderr.write("\nStarting to load genes.\n")
    count = 0
    prev = None
    genes_f = open(genes_fn, 'rb')
    for line in genes_f:
        gtf = GTF(line)

        # Find all transcripts for this gene
        gene_transcript_list = []
        for transcript in transcript_list:
            if transcript.attribute['gene_id'] ==  gtf.attribute['gene_id']:
                gene_transcript_list.append(transcript)
        if len(gene_transcript_list) == 0:
            sys.stderr.write("ERROR! No transcripts matched to this gene!")
        gene_transcript_list.sort(key=lambda x: (strand_dict[x.strand])*int(x.start))
        gtf.transcripts = gene_transcript_list

        # Print this gene to standard out
        print json.dumps(gtf)

        # Update compute time
        count += 1
        percent = int(float(count) / float(glen) * 100)
        if prev != percent:
            sys.stderr.write("\rPart 3/3: %d%%" %percent)
            sys.stderr.flush()
        prev = percent
    """

    sys.stderr.write("\nProgram is complete.\n")

# Execute this module as a command line script
if __name__ == "__main__":
    main(sys.argv[1:])
