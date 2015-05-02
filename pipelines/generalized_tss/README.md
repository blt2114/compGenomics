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

    python filter_all_tss.py ../../files/genes.json > ../../files/all_tss.json

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
          "start": 41281300, 
          "length": 2092, 
          "score": ".", 
          "tss": 41281300, 
          "strand": "+"
        }, 
        "ENST00000378307.4": {
          "seqname": "chr19", 
          "end": 41302847, 
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
          "start": 41284213, 
          "length": 18634, 
          "score": ".", 
          "tss": 41284213, 
          "strand": "+"
        },
      }
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

### Step 6: Run chip extraction script to add read counts###

The chip extraction script WORKS, but it takes way too long to run on the full list of TSS sites. Here is the metric:
 
    time python xtract_chip_all_tss.py ../../files/all_tss_rna.json ../../test_chip/ test.txt ../../files/experiment_read_counts.json 250 500 1
    
    real	32m53.612s
    user	0m0.000s
    sys	0m0.001s
    
In other words, for about 35666 tss sites, this program processes about 1000 TSS sites a minute. 

Here are some other examples:

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
    
The bottleneck appears to be the buffer. FYI, this is the output of the program, which needs more processing (merging) afterwards:

    chr1	13184053	E003	H3K9ac	[0.03333333333333333, 0.03333333333333333, 0.0, 0.03333333333333333, 0.0, 0.0, 0.0, 0.03333333333333333, 0.06666666666666667, 0.0, 0.06666666666666667, 0.03333333333333333, 0.03333333333333333, 0.0, 0.03333333333333333, 0.06666666666666667, 0.0, 0.0, 0.0, 0.0, 0.03333333333333333, 0.0, 0.03333333333333333, 0.03333333333333333, 0.0, 0.03333333333333333, 0.13333333333333333, 0.0, 0.03333333333333333, 0.0, 0.03333333333333333, 0.0, 0.0, 0.03333333333333333, 0.03333333333333333, 0.0, 0.0, 0.03333333333333333, 0.0, 0.0, 0.06666666666666667, 0.03333333333333333, 0.0, 0.0, 0.0, 0.03333333333333333, 0.0, 0.0, 0.1, 0.03333333333333333, 0.03333333333333333, 0.0, 0.03333333333333333, 0.0, 0.0, 0.0, 0.0, 0.06666666666666667, 0.0, 0.06666666666666667, 0.0, 0.0, 0.0, 0.0, 0.03333333333333333, 0.03333333333333333, 0.0, 0.03333333333333333, 0.0, 0.03333333333333333, 0.0, 0.0, 0.03333333333333333, 0.03333333333333333, 0.06666666666666667, 0.0, 0.06666666666666667, 0.0, 0.0, 0.0, 0.06666666666666667, 0.06666666666666667, 0.0, 0.0, 0.1, 0.03333333333333333, 0.0, 0.06666666666666667, 0.0, 0.0, 0.03333333333333333, 0.06666666666666667, 0.03333333333333333, 0.0, 0.0, 0.03333333333333333, 0.06666666666666667, 0.06666666666666667, 0.03333333333333333, 0.0]
    chr1	15931077	E003	H3K9ac	[0.03333333333333333, 0.03333333333333333, 0.06666666666666667, 0.03333333333333333, 0.0, 0.0, 0.0, 0.06666666666666667, 0.03333333333333333, 0.1, 0.1, 0.06666666666666667, 0.03333333333333333, 0.0, 0.0, 0.06666666666666667, 0.03333333333333333, 0.0, 0.0, 0.0, 0.03333333333333333, 0.03333333333333333, 0.0, 0.06666666666666667, 0.1, 0.03333333333333333, 0.06666666666666667, 0.1, 0.0, 0.03333333333333333, 0.0, 0.0, 0.0, 0.0, 0.13333333333333333, 0.3, 0.5666666666666667, 0.5333333333333333, 0.5333333333333333, 0.26666666666666666, 0.03333333333333333, 0.06666666666666667, 0.23333333333333334, 0.23333333333333334, 0.26666666666666666, 0.03333333333333333, 0.0, 0.03333333333333333, 0.0, 0.1, 0.0, 0.0, 0.0, 0.06666666666666667, 0.03333333333333333, 0.03333333333333333, 0.03333333333333333, 0.0, 0.03333333333333333, 0.13333333333333333, 0.03333333333333333, 0.0, 0.03333333333333333, 0.1, 0.06666666666666667, 0.03333333333333333, 0.16666666666666666, 0.06666666666666667, 0.1, 0.16666666666666666, 0.0, 0.06666666666666667, 0.03333333333333333, 0.0, 0.0, 0.03333333333333333, 0.0, 0.03333333333333333, 0.0, 0.0, 0.03333333333333333, 0.03333333333333333, 0.03333333333333333, 0.0, 0.03333333333333333, 0.0, 0.06666666666666667, 0.0, 0.0, 0.03333333333333333, 0.03333333333333333, 0.0, 0.03333333333333333, 0.03333333333333333, 0.03333333333333333, 0.06666666666666667, 0.0, 0.0, 0.03333333333333333, 0.0]
    chr1	16154724	E003	H3K9ac	[0.0, 0.03333333333333333, 0.03333333333333333, 0.03333333333333333, 0.0, 0.03333333333333333, 0.06666666666666667, 0.0, 0.03333333333333333, 0.13333333333333333, 0.0, 0.0, 0.03333333333333333, 0.06666666666666667, 0.03333333333333333, 0.03333333333333333, 0.0, 0.0, 0.1, 0.03333333333333333, 0.16666666666666666, 0.06666666666666667, 0.0, 0.0, 0.0, 0.03333333333333333, 0.0, 0.0, 0.03333333333333333, 0.0, 0.0, 0.0, 0.06666666666666667, 0.0, 0.06666666666666667, 0.06666666666666667, 0.06666666666666667, 0.06666666666666667, 0.0, 0.03333333333333333, 0.0, 0.03333333333333333, 0.03333333333333333, 0.0, 0.06666666666666667, 0.06666666666666667, 0.0, 0.0, 0.0, 0.0, 0.0, 0.03333333333333333, 0.1, 0.0, 0.0, 0.03333333333333333, 0.0, 0.06666666666666667, 0.03333333333333333, 0.06666666666666667, 0.06666666666666667, 0.0, 0.1, 0.03333333333333333, 0.03333333333333333, 0.06666666666666667, 0.13333333333333333, 0.03333333333333333, 0.1, 0.06666666666666667, 0.06666666666666667, 0.0, 0.06666666666666667, 0.06666666666666667, 0.1, 0.0, 0.03333333333333333, 0.06666666666666667, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.03333333333333333, 0.03333333333333333, 0.13333333333333333, 0.06666666666666667, 0.06666666666666667, 0.06666666666666667, 0.03333333333333333, 0.03333333333333333, 0.0, 0.0, 0.03333333333333333, 0.03333333333333333, 0.06666666666666667, 0.23333333333333334]
    ...
    
Alright. {
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
1914
