#!/usr/bin/env python

"""
Command line python script to filter gtf files.

Usage:
python filtergtf.py > [outputfile]

TODO: Implement argparse sometime later down the line when I am not
lazy. For now, edit this file and change the variables in this script.
Everything prints to std.out.
"""

import sys, argparse, csv, logging, subprocess
from utils import GTF
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

filename = "../files/gen10.long.gtf"
feature = 'transcript'

def main(argv):
    """Main method for filtergtf.py script."""

    logger.info('Opening GTF file...')
    f = open(filename, 'rb')
    logger.info('Estimating time to compute...')
    flen = file_len(filename)
    logger.info('CSV reader starting...')
    csvfile = csv.reader(f, delimiter='\t')
    count = 0
    lastpercent = None
    for row in csvfile:
        percent = int(float(count) / float(flen) * 100)
        if len(row) == 9:
            gtf = GTF(row)
            if lastpercent != percent:
                sys.stderr.write("\rPercent Complete: %d%%" %percent)
                sys.stderr.flush()
                #logger.info('\rReading file %d percent...', percent)
            if gtf.feature == feature:
                print '\t'.join(row)
        count += 1
        lastpercent = percent
    f.close()
    logger.info('Finished importing GTF file')

def file_len(fname):
    p = subprocess.Popen(['wc', '-l', fname], stdout=subprocess.PIPE, 
                                              stderr=subprocess.PIPE)
    result, err = p.communicate()
    if p.returncode != 0:
        raise IOError(err)
    return int(result.strip().split()[0])

if __name__ == "__main__":
    main(sys.argv[1:])
