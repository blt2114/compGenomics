#!/usr/bin/env python

"""
The principle to this file is to add chip read counts to all transcripts in a config file
"""

__author__ = 'jeffrey'

import sys, json, os, collections, itertools

# Global Settings
RECENT_GENE_BUFFER_LENGTH = 15000
CHIP_BUFFER_LENGTH = 2000

def child(chip_fn, rna_fn, reads_fn, window_size, bin_size):

    # load configuration file(s)
    with open(reads_fn) as experiment_read_counts_file:
        read_counts = json.load(experiment_read_counts_file)

    # Parse sample information from file name
    # The correction will be reads starts per million (RPM)
    sample = os.path.basename(chip_fn).split('-')[0]
    mark = chip_fn.split('-')[1].replace('.tagAlign','')
    correction = float(read_counts[sample][mark]) / 1000000

    # load sites of interest from json into a list
    tss_file = open(rna_fn)
    tss_site = json.loads(tss_file.readline())

    # Initialize this tss site
    window_start = tss_site['tss'] - window_size
    window_end = tss_site['tss'] + window_size
    num_bins = (window_end - window_start) / (bin_size)
    if sample in tss_site['samples']:
        if mark in tss_site['samples'][sample]:
            tss_site['samples'][sample][mark] = [0] * num_bins
        else:
            tss_site['samples'][sample] = { mark : [0] * num_bins }
    else:
        tss_site['samples'] = { sample : { mark : [0] * num_bins } }

    # Move through both the TSS and CHIP Files
    recent_genes = collections.deque()
    f = open(chip_fn, 'r')
    EOF = False
    while not EOF:

        # When there are no more TSS sites, break
        if tss_site == None: break

        # Grab a chunk of lines from the CHIP file, of specified buffer size
        lines = collections.deque(itertools.islice(f, CHIP_BUFFER_LENGTH))
        if not lines:
            EOF = True

        # Process the buffer
        while len(lines) != 0:

            # When there are no more TSS sites, break
            if tss_site == None: break

            line = lines.popleft()
            recent_genes.append(line)
            if len(recent_genes) > RECENT_GENE_BUFFER_LENGTH:
                recent_genes.pop()

            # parse out the read location
            read_seqname = line.split("\t")[0]
            read_pos = int(line.split("\t")[1])

            # If the read is before the lower boundary of the window, skip this loop
            if read_seqname != tss_site['seqname'] or read_pos < window_start:
                continue

            # If the read is within the boundaries, add one to the count and continue
            if read_pos <= window_end:
                bag = (read_pos - window_start) / bin_size
                if bag == num_bins:
                    bag -= 1
                tss_site['samples'][sample][mark][bag] += 1
                continue

            # By this point, read is upstream of the upper boundary of the window,

            # While no label available, so skip to next site.
            # Reverse the bins if the sequence on reverse strand to capture upstream/downstream
            if tss_site['strand'] == '-':
                tss_site['samples'][sample][mark].reverse()
            tss_site['samples'][sample][mark][:] = [x / correction for x in tss_site['samples'][sample][mark]]

            # Print!
            #result = tss_site['seqname'] + "\t" + str(tss_site['tss']) + "\t" + sample + "\t" + mark + "\t" + json.dumps(tss_site['samples'][sample][mark])
            print tss_site['seqname'] + "\t" + str(tss_site['tss']) + "\t" + sample + "\t" + mark + "\t" + json.dumps(tss_site['samples'][sample][mark])
            #out_queue.put(result)

            # Read the next TSS site and initialize
            current_tss_line = tss_file.readline()
            if current_tss_line == "":
                tss_site = None
                continue
            tss_site = json.loads(current_tss_line)
            window_start = tss_site['tss'] - window_size
            window_end = tss_site['tss'] + window_size
            num_bins = (window_end - window_start) / (bin_size)
            if sample in tss_site['samples']:
                if mark in tss_site['samples'][sample]:
                    tss_site['samples'][sample][mark] = [0] * num_bins
                else:
                    tss_site['samples'][sample] = { mark : [0] * num_bins }
            else:
                tss_site['samples'] = { sample : { mark : [0] * num_bins } }

            # Add the recent genes onto the beginning of the lines to process
            # This allows lines to be counted towards multiple sites
            lines.extendleft(recent_genes)
            recent_genes.clear()
    f.close()
    tss_file.close()

# Main Method
def main(argv):

    # parse args
    if len(sys.argv) is not 6:
        sys.stderr.write("invalid usage: python " + sys.argv[0] +
                    " <all_tss_rna.json> <chip_directory> <experiment_read_counts.json> <window_size> <bin_size>\n")
        sys.exit(2)

    rna_fn = sys.argv[1]
    chip_dir = sys.argv[2]
    reads_fn = sys.argv[3]
    window_size = int(sys.argv[4])
    bin_size = int(sys.argv[5])

    # Locate filelist
    filelist = []
    for file in os.listdir(chip_dir):
        if file.endswith(".tagAlign"):
            filelist.append(os.path.join(chip_dir, file))
    sys.stderr.write("A total of " + str(len(filelist)) + " files have been located in " + chip_dir + ".\n")

    for file in filelist:
        child(file, rna_fn, reads_fn, window_size, bin_size)

    # cleanup process
    sys.stderr.write("All done!\n")

# Execute this module as a command line script
if __name__ == "__main__":
    main(sys.argv[1:])





