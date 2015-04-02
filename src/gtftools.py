#!/usr/bin/env python
"""
This module contains all scripts and classes relevant to GTF files. 

This script is capable of reading GTF files from stdin as well as from
files. Please be sure to select the correct arguments. By default, the
script assumes all input comes from stdin and goes out on stdout. It is
recommended to use UNIX commands such as cat, tee, and pipes to take
advantage of this script in its entirety. 

"""
# HINT: type "python gtftools.py" on the command line to get started

import sys, argparse, logging, csv, json, copy
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
    :raises: AttributeError
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
    parser.add_argument('-t', dest='tss', action='store_true',
                        help='produce TSS json file from GTF file')
    parser.add_argument('-m', dest='merge', type=int,
                        help='merge multiple TSSs with same start sites')
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
    elif args.merge:
        log('Merge option is selected')
        GTF.mergeTSS(args.merge)
    elif args.tss:
        log('TSS option is selected')
        GTF.exportTSS()
    else:
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
        dict = ['gene_id "' + self.attribute['gene_id'] + '"',
                'transcript_id "' + self.attribute['transcript_id'] + '"',
                ]
        copy = self.attribute.copy()
        del copy['gene_id']
        del copy['transcript_id']
        for key, value in copy.iteritems():
            dict.append(key + ' "' + str(value) + '"')
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
        return '\t'.join(list) + '\n'

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
            dict.append(key + ' "' + str(value) + '"')
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

    @classmethod
    def mergeTSS(cls, threshold):
        """Merges GTF file records that have duplicate TSS start sites or no 
        alternative TSS"""

        log('Opening GTF input file from stdin')
        log(threshold)
        fi = sys.stdin
        fo = sys.stdout
        p_gene = None
        stack = []
        for line in sys.stdin:
            gtf = GTF(line.strip('\n').split('\t'))
            if gtf.strand == '+':
                tss = gtf.start
            else:
                tss = gtf.end
            tup = (gtf, tss)
            if p_gene is None or gtf.attribute['gene_id'] == p_gene:
                stack.append(tup)
            else:
                if len(stack) < 1: logw('Stack not supposed to be 0.')
                GTF.dump_stack(stack, threshold, fo)
                if len(stack) != 0: logw('Stack is supposed to be 0.')
                stack.append(tup)
            p_gene = gtf.attribute['gene_id']
        if len(stack) < 1: logw('Stack not supposed to be 0.')
        GTF.dump_stack(stack, threshold, fo)
        fi.close()
        fo.close()
        log('\nFinished merging GTF file')
        
    @staticmethod
    def dump_stack(stack, threshold, fo):
        if len(stack) < 2:
            while stack: stack.pop()
        else:
            stack.sort(key=lambda tup: tup[1])
            logd('\n' + str(len(stack)))
            listoflists = []
            mergelist = []
            p_tss = None
            while stack:
                item = stack.pop()
                # Find shared tss and group them
                if p_tss is None or (abs(item[1] - p_tss) <= threshold):
                    mergelist.append(item)
                else:
                    # Clear mergelist
                    if len(mergelist) < 1: logw('merglist len error')
                    templist = []
                    while mergelist:
                        templist.append(mergelist.pop())
                    listoflists.append(templist)
                    if len(mergelist) != 0: logw('mergelist not 0, len:' + str(len(mergelist)))
                    mergelist.append(item)
                p_tss = item[1]
            # Clear mergelist one last time
            listoflists.append(mergelist)
            # Now deal with list of lists
            for list in listoflists:
                if len(list) < 1: logw('list len error')
                if len(list) == 1:
                    temp = list[0][0]
                    logd(temp.attribute['gene_id'] + ' ' +
                        temp.attribute['transcript_id'] + '\t' + 
                        str(list[0][1]))
                    fo.write(str(list[0][0]))
                else:
                    # find average
                    sum = 0
                    for i in list: sum += i[1]
                    avg = sum / len(list)
                    # find transcript closest to average
                    record = None
                    closest = None
                    for i in list:
                        logd('  ' + i[0].attribute['gene_id'] + ' ' +
                            i[0].attribute['transcript_id'] + '\t' + 
                            str(i[1]))
                        if closest is None or abs(avg - i[1]) < closest:
                            closest = abs(avg - i[1])
                            record = i[0]
                    logd('>>' + record.attribute['gene_id'] + ' ' +
                            record.attribute['transcript_id'] + '\t' + 
                            str(closest))
                    fo.write(str(record))
        
    @classmethod
    def exportTSS(cls):
        """Reads GTF from stdin and outputs to stdout in json format."""
        
        log('Opening GTF input file from stdin')
        fi = sys.stdin
        fo = sys.stdout
        for line in sys.stdin:
            gtf = GTF(line.strip('\n').split('\t'))
            if gtf.feature == 'transcript':
                dict = {}
                TSS = None
                dir = None
                if gtf.strand == '+':
                    TSS = gtf.start
                    dir = 1
                elif gtf.strand == '-':
                    TSS = gtf.end
                    dir = -1
                dict['chrom'] = gtf.seqname
                dict['read_dir'] = dir
                dict['location'] = TSS
                dict['gene'] = gtf.attribute['gene_id']
                fo.write(json.dumps(dict) + '\n')
        fo.close
        fi.close
        log('\nFinished exporting TSS file')


# Execute this module as a command line script
if __name__ == "__main__":
    main(sys.argv[1:])
