Pipeline for TSS
================

### Background ###

This pipeline describes the commands to run to process the TSS portion of the data. Please skip
to the end of this file to obtain a comprehensive list of files and their command line options.

Pipeline Instructions
---------------------

### Step 0: Download the necessary files ###

The following files are required:

* gen10.long.gtf
* 57epigenomes.exon.RPKM.nc
* 58epigenomes.exon.RPKM.pc
* [All of the ChIP-seq data]

See the download instructions available [here]. These instructions will assume you have downloaded the
chip files to /root/chip/ and all other files to /root/files/. 

Run all commands in these instructions from the application root.

For some of these scripts, it will be necessary to add the application root to PYTHONPATH:

    export PYTHONPATH={path to the application folder}

### Step 1: Prepare downloaded data into format necessary for the pipeline ###

Combine both noncoding and protein coding RNA rpkm data into one file:

    head -1 files/57epigenomes.exon.RPKM.pc > files/57epigenomes.exon.RPKM.all
    tail -q -n +2 files/57epigenomes.exon.RPKM.pc files/57epigenomes.exon.RPKM.nc >> files/57epigenomes.exon.RPKM.all

Filter the GTF file into three relevant partitions:

    python src/gtftools.py -v -i files/gen10.long.gtf -o files/gen10.long.gtf.genes -f feature=gene
    python src/gtftools.py -v -i files/gen10.long.gtf -o files/gen10.long.gtf.transcripts -f feature=transcript
    python src/gtftools.py -v -i files/gen10.long.gtf -o files/gen10.long.gtf.exons -f feature=exon

Convert the GTF file into JSON format:

    python src/gtf2dict.py files/gen10.long.gtf.genes files/gen10_files/gen10.long.gtf.transcripts files/gen10_files/gen10.long.gtf.exons > files/genes.json

### Step 2: Obtain a list of all potential TSS sites ###

We are getting a comprehensive list of all TSS because we will save the filtering of the sites towards the last parts
of the pipeline.

Run this command:

    python tss/filter_all_tss.py files/gen10_files/genes.json > files/all_tss.json

