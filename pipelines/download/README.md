This workflow downloads all the chip files and gunzips them
===========================================================

Background and Requirements
---------------------------

Enough space to hold the uncompressed TaqAlign files. I've calculated that
the uncompressed list of files (provided by Brian) of 352 files is 334GB.
And the compressed list is 58GB, for a grand total of 400GB.

I will remove the gzip files as I download them, so by the end it'll be about
350GB.

I'm using python wget (I tried experimenting a little bit with acsp, but I
couldn't find the ftp host on the data portal. I also didn't want to risk it
using the BED files I found on other data hosts).

Python wget is nice because it only outputs the file once the entire thing
has been loaded. This means I can be sure every file I have is complete.

The point of this workflow is the gunzip as you download simultaneously on
two processes. 

Programs and Commands
---------------------

###Input Files###

* files/ChIP_filenames_core_histones.txt
* files/ChIP_filenames_non_core_marks.txt

###Step 1: Produce Experiment List###

    cat files/ChIP_filenames_core_histones.txt files/ChIP_filenames_non_core_marks.txt > pipelines/download/filenames.txt

###Step 2: Start download###

    mkdir chip
    cd pipelines/download
    python download.py filelist.txt 1>> log.txt

If for some reason you think you missed a file, you can run the script
again and it will check if it exists in the ouput directory.

###Step 3: Start gunzip###

    python gunzip.sh

This program runs infinitely (waits 20 seconds if no available files) so
you will need to kill the program with ctrl+c when the download is done.
