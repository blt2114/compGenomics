#!/usr/bin/env python

"""
This file piles up level1_tss.json and level1_tss_chip.tsv into one large json file by site.

"""

__author__ = 'jeffrey'

import sys, json, csv, collections
from src.utils import FileProgress, unix_sort

# Main Method
def main(argv):
    # parse args
    if len(sys.argv) is not 3:
        sys.stderr.write("invalid usage: python " + sys.argv[0] +
                " <level1_tss_rna.json> <level1_tss_chip.tsv>\n")
        sys.exit(2)

    rna_fn = sys.argv[1]
    chip_fn = sys.argv[2]

    progress = FileProgress(chip_fn, "Percent Complete: ")

    # Sort both files lexically by chromosome, then by position
    sys.stderr.write('Beginning to sort both files (may take a while).\n')
    rna_f = unix_sort(rna_fn, "-k2,2 -k4,4", header=False, save=True)
    chip_f = unix_sort(chip_fn, "-t $'\t' -k1,2", header=False, save=True)
    sys.stderr.write('Finished sorting.\n')

    # Initialize relevant variables necessary for the loop (RNA FILE, outer loop)
    rna_line = rna_f.readline()
    tss_site = json.loads(rna_line)
    chip_line = chip_f.readline()
    chip_row = chip_line.split("\t")
    seqname, pos, sample, mark, rpm = (chip_row[0], chip_row[1], chip_row[2], chip_row[3], eval(chip_row[4]))

    # Begin reading through both files in alternation
    while True:

        # If this position has not reached the tss site, increment the position
        if seqname < tss_site['seqname'] or int(pos) < tss_site['tss']:
            chip_line = chip_f.readline()
            if not chip_line:
                print json.dumps(tss_site)
                count = 0
                while True:
                    count += 1
                    if not chip_f.readline(): break
                print "chip left: " + count
                break
            chip_row = chip_line.split("\t")
            seqname, pos, sample, mark, rpm = (chip_row[0], chip_row[1], chip_row[2], chip_row[3], eval(chip_row[4]))
            progress.update()
            continue

        # If this position has passed the tss site, increment the tss site
        if seqname > tss_site['seqname'] or int(pos) > tss_site['tss']:

            print json.dumps(tss_site)

            rna_line = rna_f.readline()
            if not rna_line:
                count = 0
                while True:
                    count += 1
                    if not chip_f.readline(): break
                print "chip left: " + count
                break
            tss_site = json.loads(rna_line)

            continue

        # At this point, both the tss site and the chip position are equal
        # We can do the main evaluating and processing
        if sample in tss_site['samples']:
            tss_site['samples'][sample][mark] = rpm
        else:
            tss_site['samples'][sample] = { mark : rpm }

        # Increment to the next chip position in the loop
        chip_line = chip_f.readline()
        if not chip_line:
            print json.dumps(tss_site)
            count = 0
            while True:
                count += 1
                if not rna_f.readline(): break
            print "rna left: " + count
            break
        chip_row = chip_line.split("\t")
        seqname, pos, sample, mark, rpm = (chip_row[0], chip_row[1], chip_row[2], chip_row[3], eval(chip_row[4]))
        progress.update()

    rna_f.close()
    chip_f.close()

    sys.stderr.write("\nAll done!\n")

# Execute this module as a command line script
if __name__ == "__main__":
    main(sys.argv[1:])





