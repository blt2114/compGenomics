"""
This module contains utility classes and functions necessary
for our project.
"""

import sys, csv, logging, subprocess

# Aliases for logging
logging.getLogger(__name__).setLevel(logging.WARNING)
log = logging.getLogger(__name__).info
logw = logging.getLogger(__name__).warning
logd = logging.getLogger(__name__).debug

class GTF(object):
    def __init__(self, str):
        """Given a str row from a gtf file, return a GTF object"""

        list = str.strip().split('\t')
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
        """Return a str row representation of a gtf object"""

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


def file_len(fname):
    p = subprocess.Popen(['wc', '-l', fname], stdout=subprocess.PIPE, 
                         stderr=subprocess.PIPE)
    result, err = p.communicate()
    if p.returncode != 0:
        raise IOError(err)
    return int(result.strip().split()[0])

class FileProgress(object):
    def __init__(self, fname, message):
        sys.stderr.write("Estimating compute time.\n")
        self.filelen = file_len(fname)
        self.count = 0
        self.message = message
        self.previous = None

    def update(self):
        self.count += 1
        percent = int(float(self.count) / float(self.filelen) * 100)
        if self.previous != percent:
            sys.stderr.write("\r" + self.message + "%d%%" % percent)
            sys.stderr.flush()
        self.previous = percent