#!/usr/bin/env python
"""
This file is used for extracting RNA.

Imput should be sorted files (by gene) of:
RPKM exons
RPKM genes
TSS locations

Genes with RPKM<1 will be defined as not expressed.

We will calculate the the ratio of each exon relative to
the average gene/sample RPKM.

Exons with a ratio significantly less than PARAMETER will be
defined as exons that are not expressed. Exons that exceed
this parameter will be defined as expressed.

The TSS file will be used to search for locations of interest.
"""
import sys, argparse, logging, json, copy

#aliases for logging
logging.getLogger(__name__).setLevel(logging.WARNING)
log = logging.getLogger(__name__).info
logw = logging.getLogger(__name__).warning
logd = logging.getLogger(__name__).debug

def main(argv):
    """Main method if this module is run as a command line script."""
    
    # Parse Command Line Arguments
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('-v', '--verbose',
                        action='store_true',
                        help='verbose flag')
    parser.add_argument('-t', dest='tss',
                        help='input tss filename')
    parser.add_argument('-g', dest='gene',
                        help='RPKM by gene')
    parser.add_argument('-e', dest='exon',
                        help='RPKM by exon')
    args = parser.parse_args()
    
    # Evaluated Parsed Arguments
    if args.verbose:
        logging.getLogger(__name__).setLevel(logging.INFO)
        log('Logging level set to verbose (INFO).')
    else:
        logging.getLogger(__name__).setLevel(logging.WARNING)
        log('Logging level set to quiet (WARNING).')
    if args.tss and args.gene and args.exon:
        log('Proper parameters are defined')
        get_data(args.gene, args.exon, args.tss)
    else:
        parser.print_help()

def get_data(gene, exon, tss):
    gfile = open(gene, 'rb')
    efile = open(exon, 'rb')
    tfile = open(tss, 'rb')
    log('succesfully opened files')    
    
    # Iterate until EOF
    while True:
    """
    gene = gfile.next()
    For tss in tssfile:
        while (gene < tss.gene -- lexically):
            gene.next()
        if (gene != tss.gene):
            next tss
        else:
            pass
            
            
         
    try:
        while True:
            line = file.next()
            if line == 'foo':
                pass
    except(StopIteration):
        pass
        """

class GeneData(object):
    def __init__(self, string, heading):        
        list = string.strip().split('\t')
        self.gene = list[0]
        dict = {}
        for i in range(1, len(list), 1):
            dict[heading[i]] = list[i]
        self.samples = dict

class ExonData(object):
    def __init__(self, string, heading):
        list = string.strip().split('\t')
        locs = list[0].replace('<',':').replace('-',':',1).split(':')
        self.chrom = locs[0]
        self.start = locs[1]
        self.end = locs[2]
        self.strand = locs[3]
        self.gene = list[1]
        dict = {}
        for i in range(2, len(list), 1):
            dict[heading[i]] = list[i]
        self.samples = dict  

    def in_range(self, chrom, num, buf):
        if chrom == self.chrom:
            if num > (self.start-buf) and num < (self.end-buf):
                return True
        return False

class TSSData(object):
    def __init__(self, string):
        pass
        

# Execute this module as a command line script
if __name__ == "__main__":
    main(sys.argv[1:])
