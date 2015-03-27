"""
This module contains utility classes and functions necessary
for our project.
"""

import sys, csv, logging, subprocess
logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)

class FileProgress(object):
    """Utility class to count lines and print the progress through
    a file
    
    """
    def __init__(self, total=None, interval=100):
        self.line = 0
        self.total = total
        self.interval = interval
        self.prevPercent = None

    def incr(self):
        if self.total == None:
            # Count lines
            if self.line % self.interval == 0: 
                sys.stderr.write('\rLines Filtered: %d' %self.line)
                sys.stderr.flush()
        else:
            # Count percentage
            percent = int(float(self.line) / float(self.total) * 100)
            if self.prevPercent != percent:
                sys.stderr.write('\rCurrent Progress: %d%%' %percent)
                sys.stderr.flush()
        self.line += 1
 
    @staticmethod
    def file_len(fname):
        p = subprocess.Popen(['wc', '-l', fname], stdout=subprocess.PIPE, 
                             stderr=subprocess.PIPE)
        result, err = p.communicate()
        if p.returncode != 0:
            raise IOError(err)
        return int(result.strip().split()[0])

class GTF(object):
    """
    This class is the python representation of each record in
    a GTF file. 

    Please see http://mblab.wustl.edu/GTF22.html for
    specifications on the GTF2.2 file format. The attributes 
    parameter is to be stored as a python dictionary.
    """

    def __init__(self, list):
        """Constructor for the GTF class."""
        logging.debug('init GTF(list=%d): [%s]', 
                     len(list), ', '.join(list))
        self.seqname = list[0]
        self.source = list[1]
        self.feature = list[2]
        self.start = int(list[3])
        self.end = int(list[4])
        if list[5] == '.': 
            self.score = None
        else: 
            self.score = list[5]
        self.strand = list[6]
        if list[7] == '.':
            self.frame = None
        else:
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
        """returns string representation of a GTF"""
        print self.attribute['transcript_id']

    @classmethod
    def filterFeatures(cls, infile, featurelist):
        """returns a GTF file filtered for a list of features

        GTF files are large and they take a long time to process. To
        reduce the overall time to process GTF files, it will be
        economical to filter GTF files for only the features we are 
        interested in (ie: transcript, exon).
        """
        pass

    @classmethod
    def importTSS(cls, filename):
        """returns a list of GTF that contain TSS start sites

        Usage: GTF.importTSS(<filename>)
        """
        list = []
        try:
            logger.info('importTSS:Opening GTF file...')
            f = open(filename, 'rb')
            logger.info('importTSS:CSV reader starting...')
            csvfile = csv.reader(f, delimiter='\t')
            for row in csvfile:
                gtf = cls(row)
                logger.info('gtf.feature: %s-%s', gtf.feature, gtf.attribute['transcript_id'])
                if gtf.feature == 'transcript':
                    list.append(gtf)
                    logger.info('Added record to list: %s', gtf.attribute['transcript_id'])
            f.close()
            logger.info('Finished importing GTF file')
            return list
        except IOError:
            print "Error opening file."

                
