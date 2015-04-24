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

if not len(sys.argv) in [3, 4]:
    sys.stderr.write("invalid usage: python filter_exons.py"+
            " <genes_to_filter_RPKM.tsv>"+
            " <exons_RPKM.tsv> (<gene_RPKM_threshold>)\n")
    sys.exit(2)

genes_fn = sys.argv[1]
exons_fn = sys.argv[2]
gene_RPKM_threshold = 100.0 # default threshold for gene expression in sample
                            # for exons in that gene ot be included.

if len(sys.argv) is 4:      # if included, set explicitly
    gene_RPKM_threshold=float(sys.argv[3])

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
        if float(gene_split[i]) <gene_RPKM_threshold:
            gene_dict[gene_labels[i]]=None
        else:
            gene_dict[gene_labels[i]]=gene_split[i]
    genes_dict[gene_split[0]]=gene_dict # index whole line by gene name

# load exons info from json into a dictionary
with open(exons_fn) as exons_file:
    exons = list(exons_file)
exons_file.close()

# this function parses exon location entry in to 3 prime and 5 prime
# locations
def parse_3p_5p(exon_location):
    location_dir = re.split("<",exon_location)
    chr_loc1_loc2= re.split(":|-|<",exon_location)
    chrom = chr_loc1_loc2[0]
    if location_dir[1] == "-1":
        three_p = chr_loc1_loc2[1]
        five_p = chr_loc1_loc2[2]
    else:
        three_p = chr_loc1_loc2[2]
        five_p = chr_loc1_loc2[1]
    return chrom, five_p, three_p,int(location_dir[1])


exons_dict={} # this structure is similar to that of the genes_dict
exon_labels=exons[0].strip("\n").split("\t") # first row is column headings

# a marker to keep track of the location of the most recent exon end.
last_end = 0 
for exon in exons[1:]:
    exon_split=exon.strip("\n").split("\t")
    inclusion_vals=[]
    if not genes_dict.has_key(exon_split[1]): 
        continue
    exon_dict={}
    
    exon_dict[exon_labels[0]]=exon_split[0]
    exon_dict[exon_labels[1]]=exon_split[1]
    chrom, five_p_loc,three_p_loc, read_dir = parse_3p_5p(exon_split[0])
    exon_dict["chrom"]=chrom
    exon_dict["read_dir"]=read_dir
    exon_dict["five_p_loc"]=five_p_loc
    exon_dict["three_p_loc"] = three_p_loc
    last_end=three_p_loc
    for i in exon_labels[2:]:
        if genes_dict[exon_split[1]][i] is None:
            continue
        gene_RPKM = float(genes_dict[exon_split[1]][i])
        exon_RPKM = float(exon_split[exon_labels.index(i)])
        
        #create dictionary that will be a data point
        exon_dict[i]={"p_inc":exon_RPKM/gene_RPKM}
        inclusion_vals.append(exon_RPKM/gene_RPKM)
        
    exons_dict[exon_split[0]]=inclusion_vals

    print json.dumps(exon_dict)


# this plots a fairly arbitrary subset of exon inclusions rates. This was
# done in order to get a sense of how the inclusion proportion of some exons 
# are distributed on single exon basis across samples
if True: #set to True to produce figures
    keys= exons_dict.keys()
    vals = exons_dict[keys[0]]
    count = 0
    side_len =6
    for i in range(0,side_len):
        for j  in range (0,side_len):
            exon_idx=np.random.randint(0,len(keys)-1)
            count+=1
            plt.subplot(side_len,side_len,count)
            plt.title("mean: " +
                str(np.mean(exons_dict[keys[exon_idx]]))[0:5])
            plt.hist(exons_dict[keys[exon_idx]],bins=100,range=(0,3))
            plt.axis([0,3,0,10])
    plt.show()
