#!/bin/bash
chr=""
if [ "$#" -ne 4 ];then
    if [ "$#" -ne 5 ];then
        echo "./exon_dowload_and_extract_read_counts.sh <working_dir> <output_dir> <ChIP_experiment_list> <sites.json> (<chr#>)"
        exit
    fi
    echo running on chr $5
    chr=$5
fi
root=http://egg2.wustl.edu/roadmap/data/byFileType/alignments/consolidated/
wd=$1
output_dir=$2
ChIP_experiment_list=$3
sites=$4
config=config-files/config.json
output_fn_base=$output_dir"/"$$"_" #include PID so script don't overwrite eachother's progress
stage=0
next_stage=$(($stage+1))

#copy the original sites to a new location
cp $sites $output_fn_base$stage
while read l; do
    data_url=$root$l
    echo $$ wget $data_url -O $wd"/"$l
    wget $data_url -O $wd"/"$l  > /dev/null 2>&1
    if [ $? -ne 0 ]; then
        echo wget failed, waiting 20 seconds and trying again.
        sleep 20
        wget $data_url -O $wd"/"$l  > /dev/null
    fi
    if [ $? -ne 0 ]; then
        echo wget failed again, exiting now.
        exit 1
    fi
    gunzip -f $wd"/"$l

    unzipped_fn=`echo $wd"/"$l | sed "s/.gz//g"`

    #this should be uncommented if one is intending to use this on a single 
    #chromosome

    #if [ -z $chr ]; then 
    #    unzipped_chr=$unzipped_fn"_chr"
    #    grep $chr < $unzipped_fn > $unzipped_chr
    #    mv $unzipped_chr $unzipped_fn
    #fi

    sample_mark=`echo $l | sed "s/.tagAlign.gz//g"`
    echo $$ : python src/ChIP/exon_extract_reads_from_TagAlign.py $config $sample_mark $output_fn_base$stage $wd
    python src/ChIP/exon_extract_reads_from_TagAlign.py $config $sample_mark $output_fn_base$stage $wd > $output_fn_base$next_stage 
    echo $$ ": finished parsing "$l
    stage=$(($stage+1))
    next_stage=$(($stage+1))
    rm $unzipped_fn
done <$ChIP_experiment_list

mv $output_fn_base$stage $output_fn_base"final_output" 
