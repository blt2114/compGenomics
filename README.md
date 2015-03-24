Jeff Zhou and Brian Trippe

Course Project for Columbia Course in Computational Genomics 
CBMF W4761 taught by Itshack Pe'er

using data from epigenetics roadmap project
http://egg2.wustl.edu/roadmap/web_portal/processed_data.html

First Part of Project:
Goal: using chip-seq data for samples at known TSS for given genes to predict 
whether or not the TSS is used in that sample 

First Part of Project is Data formatting.

RNA-Seq Processing pipeline will work as follows:
cat 57epigenomes.exon.N.pc > script-1.py | script-2.py | ... | script-n.py > TSS-data.json
        -individual scripts will likely have their own command line arguments
         to specify things like thresholds or parameter files

-Where TSS-data.json contains the TSS data as JSON objects, one on each line.
-Each object looks like:
{
        "sample":sample_name,   # as a string, e.g. "E001"
        "tss-id":identifer,     # some thing that will be unique to a given 
                                # possible TSS, possible a nested object, 
                                        # e.g. {"gene":"yfg-1","exon_number":2}
        "site-used": is_TSS     # an integer, 1 if it is the TSS used in that 
                                # given sample, 0 otherwise.
}
