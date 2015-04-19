Things Jeff is Working On
-------------------------

###Questions that Jeff is asking right now:###
* Can we train a model on genes that only have one TSS site?
    * Implies we need to filter for all genes that only have one TSS site, and get that location
        * I should check to see that none of these locations overlap by our definition of GRANULARITY. If they overlap, I should remove them.
    * Get the RNA data RPKMe/RPKMg of the closest exon (withint GRANULARITY). Return if RPKM > 1, as our definition for expressed.
* Can we train a model on genes that have exactly two TSS sites?
    * Implies we need to filter for all genes that have exactly two TSS sites, and get those locations.
        * I should check to see that none of these locations overlap by our definition of GRANULARITY. If they overlap, I should remove them.
   
    * Get the RNA data (


###Priority:###
* ~~GTF class~~ -- **DONE**
* Import GTF file -- **CAN DO**
* Filter GTF file for feature or attributes -- **HACKED/DONE**
* Produce a list of TSS coordinate in json format -- **IN PROGRESS**

###Other Things:###
* Package GTF utils into one file
* Documentation

Things Brian is Working On
--------------------------

###Priority###
* Write script to break output of ChIP\_extract.py into individual experiment (i.e. by gene or by tissue type)
* Use ChIP-Seq Metadata to scale read-count by number of reads in experiment


###Other Things###
* Find out if a logistic model can be trained if not all data points have every feature defined
* consider inclduding expression of snRNAs as additona features in the feature vector we train on.

###Completed###
* ~~Write first iteration of ChIP-Seq read count extraction~~ -- **DONE**
* ~~Update find\_sites.py to take experiment ID and sample ID as command line argumentsand carry them into the output~~ -- **DONE**
* ~~update find\_sites.py to take gene orientation into account~~ -- **DONE**
* ~~Write bash script to automate the running of this script once the TSS coordinates are available~~ -- **DONE**
        -download, decompress, parse revelant info and delete continuously
* ~~Script to break up list of experiments into chunks and run extract\_chip.sh~~ -- **DONE**
* ~~Python Script to merge the results from multiple outputs of extract\_ChIP.sh~~ -- **DONE**
* ~~Python Script to sort JSON dictionaries by chromosome and location~~ -- **DONE**

###Additional things to think about/relevant papers###
* [H3K4me3 leads to recruitment of splicing factors](http://www.ncbi.nlm.nih.gov/pmc/articles/PMC2276655/pdf/nihms35172.pdf)
 * Published out of James Manleys goup

* [H3K36me3 at lower levels in AS exons](http://liulab.dfci.harvard.edu/publications/Kolasinska\_H3K36me3\_NatGen\_2009.pdf)
 * Published by Shirley Liu, a former student of Marty

* Null hypothesis supported by potentially sequence specific role of [snRNAs](http://en.wikipedia.org/wiki/Small\_nuclear\_RNA)
 
* Should we consider final exons? Perhaps their are signals for end of transcription (e.g.histone marks recruiting factors that end transcription)

* When considering AS, it seems that for the 3 prime exon sites, we are primarily concerned with the state of the around the adenosine 20-40 bp upstream of the exon start that attacks the 5 prime exon end.
 * **NO, ChIP Resolution is not high enough**

* For 5 prime exon sites, we are concerned with the sequences downstream of the end of the exon.

* Consider ignoring [splicing that does not go through the major splicing pathway](http://en.wikipedia.org/wiki/Minor_spliceosome)
 * It is possible that the selection mechanisms are different from the major pathways so including them may introduce noise into our data.

* Consider adding reads within upstream/ dowstream ranges as separate features

* Checking assumptions we are making with scaling down by read counts. 
* Using Narrow/Broad peaks insatead of reads within a BP range of sites of interst


###TSS###
####Possible Experimental Question:####
For genes with two TSS observed in our data set, can histone state around these sites predict which TSS predominates?

####General Data Subset Selection ####
#####Limit data pool to the set of genes, G, such that for every g\_i in G#####
* g\_i is expressed is a signifcant portion of the samples
* g\_i has exactly two observed TSS in our data-set
* The two TSSs of g\_i are sufficiently separated to be differentiaed by ChIP labels (ideally ~1Kb cutoff)
* A significant portion of cell-line samples use the other TSS (perhaps ~20% cutoff)
 * drop data points from samples where the level of expression is below some threshold

####Feature Vectors and Labels ####
#####For all g\_i in G, we will have a feature vector x\_i and a label y\_i.#####
* x\_i is a 10 dimentional vector, 5 dimensions representing the states of the core histone marks for each TSS.
* y\_i is a real number, that is the portion of transcripts that used the first site 
 * we can consider binarizing this (e.g. TSS 1 is most frequently used)

###AS###
####Possible Experimental Question:
For exons with that have observed alternative splicing in our data set, can histone state around these sites predict the exon with be included?

####General Data Subset Selection
#####Limit data pool to the set of exons, E, such that for every e\_i in E#####
* e\_i is expressed is a signifcant portion of the samples
* e\_i shows a significant range of inclusion/exclusion ratio our data-set
 * drop data points from samples where the level of expression is below some threshold
* (perhaps, there is significant variation in the histon state in the region)

####Feature Vectors and Labels
#####For all e\_i in E, we will have a feature vector x\_i and a label y\_i.#####
* x\_i is a 10 dimentional vector, 5 dimensions representing the states of the core histone marks for the 3' and 5' ends
* y\_i is a real number, that is the portion of transcripts that used the first site 
 * we can consider binarizing this (e.g. exon is usually used)
