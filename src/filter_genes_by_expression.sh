#!/bin/bash

#this will filter out genes for which more than a given number have less than a given order of magnitude of expression

if [ "$#" -ne 5 ];then
    echo "./filter_genes_by_expression.sh <gene_RPKM_raw> <order of magnitude> <most_significant_digit> <number of genes that must meet it> <output_loc>"
    exit
fi

raw_gene_RPKMs=$1
order_of_magnitude=$2
MSD=$3
num_repeats=$4
output_fn=$5

repeated_pat=""
small_RPKM_pat="\t[0-9]{0,$order_of_magnitude}\..*"
#small_RPKM_pat="\t[0-$MSD][0-9]{0,$order_of_magnitude}\..*"
for i in $(seq 1 $num_repeats); do 
    echo pat: $repeated_pat
    repeated_pat=$repeated_pat$small_RPKM_pat
done

cmd="grep -v -E "\""$repeated_pat"\""" 
echo cmd: $cmd

