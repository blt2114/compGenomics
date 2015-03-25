"""
This module contains utility classes and functions necessary
for our project.
"""

import csv

class GTFRecord(object):
    """
    This class is the python representation of each record in
    a GTF file. 

    Please see http://mblab.wustl.edu/GTF22.html for
    specifications on the GTF2.2 file format. The attributes 
    parameter is to be stored as a python dictionary.
    """

    def __init__(self, seqname, source, feature, start, end, 
                 score, strand, frame, attribute):
        """Constructor for the GTFRecord class."""
        self.seqname = seqname
        self.source = source
        self.feature = feature
        self.start = int(start)
        self.end = int(end)
        self.score = score
        self.strand = strand
        self.frame = frame

        # Converts str attribute => dictionary
        self.attribute = {}
        list = attribute.split("; ")
        for item in list:
            key = item.split(" ")[0]
            value = item.split(" ")[1]
            self.attribute[key] = value.strip('"')

    def __str__(self):
        """returns string representation of a GTFRecord"""
        pass

    @classmethod
    def importFile(cls, filename, function):
        """returns a list of GTFRecords that satisfy the function

        Since GTFs are very large files to hold in memory and we
        only need a subset of the data, we can apply a function as
        a filter to obtain only the records we need.

        Usage: GTFRecord.importFile(<filename>, <function>)
        """
        try:
            f = open(filename, 'rb')
            csvfile = csv.reader(f)
            for row in csvfile:
                # do something
                print row[0]
            f.close()
        except IOError:
            print "file error"

                
