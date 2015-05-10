# Adapted from sklearn example randomforest code
# http://scikit-learn.org/dev/modules/ensemble.html#random-forests 
# Authors: Jan Hendrik Metzen <jhm@informatik.uni-bremen.de>
# License: BSD 3 clause
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cross_validation import cross_val_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import AdaBoostClassifier
from sklearn import linear_model
from sklearn.externals.six.moves import xrange
import operator
import itertools
import json
import sys
if len(sys.argv) != 2:
    sys.stderr.write("invalid usage: python ensembe_test.py"+
            " <exons.txt>\n")
    sys.exit(2)

#names of marks from windowed trials
keys=[ 
        #core marks
        "H3K36me3_reads",
        "H3K4me1_reads",
        "H3K4me3_reads",
        "H3K27me3_reads",
        "H3K9me3_reads",

        "H2A.Z_reads",
        "H3K4me2_reads",
        "H3K27ac_reads",
        "H4K20me1_reads",
        "H3K9ac_reads",
        "DNase_reads",
        "H3K79me2_reads"
        ]
'''
keys=[
#        "H2A.Z_num_reads_five_p",
#        "H3K4me2_num_reads_five_p",
#        "H3K9ac_num_reads_five_p",
#        "H3K27ac_num_reads_five_p",
#        "H3K79me2_num_reads_five_p",
#        "H4K20me1_num_reads_five_p",
#        "DNase_num_reads_five_p",

        #core marks 
        "H3K4me1_num_reads_five_p",
        "H3K4me3_num_reads_five_p",
        "H3K27me3_num_reads_five_p",
        "H3K36me3_num_reads_five_p",
        "H3K9me3_num_reads_five_p",

#        "H3K4me1_num_reads_three_p",
#        "H3K4me3_num_reads_three_p",
#        "H3K27me3_num_reads_three_p",
#        "H3K36me3_num_reads_three_p",
#        "H3K9me3_num_reads_three_p",

#        "H2A.Z_num_reads_three_p",
#        "H3K4me2_num_reads_three_p",
#        "H3K9ac_num_reads_three_p",
#        "H3K27ac_num_reads_three_p",
#        "H3K79me2_num_reads_three_p",
#        "H4K20me1_num_reads_three_p",
#        "DNase_num_reads_three_p",
    ]

'''
#label="p_inc_gene" # for alternative label
label="p_inc"
labels=[0,1]

#these settings work well for casset exons ~75% average accuracy
#min_mean_label=0.000
#label_min=0.000 #  works very well for casset exons
#label_max=1.5

# these setting worked well for all dim scaled 10 to 100
#min_mean_label=0.00
#label_min=0.0000 #
#label_max=1.5

min_exon_var=.000000
min_mean_label=0.00
max_mean_label=100.5
label_min=0.0000 #  works very well for casset exons
label_max=1.5


def exon_label_mean_and_var (exon_dict):
    labels= []
    for key in exon_dict.keys():
        if type(exon_dict[key]) == dict:
            if len(exon_dict[key]) < len(keys): 
                continue
            if not exon_dict[key].has_key(label):
                continue
            labels.append(exon_dict[key][label])
    if not len(labels) == 0:
        label_mean=np.mean(labels)
        label_var=np.var(labels)
    else:
        label_mean=0
        label_var=0
    return label_mean, label_var 

#parse data in to feature vectors and labels:
fn=sys.argv[1]
exons_file = open(fn)
experiment_dicts=[]
sample_dicts={}
for l in exons_file:
    exon_dict=json.loads(l)
    exon_mean, exon_var = exon_label_mean_and_var(exon_dict)
    if exon_mean<min_mean_label:
        continue
    if exon_mean>max_mean_label:
        continue
    if exon_var<min_exon_var:
        continue
    for key in exon_dict.keys():
        if type(exon_dict[key]) == dict:
            if len(exon_dict[key]) < len(keys): 
                continue
            if not exon_dict[key].has_key(label):
                continue
            elif exon_dict[key][label]<label_min:
                continue
            elif exon_dict[key][label]>label_max:
                continue
            experiment_dicts.append(exon_dict[key])

            if not sample_dicts.has_key(key):
                sample_dicts[key]=[]
            sample_dicts[key].append(exon_dict[key])
