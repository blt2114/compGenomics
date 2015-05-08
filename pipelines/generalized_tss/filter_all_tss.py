#!/usr/bin/env python

"""
This file fetches all TSS sites from a JSON GTF file and extracts all information relevant for downstream
processing.

It produces a JSON output file with a series of nested dictionaries. Each line is a gene dictionary. Nested
within each gene is a dictionary of transcripts, each transcript containing a list of exons and introns. The
TSS is calculated for each transcript.

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

                exon_list = []
                for exon in transcript['exons']:
                    exon_list.append( (exon['start'], exon['end']) )

                transcript.pop("exons", None)
                transcript['exons'] = exon_list

                if (transcript['strand'] == "+"):
                    transcript['tss'] = transcript['start']
                    transcript['exons'].sort(key=lambda tup: tup[0])
                else:
                    transcript['tss'] = transcript['end']
                    transcript['exons'].sort(key=lambda tup: tup[1], reverse=True)
                transcript['length'] = int(transcript['end']) - int(transcript['start'])

                # Generate a list of introns
                intron_list = []
                if (transcript['strand'] == "+"):
                    for i in range(0, len(transcript['exons']) - 1):
                        intron_start = transcript['exons'][i][1] + 1
                        intron_end = transcript['exons'][i + 1][0] - 1
                        intron_list.append( (intron_start, intron_end) )
                else:
                    for i in range(0, len(transcript['exons']) - 1):
                        intron_start = transcript['exons'][i][0] - 1
                        intron_end = transcript['exons'][i + 1][1] + 1
                        intron_list.append( (intron_start, intron_end) )
                transcript['introns'] = intron_list

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