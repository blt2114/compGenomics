#!/bin/bash
wget  http://egg2.wustl.edu/roadmap/data/byFileType/alignments/consolidated/ -O raw_data_filenames.html
cat raw_data_filenames.html |  grep -v tbi | sed 's/.*href="//g' | sed 's/">.*//g' | grep tagAlign | grep H 
