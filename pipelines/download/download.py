#!/usr/bin/python
"""
Downloads files using wget

File extensions must be .gz in order to use concurrently with gunzip
"""

import os, sys, csv, wget

def main(argv):

    # Parse Args
    if len(sys.argv) != 2:
        sys.stderr.write("Note: pip install wget, in order to use\n")
        sys.stderr.write("Usage: python " + sys.argv[0] + " <filelist>\n")
        exit(2)

    # Arguments
    files = sys.argv[1]
    url = "http://egg2.wustl.edu/roadmap/data/byFileType/alignments/consolidated/"
    dest_path = "../../chip/"

    # Load list of files
    filelist = []
    f = open(files, 'rb')
    for line in f:
        filelist.append(line.strip())

    # Begin downloading files
    count = 0
    for file in filelist:    
        count += 1
        if os.path.isfile(dest_path + file):
	    sys.stderr.write("File " + str(count) + " of " + str(len(filelist)) + " already exists.\n")
        elif os.path.isfile((dest_path+file)[:-3]):
            sys.stderr.write("File " + str(count) + " of " + str(len(filelist)) + " already exists.\n")
	else:
            # Only download file if it doesn't already exist
	    wget.download(url+file, dest_path)
            sys.stderr.write("Finished downloading file " + str(count) + " of " + str(len(filelist)) + "\n")
    f.close()
    sys.stderr.write("All done!\n")

# Execute this module as a command line script
if __name__ == "__main__":
    main(sys.argv[1:])
