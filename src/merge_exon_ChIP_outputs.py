#!/usr/bin/env python
'''
This is also very similar to its TSS counterpart
'''

import json
import sys


if len(sys.argv) != 3:
    sys.stderr.write("invalid usage: python merge_exon_outputs_ChIP.py  <dir> <files_to_merge.txt>\n")
    sys.exit(2)

wd = sys.argv[1]
filenames_fn = sys.argv[2]

# load config info from json into a dictionary
with open(filenames_fn) as filenames_file:
    filenames= filenames_file.readlines()
filenames_file.close()

for i in range(0,len(filenames)):
    filenames[i]=filenames[i].strip('\n')

files=[]
for name in filenames:
    files.append(open(wd+"/"+name))

for l in files[0]:
    site_dict=json.loads(l)
    for f in files[1:]:
        l_f =f.next()
        new_site_dict = json.loads(l_f)
        if site_dict["exon_location"] != new_site_dict["exon_location"]:
            sys.stderr.write("FUCK! the locations of the genes are not lined"
                    +"up\n\n\n") 
            continue
        for key in new_site_dict.keys():
            if not type(new_site_dict[key])==dict:
                continue
            if site_dict.has_key(key):
                for s_key in new_site_dict[key].keys():
                    if not site_dict[key].has_key(s_key):
                        site_dict[key][s_key]=new_site_dict[key][s_key]
                    elif site_dict[key][s_key] != new_site_dict[key][s_key]:
                        sys.stderr.write("key: "+key+"-"+s_key+" defined"+
                               " differently in  multiple files")
            else:
                site_dict[key]=new_site_dict[key]
    print json.dumps(site_dict)

for name in files:
    name.close()
