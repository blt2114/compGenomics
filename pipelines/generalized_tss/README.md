Generalized Pipeline for Obtaining TSS Information
--------------------------------------------------

### Background ###

Is better suited for computational resource reasons.

Programs and Commands
---------------------

### Input Files ###
* gen10.long.gtf
* 57epigenomes.RPKM.nc
* 58epigenomes.RPKM.pc

### Step 1: Combine the two RPKM by gene files ###
    head -1 57epigenomes.RPKM.pc >> 57epigenomes.exon.RPKM.all
    tail -q -n +2 57epigenomes.RPKM.pc 57epigenomes.RPKM.nc >> 57epigenomes.RPKM.all
    
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

    python xtract_rna_all_tss.py ../../files/all_tss.json ../../files/57epigenomes.exon.RPKM.all > ../../files/all_tss_rna.json

It outputs a json file that looks like this:

    {
      "seqname": "chr10", 
      "tss": 100148265, 
      "strand": "-", 
      "gene_id": "ENSG00000119943", 
      "transcripts": [
        {
          "seqname": "chr10", 
          "end": 100148193, 
          "start": 100146958, 
          "attribute": {
            "transcript_status": "KNOWN", 
            "gene_status": "KNOWN", 
            "havana_gene": "OTTHUMG00000018877.1", 
            "level": "2", 
            "transcript_type": "processed_transcript", 
            "gene_id": "ENSG00000119943.6", 
            "transcript_id": "ENST00000464808.1", 
            "havana_transcript": "OTTHUMT00000049784.1", 
            "gene_type": "protein_coding", 
            "transcript_name": "PYROXD2-003", 
            "gene_name": "PYROXD2"
          }, 
          "frame": ".", 
          "feature": "transcript", 
          "source": "HAVANA", 
          "length": 1235, 
          "score": ".", 
          "tss": 100148193, 
          "strand": "-"
        }
      ], 
      "samples": {
        "E071": {
          "rpkm": "3.931"
        }, 
        "E016": {
          "rpkm": "2.902"
        }, 
        "E120": {
          "rpkm": "11.220"
        }, 
        "E062": {
          "rpkm": "2.938"
        }, 
        "E003": {
          "rpkm": "0.461"
        }, 
        "E028": {
          "rpkm": "2.277"
        }, 
        "E000": {
          "rpkm": "7.299"
        }, 
        "E007": {
          "rpkm": "2.058"
        }, 
        "E006": {
          "rpkm": "2.482"
        },
      }
    }
