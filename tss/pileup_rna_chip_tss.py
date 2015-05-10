#!/usr/bin/env python

"""
This file piles up sites.json and chip.tsv into one large json file by site. It also normalizes the
chip read count by reads per million.

In this step, both the RNA file and the ChIP file are sorted (unix sort) by position. The RNA file is
read into memory, and the chip data is progressively added into the json dictionary. To keep the memory
footprint small, each site is popped once all its data has been read.

"""

__author__ = 'jeffrey'

import sys, json, csv, collections
from src.utils import FileProgress, unix_sort

# Main Method
def main(argv):
    # parse args
    if len(sys.argv) is not 4:
        sys.stderr.write("invalid usage: python " + sys.argv[0] +
                " <nosplice_tss_rna.json> <nosplice_tss_chip.tsv> <experiment_read_counts.json>\n")
        sys.exit(2)

    rna_fn = sys.argv[1]
    chip_fn = sys.argv[2]
    reads_fn = sys.argv[3]
    progress = FileProgress(chip_fn, "Percent Complete: ")

    # Load read count normalization file
    with open(reads_fn) as experiment_read_counts_file:
        read_counts = json.load(experiment_read_counts_file)

    # Sort both files lexically by chromosome, then by position
    sys.stderr.write('Beginning to sort both files (may take a while).\n')
    rna_f = unix_sort(rna_fn, "-k2,2 -k4,4", header=False, save=True)
    chip_f = unix_sort(chip_fn, "-t $'\t' -k1,2", header=False, save=True)
    sys.stderr.write('Finished sorting.\n')

    # Read RNA-seq data into memory
    sys.stderr.write('Reading the RNA-seq data into memory.\n')
    dict = {}
    for line in rna_f:
        site = json.loads(line, object_pairs_hook=collections.OrderedDict)
        seqname = site['seqname']
        tss = site['location']

        if seqname in dict:
            if tss in dict[seqname]:
                print "Error!"
            else:
                dict[seqname][str(tss)] = site
        else:
            dict[seqname] = { str(tss) : site }
    rna_f.close()

    # Begin looping through chip file
    sys.stderr.write('Beginning to read the ChIP data.\n')
    previous_seqname = None
    previous_tss = None
    for line in chip_f:
        chip_row = line.strip("\n").split("\t")
        if len(chip_row) != 5:
            continue
        seqname, tss, sample, mark, rpm = (chip_row[0], chip_row[1], chip_row[2], chip_row[3], eval(chip_row[4]))

        if previous_tss is None:
            previous_seqname = seqname
            previous_tss = tss
            progress.update()
            continue

        if previous_seqname != seqname or previous_tss != tss:
            print json.dumps(dict[previous_seqname][previous_tss])
            dict[previous_seqname].pop(previous_tss, None)

        tss_site = dict[seqname][tss]
        correction = float(read_counts[sample][mark]) / 1000000

        if sample in tss_site['samples']:
            tss_site['samples'][sample][mark] = [x / correction for x in rpm]
        else:
            tss_site['samples'][sample] = { mark : [x / correction for x in rpm] }

        previous_seqname = seqname
        previous_tss = tss
        progress.update()
    print json.dumps(dict[previous_seqname][previous_tss])

    chip_f.close()
    sys.stderr.write("\nAll done!\n")

# Execute this module as a command line script
if __name__ == "__main__":
    main(sys.argv[1:])





