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

### Step 3: Append RNA-seq values to this list of TSS sites ###

The RNA-seq matrix file contains RPKM values by exon. Since our "resolution" on the RNA-seq level is not better than
the size of an exon, we will consider all TSS sites that map to the same exon the same effective TSS. The start 
(or end) of the exon is taken to be the new "effective TSS" of all transcripts that map to that exon.

Any transcript that does not map to any exon in the RNA-seq dataset is automatically discarded.

The "granularity" argument is how much wiggle room you will allow transcripts to be mapped to the same exon. 
With a granularity of 0, only TSS sites that fall exactly within the boundaries of an exon will be mapped to it.
A granularity of 200 will allow TSS sites up to 200bp upstream or downstream of an exon to be mapped to it. 
I recommend a higher granularity (ie. 200) because the boundaries defined by the RPKM matrix do not necessarily encompass
all transcripts--it is more of an approximation of the exons detected during RNA-seq.

To run this step:

    python tss/xtract_rna_all_tss.py files/all_tss.json files/57epigenomes.exon.RPKM.all config-files/chromosome_order.json 200 > files/all_tss_rna.json

It outputs a json file in [this format](https://github.com/blt2114/compGenomics/blob/master/vignettes/sample_files/all_tss_rna.json)

Some explanations on the output:

    # Each line is an exon in from the RPKM matrix that contain a TSS site
    
    "seqname":          Chromosome
    "location":         Location of the TSS (exon start for positive strand, exon end for negative strand)
    "strand":           1 for the positive strand, and -1 for the negative strand
    "gene_id":          The ensembl gene ID
    "exon_number":      The exon number in the RPKM matrix this TSS site maps to, for this gene id
    "exon_total":       Total number of exons in the RPKM matrix for this gene id
    "splice_count":     The number of transcripts that have an intron overlapping with this exon
    "splice_before":    The number of transcripts that have an intron upstream of this exon (or transcript end)
    "coverage_count":   The number of transcripts that have an exon overlapping with this exon
    "tss_mapped":       The number of transcripts have mapped to this TSS site
    "tss_total":        Number of "effective TSS" sites for this gene -- (all TSS site that map to the same exon, count as a single effective TSS site).
    "transcript_total": Total number of theoretical TSS sites reported for this gene   
    "transcripts":      A list of all transcripts that have their TSS mapped to this exon 
    "samples":          A dictionary of samples, containing RPKM data for each sample.

### Step 3a: Reduce the number of TSS sites for performance issues (optional) ###

If your computer is limited by the amount of RAM (we load the entire JSON file into memory during certain portions
of the pipeline), it may be desirable reduce the overall number of sites at this point. 

A template filtering file is provided below. With a little knowledge of python, you can modify this template file
to filter for certain features you know you will be looking at in the future.

In my case, I have chosen to filter for TSS sites that are part of exons that are theoretically never spliced, never
have any introns located before it, and never have any prematuring ending transcripts located before it.

Run the file: 
    
    python tss/filter_tss_file_template.py files/all_tss_rna.json > files/nosplice_tss_rna.json 
       

### Step 6: Run chip extraction script to add read counts ###

The chip extraction is written in C++. To compile this script, use:

    make

Now run:

    bash src/ChIP/run_download_and_extract.sh chip out files/all_experiments_to_acquire.txt files/nosplice_tss_rna.json config-files/config_windows_for_C.json 4 1

Here is an explanation of the arguments:

* 1st Argument: The input directory. This directory should contain all of the unzipped chip files.
* 2nd Argument: The ouput directory, which will hold the results in the end.
* 3rd Argument: A list of all chip files to acquire. (with a .gz extension)
* 4th Argument: The sites.json file that was put together in the previous steps of this pipeline.
* 5th Argument: Configuration file for the extraction
* 6th Argument: Number of threads (4 CPUs, for instance)
* 7th Argument (Optional): Use this argument if you have already downloaded the files.

This step takes several hours to run. Start this command and monitor the progress by checking the log files
periodically in the input directory. It is typically useful to run a grep command to see if any script is still running.

    ps -e | grep extract
    
It takes close to 2 minutes to parse through an 80k sites and one ChIP file. 

This program outs a tab delimited text file in [this format](https://github.com/blt2114/compGenomics/blob/master/vignettes/sample_files/nosplice_tss_chip.tsv)

# Step 7: merge, sort, and pile up the output ###

Cat all of the output from the previous step together

    cat ####_ ####_ ####_ ####_ > files/nosplice_tss_chip.tsv
    
Run this command:

    python tss/pileup_rna_chip_tss.py files/nosplice_tss_rna.json files/nosplice_tss_chip.tsv files/experiment_read_counts.json > files/nosplice_tss_rna_chip.json

Note that to run this step, you need to obtain the json file called experiment_read_counts.json. This file contains the
number of reads per experiment. This step performs the read-count normalization.

This program outs a json file in [this format](https://github.com/blt2114/compGenomics/blob/master/vignettes/sample_files/nosplice_tss_rna_chip.json)

### Step 8b: At this point, filter for relevant entries and unpack them ###

This is the point in the workflow where all filtering occurs. The information in the previous step must be transformed
into feature vectors and binary feature labels. I am going to use arbitrary cutoffs such as ln(RPKM)<1 as the cutoff
for expression, but the end-user should be able to go into this file and modify items to suit their implementation
details. For instance, it is perfectly possible to filter for TSS sites only of lincRNA's or some other arbitrary
detail.

To reiterate my process:

* Expressed sites need to have a ln(delta_RPKM) >= 1
* The window sizes will be +500 and -500 for every ChIP mark, by default. The normalized reads per million will be
summed within this range.
* I will examine 12 marks, and discard any samples that do not have these 12 marks: "H3K4me1", "H3K4me3", "H3K27me3", 
"H3K36me3", "H3K9me3", "H2A.Z", "H3K4me2", "H3K27ac", "H4K20me1", "H3K9ac", "DNase", "H3K79me2"

It is possible to pass as a parameter windows for each different mark.

Run this command

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

