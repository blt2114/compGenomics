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

from pprint import pprint

if len(sys.argv) is not 2:
    sys.stderr.write("invalid usage: python find_sites.py <config.json>")
    sys.exit(2)

config_fn = sys.argv[1]

# load config info from json into a dictionary
with open(config_fn) as config_file:
    config = json.load(config_file)


upstream_window =config["upstream_window"]
downstream_window =config["downstream_window"]

# load expected chromosome order from json into a dictionary
chromosomes_fn = config["chromosome_order_fn"] 
with open(chromosomes_fn) as chromosomes_file:
    chromosomes = json.load(chromosomes_file)

sites_json_fn = config["sites_fn"]
# load sites of interest from json into a list
with open(sites_json_fn) as sites_file:
    sites_dict = json.load(sites_file)
    sites = sites_dict["sites"]

num_sites = len(sites)

current_site_idx = 0
current_site = sites[current_site_idx]
current_site["num_reads"] = 0
#iterate through lines of stdin
for line in sys.stdin:
    # parse out the read location
    values = line.split("\t")
    chromosome = values[0]
    read_loc = int(values[1])
    if chromosome == current_site["chrom"]:
        # if the read is downstream of the lower boundary of the window,
        # continue
        if current_site["location"] - upstream_window > read_loc:
            continue

        # if the read is within the boundaries, add one to the count and
        # continue
        # since this is repeated below, this first replicate is functionally
        # unnessary, however it improves the programs efficiency
        if current_site["location"] + downstream_window >= read_loc:
            current_site["num_reads"]+=1
            continue
    
        # if the read is upstream of the upper boundary of the window, 
        while chromosome == current_site["chrom"] and current_site["location"] + downstream_window < read_loc:
            # print the site with the additional information to stdout 
            pprint(current_site)
            sites[current_site_idx]=current_site

            current_site_idx+=1
            if current_site_idx is num_sites:
                current_site = None
                break
            current_site = sites[current_site_idx]
            current_site["num_reads"] = 0
        
        #when there are no more sites to go check, break
        if current_site is None:
            break
        
        # at this point, the downstream end of the current window is past
        # the current read  

        # if the read is above the upstream end
        if chromosome == current_site["chrom"] and  current_site["location"] - upstream_window <= read_loc:
            current_site["num_reads"]+=1
        continue

    if chromosomes[chromosome] < chromosomes[current_site["chrom"]]:
        continue
    
    # if the current site is on an earlier chromosome than the current read
    while chromosomes[current_site["chrom"]] < chromosomes[chromosome]: 
        # print the site with the additional information to stdout 
        pprint(current_site)
        sites[current_site_idx]=current_site

        current_site_idx+=1
        if current_site_idx is num_sites:
            current_site = None
            break
        current_site = sites[current_site_idx]
        current_site["num_reads"] = 0

    #TODO: fix so that if the first read on a chromosome is within the range
    # it is counted, currently this case is ignored.

    #when there are no more sites to go check, break
    if current_site is None:
        break
