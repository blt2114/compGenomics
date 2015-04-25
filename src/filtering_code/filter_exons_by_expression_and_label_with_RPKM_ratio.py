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
if not len(sys.argv) in [4, 5]:
    sys.stderr.write("invalid usage: python filter_exons.py"+
            " <genes_to_filter_RPKM.tsv>"+
            " <exons_RPKM.tsv> <most_expressed_exons.json> (<gene_RPKM_threshold>)\n")
    sys.exit(2)

genes_fn = sys.argv[1]
exons_fn = sys.argv[2]
most_expressed_exons_fn=sys.argv[3]
gene_RPKM_threshold = 1.0 # default threshold for gene expression in sample
                            # for exons in that gene ot be included.
ref_exon_RPKM_threshold=1.0

if len(sys.argv) is 5:      # if included, set explicitly
    gene_RPKM_threshold=float(sys.argv[4])

# load genes info from json into a dictionary
    # Presumably this file will be small enough that doing this is not a
    # problem.
with open(genes_fn) as genes_file:
    genes = list(genes_file)
genes_file.close()

with open(most_expressed_exons_fn) as most_expressed_exons_file:
    most_expressed_exons=json.loads(most_expressed_exons_file.readline())#,object_hook=_decode_dict)
most_expressed_exons_file.close()


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
exon=exons[1]
exon_split=exon.strip("\n").split("\t")
line_num=1
num_lines= len(exons)
while (not exon_split[1] in most_expressed_exons.keys()) or (not exon_split[1] in genes_dict.keys()):
    exon=exons[line_num]
    line_num+=1
    exon_split=exon.strip("\n").split("\t")
current_gene=exon_split[1]
exons_of_gene={exon_split[0]:exon_split}
while line_num < len(exons):
    exon=exons[line_num]
    line_num+=1
    exon_split=exon.strip("\n").split("\t")
    while (not exon_split[1] in most_expressed_exons.keys()) or (not exon_split[1] in genes_dict.keys()):
        exon=exons[line_num]
        line_num+=1
        if line_num%10000 == 0:
            sys.stderr.write("on line: "+str(line_num)+" of "+str(num_lines)+"\n")
        exon_split=exon.strip("\n").split("\t")

    if not exon_split[1] == current_gene:
        if not exon_split[1] in genes_dict.keys():
            current_gene=exon_split[1]
            exons_of_gene={exon_split[0]:exon_split}
            continue
        reference_exon =exons_of_gene[most_expressed_exons[current_gene]][0]
        ref_RPKMs=exons_of_gene[reference_exon]
        for exon_key in exons_of_gene.keys():
            past_exon_split=exons_of_gene[exon_key]

            # used to collect all inclusion values of the present exon
            # to plot later. 
            inclusion_vals=[] 

            # we do not want to include this reference exon in our
            # calculation since its inclusion value will be one by
            # definition.
            if exon_key==reference_exon:
                continue

            # create dictionary that will contain a data point for each
            # sample.
            exon_dict={}
            exon_dict[exon_labels[0]]=past_exon_split[0]
            exon_dict[exon_labels[1]]=past_exon_split[1]

            # parse out the chromosome, 5' end, 3' end and read
            # direction from the first entry
            chrom, five_p_loc,three_p_loc, read_dir = parse_3p_5p(past_exon_split[0])
            exon_dict["chrom"]=chrom
            exon_dict["read_dir"]=read_dir
            exon_dict["five_p_loc"]=five_p_loc
            exon_dict["three_p_loc"] = three_p_loc

            # loop through all of the samples for the present exon.
            for i in exon_labels[2:]:
                # if the gene is not expressed at high enough an RPMK to
                # have been assigned an RPKM previously, continue
                if (not past_exon_split[1] in genes_dict.keys())  or genes_dict[past_exon_split[1]][i] is None: 
                    continue

                #make calculations for exons of current gene and move on.
                # grap the RPMK value from the column corresponding to
                # label i.
                exon_RPKM = float(past_exon_split[exon_labels.index(i)])
                
                # calculate an approximation of the portion of
                # transcripts that include the present exon in the
                # present sample.
                ref_RPKM=ref_RPKMs[exon_labels.index(i)]
                if float(ref_RPKM) < float(ref_exon_RPKM_threshold):
                    continue
                p_inclusion = exon_RPKM/float(ref_RPKM)

                # add the p_inclusion to the exon dict
                exon_dict[i]={"p_inc":p_inclusion}
                inclusion_vals.append(p_inclusion)
            print json.dumps(exon_dict)

            exons_dict[past_exon_split[0]]=inclusion_vals

        # Reset necessary variables for processing exons on the next
        # gene.
        current_gene=exon_split[1]
        exons_of_gene={exon_split[0]:exon_split}
    else:
        exons_of_gene[exon_split[0]]=exon_split

# this plots a fairly arbitrary subset of exon inclusions rates. This was
# done in order to get a sense of how the inclusion proportion of some exons 
# are distributed on single exon basis across samples
if False: #set to True to produce figures
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
