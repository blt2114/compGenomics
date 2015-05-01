#!/usr/bin/env python

"""
This file gets all TSS sites and preserves all the information from the annotations.

Usage:
python filter_all_tss.py ../../files/genes.json > all_tss.json

"""

__author__ = 'jeffrey'

import sys, json, collections
from src.utils import FileProgress

# Main Method
def main(argv):
    if len(sys.argv) is not 2:
        sys.stderr.write("invalid usage: python " + sys.argv[0] + " <genes.json>\n")
        sys.exit(2)

    # Initialize Variables and report progress in file
    genes_fn = sys.argv[1]
    progress = FileProgress(genes_fn, "Percent Complete: ")

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

            # Reorder the gene dictionary so it is easier to sort in the future
            d = collections.OrderedDict()
            d['gene_id'] = gene['attribute']['gene_id'].split('.')[0]
            d['seqname'] = gene['seqname']
            d['source'] = gene['source']
            d['start'] = gene['start']
            d['end'] = gene['end']
            d['strand'] = gene['strand']
            d['attribute'] = gene['attribute']
            d['transcripts'] = gene['transcripts']
            print json.dumps(d)
            progress.update()

    json_file.close()
    sys.stderr.write("\nAll Done\n")

# Execute this module as a command line script
if __name__ == "__main__":
    main(sys.argv[1:])