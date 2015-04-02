#!/bin/bash
if [ "$#" -ne 2 ];then
    echo "./extract_data.sh <working_directory> <ChIP_experiment_list>"
    exit
fi
root=http://egg2.wustl.edu/roadmap/data/byFileType/alignments/consolidated/
wd=$1
config=config-files/config.json
output_fn_base="test_files/output_"
stage=0
next_stage=$(($stage+1))
while read l; do
        data_url=$root$l
        #wget $data_url -O $wd"/"$l
        #gunzip -f $wd"/"$l
        unzipped_fn=`echo $wd"/"$l | sed "s/.gz//g"`
        sample_mark=`echo $l | sed "s/.tagAlign.gz//g"`
        echo about to run: python src/ChIP_extract.py $config $sample_mark $output_fn_base$stage $wd
        python src/ChIP_extract.py $config $sample_mark $output_fn_base$stage $wd > $output_fn_base$next_stage 
        echo "finished parsing "$l >&2
        stage=$(($stage+1))
        next_stage=$(($stage+1))
done <$2
