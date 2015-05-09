#!/usr/bin/env python
"""
This main looks through raw tagAlign chip-seq files and finds the number of
reads upstream/downstream of locations provided in JSON file.

The sites of interest in the json file are assumeded to be in the same order
as mapped ChIP-Seq reads

this is very similar to the equivalent extraction file for ChIP reads for
TSS's. The biggest difference is that it keeps track of 5' and 3' sites
separately
"""

import json
import collections
import sys
import itertools

if len(sys.argv) is not 5:
    sys.stderr.write("invalid usage: python exon_extract_reads_from_TagAlign.py <config.json>"+
            " <sample_ID-mark_ID> <sites.json> <data_root>\n")
    sys.exit(2)

config_fn = sys.argv[1]
data_root = sys.argv[4]

# load config info from json into a dictionary
with open(config_fn) as config_file:
    config = json.load(config_file)
config_file.close()

sample_mark = sys.argv[2].split("-")
sample_ID = sample_mark[0]
mark_ID =sample_mark[1]

data_fn = data_root + "/" + sample_ID + "-" + mark_ID + ".tagAlign"

upstream_window =config["upstream_window"]
downstream_window =config["downstream_window"]

# load expected chromosome order from json into a dictionary
chromosomes_fn = config["chromosome_order_fn"] 
with open(chromosomes_fn) as chromosomes_file:
    chromosomes = json.load(chromosomes_file)
chromosomes_file.close()

sites_json_fn = sys.argv[3]
# load sites of interest from json into a list
sites_file= open(sites_json_fn)
while True:
    site_line = sites_file.readline().strip("\n")
    current_site = json.loads(site_line)
    if current_site.has_key(sample_ID):
        break 
    print json.dumps(current_site)

#calculate new site information 
exon_sides=[]
exon_side_order=[]
if current_site["read_dir"] == 1:
    exon_sides.append((int(current_site["five_p_loc"])-upstream_window,int(current_site["five_p_loc"])+downstream_window))
    exon_sides.append((int(current_site["three_p_loc"])-upstream_window,int(current_site["three_p_loc"])+downstream_window))
    exon_side_order=("_five_p","_three_p")
else:
    exon_sides.append((int(current_site["three_p_loc"])-downstream_window,int(current_site["three_p_loc"])+upstream_window))
    exon_sides.append((int(current_site["five_p_loc"])-downstream_window,int(current_site["five_p_loc"])+upstream_window))
    exon_side_order=("_three_p","_five_p")
(win_start,win_end)=exon_sides[0]
site_label=mark_ID+"_num_reads"+exon_side_order[0]
site_chrom = chromosomes[current_site["chrom"]]
site_start=(site_chrom,win_start)
site_end = (site_chrom,win_end)
current_site[sample_ID][site_label]=0
finished_exon=False # other end will need to be processed after

#iterate through lines of stdin
f = open(data_fn, 'r')
recent_genes= collections.deque()
RECENT_GENE_BUFFER_LENGTH=2000
file_not_over=True
CHIP_BUFFER_LENGTH= 2000 #number of line to read at once

while True:
    #when there are no more sites to go check, break
    if current_site == None:
        break

    lines=collections.deque(itertools.islice(f,CHIP_BUFFER_LENGTH)) 
    if not lines:
        break 
        
    while len(lines) != 0:
        #when there are no more sites to go check, break
        if current_site == None:
            break

        line = lines.popleft()
        recent_genes.appendleft(line)
        if len(recent_genes)>RECENT_GENE_BUFFER_LENGTH:
            recent_genes.pop()
        # parse out the read location
        values = line.split("\t")

        chromosome = chromosomes[values[0]]
        read_loc = int(values[1])

        read_pos = (chromosome,read_loc)

        # if the read is before the lower boundary of the window,
        # continue
        if read_pos < site_start:
            continue

        # if the read is within the boundaries, add one to the count and
        # continue
        if read_pos <= site_end:
            current_site[sample_ID][site_label]+=1
            continue

        # by this point, read is upstream of the upper boundary of the window, 

        # while no label available, so skip to next site.
        while True:
            if not finished_exon:
                if not exon_sides:
                    std.stderr.write("exon_sides not defined!\n")
                    sys.exit(2)
                break

            # print the site(which has now been passed) with the additional information to stdout 
            print json.dumps(current_site)
            exon_sides=[]
            exon_side_order=[]
            current_site_line= sites_file.readline()
            # if finished going through all of the sites...
            if current_site_line == "":
                current_site = None
                break
            current_site= json.loads(current_site_line)
            if current_site.has_key(sample_ID):
                # skip to next if no label is available
                break

        # if finished going through all of the sites...
        if current_site == None:
            continue
        if not finished_exon:
            (win_start,win_end)=exon_sides[1]
            site_label=mark_ID+"_num_reads"+exon_side_order[1]
            finished_exon=True
        else:
            if current_site["read_dir"] == 1:
                exon_sides.append((int(current_site["five_p_loc"])-upstream_window,int(current_site["five_p_loc"])+downstream_window))
                exon_sides.append((int(current_site["three_p_loc"])-upstream_window,int(current_site["three_p_loc"])+downstream_window))
                exon_side_order=("_five_p","_three_p")
            else:
                exon_sides.append((int(current_site["three_p_loc"])-downstream_window,int(current_site["three_p_loc"])+upstream_window))
                exon_sides.append((int(current_site["five_p_loc"])-downstream_window,int(current_site["five_p_loc"])+upstream_window))
                exon_side_order=("_three_p","_five_p")

            #calculate new site information 
            (win_start,win_end)=exon_sides[0]
            site_label=mark_ID+"_num_reads"+exon_side_order[0]
            finished_exon=False
        site_chrom = chromosomes[current_site["chrom"]]
        site_start=(site_chrom,win_start)
        site_end = (site_chrom,win_end)
        
        current_site[sample_ID][site_label]=0
            
        #add the recent genes onto the beginning of the lines to process
        #this allows lines to be counted towards multiple sites
        lines.extendleft(recent_genes)
        recent_genes.clear()
        line=None
            
f.close()
sites_file.close()
