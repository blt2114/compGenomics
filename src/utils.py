"""
This module contains utility classes and functions necessary
for our project.
"""

import sys, csv, logging, subprocess
logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)

def file_len(fname):
    p = subprocess.Popen(['wc', '-l', fname], stdout=subprocess.PIPE, 
                         stderr=subprocess.PIPE)
    result, err = p.communicate()
    if p.returncode != 0:
        raise IOError(err)
    return int(result.strip().split()[0])

