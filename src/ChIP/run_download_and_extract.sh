#!/bin/bash

if [ "$#" -eq 6 ];then

    wd=$1
    out_dir=$2
    ChIP_expr_list=$3
    sites_fn=$4
    num_batches=$5
    config=$6

    total_lines=`wc -l<$ChIP_expr_list`
    part_len=`expr $total_lines / $num_batches`
    part_len=`expr $part_len + 1` #round up so no experiments are missed
    ChIP_part_prefix=$wd"/"ChIP_File_
    split -l $part_len $ChIP_expr_list $ChIP_part_prefix
    ChIP_parts=`ls $ChIP_part_prefix*`

    for part in $ChIP_parts; do

        echo "command: ./src/ChIP/download_and_extract_read_counts.sh $wd $out_dir $part $sites_fn $config"
            ./src/ChIP/download_and_extract_read_counts.sh $wd $out_dir $part $sites_fn $config > $part"_log" 2>&1 &

    done


else
    if [ "$#" -eq 7 ]; then

        wd=$1
        out_dir=$2
        ChIP_expr_list=$3
        sites_fn=$4
        num_batches=$6
        config=$5

        total_lines=`wc -l<$ChIP_expr_list`
        part_len=`expr $total_lines / $num_batches`
        part_len=`expr $part_len + 1` #round up so no experiments are missed
        ChIP_part_prefix=$wd"/"ChIP_File_
        split -l $part_len $ChIP_expr_list $ChIP_part_prefix
        ChIP_parts=`ls $ChIP_part_prefix*`

        for part in $ChIP_parts; do

            echo "command: ./src/ChIP/download_and_extract_read_counts.sh $wd $out_dir $part $sites_fn $config 1"
            ./src/ChIP/download_and_extract_read_counts.sh $wd $out_dir $part $sites_fn $config 1 > $part"_log" 2>&1 &

        done

    else
        echo "./run_download_and_extract.sh <working_dir> <output_dir> <ChIP_experiment_list> <sites.json> <config file> <num_batches> (true-if-files-exist-already)"
        exit
    fi
fi

