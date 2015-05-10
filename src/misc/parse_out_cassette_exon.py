import sys
import json

if len(sys.argv)!=2:
    sys.stderr.write("invalid usage: python parse_out_cassette_exon.py"+
    " <exons_list.txt>\n")
    sys.exit(2)

exons_fn = sys.argv[1]

exons_file = open(exons_fn)

dir_dict={"+":"1","-":"-1"}

cassettes =[]
for line in exons_file:
    cassette_exon=line.split("@")[1]
    name_pieces = cassette_exon.split(":")
    exon_name=name_pieces[0]+":"+name_pieces[1]+"-"+name_pieces[2]+"<"+dir_dict[name_pieces[3]]
    # if the exon isn't already present
    if not cassettes.count(exon_name):
        cassettes.append(exon_name)
exons_file.close()

for cassette in cassettes:
    print cassette
