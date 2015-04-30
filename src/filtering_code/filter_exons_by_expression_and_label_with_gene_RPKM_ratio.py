#!/usr/bin/env python
"""
Filter_exons goes through a file gene expression data (from raw gene RPKM
file) and file of exon RPKM data and selects those exons which are part of
genes in the list provided and for which the gene RPKM for that sample 
meets a specifed threshold. This is useful because it allows us data from
samples in which that gene in question is not expressed, since in such cases
exon inclusion likely is not under regulation.

"""

import json
import sys
import re
import numpy as np
import matplotlib.pyplot as plt
if not len(sys.argv) in [4,5]:
    sys.stderr.write("invalid usage: python filter_exons.py"+
            " <exons_RPKM.json> <genes_to_filter_RPKM.tsv>"+
            " <exons_to_label.tsv> (<gene_RPKM_threshold>)\n")
    sys.exit(2)

exon_RPKMS_fn = sys.argv[1]
genes_fn = sys.argv[2]
exons_fn = sys.argv[3]
gene_RPKM_threshold = 1.0 # default threshold for gene expression in sample
                            # for exons in that gene ot be included.

if len(sys.argv) is 5:      # if included, set explicitly
    gene_RPKM_threshold=float(sys.argv[4])

# load genes info from json into a dictionary
    # Presumably this file will be small enough that doing this is not a
    # problem.
with open(genes_fn) as genes_file:
    genes = list(genes_file)
genes_file.close()

genes_dict={} # holds information by gene
gene_labels=genes[0].strip("\n").split("\t") # first row is column headings
for gene in genes[1:]: # for all lines after the headings
    # remove newline and split tsv's in the line into a list
    gene_split = gene.strip("\n").split("\t") 
    gene_dict={}
    for i in range(1,len(gene_labels)):
        # if the gene is not sufficiently expressed in the sample, we do
        # not want to provide lables for exons in it, so don't even record
        # it't RPKM
        if float(gene_split[i]) <gene_RPKM_threshold:
            gene_dict[gene_labels[i]]=None
        else:
            gene_dict[gene_labels[i]]=gene_split[i]
    genes_dict[gene_split[0]]=gene_dict # index whole line by gene name
    
exons_RPKM_file = open(exon_RPKMS_fn)

exons_RPKM_dict={} # holds information by gene
for line in exons_RPKM_file: # for all lines after the headings
    exon=json.loads(line)
    exons_RPKM_dict[exon["exon_location"]]=exon # index whole line by gene name
exons_RPKM_file.close()

# load exons info from json into a dictionary
exons_file= open(exons_fn)
exon=json.loads(exons_file.readline())
while exon !=None:
    current_gene=exon["gene_id"]
    exon_RPKM_dict=exons_RPKM_dict[exon["exon_location"]]
    # if the gene is not expressed at high enough an RPKM to
    # have been assigned an RPKM previously, continue
    #make calculations for exons of current gene and move on.
    # grap the RPKM value from the column corresponding to
    # label i.
    for l in gene_labels[1:len(gene_labels)]:
        if not exon.has_key(l):
            continue
        gene_RPKM = genes_dict[current_gene][l]
        if gene_RPKM is None:
            continue
        exon_RPKM = float(exon_RPKM_dict[l])

        # calculate an approximation of the portion of
        # transcripts that include the present exon in the
        # present sample.
        p_inclusion_gene = exon_RPKM/float(gene_RPKM)

        # add the p_inclusion to the exon dict
        exon[l]["p_inc_gene"]=p_inclusion_gene
    print json.dumps(exon)

    line = exons_file.readline()
    if line != None:
        exon=json.loads(line)
    else:
        exon=None
exons_file.close()
