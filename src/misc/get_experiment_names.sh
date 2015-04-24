#!/bin/bash
#this script gets the experiment filenames present in the consolidated dataset
#       -which are from samples that are in the sample_ids list
#       - and which are of the assay types provided
if [ "$#" -ne 2 ];then
    echo "./get_experiment_names.sh <assay_types_filename> <sample_ids_filename>"
    exit
fi
file_exists=`ls raw_data_filenames.html | wc -l`
if [ "$file_exists" -ne 1 ]; then
        wget  http://egg2.wustl.edu/roadmap/data/byFileType/alignments/consolidated/ -O raw_data_filenames.html
fi
cat raw_data_filenames.html |  grep -v tbi | sed 's/.*href="//g' | sed 's/">.*//g' | grep tagAlign >tmp_results_all_marks_and_samples
cat /dev/null > temp_results_some_marks
while read l; do
    cat tmp_results_all_marks_and_samples | grep $l | grep -v Control >> temp_results_some_marks
done < $1
rm tmp_results_all_marks_and_samples

cat /dev/null > temp_results_not_complete
while read l; do
    cat temp_results_some_marks | grep $l >>temp_results_not_complete 
done < $2
rm temp_results_some_marks

num_marks=`wc -l < $1`
while read l; do
    cat temp_results_not_complete | grep $l > tmp_file_asdf
    num_marks_for_sample=`wc -l <tmp_file_asdf`
    if [ "$num_marks" -eq "$num_marks_for_sample" ];then
       cat tmp_file_asdf 
    fi 
done < $2
rm temp_results_not_complete
rm tmp_file_asdf
