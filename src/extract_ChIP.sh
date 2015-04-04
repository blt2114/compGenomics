#!/bin/bash
if [ "$#" -ne 3 ];then
    echo "./extract_data.sh <working_directory> <ChIP_experiment_list> <sites.json>"
    exit
fi
root=http://egg2.wustl.edu/roadmap/data/byFileType/alignments/consolidated/
wd=$1
config=config-files/config.json
output_fn_base=$wd"/output_"$$ #include PID so script don't overwrite eachother's progress
stage=0
next_stage=$(($stage+1))

#copy the original sites to a new location
cp $3 $output_fn_base$stage
while read l; do
        data_url=$root$l
        wget $data_url -O $wd"/"$l
        gunzip -f $wd"/"$l
        unzipped_fn=`echo $wd"/"$l | sed "s/.gz//g"`
        sample_mark=`echo $l | sed "s/.tagAlign.gz//g"`
        echo $$ : about to run: python src/ChIP_extract.py $config $sample_mark $output_fn_base$stage $wd
        python src/ChIP_extract.py $config $sample_mark $output_fn_base$stage $wd > $output_fn_base$next_stage 
        echo $$ ": finished parsing "$l >&2
        rm $output_fn_base$stage
        stage=$(($stage+1))
        next_stage=$(($stage+1))
        rm $unzipped_fn
done <$2

mv $output_fn_base$stage $output_fn_base"final_output" 
