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

    def __init__(self, list):
        """Constructor for the GTFRecord class."""
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
        attribute_list = list[8].split("; ")
        for item in attribute_list:
            key = item.split(" ")[0]
            value = item.split(" ")[1]
            self.attribute[key] = value.strip('"')

    def __str__(self):
        """returns string representation of a GTFRecord"""
        print self.attribute['transcript_id']

    @classmethod
    def importTSS(cls, filename):
        """returns a list of GTFRecords that contain TSS start sites

        Usage: GTFRecord.importTSS(<filename>)
        """
        list = []
        try:
            f = open(filename, 'rb')
            csvfile = csv.reader(f)
            for row in csvfile:
                gtf = cls(row)
                if gtf.feature == transcript:
                    list.append(gtf)
            f.close()
            return list
        except IOError:
            print "file error"

                
