Generalized Pipeline for Obtaining TSS Information
--------------------------------------------------

### Background ###

Is better suited for computational resource reasons.

Programs and Commands
---------------------

### Input Files ###
* gen10.long.gtf
* 57epigenomes.exon.RPKM.nc
* 58epigenomes.exon.RPKM.pc

### Step 1: Combine the two RPKM by gene files ###
    head -1 57epigenomes.exon.RPKM.pc > 57epigenomes.exon.RPKM.all
    tail -q -n +2 57epigenomes.exon.RPKM.pc 57epigenomes.exon.RPKM.nc >> 57epigenomes.exon.RPKM.all
    
### Step 2: Use genes.json file for annotation purposes ###

Run pipeline (convert_gtf_file_into_json). This produces this file:

    files/genes.json
    
### Step 3: Get a list of all TSS ###

To use this python be sure to:

    export PYTHONPATH={path to the compgenomics folder}

We are getting a comprehensive list of all TSS because there's no real reason to begin filtering until we limit
ourselves to the granularity present in the physical RNA-seq. We can collapse the transcripts that we see at that point.
Run this program:

    python filter_all_tss.py ../../files/gen10_files/genes.json > ../../files/all_tss.json

It outputs a json file in this format, with one gene on each line:

    {
      "gene_id": "ENSG00000167578", 
      "seqname": "chr19", 
      "source": "ENSEMBL", 
      "start": 41277553, 
      "end": 41302847, 
      "strand": "+", 
      "attribute": {
        "gene_status": "KNOWN", 
        "level": "3", 
        "transcript_type": "protein_coding", 
        "gene_id": "ENSG00000167578.10", 
        "transcript_name": "MIA", 
        "transcript_id": "ENSG00000167578.10", 
        "gene_type": "protein_coding", 
        "transcript_status": "KNOWN", 
        "gene_name": "MIA"
      }, 
      "transcripts": {
        "ENST00000263369.2": {
          "seqname": "chr19", 
          "end": 41283392, 
          "exons": [
            [
              41281300, 
              41281574
            ], 
            [
              41281657, 
              41281790
            ], 
            [
              41282874, 
              41282984
            ], 
            [
              41283302, 
              41283392
            ]
          ], 
          "source": "ENSEMBL", 
          "attribute": {
            "gene_status": "KNOWN", 
            "level": "3", 
            "transcript_type": "protein_coding", 
            "gene_id": "ENSG00000167578.10", 
            "tag": "CCDS", 
            "gene_type": "protein_coding", 
            "ccdsid": "CCDS12566.1", 
            "transcript_id": "ENST00000263369.2", 
            "transcript_name": "MIA-201", 
            "transcript_status": "KNOWN", 
            "gene_name": "MIA"
          }, 
          "frame": ".", 
          "feature": "transcript", 
          "introns": [
            [
              41281575, 
              41281656
            ], 
            [
              41281791, 
              41282873
            ], 
            [
              41282985, 
              41283301
            ]
          ], 
          "start": 41281300, 
          "length": 2092, 
          "score": ".", 
          "tss": 41281300, 
          "strand": "+"
        }, 
        "ENST00000378307.4": {
          "seqname": "chr19", 
          "end": 41302847, 
          "exons": [
            [
              41284213, 
              41284296
            ], 
            [
              41285924, 
              41286004
            ], 
            [
              41286290, 
              41286404
            ], 
            [
              41289683, 
              41289745
            ], 
            [
              41292570, 
              41292665
            ], 
            [
              41292753, 
              41292883
            ], 
            [
              41302475, 
              41302847
            ]
          ], 
          "source": "ENSEMBL", 
          "attribute": {
            "gene_status": "KNOWN", 
            "level": "3", 
            "transcript_type": "protein_coding", 
            "gene_id": "ENSG00000167578.10", 
            "transcript_name": "MIA-203", 
            "transcript_id": "ENST00000378307.4", 
            "gene_type": "protein_coding", 
            "transcript_status": "KNOWN", 
            "gene_name": "MIA"
          }, 
          "frame": ".", 
          "feature": "transcript", 
          "introns": [
            [
              41284297, 
              41285923
            ], 
            [
              41286005, 
              41286289
            ], 
            [
              41286405, 
              41289682
            ], 
            [
              41289746, 
              41292569
            ], 
            [
              41292666, 
              41292752
            ], 
            [
              41292884, 
              41302474
            ]
          ], 
          "start": 41284213, 
          "length": 18634, 
          "score": ".", 
          "tss": 41284213, 
          "strand": "+"
        },
    }


### Step 4: Append RNA-seq values to this list of TSS sites ###

Since the granularity of our RNA-seq data is limited to the size of the exon, we will refine multiple transcripts down
into the exon level. The start (or end) of the exon is taken to be the TSS of all the transcripts that map to that exon.

Any transcript that does not map to any exon in the RNA-seq dataset is automatically discarded.

To run this step:

    python xtract_rna_all_tss.py ../../files/all_tss.json ../../files/57epigenomes.exon.RPKM.all ../../config-files/chromosome_order.json > ../../files/all_tss_rna.json

It outputs a json file that looks like this:

    {
      "seqname": "chr1", 
      "tss": 11869, 
      "strand": "+", 
      "gene_id": "ENSG00000223972", 
      "tss_type": "leading", 
      "transcripts": [
        {
          "seqname": "chr1", 
          "end": 14412, 
          "start": 11872, 
          "attribute": {
            "transcript_status": "KNOWN", 
            "gene_status": "KNOWN", 
            "havana_gene": "OTTHUMG00000000961.2", 
            "level": "3", 
            "transcript_type": "transcribed_unprocessed_pseudogene", 
            "gene_id": "ENSG00000223972.4", 
            "transcript_id": "ENST00000515242.2", 
            "gene_type": "pseudogene", 
            "transcript_name": "DDX11L1-201", 
            "gene_name": "DDX11L1"
          }, 
          "frame": ".", 
          "feature": "transcript", 
          "source": "ENSEMBL", 
          "length": 2540, 
          "score": ".", 
          "tss": 11872, 
          "strand": "+"
        }, 
        {
          "seqname": "chr1", 
          "end": 14409, 
          "start": 11874, 
          "attribute": {
            "transcript_status": "KNOWN", 
            "gene_status": "KNOWN", 
            "havana_gene": "OTTHUMG00000000961.2", 
            "level": "3", 
            "transcript_type": "transcribed_unprocessed_pseudogene", 
            "gene_id": "ENSG00000223972.4", 
            "transcript_id": "ENST00000518655.2", 
            "gene_type": "pseudogene", 
            "transcript_name": "DDX11L1-202", 
            "gene_name": "DDX11L1"
          }, 
          "frame": ".", 
          "feature": "transcript", 
          "source": "ENSEMBL", 
          "length": 2535, 
          "score": ".", 
          "tss": 11874, 
          "strand": "+"
        },
      ], 
      "samples": {
        "E071": {
          "rpkm": "0.000"
        }, 
        "E016": {
          "rpkm": "0.041"
        }, 
        "E120": {
          "rpkm": "0.182"
        }, 
        "E062": {
          "rpkm": "0.191"
        }, 
        "E003": {
          "rpkm": "0.120"
        }, 
        "E028": {
          "rpkm": "0.013"
        }, 
        "E066": {
          "rpkm": "0.320"
        }, 
        "E007": {
          "rpkm": "0.000"
        }, 
        "E006": {
          "rpkm": "0.000"
      }
    }

### Step 5a: Reduce the number of TSS sites for performance issues ###

Run the file: 
    
    python utils/filter_tss_file_template.py ../../files/all_tss_rna.json > ../../files/level1_tss_rna.json 
       
It's a poorly commented file right now, so just open it up and modify the desirable filtered items.
 
In the case of this vignette, I filtered for: All sites that contain "Level 1" transcripts, reducing the total site
count to about 2 thousand.

### Step 5b: Summarize the file that you have (get summary info) ###

    python utils/summarize_tss_file.py level1_tss.json
    
Produces a summary output some output like this:

    {
      "tss_number": {
        "2_tss": 170, 
        "3_tss": 32, 
        "6_tss": 1, 
        "4_tss": 5, 
        "5_tss": 2, 
        "1_tss": 1716
      }, 
      "level": {
        "1": 2600, 
        "3": 494, 
        "2": 4503
      }, 
      "transcript_status": {
        "KNOWN": 4317, 
        "NOVEL": 1061, 
        "PUTATIVE": 2219
      }, 
      "source": {
        "HAVANA": 7076, 
        "ENSEMBL": 521
      }, 
      "tss_type": {
        "leading": 1069, 
        "cassette": 1120
      }, 
      "transcript_type": {
        "unitary_pseudogene": 1, 
        "sense_intronic": 2, 
        "lincRNA": 72, 
        "retained_intron": 723, 
        "antisense": 152, 
        "protein_coding": 4427, 
        "transcribed_unprocessed_pseudogene": 27, 
        "processed_transcript": 1168, 
        "pseudogene": 5, 
        "transcribed_processed_pseudogene": 67, 
        "unprocessed_pseudogene": 13, 
        "polymorphic_pseudogene": 2, 
        "retrotransposed": 2, 
        "TEC": 1, 
        "processed_pseudogene": 96, 
        "nonsense_mediated_decay": 839
      }
    }
    1914        # Total number of unique genes

Interestingly, the number of unique genes does not match my measure of calculating leading and cassette exons. This
either means I was too stringent with forcing sites to fall within the defined exon regions, or there is a bug in my 
code.

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
      "gene_id": "ENSG00000117620", 
      "tss_type": "leading", 
      "samples": {
        "E070": {
          "rpkm": "1.056", 
          "H3K36me3": [
            0.04738617839948443, 
            0.09477235679896887, 
            0.04738617839948443, 
            0.0, 
            0.04738617839948443, 
            0.0, 
            0.0, 
            0.0, 
            0.0, 
            0.0, 
            0.0, 
            0.09477235679896887, 
            0.04738617839948443, 
            0.0, 
            0.0, 
            0.04738617839948443, 
            0.04738617839948443, 
            0.09477235679896887, 
            0.04738617839948443, 
            0.0, 
            0.0, 
            0.0, 
            0.0, 
            0.0, 
            0.0, 
            0.0, 
            0.0, 
            0.09477235679896887, 
            0.04738617839948443, 
            0.09477235679896887, 
            0.04738617839948443, 
            0.09477235679896887, 
            0.0, 
            0.0, 
            0.04738617839948443, 
            0.0, 
            0.0, 
            0.04738617839948443, 
            0.04738617839948443, 
            0.0, 
            0.0, 
            0.0, 
            0.04738617839948443, 
            0.04738617839948443, 
            0.0, 
            0.0, 
            0.0, 
            0.0, 
            0.0, 
            0.0, 
            0.0, 
            0.0, 
            0.04738617839948443, 
            0.09477235679896887, 
            0.0, 
            0.0, 
            0.1421585351984533, 
            0.04738617839948443, 
            0.18954471359793773, 
            0.0
          ],
      }, 
      "transcripts": [
        {
          "seqname": "chr1", 
          "end": 100488512, 
          "source": "HAVANA", 
          "attribute": {
            "gene_status": "KNOWN", 
            "havana_gene": "OTTHUMG00000010805.2", 
            "level": "1", 
            "transcript_name": "SLC35A3-004", 
            "transcript_status": "KNOWN", 
            "gene_id": "ENSG00000117620.7", 
            "tag": "CCDS", 
            "havana_transcript": "OTTHUMT00000029786.2", 
            "ccdsid": "CCDS762.1", 
            "transcript_id": "ENST00000427993.2", 
            "gene_type": "protein_coding", 
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
      "tss": 100435345, 
      "strand": "+"
    }

### Step 8: At this point, filter for relevant entries and unpack them ###

In the case for this experiment, I'm going to filter for only non-cassette TSS sites.