exons_file.close()

ranges=[
        #           (20,40),
#        (48,52),(45,55) # works well for cassette exons
        (48,52),
        (45,55),
#                (35,50),
#                (50,65),
        #        (30,70),
        ]

X=[]
Y_R=[]#for regression
experiment_dicts_filtered=[]
for i in experiment_dicts:
    exprmt_feature_vector=[]
    for k in keys:
        if type(i[k]) is list:
            for tup in ranges:
                st=tup[0]
                end=tup[1]
                start_read_num=i[k][st]
                end_read_num=i[k][end]
                reads_in_range =end_read_num-start_read_num
                exprmt_feature_vector.append(reads_in_range)
        else:
            exprmt_feature_vector.append(i[k])
    exprmt_label=i[label]
    X.append(exprmt_feature_vector)
    Y_R.append(exprmt_label)
    experiment_dicts_filtered.append(i)

experiment_dicts=experiment_dicts_filtered

label_cutoff =np.median(Y_R)
print "label_cutoff: "+str(label_cutoff)

Y_C=[]#for classification
for i in experiment_dicts:
    exprmt_label=i[label]
    Y_C.append(int(float(exprmt_label)<label_cutoff))

print "p_inc median: "+ str(label_cutoff)
print "p_inc mean: "+ str(np.mean(Y_R))

samples_features_and_labels={}
for key in sample_dicts.keys():
    samples_features_and_labels[key]={}
    samples_features_and_labels[key]["X"]=[]
    samples_features_and_labels[key]["Y_R"]=[]
    samples_features_and_labels[key]["Y_C"]=[]
    for i in sample_dicts[key]:
        exprmt_feature_vector=[]
        if type(i[k]) is list:
            for k in keys:
                for tup in ranges:
                    st=tup[0]
                    end=tup[1]
                    start_read_num=i[k][st]
                    end_read_num=i[k][end]
                    reads_in_range =end_read_num-start_read_num
                    exprmt_feature_vector.append(reads_in_range)
        else:
            for k in keys:
                exprmt_feature_vector.append(i[k])
        exprmt_label=i[label]
        samples_features_and_labels[key]["X"].append(exprmt_feature_vector)
        samples_features_and_labels[key]["Y_R"].append(exprmt_label)
        samples_features_and_labels[key]["Y_C"].append(int(float(exprmt_label)<label_cutoff))

num_points = len(Y_C)
print "number of datapoints: " + str(num_points)
Y_R_sorted=sorted(Y_R)
num_buckets = 10
cuttoffs=[0]*(num_buckets-1)
for i in range(0,len(cuttoffs)):
    cuttoffs[i]=Y_R_sorted[(i+1)*len(Y_R_sorted)/num_buckets]

Y_R_decile=[0]*len(Y_R)
for i in range(0,len(Y_R)):
    bucket=0
    cuttoff = cuttoffs[bucket]
    label=Y_R[i]
    # place the sample in the correct bucket

    #start off assuming it's in the lowest bucket.
    while bucket<(num_buckets-1) and Y_R[i]> cuttoff:
        cuttoff = cuttoffs[bucket]
        bucket+=1
    Y_R_decile[i]=float(bucket)/10

perms = np.random.permutation(len(X))

X_p=[]
Y_C_p=[]
Y_R_p=[]
Y_R_decile_p=[]
for i in range (0,len(X)):
    X_p.append(X[perms[i]])
    Y_C_p.append(Y_C[perms[i]])
    Y_R_p.append(Y_R[perms[i]])
    Y_R_decile_p.append(Y_R_decile[perms[i]])

Y_C=Y_C_p
Y_R=Y_R_p
Y_R_decile=Y_R_decile_p
X=X_p

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


