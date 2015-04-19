#!/bin/bash

#this will filter out genes for which more than a given number have less than a given order of magnitude of expression

if [ "$#" -ne 5 ];then
    echo "./filter_genes_by_expression.sh <gene_RPKM_raw> <order of magnitude> <most_significant_digit> <number of genes that must meet it> <output_loc>"
    exit
fi

raw_gene_RPKMs=$1
order_of_magnitude=$2 # the number of digits RPKM values must excede to count as expressed
MSD=$3 #most significant digit
num_repeats=$4
output_fn=$5

# this pattern looks for values that are either $order_of_magnitude digits or 
# start with MSD and have $order_of_magnitude - 1 digits following.  This must 
# be in the line at least num_repeats times.
pattern_for_line="(\t([0-9]{0,$order_of_magnitude}|[0-$MSD][0-9]{"$((order_of_magnitude-1))"})\..*){$num_repeats}"

echo $pattern_for_line
cmd="grep -v -E ""'"$pattern_for_line"'"
echo $cmd
grep -v -E "'"$pattern_for_line"'" < $raw_gene_RPKMs > $output_fn
echo "finished filtering through genes"
