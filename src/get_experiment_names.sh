#!/bin/bash
#this script gets the experiment filenames present in the consolidated dataset
#       -which are from samples that are in the sample_ids list
#       - and which are of the assay types provided
if [ "$#" -ne 2 ];then
    echo "./get_experiment_names.sh <assay_types_filename> <sample_ids_filename>"
    exit
fi
wget  http://egg2.wustl.edu/roadmap/data/byFileType/alignments/consolidated/ -O raw_data_filenames.html
cat raw_data_filenames.html |  grep -v tbi | sed 's/.*href="//g' | sed 's/">.*//g' | grep tagAlign >tmp_results_all_marks_and_samples
rm temp_results_some_marks
while read l; do
    cat tmp_results_all_marks_and_samples | grep $l >> temp_results_some_marks
done < $1
rm tmp_results_all_marks_and_samples

while read l; do
    cat temp_results_some_marks | grep $l  
done < $2
rm temp_results_some_marks