#train_X=X[0:train_size]
#train_Y_C=Y_C[0:train_size]
#train_Y_R=Y_R[0:train_size]
#train_Y_R_decile=Y_R_decile[0:train_size]

#test_X=X[train_size:train_size+test_size]
#test_Y_C=Y_C[train_size:train_size+test_size]
#test_Y_R=Y_R[train_size:train_size+test_size]
#test_Y_R_decile=Y_R_decile[train_size:train_size+test_size]

# Regression!

print "len Y_C: "+str(len(Y_C)) 
#print "len train_Y_R[0]: "+str(len(train_Y_R[0]) )
print "len X: "+str(len(X)) 
print "len X[0]: "+str(len(X[0]) )

for n_estimators in [200]:
    for depth in [8,12]:#12 is good for cassette exons
        clf =RandomForestClassifier(n_estimators=n_estimators,max_depth=depth,
                min_samples_split=20, random_state=0)#min per split was 10
                                                #as good for all_dim/scaled_10_to_200.
                                                # 2 samples per split works
                                                # better for small dataset

        # To make this use AdaBoost not RandomForest, uncomment below.
    #    clf = AdaBoostClassifier(n_estimators=n_estimators)
        clf.fit(X,Y_C)
        # print "params: "+str(clf.get_params())
        print "n_estimators: "+str(n_estimators)
        print "depth: "+str(depth)
        feature_importances = clf.feature_importances_
        print "feature_importances: "
        if len(X[0]) == len(keys):
            for i in range(0,len(keys)):
                print "\t"+keys[i]+":\t"+str(feature_importances[i])
        else:
            for i in range(0,len(ranges)*len(keys)):
                if i%len(ranges) ==0:
                    print ""
                print "\t"+keys[i/len(ranges)]+str(ranges[i%len(ranges)])+":\t"+str(feature_importances[i])
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
        scores = cross_val_score(clf, X, Y_C)
        print "RandomForest mean cross validation score: " + str( scores.mean())

#if only two dimensions are being used, we can plot two dimentionally
if False:
    # Plot decision bondary based on first two dimensions.
    def extrema (lol,index,reverse): # list of lists
        return sorted(lol,key=operator.itemgetter(index),reverse=reverse)[0][index]


    sorted_feature_importances =sorted(feature_importances,reverse=True)
    x_idx = np.where(feature_importances==sorted_feature_importances[0])[0][0]
    y_idx = np.where(feature_importances==sorted_feature_importances[1])[0][0]

    plt.ylabel(keys[y_idx])
    plt.xlabel(keys[x_idx])

    x_min= extrema(X,x_idx,False)
    x_max= extrema(X,x_idx,True) + 1
    y_min= extrema(X,y_idx,False)
    y_max= extrema(X,y_idx,True) + 1
    print "x range: "+str(x_min)+" - " + str(x_max)
    print "y range: "+str(y_min)+" - " + str(y_max)

    plot_step=1
    xx, yy = np.meshgrid(np.arange(x_min, x_max, plot_step),
            np.arange(y_min, y_max, plot_step))

    cmap = plt.cm.RdBu
    Z = clf.predict(np.c_[xx.ravel(), yy.ravel()])
    Z = Z.reshape(xx.shape)
    cs = plt.contourf(xx, yy, Z, cmap=cmap)

    # Plot the training points, these are clustered together and have a
    # black outline
    Y_C_plot=np.array(Y_C)
    plot_colors="rb" # red and blue points
    for i, c in zip(xrange(len(labels)), plot_colors):
        idx = np.where(Y_C_plot == i)
        # only plot the first 500 in each class
        X_vals=np.array(zip(*X)[x_idx])[idx][0:500]
        Y_vals=np.array(zip(*X)[y_idx])[idx][0:500]
        plt.scatter(X_vals,Y_vals, c=c, cmap=cmap,s=8)

    plt.suptitle("Random Forest decision boundaries on best two dimensions.")
    plt.axis("tight")
    plt.show()