It outputs a json file in [this format](https://github.com/blt2114/compGenomics/blob/master/vignettes/sample_files/all_tss.json)

### Step 4: Append RNA-seq values to this list of TSS sites ###

The RNA-seq matrix file contains RPKM values by exon. Since our "resolution" on the RNA-seq level is not better than
the size of an exon, we will consider all TSS sites that map to the same exon the same TSS. The start (or end) of the
exon is taken to be the new "effective TSS" of all transcripts that map to that exon.

Any transcript that does not map to any exon in the RNA-seq dataset is automatically discarded.

The "granularity" argument is how much wiggle room you will allow transcripts to be mapped to the same exon. 
With a granularity of 0, only TSS sites that fall exactly within the boundaries of an exon will be mapped to it.
A granularity of 200 will allow TSS sites up to 200bp upstream or downstream of an exon to be mapped to it. 
I recommend a higher granularity (ie. 200) because the boundaries defined by the RPKM matrix do not necessarily encompass
all transcripts--it is more of an approximation of the exons detected during RNA-seq.

To run this step:

    python tss/xtract_rna_all_tss.py files/all_tss.json files/57epigenomes.exon.RPKM.all config-files/chromosome_order.json 200 > files/all_tss_rna.json

It outputs a json file in [this format](https://github.com/blt2114/compGenomics/blob/master/vignettes/sample_files/all_tss_rna.json)

### Step 4b: Load Gene Expression data into the file ###
    
If necessary, load the gene RPKM expression data as well.

    python utils/load_gene_rpkm.py ../../files/all_tss_rna.json ../../files/57epigenomes.RPKM.all > ../../files/all_tss_rna.json2

Most likely, this step is not necessary. 

### Step 5a: Reduce the number of TSS sites for performance issues ###

Run the file: 
    
    python utils/filter_tss_file_template.py ../../files/all_tss_rna.json > ../../files/level1_tss_rna.json 
       
It's a poorly commented file right now, so just open it up and modify the desirable filtered items.
 
In the case of this vignette, I filtered for: All sites that contain "Level 1" transcripts, reducing the total site
count to about 2 thousand.

I am also running a version where I filter for TSS sites that that are never spliced and TSS sites that have no
splicing before its position.

### Step 6: Run chip extraction script to add read counts ###

The chip extraction script WORKS, but it takes way too long to run on the full list of TSS sites. Here is the metric:
 
    time python xtract_chip_all_tss.py ../../files/all_tss_rna.json ../../test_chip/ test.txt ../../files/experiment_read_counts.json 250 500 1
    
    real	32m53.612s
    user	0m0.000s
    sys	0m0.001s
    
In other words, for about 35666 tss sites, this program processes about 1000 TSS sites a minute. Instead of using the
full TSS list, I decided at this point to limit the list to about 2000 sites:

    python xtract_chip_all_tss.py ../level1_tss.json ../../test_chip/ test.txt ../../files/experiment_read_counts.json 250 500 1

    real	3m28.225s
    user	0m0.000s
    sys	0m0.001s
    
    python xtract_chip_all_tss.py ../level1_tss.json ../../test_chip/ test.txt ../../files/experiment_read_counts.json 1000 200 1

    real	3m20.300s
    user	3m16.730s
    sys	0m14.668s

About 663 genes per minute. To process 352 samples, this is 19.4 CPU hours ~ 5 hours on 4 cores

    time python xtract_chip_all_tss.py ../level1_tss.json ../../test_chip/ test.txt ../../files/experiment_read_counts.json 2000 100 1

    real	3m22.420s
    user	3m17.750s
    sys	0m13.605s
    
The bottleneck appears to be the buffer. Changing the number of windows does not have an extremely appreciable affect
on how long it takes the program to run.

FYI, this is the output of the program, which needs more processing (merging) 
afterwards:

    chr1	13184053	E003	H3K9ac	[0.03333333333333333, 0.03333333333333333, 0.0, 0.03333333333333333, 0.0, 0.0, 0.0, 0.03333333333333333, 0.06666666666666667, 0.0, 0.06666666666666667, 0.03333333333333333, 0.03333333333333333, 0.0, 0.03333333333333333, 0.06666666666666667, 0.0, 0.0, 0.0, 0.0, 0.03333333333333333, 0.0, 0.03333333333333333, 0.03333333333333333, 0.0, 0.03333333333333333, 0.13333333333333333, 0.0, 0.03333333333333333, 0.0, 0.03333333333333333, 0.0, 0.0, 0.03333333333333333, 0.03333333333333333, 0.0, 0.0, 0.03333333333333333, 0.0, 0.0, 0.06666666666666667, 0.03333333333333333, 0.0, 0.0, 0.0, 0.03333333333333333, 0.0, 0.0, 0.1, 0.03333333333333333, 0.03333333333333333, 0.0, 0.03333333333333333, 0.0, 0.0, 0.0, 0.0, 0.06666666666666667, 0.0, 0.06666666666666667, 0.0, 0.0, 0.0, 0.0, 0.03333333333333333, 0.03333333333333333, 0.0, 0.03333333333333333, 0.0, 0.03333333333333333, 0.0, 0.0, 0.03333333333333333, 0.03333333333333333, 0.06666666666666667, 0.0, 0.06666666666666667, 0.0, 0.0, 0.0, 0.06666666666666667, 0.06666666666666667, 0.0, 0.0, 0.1, 0.03333333333333333, 0.0, 0.06666666666666667, 0.0, 0.0, 0.03333333333333333, 0.06666666666666667, 0.03333333333333333, 0.0, 0.0, 0.03333333333333333, 0.06666666666666667, 0.06666666666666667, 0.03333333333333333, 0.0]
    chr1	15931077	E003	H3K9ac	[0.03333333333333333, 0.03333333333333333, 0.06666666666666667, 0.03333333333333333, 0.0, 0.0, 0.0, 0.06666666666666667, 0.03333333333333333, 0.1, 0.1, 0.06666666666666667, 0.03333333333333333, 0.0, 0.0, 0.06666666666666667, 0.03333333333333333, 0.0, 0.0, 0.0, 0.03333333333333333, 0.03333333333333333, 0.0, 0.06666666666666667, 0.1, 0.03333333333333333, 0.06666666666666667, 0.1, 0.0, 0.03333333333333333, 0.0, 0.0, 0.0, 0.0, 0.13333333333333333, 0.3, 0.5666666666666667, 0.5333333333333333, 0.5333333333333333, 0.26666666666666666, 0.03333333333333333, 0.06666666666666667, 0.23333333333333334, 0.23333333333333334, 0.26666666666666666, 0.03333333333333333, 0.0, 0.03333333333333333, 0.0, 0.1, 0.0, 0.0, 0.0, 0.06666666666666667, 0.03333333333333333, 0.03333333333333333, 0.03333333333333333, 0.0, 0.03333333333333333, 0.13333333333333333, 0.03333333333333333, 0.0, 0.03333333333333333, 0.1, 0.06666666666666667, 0.03333333333333333, 0.16666666666666666, 0.06666666666666667, 0.1, 0.16666666666666666, 0.0, 0.06666666666666667, 0.03333333333333333, 0.0, 0.0, 0.03333333333333333, 0.0, 0.03333333333333333, 0.0, 0.0, 0.03333333333333333, 0.03333333333333333, 0.03333333333333333, 0.0, 0.03333333333333333, 0.0, 0.06666666666666667, 0.0, 0.0, 0.03333333333333333, 0.03333333333333333, 0.0, 0.03333333333333333, 0.03333333333333333, 0.03333333333333333, 0.06666666666666667, 0.0, 0.0, 0.03333333333333333, 0.0]
    chr1	16154724	E003	H3K9ac	[0.0, 0.03333333333333333, 0.03333333333333333, 0.03333333333333333, 0.0, 0.03333333333333333, 0.06666666666666667, 0.0, 0.03333333333333333, 0.13333333333333333, 0.0, 0.0, 0.03333333333333333, 0.06666666666666667, 0.03333333333333333, 0.03333333333333333, 0.0, 0.0, 0.1, 0.03333333333333333, 0.16666666666666666, 0.06666666666666667, 0.0, 0.0, 0.0, 0.03333333333333333, 0.0, 0.0, 0.03333333333333333, 0.0, 0.0, 0.0, 0.06666666666666667, 0.0, 0.06666666666666667, 0.06666666666666667, 0.06666666666666667, 0.06666666666666667, 0.0, 0.03333333333333333, 0.0, 0.03333333333333333, 0.03333333333333333, 0.0, 0.06666666666666667, 0.06666666666666667, 0.0, 0.0, 0.0, 0.0, 0.0, 0.03333333333333333, 0.1, 0.0, 0.0, 0.03333333333333333, 0.0, 0.06666666666666667, 0.03333333333333333, 0.06666666666666667, 0.06666666666666667, 0.0, 0.1, 0.03333333333333333, 0.03333333333333333, 0.06666666666666667, 0.13333333333333333, 0.03333333333333333, 0.1, 0.06666666666666667, 0.06666666666666667, 0.0, 0.06666666666666667, 0.06666666666666667, 0.1, 0.0, 0.03333333333333333, 0.06666666666666667, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.03333333333333333, 0.03333333333333333, 0.13333333333333333, 0.06666666666666667, 0.06666666666666667, 0.06666666666666667, 0.03333333333333333, 0.03333333333333333, 0.0, 0.0, 0.03333333333333333, 0.03333333333333333, 0.06666666666666667, 0.23333333333333334]
    ...
    
Since it seemed like the python multithreading doesn't work very well (or efficently), I decided to simply run 4 parallel
instances of the one-core version of the program. I split up the files between 4 directories before starting.

This was the command that I ran (all in parallel):

    python pipelines/generalized_tss/xtract_chip_all_tss_1core.py pipelines/generalized_tss/level1_tss.json chip files/experiment_read_counts.json 3000 100 > out1.tsv
    python pipelines/generalized_tss/xtract_chip_all_tss_1core.py pipelines/generalized_tss/level1_tss.json chip2 files/experiment_read_counts.json 3000 100 > out2.tsv
    python pipelines/generalized_tss/xtract_chip_all_tss_1core.py pipelines/generalized_tss/level1_tss.json chip3 files/experiment_read_counts.json 3000 100 > out3.tsv
    python pipelines/generalized_tss/xtract_chip_all_tss_1core.py pipelines/generalized_tss/level1_tss.json chip4 files/experiment_read_counts.json 3000 100 > out4.tsv

Realistically, it took about 9 hours.

# Step 7: merge, sort, and pile up the output ###

Run these two commands (make sure you're in the right directories)

    cat out1.tsv out2.tsv out3.tsv out4.tsv > files/level1_tss_chip.tsv
    python pileup_rna_chip_tss.py ../../files/level1_tss_rna.json ../../files/level1_tss_chip.tsv > ../../files/level1_tss_rna_chip.json


The output looks like this:

    {
      "seqname": "chr1", 
      "tss_total": 5, 
      "transcript_total": 9, 
      "tss_mapped": 3, 
      "coverage_count": 3, 
      "gene_id": "ENSG00000117620", 
      "tss": 100435345, 
      "exon_number": 1, 
      "tss_type": "leading", 
      "samples": {
        "E057": {
          "H3K4me3": [
            0.040773509353116855, 
            0.0, 
            0.0, 
            0.0, 
            0.0, 
            0.040773509353116855, 
            0.0, 
            0.0, 
            0.0, 
            0.0, 
            0.040773509353116855, 
            0.040773509353116855, 
            0.0, 
            0.040773509353116855, 
            0.0, 
            0.0, 
            0.0, 
            0.08154701870623371, 
            0.0, 
            0.040773509353116855, 
            0.08154701870623371, 
            0.08154701870623371, 
            0.12232052805935056, 
            0.24464105611870113, 
            0.5300556215905191, 
            1.386299318005973, 
            1.712487392830908, 
            2.1202224863620764, 
            2.364863542480778, 
            2.527957579893245, 
            2.242543014421427, 
            3.058013201483764, 
            3.098786710836881, 
            3.2211072388962316, 
            3.5065218043680497, 
            3.465748295014933, 
            3.3434277669555823, 
            3.098786710836881, 
            2.487184070540128, 
            1.6717138834777912, 
            1.182431771240389, 
            0.856243696415454, 
            0.7746966777092202, 
            0.856243696415454, 
            0.6931496590029865, 
            0.08154701870623371, 
            0.0, 
            0.040773509353116855, 
            0.20386754676558427, 
            0.08154701870623371, 
            0.12232052805935056, 
            0.040773509353116855, 
            0.08154701870623371, 
            0.040773509353116855, 
            0.08154701870623371, 
            0.040773509353116855, 
            0.08154701870623371, 
            0.040773509353116855, 
            0.08154701870623371, 
            0.0
          ], 
          "rpkm": 3.549, 
          "max_rpkm": 3.649,
          "gene_rpkm": "2.604",
          "delta_rpkm": -0.935
        },
      }, 
      "splice_count": 0, 
      "transcripts": [
        {
          "seqname": "chr1", 
          "end": 100488512, 
          "source": "HAVANA", 
          "attribute": {
            "gene_status": "KNOWN", 
            "havana_gene": "OTTHUMG00000010805.2", 
            "level": "1", 
            "transcript_status": "KNOWN", 
            "gene_id": "ENSG00000117620.7", 
            "tag": "CCDS", 
            "gene_type": "protein_coding", 
            "havana_transcript": "OTTHUMT00000029786.2", 
            "ccdsid": "CCDS762.1", 
            "transcript_id": "ENST00000427993.2", 
            "transcript_name": "SLC35A3-004", 
            "transcript_type": "protein_coding", 
            "gene_name": "SLC35A3"
          }, 
          "frame": ".", 
          "feature": "transcript", 
          "start": 100435535, 
          "length": 52977, 
          "score": ".", 
          "tss": 100435535, 
          "strand": "+"
        }
      ], 
      "exon_total": 11, 
      "strand": "+"
    }


### Step 8a: Apply meta data to chip experiments ###

Since I missed a lot of the data the first time through, the metadata is being applied now:

    python misc/summarize_tss_file.py ../files/level1_tss_rna_chip.json 

### Step 8b: At this point, filter for relevant entries and unpack them ###

In the case for this experiment, I'm going to take everything.

    python generalized_tss/unpack_rna_chip_tss.py ../files/level1_tss_rna_chip.json > generalized_tss/level1_trials/files/all_level1.json

Output format:

    {
      "E057": {
        "H3K4me3": [
          0.040773509353116855, 
          0.0, 
          0.0, 
          0.0, 
          0.0, 
          0.040773509353116855, 
          0.0, 
          0.0, 
          0.0, 
          0.0, 
          0.040773509353116855, 
          0.040773509353116855, 
          0.0, 
          0.040773509353116855, 
          0.0, 
          0.0, 
          0.0, 
          0.08154701870623371, 
          0.0, 
          0.040773509353116855, 
          0.08154701870623371, 
          0.08154701870623371, 
          0.12232052805935056, 
          0.24464105611870113, 
          0.5300556215905191, 
          1.386299318005973, 
          1.712487392830908, 
          2.1202224863620764, 
          2.364863542480778, 
          2.527957579893245, 
          2.242543014421427, 
          3.058013201483764, 
          3.098786710836881, 
          3.2211072388962316, 
          3.5065218043680497, 
          3.465748295014933, 
          3.3434277669555823, 
          3.098786710836881, 
          2.487184070540128, 
          1.6717138834777912, 
          1.182431771240389, 
          0.856243696415454, 
          0.7746966777092202, 
          0.856243696415454, 
          0.6931496590029865, 
          0.08154701870623371, 
          0.0, 
          0.040773509353116855, 
          0.20386754676558427, 
          0.08154701870623371, 
          0.12232052805935056, 
          0.040773509353116855, 
          0.08154701870623371, 
          0.040773509353116855, 
          0.08154701870623371, 
          0.040773509353116855, 
          0.08154701870623371, 
          0.040773509353116855, 
          0.08154701870623371, 
          0.0
        ], 
        "rpkm": 3.549, 
        "max_rpkm": 3.649,
        "gene_rpkm": "2.604",
        "delta_rpkm": -0.935
      },
    }


### Step 9: Throw into ML program ###

The ML takes input in this format (Brian's format):
    
    {
      "E065": {
        "p_inc": 2.1222970919414976, 
        "H3K9me3_num_reads_five_p": 27, 
        "H3K27me3_num_reads_three_p": 10, 
        "H3K36me3_num_reads_three_p": 56, 
        "H3K4me3_num_reads_five_p": 9, 
        "H3K9me3_num_reads_three_p": 16, 
        "H3K4me1_num_reads_five_p": 11, 
        "H3K4me3_num_reads_three_p": 9, 
        "H3K36me3_num_reads_five_p": 81, 
        "H3K27me3_num_reads_five_p": 11, 
        "H3K4me1_num_reads_three_p": 5
      }, 
      "E028": {
        "p_inc": 1.559579714669844, 
        "H3K9me3_num_reads_five_p": 2, 
        "H3K27me3_num_reads_three_p": 8, 
        "H3K36me3_num_reads_three_p": 31, 
        "H3K4me3_num_reads_five_p": 0, 
        "H3K9me3_num_reads_three_p": 2, 
        "H3K4me1_num_reads_five_p": 15, 
        "H3K4me3_num_reads_three_p": 4, 
        "H3K36me3_num_reads_five_p": 74, 
        "H3K27me3_num_reads_five_p": 7, 
        "H3K4me1_num_reads_three_p": 45
      },
    }

