#!/usr/bin/env python

"""
This file gets all TSS sites and preserves all the information from the annotations.

Usage:
python filter_all_tss.py ../../files/genes.json > all_tss.json

"""

__author__ = 'jeffrey'

import sys, json

# Main Method
def main(argv):
    if len(sys.argv) is not 2:
        sys.stderr.write("invalid usage: python filter_all_tss.py"+
                " <genes.json>\n")
        sys.exit(2)

    # Initialize Variables
    genes_fn = sys.argv[1]

    # Load GTF file in json format
    with open(genes_fn) as json_file:
        for line in json_file:
            gene = json.loads(line)
            for transcript in gene['transcripts'].itervalues():
                transcript.pop("exons", None)
                if (transcript['strand'] == "+"):
                    transcript['tss'] = transcript['start']
                else:
                    transcript['tss'] = transcript['end']
                transcript['length'] = int(transcript['end']) - int(transcript['start'])
            print json.dumps(gene)
    json_file.close()

# Execute this module as a command line script
if __name__ == "__main__":
    main(sys.argv[1:])

