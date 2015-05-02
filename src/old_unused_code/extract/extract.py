#!/usr/bin/python

from src.old_unused_code.extract.windowed_extract_from_TagAlign import windowed_extract

#if len(sys.argv) != 5:
 #   print "Usage: python " + sys.argv[0] + "<files_dir> <output_dir> <experiment list> <sites.json>"
  #  exit(2)

#in_dir = sys.argv[1]
#out_dir = sys.argv[2]
config = "../../config-files/config.json"

windowed_extract(config, "E003-DNase", "../../files/i_files/labeled_exons_in_middle_of_genes.txt", "E003-DNase.tagAlign")
