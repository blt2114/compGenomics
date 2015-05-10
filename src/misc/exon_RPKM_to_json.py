#!/usr/bin/env python

import json
import re
import sys
if not len(sys.argv) in [2]:
    sys.stderr.write("invalid usage: python exon_RPKM_to_JSON.py"+
            " <exons_RPKM.tsv> \n")
    sys.exit(2)

exons_fn = sys.argv[1]
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
current_gene=exon_split[1]
exons_of_gene={exon_split[0]:exon_split}
while line_num < len(exons):
    exon_dict={}
    exon_dict["exon_location"]=exon_split[0]
    exon_dict["gene_id"]=exon_split[1]
    chrom, five_p_loc,three_p_loc, read_dir = parse_3p_5p(exon_split[0])
    exon_dict["chrom"]=chrom
    exon_dict["five_p_loc"]=five_p_loc
    exon_dict["three_p_loc"]=three_p_loc
    exon_dict["read_dir"]=read_dir
    exon_dict["RPKM_by_sample"]={}
    for i in range(2,len(exon_labels)):
        exon_dict["RPKM_by_sample"][exon_labels[i]]=float(exon_split[i])
    print json.dumps(exon_dict)
    exon=exons[line_num]
    line_num+=1
    exon_split=exon.strip("\n").split("\t")
