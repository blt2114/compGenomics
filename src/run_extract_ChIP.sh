#!/bin/bash
if [ "$#" -ne 4 ];then
    echo "./run_extract_ChIP.sh <working_directory> <ChIP_experiment_list> <sites.json> <num_batches>"
    exit
fi

wd=$1
num_batches=$4

total_lines=`wc -l<$2`

part_len=`expr $total_lines / $num_batches`
part_len=`expr $part_len + 1` #round up so no experiments are missed 

ChIP_part_prefix=$wd"/"ChIP_File_

echo split -l $part_len $1 $ChIP_part_prefix
split -l $part_len $2 $ChIP_part_prefix

ChIP_parts=`ls $ChIP_part_prefix*` 

for part in $ChIP_parts; do
    ./src/extract_ChIP.sh $wd $part $3 2>&1 > $part"_log" &
done
