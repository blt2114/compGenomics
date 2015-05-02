#!/usr/bin/env python

"""
This file unpacks the rna data

"""

__author__ = 'jeffrey'

import sys, json, csv, collections
from src.utils import FileProgress, unix_sort

# Main Method
def main(argv):

    # Parse args
    if len(sys.argv) is not 5:
        sys.stderr.write("invalid usage: python " + sys.argv[0] + " <level1_tss_rna_chip.json> <left_bin> <right_bin> <bin_size>\n")
        sys.exit(2)

    # Set args
    data_fn = sys.argv[1]
    bins_left = int(sys.argv[2])
    bins_right = int(sys.argv[3])
    bin_size = int(sys.argv[4])
    progress = FileProgress(data_fn, "Percent Complete: ")

    # Main loop
    with open(data_fn) as json_file:
        for line in json_file:
            site = json.loads(line)

            # Filter for criteria
            analyze_this_site = False
            """
            for transcript in site['transcripts'].iterValues():
                if 'tag' in transcript['attribute']:
                    if transcript['tag'] == "CCDS":
                        analyze_this_site = True
            """
            if site['tss_type'] == "leading":
                analyze_this_site = True

            # Print all samples in this site
            if analyze_this_site:
                for sample in site['samples'].iterValues():
                    pass

    """
    I kind of can't really finish this without knowing exactly what the input into the SVM is
    """



    sys.stderr.write("\nAll done!\n")

# Execute this module as a command line script
if __name__ == "__main__":
    main(sys.argv[1:])





