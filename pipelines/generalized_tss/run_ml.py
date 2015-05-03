#!/usr/bin/env python

# Adapted from sklearn example randomforest code
# http://scikit-learn.org/dev/modules/ensemble.html#random-forests 
# Authors: Jan Hendrik Metzen <jhm@informatik.uni-bremen.de>
# License: BSD 3 clause
import numpy as np
#import matplotlib.pyplot as plt
from sklearn.cross_validation import cross_val_score
from sklearn.ensemble import RandomForestClassifier
from src.utils import FileProgress

import operator
import itertools
import json
import sys

def listsum(numList):
   if len(numList) == 1:
        return numList[0]
   else:
        return numList[0] + listsum(numList[1:])

# Main Method
def main(argv):
    if len(sys.argv) != 2:
        sys.stderr.write("invalid usage: python ensembe_test.py <all_level1.json>\n")
        sys.exit(2)


    keys=[
        #core marks
        "H3K4me1",
        "H3K4me3",
        "H3K27me3",
        "H3K36me3",
        "H3K9me3",

        "H2A.Z",
        "H3K4me2",
        "H3K27ac",
        "H4K20me1",
        "H3K9ac",
        "DNase",
        "H3K79me2"
    ]
    ranges = (25, 35)


    # Load file
    tss_list =[]
    datapoint_list=[]
    file = sys.argv[1]
    progress = FileProgress(file, "Reading file: ")
    with open(file) as json_file:
        for line in json_file:
            tss_dict = json.loads(line)
            tss_list.append(tss_dict)
            for sample in tss_dict.values():
                remove = False
                for mark in keys:
                    if mark not in sample:
                        remove = True
                if remove: continue
                datapoint_list.append(sample)
            progress.update()
    sys.stderr.write("\nFinished reading file\n")


    # For regression, create vector
    X = []
    Y_R = []
    for datapoint in datapoint_list:

        # Assign feature vector
        exprmt_feature_vector=[]
        for mark in keys:
            if type(datapoint[mark]) is list:
                reads_in_range = listsum(datapoint[mark][ranges[0]:ranges[1]])
                exprmt_feature_vector.append(reads_in_range)
            else:
                exprmt_feature_vector.append(datapoint[mark])

        # Assing feature label
        if datapoint["delta_rpkm"] < 0:
            datapoint["delta_rpkm"] = 0
        if datapoint["max_rpkm"] == 0:
            # This gene is not expressed
            exprmt_label = 0
        else:
            exprmt_label = datapoint["delta_rpkm"] / datapoint["max_rpkm"]

        # Add both vectors
        X.append(exprmt_feature_vector)
        Y_R.append(exprmt_label)

    # Classify feature labels into binary space
    label_cutoff = np.median(Y_R)
    print "label cutoff: " + str(label_cutoff)
    Y_C = []
    for datapoint in datapoint_list:

        # Recaulate feature label (for classification)
        if datapoint["delta_rpkm"] < 0:
            datapoint["delta_rpkm"] = 0
        if datapoint["max_rpkm"] == 0:
            # This gene is not expressed
            exprmt_label = 0
        else:
            exprmt_label = datapoint["delta_rpkm"] / datapoint["max_rpkm"]
        Y_C.append(int(float(exprmt_label) < label_cutoff))

    print "mean label: " + str(np.mean(Y_R))
    print "median label: " + str(np.median(Y_R))


    """
    ### DUPLICATE
    # Perform the same thing for items stratified by mark type
    samples_features_and_labels={}
    for mark in sample_dicts.keys():
        samples_features_and_labels[mark]={}
        samples_features_and_labels[mark]["X"]=[]
        samples_features_and_labels[mark]["Y_R"]=[]
        samples_features_and_labels[mark]["Y_C"]=[]
        for datapoint in sample_dicts[mark]:
            exprmt_feature_vector=[]
            for mark in keys:
                exprmt_feature_vector.append(datapoint[mark])

             # Calculate feature label
            if datapoint["delta_rpkm"] < 0:
                datapoint["delta_rpkm"] = 0
            if datapoint["max_rpkm"] == 0:
                # This gene is not expressed
                exprmt_label = 0
            else:
                exprmt_label = datapoint["delta_rpkm"] / datapoint["max_rpkm"]

            samples_features_and_labels[mark]["X"].append(exprmt_feature_vector)
            samples_features_and_labels[mark]["Y_R"].append(exprmt_label)
            samples_features_and_labels[mark]["Y_C"].append(int(float(exprmt_label) < label_cutoff))
    """

    print "number of datapoints: " + str(len(Y_C))

    # Permutate the datapoints
    perms = np.random.permutation(len(X))
    X_p=[]
    Y_C_p=[]
    Y_R_p=[]
    for i in range (0,len(X)):
        X_p.append(X[perms[i]])
        Y_C_p.append(Y_C[perms[i]])
        Y_R_p.append(Y_R[perms[i]])

    Y_C=Y_C_p
    X=X_p

    """
    for sample in samples_features_and_labels.keys():
        X_sample=samples_features_and_labels[sample]["X"]
        Y_sample_C=samples_features_and_labels[sample]["Y_C"]
        Y_sample_R=samples_features_and_labels[sample]["Y_R"]
        perms = np.random.permutation(len(X_sample))
        X_sample_p=[]
        Y_sample_R_p=[]
        Y_sample_C_p=[]
        for i in range(0,len(X_sample)):
            X_sample_p.append(X_sample[perms[i]])
            Y_sample_C_p.append(Y_sample_C[perms[i]])
            Y_sample_R_p.append(Y_sample_R[perms[i]])
        samples_features_and_labels[sample]["X"]=X_sample_p
        samples_features_and_labels[sample]["Y_C"]=Y_sample_C_p
        samples_features_and_labels[sample]["Y_R"]=Y_sample_R_p
    """


    # Regression!
    print "len Y_C: " + str(len(Y_C))
    print "len X: " + str(len(X))
    print "len X[0]: " + str(len(X[0]) )

    for n_estimators in [10,50,150]:
        for depth in [8,12]:
            clf =RandomForestClassifier(n_estimators=n_estimators,max_depth=depth,
                    min_samples_split=10, random_state=0)

            clf.fit(X,Y_C)
            print "n_estimators: " + str(n_estimators)
            print "depth: " + str(depth)
            feature_importances = clf.feature_importances_

            print "feature_importances: "
            for i in range(0,len(keys)):
                print "\t" + keys[i] + ":\t" + str(feature_importances[i])


            """
            print "score by experiment:"
            mean_acc=[]
            for sample in samples_features_and_labels.keys():
                Y_C_sample=samples_features_and_labels[sample]["Y_C"]
                X_sample=samples_features_and_labels[sample]["X"]
                print "\t" +sample+": "+str(len(X_sample))+" points"
                sample_scores=cross_val_score(clf,X_sample,Y_C_sample)
                mean_acc.append(np.mean(sample_scores)*(float(len(X_sample)/float(num_points))))
                print "\t"+sample+" test accuracy: "+str(np.mean(sample_scores))
            print "average sample accuracy:"+str(sum(mean_acc))
            """

            scores = cross_val_score(clf, X, Y_C)
            print "RandomForest mean cross validation score: " + str( scores.mean())

# Execute this module as a command line script
if __name__ == "__main__":
    main(sys.argv[1:])
