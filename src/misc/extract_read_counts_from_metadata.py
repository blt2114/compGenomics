

import json

meta_data_file = open("files/metadata_p2.tsv")

reads_dict={}
throw_away=meta_data_file.readline()
for line in meta_data_file:
    parsed=line.split("\t")
    sample_id= parsed[1]
    if reads_dict.has_key(sample_id):
        reads_dict[sample_id][parsed[0]]=parsed[7]
    else:
        reads_dict[sample_id]={parsed[0]:parsed[7]}
print json.dumps(reads_dict)
