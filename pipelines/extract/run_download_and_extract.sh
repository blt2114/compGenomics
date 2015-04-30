#!/bin/bash
chr=""
if [ "$#" -ne 5 ];then
    if [ "$#" -ne 6 ];then
        echo "./run_download_and_extract.sh <working_dir> <output_dir> <ChIP_experiment_list> <sites.json> <num_batches> (<chr#>)"
        exit
    fi
    chr=$6
fi

wd=$1
out_dir=$2
ChIP_expr_list=$3
sites_fn=$4
num_batches=$5

total_lines=`wc -l<$ChIP_expr_list`

part_len=`expr $total_lines / $num_batches`
part_len=`expr $part_len + 1` #round up so no experiments are missed 

ChIP_part_prefix=$wd"/"ChIP_File_

split -l $part_len $ChIP_expr_list $ChIP_part_prefix

ChIP_parts=`ls $ChIP_part_prefix*` 

for part in $ChIP_parts; do
    if [ "$#" -lt 6 ];then
        ./pipelines/extract/download_and_extract_read_counts.sh $wd $out_dir $part $sites_fn > $part"_log" 2>&1 &
    fi
    if [ "$#" -ge 6 ];then
        ./pipelines/extract/download_and_extract_read_counts.sh $wd $out_dir $part $sites_fn $chr > $part"_log" 2>&1 &
    fi

done
