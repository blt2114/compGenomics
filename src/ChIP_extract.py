#!/usr/bin/env python
"""
This main looks through raw tagAlign chip-seq files and finds the number of
reads upstream/downstream of locations provided in JSON file.

The sites of interest in the json file are assumeded to be in the same order
as mapped ChIP-Seq reads

"""

#TODO: update to take sample ID and Experiment type as command line
# arguments and carry that include that with the read count.

import json
import sys


if len(sys.argv) is not 5:
    sys.stderr.write("invalid usage: python find_sites.py <config.json>"+
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
current_site = json.loads(sites_file.readline())


if current_site.has_key(sample_ID):
    current_site[sample_ID][mark_ID]={"num_reads":0}
else:
    current_site[sample_ID]={mark_ID:{"num_reads":0}}

if current_site["read_dir"] == 1:
    win_start=current_site["location"]-upstream_window
    win_end=current_site["location"]+downstream_window
else:
    win_start=current_site["location"]-downstream_window
    win_end=current_site["location"]+upstream_window

site_chrom = chromosomes[current_site["chrom"]]
site_start=(site_chrom,win_start)
site_end = (site_chrom,win_end)

#iterate through lines of stdin
f = open(data_fn, 'r')
for line in f:

    # parse out the read location
    values = line.split("\t")

    chromosome = chromosomes[values[0]]
    read_loc = int(values[1])

    read_pos = (chromosome,read_loc)

    # if the read is before the lower boundary of the window,
    # continue
    if read_pos < site_start:
        continue

    # since this is repeated below, this first replicate is functionally
    # unnessary, however it improves the programs efficiency
    # if the read is within the boundaries, add one to the count and
    # continue
    if read_pos <= site_end:
        current_site[sample_ID][mark_ID]["num_reads"]+=1
        continue
    
        # if the read is upstream of the upper boundary of the window, 
    while read_pos > site_end:
        # print the site with the additional information to stdout 
        print json.dumps(current_site)

        current_site_line= sites_file.readline()
        if current_site_line == "":
            current_site = None
            break
        current_site= json.loads(current_site_line)

        if current_site.has_key(sample_ID):
            current_site[sample_ID][mark_ID]={"num_reads":0}
        else:
            current_site[sample_ID]={mark_ID:{"num_reads":0}}
        if current_site["read_dir"] == 1:
            win_start=current_site["location"]-upstream_window
            win_end=current_site["location"]+downstream_window
        else:
            win_start=current_site["location"]-downstream_window
            win_end=current_site["location"]+upstream_window
        site_chrom = chromosomes[current_site["chrom"]]
        site_start=(site_chrom,win_start)
        site_end = (site_chrom,win_end)
        
    #when there are no more sites to go check, break
    if current_site == None:
        break
    
    # at this point, the downstream end of the current window is past
    # the current read  

    # if the read is above the upstream end
    if read_pos >= site_start:
        current_site[sample_ID][mark_ID]["num_reads"]+=1
f.close()
sites_file.close()

