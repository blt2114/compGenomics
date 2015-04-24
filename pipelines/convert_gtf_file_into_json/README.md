Simple Tool to Convert GTF File into a nested json file
-------------------------------------------------------

### Background ###

It is well known that the H3K27Ac histone mark correlates well with the start of transcription. Since this is
**known** information, it would be worthwhile to test whether any ML that we construct can validate something 
that is **extremely** well established in literature. 

Programs and Commands
---------------------

### Input Files ###
* files/gen10.long.gtf
* src/gtftools.py

### Step 1: Filter gtf file into three partitions ###
    python src/gtftools.py -v -i files/gen10.long.gtf -o files/gen10.long.gtf.genes -f feature=gene
    python src/gtftools.py -v -i files/gen10.long.gtf -o files/gen10.long.gtf.transcripts -f feature=transcript
    python src/gtftools.py -v -i files/gen10.long.gtf -o files/gen10.long.gtf.exons -f feature=exon
    
### Step 2: Run the conversion script ###
Note: To use the gtf2dict.py script, you need to:

    export PYTHONPATH={path to the compgenomics folder}

Command Used:

    python gtf2dict.py ../../files/gen10.long.gtf.genes ../../files/gen10.long.gtf.transcripts ../../files/gen10.long.gtf.exons > ../../files/genes.json

stderr output:

    Estimating compute time.
    Starting to load genes.
    Part 1/3: 100%
    Starting to load transcripts.
    Part 2/3: 100%
    Starting to load exons.
    Part 3/3: 100%
    Beginning to print.
