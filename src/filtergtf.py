#!/usr/bin/env python

"""
Command line python script to filter gtf files.

Usage:
python filtergtf.py -f <inputfile> -o <outputfile> {filter criteria}
"""

import sys, argparse

def main(argv):
    """Main method for filtergtf.py script."""

    # Prepare and parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("inputfile", 
                        help="Path to GTF file to filter.")
    parser.add_argument("-o", "--outputfile", 
                        help="Path to output GTF file.")
    parser.add_argument("criteria", nargs='+',
                        help="Criteria to filter GTF for.")
    args = parser.parse_args()
    
    if args.outputfile:
        # Print to a file
        print "outputfile is defined"

    else:
        # print to std.out
        


if __name__ == "__main__":
    main(sys.argv[1:])
