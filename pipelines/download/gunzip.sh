#!/bin/bash

# Set absolute path to directory containing gzips
DIRECTORY=/Users/jeffrey/src/python/compGenomics/chip/*.gz

for f in $DIRECTORY
do
    gunzip -f $f
    rm -f $f
done