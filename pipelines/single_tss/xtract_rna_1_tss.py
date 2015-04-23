#!/usr/bin/env python

"""
This file is used for extracting RNA RPKM by gene.

The input is a gene list, and the output is the gene RPKM.
"""

__author__ = 'jeffrey'

import sys, tempfile, subprocess, json

# parse args
if len(sys.argv) is not 3:
    sys.stderr.write("invalid usage: python xtract_rna_1_tss.py " +
            " <single_tss.json> <57epigenomes.RPKM.all>\n")
    sys.exit(2)

tss_fn = sys.argv[1]
rna_fn = sys.argv[2]

# Sort JSON file by gene id (column 4 is the gene ID)
tss_temp = tempfile.NamedTemporaryFile()
tss_f = open(tss_temp.name, 'r+b')
sys.stderr.write('Sorting TSS file based on ensembl gene ID.\n')
subprocess.call("sort -k4,4 " + tss_fn, shell=True, stdout=tss_f)
tss_f.seek(0)

# Sort RPKM file by gene id (column 1 is gene ID, note that first line is header)
rna_temp = tempfile.NamedTemporaryFile()
rna_f = open(rna_temp.name, 'r+b')
sys.stderr.write('Sorting Gene RPKM file based on ensembl gene ID.\n')
subprocess.call("(head -n 1 " + rna_fn + " && tail -n +2 " + rna_fn + " | sort -k1,1)",
                shell=True, stdout=rna_f)
rna_f.seek(0)

# For each match, generate a json_file for all the TSS+RNA+Sample data
tss_lines = tss_f.readlines()
rna_lines = rna_f.readlines()
samples = rna_lines[0].strip().split('\t')
i = 0
j = 1
while i < len(tss_lines) and j < len(rna_lines):
    tss_site = json.loads(tss_lines[i])
    print tss_site
    i += 1
