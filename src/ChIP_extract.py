#!/usr/bin/env python
"""
This main looks through raw tagAlign chip-seq files and finds the number of
reads upstream/downstream of locations provided in JSON file.

The sites of interest in the json file are assumeded to be in the same order
as mapped ChIP-Seq reads

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
recent_genes= collections.deque()
RECENT_GENE_BUFFER_LENGTH=2000
file_not_over=True
CHIP_BUFFER_LENGTH= 2000 #number of line to read at once
#recent_genes.append(list(itertools.islice(f,CHIP_BUFFER_LENGTH)))

while file_not_over:
    #when there are no more sites to go check, break
    if current_site == None:
        break

    lines=collections.deque(itertools.islice(f,CHIP_BUFFER_LENGTH)) 
    if not lines:
        file_not_over=False 
        

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
        '''
        if read_pos[1] >540520 and read_pos[1] < 540820:
            print "current site: "+json.dumps(current_site)
            print "current site_start: "+str(site_start)
            print "current site_end: "+str(site_end)
            print "current read loc: "+str(read_pos) 
        '''
        #print "read pos" + str(read_pos)
        #print "site start" + str(site_start)
        # if the read is before the lower boundary of the window,
        # continue
        if read_pos < site_start:
            continue

        # if the read is within the boundaries, add one to the count and
        # continue
        if read_pos <= site_end:
            current_site[sample_ID][mark_ID]["num_reads"]+=1
            continue
        print "moving to next site"
        '''
        print "current site: "+json.dumps(current_site)
        print "current site_start: "+str(site_start)
        print "current site_end: "+str(site_end)
        print "current read loc: "+str(read_pos) 
        '''
        # by this point, read is upstream of the upper boundary of the window, 
        
        # print the site(which has now been passed) with the additional information to stdout 
        print json.dumps(current_site)

        current_site_line= sites_file.readline()
        if current_site_line == "":
            current_site = None
            continue
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

        #calculate new site information 
        site_chrom = chromosomes[current_site["chrom"]]
        site_start=(site_chrom,win_start)
        site_end = (site_chrom,win_end)
        
        #add the recent genes onto the beginning of the lines to process
        #this allows lines to be counted towards multiple sites
        #print "extending lines now\n\tlen deque:"+str(len(recent_genes))+"\n\tlen before: "+str(len(lines))
        lines.extendleft(recent_genes)
        #print "\tlen after: "+str(len(lines))
        recent_genes.clear()
        line=None
            
f.close()
sites_file.close()

