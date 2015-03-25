#!/usr/bin/env python

"""
This module is a python script that takes a gtf file and outputs a list
of TSS start sites to std.out.

Usage: python gtf2tss.py <gtf_filename> > <output_file>
"""

from utils import GTF

# Pseudocode

# 1: Read GTF file
# 2: Filter only records that have feature=transcript
# 3: Add attribute called "TSS" based on start/end/strand attribute
# 4: OPTION: Remove genes with only one transcript
# 5: Unix sort filtered list
# 6: Merge transcripts that have the same TSS
# 7: Output to std.out

list = GTF.importTSS('../files/gen10.long.gtf')
print str(list[0])
