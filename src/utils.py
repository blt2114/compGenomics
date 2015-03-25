"""
This module contains utility classes and functions necessary
for our project.
"""

import csv, logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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
            logging.info('item:%s', item)
            cleanitem = item.strip(' ')
            logging.info('cleanitem:%s', cleanitem)
            key = cleanitem.split(" ")[0]
            value = cleanitem.split(" ")[1]
            self.attribute[key] = value.strip('"')

    def __str__(self):
        """returns string representation of a GTF"""
        print self.attribute['transcript_id']

    @classmethod
    def filterFeatures(cls, infile, outfile, featurelist):
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
            logger.info('Opening GTF file...')
            f = open(filename, 'rb')
            logger.info('CSV reader starting...')
            csvfile = csv.reader(f, delimiter='\t')
            for row in csvfile:
                logger.debug('CSVreader row: %s', row)
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

                
