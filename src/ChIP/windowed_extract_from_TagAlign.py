#!/usr/bin/env python
"""
This main looks through raw tagAlign chip-seq files and finds the number of
reads upstream/downstream of five_p_locs provided in JSON file.

The sites of interest in the json file are assumeded to be in the same order
as mapped ChIP-Seq reads

this is very similar to the equivalent extraction file for ChIP reads for
TSS's.

This does not assume that the sites already have fields corresponding to
each sampleID.  If the field is not present it is created.
"""

import json
import collections
import sys
import itertools

if len(sys.argv) is not 5:
    sys.stderr.write("invalid usage: python ChIP_extract.py <config.json>"+
            " <sample_ID-mark_ID> <sites.json> <data_root>\n")
    sys.exit(2)

config_fn = sys.argv[1]
data_root = sys.argv[4]

# a fucntion to get the running count from counts in bins
def sums(list_of_counts):
    new_l=[0]*len(list_of_counts)
    new_l[0]=list_of_counts[0]
    for i in range(1,len(list_of_counts)):
            new_l[i]=new_l[i-1]+list_of_counts[i]
    return new_l

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
win_size=config["window_size"]

# load expected chromosome order from json into a dictionary
chromosomes_fn = config["chromosome_order_fn"] 
with open(chromosomes_fn) as chromosomes_file:
    chromosomes = json.load(chromosomes_file)
chromosomes_file.close()

sites_json_fn = sys.argv[3]
# load sites of interest from json into a list
sites_file= open(sites_json_fn)
site_line = sites_file.readline().strip("\n")
current_site = json.loads(site_line)
#calculate new site information 
exon_sides=[]
exon_side_order=[]
if current_site["read_dir"] == 1:
    (win_start,win_end)=(int(current_site["five_p_loc"])-upstream_window,int(current_site["five_p_loc"])+downstream_window)
else:
    (win_start,win_end)=(int(current_site["five_p_loc"])-downstream_window,int(current_site["five_p_loc"])+upstream_window)
site_label=mark_ID+"_reads"
site_chrom = chromosomes[current_site["chrom"]]
site_start=(site_chrom,win_start)
site_end = (site_chrom,win_end)
num_windows=(win_end-win_start)/(win_size)
if current_site.has_key(sample_ID):
    current_site[sample_ID][site_label]=[0]*num_windows
else:
    current_site[sample_ID]={site_label:[0]*num_windows}

#iterate through lines of stdin
f = open(data_fn, 'r')
recent_genes= collections.deque()
RECENT_GENE_BUFFER_LENGTH=15000
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
        # parse out the read five_p_loc
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
            bag=(read_pos[1]-site_start[1])/win_size
            if bag==num_windows:
                bag-=1
            current_site[sample_ID][site_label][bag]+=1
            continue

        # by this point, read is upstream of the upper boundary of the window, 

        # while no label available, so skip to next site.
        if current_site["read_dir"]==-1:
            current_site[sample_ID][site_label].reverse()
        current_site[sample_ID][site_label]=sums(current_site[sample_ID][site_label])

        print json.dumps(current_site)
        current_site_line= sites_file.readline()
        # if finished going through all of the sites...
        if current_site_line == "":
            current_site = None
            continue
        current_site= json.loads(current_site_line)

        if current_site.has_key(sample_ID):
            current_site[sample_ID][site_label]=[0]*num_windows
        else:
            current_site[sample_ID]={site_label:[0]*num_windows}

        if current_site["read_dir"] == 1:
            (win_start,win_end)=(int(current_site["five_p_loc"])-upstream_window,int(current_site["five_p_loc"])+downstream_window)
        else:
            (win_start,win_end)=(int(current_site["five_p_loc"])-downstream_window,int(current_site["five_p_loc"])+upstream_window)

        #calculate new site information 

        site_chrom = chromosomes[current_site["chrom"]]
        site_start=(site_chrom,win_start)
        site_end = (site_chrom,win_end)
        
        #add the recent genes onto the beginning of the lines to process
        #this allows lines to be counted towards multiple sites
        lines.extendleft(recent_genes)
        recent_genes.clear()
        line=None
f.close()
sites_file.close()
