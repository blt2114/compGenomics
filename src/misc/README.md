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