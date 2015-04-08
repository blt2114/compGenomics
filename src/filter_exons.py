#!/usr/bin/env python
"""
"""

import json
import sys


if len(sys.argv) is not 3:
    sys.stderr.write("invalid usage: python filter_exons.py"+
            " <genes_to_filter_RPKM.tsv>"+
            " <exons_RPKM.txv>\n")
    sys.exit(2)

genes_fn = sys.argv[1]
exons_fn = sys.argv[2]

# load genes info from json into a dictionary
with open(genes_fn) as genes_file:
    genes = list(genes_file)
genes_file.close()

genes_dict={}
gene_labels=genes[0].strip("\n").split("\t") # first row is column headings
for gene in genes[1:]:
    gene_split = gene.strip("\n").split("\t")
    gene_dict={}
    for i in range(1,len(gene_labels)):
        if float(gene_split[i]) == 0.0:
            gene_dict[gene_labels[i]]=None
        else:
            gene_dict[gene_labels[i]]=gene_split[i]
    genes_dict[gene_split[0]]=gene_dict #index whole line by gene name

# load exons info from json into a dictionary
with open(exons_fn) as exons_file:
    exons = list(exons_file)
exons_file.close()

exons_dict={}
exon_labels=exons[0].strip("\n").split("\t") # first row is column headings
for exon in exons[1:]:
    exon_split=exon.strip("\n").split("\t")
    if not genes_dict.has_key(exon_split[1]): 
        continue
    exon_dict={}
    exon_dict[exon_labels[0]]=exon_split[0]
    for i in exon_labels[2:]:
        if genes_dict[exon_split[1]][i] is None:
            exon_dict[i]=None
            continue
        gene_RPKM = float(genes_dict[exon_split[1]][i])
        exon_RPKM = float(exon_split[exon_labels.index(i)])
        exon_dict[i]=exon_RPKM/gene_RPKM
    exons_dict[exon_split[0]]=exon_dict
    print json.dumps(exon_dict)
#print "genes" + str(genes[0])
#print "exons" + str(exons[0])
