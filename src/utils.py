"""
This module contains utility classes and functions necessary
for our project.
"""

import sys, csv, logging, subprocess, tempfile

# Aliases for logging
logging.getLogger(__name__).setLevel(logging.WARNING)
log = logging.getLogger(__name__).info
logw = logging.getLogger(__name__).warning
logd = logging.getLogger(__name__).debug


def file_len(fname):
    p = subprocess.Popen(['wc', '-l', fname], stdout=subprocess.PIPE, 
                         stderr=subprocess.PIPE)
    result, err = p.communicate()
    if p.returncode != 0:
        raise IOError(err)
    return int(result.strip().split()[0])

# Returns a temporary file handle
def unix_sort(fname, args, header=False):
    temporary_file = tempfile.NamedTemporaryFile()
    f = open(temporary_file.name, 'r+b')
    sys.stderr.write('Sorting ' + fname + ' file based on arguments.\n')
    if header:
        subprocess.call("(head -n 1 " + fname + " && tail -n +2 " + fname + " | sort " + args + ")",
                        shell=True, stdout=f)
    else:
        subprocess.call("sort " + args + " " + fname, shell=True, stdout=f)
    f.seek(0)
    return f

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

    def count(self):
        return self.count