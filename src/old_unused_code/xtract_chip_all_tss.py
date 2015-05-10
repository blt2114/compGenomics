#!/usr/bin/env python

"""
The principle to this file is to add chip read counts to all transcripts in a config file
"""

__author__ = 'jeffrey'

import sys, json, os, collections, itertools, traceback
import Queue, threading, subprocess

# Global variables
count_files = 0
total_files = 0

class ProcessThread(threading.Thread):
    def __init__(self, in_queue, out_queue):
        threading.Thread.__init__(self)
        self.in_queue = in_queue
        self.out_queue = out_queue
        self.keepRunning = True

    def run(self):
        global count_files
        global total_files
        while self.keepRunning:
            tuple = self.in_queue.get()
            try:
                self.process(tuple, self.out_queue)
            except:
                traceback.print_exc()
            count_files += 1
            sys.stderr.write("Finished processing file " +
                             str(count_files) + "/" + str(total_files) + ": " + tuple[0] + "\n")
            self.in_queue.task_done()

    def process(self, tuple, out_queue):
        path, rna_fn, reads_fn, window_size, bin_size = tuple
        output_string = child(path, rna_fn, reads_fn, window_size, bin_size, out_queue)
        return output_string

# Main Method
def main(argv):

    # parse args
    if len(sys.argv) is not 8 or len(sys.argv) is not 7:
        sys.stderr.write("invalid usage: python " + sys.argv[0] +
                    " <sites.json> <working_dir> <out_dir> <experiment_list> <config-file> <threads> <download? T/F>\n")
        sys.exit(2)

    rna_fn = sys.argv[1]
    chip_dir = sys.argv[2]
    out_fn = sys.argv[3]
    files = sys.argv[4]
    config = sys.argv[5]
    num_threads = int(sys.argv[6)

    # Locate filelist
    filelist = []
    with open(files) as f:
        for line in f:
            filelist.append()
    sys.stderr.write("A total of " + str(len(filelist)) + " files have been located in " + chip_dir + ".\n")
    global total_files
    total_files = len(filelist)

    pathqueue = Queue.Queue()
    resultqueue = Queue.Queue()
    paths = filelist

    # spawn threads to process
    threads = []
    for i in range(0, int(num_threads)):
        t = ProcessThread(pathqueue, resultqueue)
        t.setDaemon(True)
        t.start()
        threads.append(t)

    # add paths to queue
    for path in paths:
        pathqueue.put((path, rna_fn, reads_fn, window_size, bin_size))

    # wait for queue to get empty and close threads
    pathqueue.join()
    sys.stderr.write("File queue has been emptied.\n")
    resultqueue.join()
    sys.stderr.write("All results have been printed.\n")
    t.keepRunning = False
    for thread in threads:
        thread.keepRunning = False

    # cleanup process
    sys.stderr.write("All done!\n")

# Execute this module as a command line script
if __name__ == "__main__":
    main(sys.argv[1:])





