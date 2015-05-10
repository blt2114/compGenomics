#!/bin/bash

if [ "$#" -eq 5 ];then

    root=http://egg2.wustl.edu/roadmap/data/byFileType/alignments/consolidated/
    wd=$1
    output_dir=$2
    sites=$4
    config=$5
    output_fn_base=$output_dir"/"$$ #include PID so script don't overwrite eachother's progress
    output_fn=output

    #copy the original sites to a new location
    while read l; do
        data_url=$root$l
        echo $$ wget $data_url -O $wd"/"$l
        wget $data_url -O $wd"/"$l  > /dev/null 2>&1
        if [ $? -ne 0 ]; then
            echo wget failed, waiting 20 seconds and trying again.
            sleep 200
            wget $data_url -O $wd"/"$l  > /dev/null
        fi
        if [ $? -ne 0 ]; then
            echo wget failed again, exiting now.
            exit 1
        fi
        gunzip -f $wd"/"$l

        unzipped_fn=`echo $wd"/"$l | sed "s/.gz//g"`
        sample_mark=`echo $l | sed "s/.tagAlign.gz//g"`
        IFS='-' read -a array <<< "$sample_mark"

        echo $$ : src/ChIP/extract_chip $config ${array[0]} ${array[1]} $sites $unzipped_fn >> $output_fn_base$output
            src/ChIP/extract_chip $config ${array[0]} ${array[1]} $sites $unzipped_fn >> $output_fn_base$output
        echo $$ ": finished parsing "$l
        #rm $unzipped_fn
    done <$3

else
    if [ "$#" -eq 6 ]; then

        wd=$1
        output_dir=$2
        sites=$4
        config=$5
        output_fn_base=$output_dir"/"$$ #include PID so script don't overwrite eachother's progress
        output_fn=output

        while read l; do
            unzipped_fn=`echo $wd"/"$l | sed "s/.gz//g"`

            sample_mark=`echo $l | sed "s/.tagAlign.gz//g"`
            IFS='-' read -a array <<< "$sample_mark"

            echo $$ : src/ChIP/extract_chip $config ${array[0]} ${array[1]} $sites $unzipped_fn >> $output_fn_base$output
            src/ChIP/extract_chip $config ${array[0]} ${array[1]} $sites $unzipped_fn >> $output_fn_base$output
            echo $$ ": finished parsing "$l

        done <$3

    else
        echo "invalid use: ./download_and_extract_reads.sh <working_dir> <output_dir> <ChIP_experiment_list> <sites.json> <config file>"
        echo "or: ./download_and_extract_reads.sh <working_dir> <output_dir> <ChIP_experiment_list> <sites.json> <config file> <1 - if files exist already>"
        exit
    fi
fi



