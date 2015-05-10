#!/usr/bin/env python

import json
import re
import sys
if not len(sys.argv) in [2]:
    sys.stderr.write("invalid usage: python gene_RPKM_to_JSON.py"+
            " <gene_RPKM.tsv> \n")
    sys.exit(2)

genes_fn = sys.argv[1]
# load genes info from json into a dictionary
with open(genes_fn) as genes_file:
    genes = list(genes_file)
genes_file.close()

genes_dict={} 
gene_labels=genes[0].strip("\n").split("\t") # first row is column headings

# a marker to keep track of the location of the most recent gene end.
line_num=1
num_lines= len(genes)
while line_num < len(genes):
    gene=genes[line_num]
    gene_split=gene.strip("\n").split("\t")
    gene_id=gene_split[0]
    genes_dict[gene_id]={"RPKM_by_sample":{}}
    for i in range(1,len(gene_labels)):
        genes_dict[gene_id]["RPKM_by_sample"][gene_labels[i]]=float(gene_split[i])
    line_num+=1
print json.dumps(genes_dict)
