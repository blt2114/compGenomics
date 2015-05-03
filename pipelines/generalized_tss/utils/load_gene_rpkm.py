#!/usr/bin/env python

"""
The principle to this file is to add chip read counts to all transcripts in a config file
"""

__author__ = 'jeffrey'

import sys, json, collections
from src.utils import FileProgress

# Main Method
def main(argv):

    # parse args
    if len(sys.argv) is not 3:
        sys.stderr.write("invalid usage: python " + sys.argv[0] +
                    " <all_tss_rna.json> <57epigenomes.RPKM.all> \n")
        sys.exit(2)

    json_fn = sys.argv[1]
    rna_fn = sys.argv[2]
    progress1 = FileProgress(rna_fn, "Part 1/2: ")
    progress2 = FileProgress(json_fn, "Part 1/2: ")

    # Read gene RPKM into memory
    gene_dict = {}
    header = []
    with open(rna_fn) as csv_file:
        for line in csv_file:
            row = line.strip('\n').split("\t")
            if progress1.count == 0:
                header = row[1:]
            else:
                gene = row[0]
                samples = row[1:]
                gene_dict[gene] = samples
            progress1.update()
    sys.stderr.write("\nFirst part done.\n")


    # Now read through json file and append
    with open(json_fn) as json_file:
        for line in json_file:
            site = json.loads(line, object_pairs_hook=collections.OrderedDict)
            for i in range(0, len(header)):
                if header[i] in site['samples']:
                    site['samples'][header[i]]['gene_rpkm'] = gene_dict[site['gene_id']][i]
                else:
                    site['samples'][header[i]] = { 'gene_rpkm':  gene_dict[site['gene_id']][i] }
            print json.dumps(site, indent=2)
            break
            progress2.update()

    sys.stderr.write("All done!\n")

# Execute this module as a command line script
if __name__ == "__main__":
    main(sys.argv[1:])





