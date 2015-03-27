#!/usr/bin/env python

"""
This module contains all scripts and classes relevant to GTF files. 

This script is capable of reading GTF files from stdin as well as from
files. Please be sure to select the correct arguments. By default, the
script assumes all input comes from stdin and goes out on stdout. It is
recommended to use UNIX commands such as cat, tee, and pipes to take
advantage of this script in its entirety. 

"""

import sys, argparse, logging, csv
from utils import file_len

#aliases for logging
logging.getLogger(__name__).setLevel(logging.WARNING)
log = logging.getLogger(__name__).info
logw = logging.getLogger(__name__).warning
logd = logging.getLogger(__name__).debug

def main(argv):
    """Main method if this module is run as a command line script.
    
    :param argv: Command line arguments.
    :type arv: list.
    :returns: None. Output printed to stdout.
    :raises: n/a.
    """
    
    # Parse Command Line Arguments
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('-v', '--verbose',
                        action='store_true',
                        help='verbose flag')
    parser.add_argument('-i', dest='infile',
                        help='input filename (default: stdin)')
    parser.add_argument('-o', dest='outfile',
                        help='output filename (default: stdout)')
    parser.add_argument('-f', dest='filter',
                        help='filter GTF. Ex: [-f feature=exon] or ' 
                        '[-f seqname=chr1]')
    args = parser.parse_args()
    
    # Evaluated Parsed Arguments
    if args.verbose:
        logging.getLogger(__name__).setLevel(logging.INFO)
        log('Logging level set to verbose (INFO).')
    else:
        logging.getLogger(__name__).setLevel(logging.WARNING)
        log('Logging level set to quiet (WARNING).')
    if args.filter:
        log('Filter is defined: %s', args.filter)
        criteria = args.filter.split('=')
        if len(criteria) != 2: 
            parser.error('\n\tImproper parameter provided for filter.' +
                         '\n\tCorrect usage: "-f feature=exon"')
        try:
            GTF.filter(criteria[0], criteria[1], args.infile, args.outfile)
        except AttributeError, e:
            logw(e)
            parser.error('\n\tImproper parameter provided for filter.' +
                         '\n\tCorrect usage: "-f feature=exon"')
    else:
        log('Filter is not defined')
        parser.print_help()

class GTF(object):
    """This class is the python representaiton of each record in a GTF file.
    
    Please see http://mblab.wustl.edu/GTF22.html for specifications on 
    the GTF2.2 file format. The attributes parameter is to be stored as 
    a python dictionary.
    """
    def __init__(self, list):
        """Constructor for the GTF class.

        :param: list: The str list representation of GTF. Must be 9 
                      elements long.
        :type list:   list.
        :returns:     GTF -- GTF object.
        :raises:      AttributeError, KeyError

        """
        if len(list) != 9:
            logw('GTF initialized with list n=%d!', len(list))
        self.seqname = list[0]
        self.source = list[1]
        self.feature = list[2]
        self.start = int(list[3])
        self.end = int(list[4])
        self.score = list[5]
        self.strand = list[6]
        self.frame = list[7]

        # Converts str attribute => dictionary
        self.attribute = {}
        attribute_list = list[8].split(";")
        for item in attribute_list:
            attribute = item.strip(' ')
            if len(attribute) > 0:
                key = attribute.split(" ")[0]
                value = attribute.split(" ")[1]
                self.attribute[key] = value.strip('"')

    def __str__(self):
        """Returns a string representation of GTF

        :returns: str -- String representation of GTF.
        :raises: AttributeError, KeyError

        """
        pass

    def __repr__(self):
        """Returns a str representation of GTF that can eval()

        :returns: str -- String representation of GTF that can eval().
        :raises: AttributeError, KeyError

        """
        dict = ['gene_id "' + self.attribute['gene_id'] + '"',
                'transcript_id "' + self.attribute['transcript_id'] + '"',
                ]
        copy = self.attribute.copy()
        del copy['gene_id']
        del copy['transcript_id']
        for key, value in copy.iteritems():
            dict.append(key + ' "' + value + '"')
        list = [
            self.seqname,
            self.source,
            self.feature,
            str(self.start),
            str(self.end),
            self.score,
            self.strand,
            self.frame,
            "; ".join(dict),
            ]
        return "GTF(" + repr(list) + ")"

    @classmethod
    def filter(cls, field, value, infile=None, outfile=None): 
        """Filters a GTF file based on a column in the data.
    
        :param field: Str field to examine.
        :type field: str.
        :param value: Criteria to filter column on.
        :type column: str.
        """
        # Setting output file (default to stdout)
        log('Opening GTF output file: %s', outfile or 'stdout')
        fo = sys.stdout
        if outfile != None:
            fo = open(outfile, 'wb')
        
        # Perform different loop depending on input file
        log('Opening GTF input file: %s', infile or 'stdin')
        fi = sys.stdin
        count = 0
        if infile != None:
            # Infile was provided
            try:
                fi = open(infile, 'rb')
            except IOError as e:
                sys.stderr.write('Cannot open file %s' %infile)
            log('Estimating time to compute...')
            flen = file_len(infile)
            log('CSV reader starting...')
            csvfile = csv.reader(fi, delimiter='\t')
            log('Beginning import')
            count = 0
            prev = None
            for row in csvfile:
                percent = int(float(count) / float(flen) * 100)
                if len(row) == 9:
                    gtf = GTF(row)
                    if prev != percent:
                        sys.stderr.write("\rPercent Complete: %d%%" 
                                         %percent)
                        sys.stderr.flush()
                    if eval('gtf.' + field) == value:
                        fo.write('\t'.join(row) + '\n')
                count += 1
                prev = percent
            fi.close()
        else:
            count = 0
            interval = 100
            for line in sys.stdin:
                gtf = GTF(line.strip('\n').split('\t'))
                if eval('gtf.' + field) == value:
                    fo.write(line)
                if count % interval == 0:
                     sys.stderr.write("\rLines Read: %d" %count)
                     sys.stderr.flush()
                count += 1
            fi.close()
        fo.close()
        log('\nFinished filtering file')

# Execute this module as a command line script
if __name__ == "__main__":
    main(sys.argv[1:])
