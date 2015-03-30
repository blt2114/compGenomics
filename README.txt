Jeff Zhou and Brian Trippe

Course Project for Columbia Course in Computational Genomics 
CBMF W4761 taught by Itshack Pe'er

using data from epigenetics roadmap project
http://egg2.wustl.edu/roadmap/web_portal/processed_data.html

First Part of Project:
Goal: using chip-seq data for samples at known TSS for given genes to predict 
whether or not the TSS is used in that sample 

Essential Dimensions included in Feature Vectors
(will be same for Alternative Splicing):
ChIP-Seq for 5 core methylation marks present in all data samples
        -H3K4me1
	-H3K4me3
	-H3K27me3
	-H3K36me3-- is involved in splicing
	-H3K9me3
Many to Most samples also have
        -H3K27ac
        -H3K9ac


Data Labels will be a binary label for whether or not the TSS was used:
-y in set of {0,1} 
-labels describing if a TSS is used may be determined using some reasonable 
threshold of the portion of transcripts that must contain exon v.s. those 
that don't.
-This is only available for 56 of the epigenomes. The sample identifiers for 
these are present on the first line of the RNA-Seq exon count 
file('57epigenomes.exon.N.pc').


First Part of Project is Data formatting.

RNA-Seq Processing pipeline will work as follows:
cat 57epigenomes.exon.N.pc > script-1.py | script-2.py | ... | script-n.py > TSS-data.json
        -individual scripts will likely have their own command line arguments
         to specify things like thresholds or parameter files
        -somewhere along the way, dump the TSS locations into a file, TSS-starts.json
        with objects that look like:
{
        "chrom":"X",            # chromosome identifier as a string

        "location":1220,        # base offset from chromosome start

        "read_dir":1,           # 1 if forward, 0 if backwards. This is 
                                # important if we are interested in looking
                                # at positions upstream/ downstream of the TSS
}


-Where TSS-data.json contains the TSS data as JSON objects, one on each line.
-Each object looks like:
{
        "sample":sample_name,   # as a string, e.g. "E001"

        "tss-id":identifer,     # identifier unique to a given possible TSS, 
                                # This will be a nested obj, defined below

        "site-used": is_TSS     # an integer, 1 if it is the TSS used in that 
                                # given sample, 0 otherwise.
}

The format of identifier must contain sufficent information to do subsequent analysis
identifer will look like:
{
        "gene":"yfg-1",         # this is just good to keep around for when we
                                #  process result later on.

        "chrom":"X",            # chromosome identifier as a string

        "location":1220,        # base offset from chromosome start

        "read_dir":1,           # 1 if forward, 0 if backwards. This is 
                                # important if we are interested in looking
                                #  at positions upstream/ downstream of the TSS
}



ChIP-Seq Processing Pipeline for TSS
-requires TSS-starts.json (can hold in memory)

Working off of aligned reads, TagAlign Files.
        -data available at:
         http://egg2.wustl.edu/roadmap/data/byFileType/alignments/consolidated/
        -format described at: http://genome.ucsc.edu/FAQ/FAQformat.html#format15

-windows must be specified for # of BP's upstream and downstream of the given
 position within which reads will be counted.
-the read counts within the region will be scaled down by the region and the 
 number of reads in the ChIP-seq experiment
-The number of reads in each ChIP-Seq experiement can be found at:
docs.google.com/spreadsheet/ccc?key=0Am6FxqAtrFDwdHU1UC13ZUxKYy1XVEJPUzV6MEtQOXc&usp=sharing#gid=15
        -this also contains information on which samples have which data.


