import sys
import re
import json

if len(sys.argv) != 3:
    sys.stderr.write("invalid usage: python filter_cassette_exons.py"+
    "<cassette_exons.txt> <exons.json>\n")
    sys.exit(2)

cassettes_fn = sys.argv[1]
exons_fn = sys.argv[2]

with open(cassettes_fn) as cassettes_file:
    cassettes_lines=cassettes_file.readlines()

# this function parses exon location entry in to 3 prime and 5 prime
# locations
def parse_3p_5p(exon_location):
    location_dir = re.split("<",exon_location)
    chr_loc1_loc2= re.split(":|-|<",exon_location)
    chrom = chr_loc1_loc2[0]
    if location_dir[1] == "-1":
        three_p = chr_loc1_loc2[1]
        five_p = chr_loc1_loc2[2]
    else:
        three_p =chr_loc1_loc2[2]
        five_p =chr_loc1_loc2[1]
    return chrom,five_p,three_p,int(location_dir[1])

cassettes=[]
for i in range(0,len(cassettes_lines)):
    cassettes.append({})
    stripped = cassettes_lines[i].strip("\n")
    chrom,five_p,three_p, read_dir =parse_3p_5p(stripped)
    cassettes[i]["chrom"]=chrom
    cassettes[i]["five_p_loc"]=five_p
    cassettes[i]["three_p_loc"]=three_p
    cassettes[i]["read_dir"]=read_dir

exons_file = open(exons_fn)

for line in exons_file:
    exon = json.loads(line)
    for cassette in cassettes:
        overlap=0
        if not cassette["chrom"] == exon["chrom"]:
            continue
        if not cassette["read_dir"] == exon["read_dir"]:
            continue
        cassette_5p=int(cassette["five_p_loc"])
        cassette_3p=int(cassette["three_p_loc"])
        if cassette["read_dir"] == 1:
            start= max(cassette_5p,int(exon["five_p_loc"]))
            end= min(cassette_3p,int(exon["three_p_loc"]))
        else:
            start= max(cassette_3p,int(exon["three_p_loc"]))
            end= min(cassette_5p,int(exon["five_p_loc"]))
        overlap= end-start
        if overlap > -10:
            sys.stderr.write("cassette is " +str(cassette)+"\n")
            sys.stderr.write("overlap is " +str(overlap)+"\n")
            print json.dumps(exon)
            break

exons_file.close()
