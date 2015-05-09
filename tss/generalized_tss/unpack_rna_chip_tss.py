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
    if len(sys.argv) is not 2:
        sys.stderr.write("invalid usage: python " + sys.argv[0] + " <level1_tss_rna_chip.json>\n")
        sys.exit(2)

    # Set args
    data_fn = sys.argv[1]
    progress = FileProgress(data_fn, "Percent Complete: ")

    # Main loop
    with open(data_fn) as json_file:
        for line in json_file:
            site = json.loads(line)

            # Filter for criteria
            analyze_this_site = False

            """
            for transcript in site['transcripts']:
                if 'tag' in transcript['attribute']:
                    if transcript['attribute']['tag'] == "CCDS":
                        analyze_this_site = True
            """


            if site['exon_number'] != 1:
                analyze_this_site = True


            # This is the main printing section
            if analyze_this_site:
                print json.dumps(site['samples'])
            progress.update()

    sys.stderr.write("\nAll done!\n")

# Execute this module as a command line script
if __name__ == "__main__":
    main(sys.argv[1:])





