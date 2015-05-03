# Adapted from sklearn example randomforest code
# http://scikit-learn.org/dev/modules/ensemble.html#random-forests 
# Authors: Jan Hendrik Metzen <jhm@informatik.uni-bremen.de>
# License: BSD 3 clause
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cross_validation import cross_val_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import AdaBoostClassifier
from sklearn.ensemble import AdaBoostRegressor
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.kernel_ridge import KernelRidge
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

#parse data in to feature vectors and labels:
fn=sys.argv[1]
exons_file = open(fn)
exon_dicts =[]
experiment_dicts=[]
sample_dicts={}
for l in exons_file:
    exon_dict=json.loads(l)
    exon_dicts.append(exon_dict)
    for key in exon_dict.keys():
        if type(exon_dict[key]) == dict:
            if len(exon_dict[key]) < 5: 
                continue
            if not sample_dicts.has_key(key):
                sample_dicts[key]=[]
            experiment_dicts.append(exon_dict[key])
            sample_dicts[key].append(exon_dict[key])
exons_file.close()
'''
keys=[
"H2A.Z_num_reads_five_p",
"H3K4me1_num_reads_five_p",
"H3K4me2_num_reads_five_p",
"H3K4me3_num_reads_five_p",
"H3K9ac_num_reads_five_p",
"H3K9me3_num_reads_five_p",
"H3K27ac_num_reads_five_p",
"H3K27me3_num_reads_five_p",
"H3K36me3_num_reads_five_p",
"H3K79me2_num_reads_five_p",
"H4K20me1_num_reads_five_p",
"DNase_num_reads_five_p",

#"H2A.Z_num_reads_three_p",
#"H3K4me1_num_reads_three_p",
#"H3K4me2_num_reads_three_p",
#"H3K4me3_num_reads_three_p",
#"H3K9ac_num_reads_three_p",
#"H3K9me3_num_reads_three_p",
#"H3K27ac_num_reads_three_p",
#"H3K27me3_num_reads_three_p",
#"H3K36me3_num_reads_three_p",
#"H3K79me2_num_reads_three_p",
#"H4K20me1_num_reads_three_p",
#"DNase_num_reads_three_p",
]
'''
keys=[
    "H3K9me3_num_reads_five_p",
    "H3K27me3_num_reads_five_p",
    "H3K36me3_num_reads_five_p",
    "H3K4me3_num_reads_five_p",
    "H3K4me1_num_reads_five_p",
#    "H3K9me3_num_reads_three_p",
#    "H3K27me3_num_reads_three_p",
#    "H3K36me3_num_reads_three_p",
#    "H3K4me3_num_reads_three_p",
#    "H3K4me1_num_reads_three_p"
    ]
label="p_inc"
labels=[0,1]

X=[]
Y_R=[]#for regression
for i in experiment_dicts:
    exprmt_feature_vector=[]
    for k in keys:
        exprmt_feature_vector.append(i[k])
    exprmt_label=i[label]
    X.append(exprmt_feature_vector)
    Y_R.append(exprmt_label)

#label_cutoff=np.median(Y_R)
label_cutoff=np.median(Y_R)
print "label cutoff: "+str(label_cutoff)
Y_C=[]#for classification
for i in experiment_dicts:
    exprmt_label=i[label]
    Y_C.append(int(float(exprmt_label)<label_cutoff))

print "mean label: "+str(np.mean(Y_R))
print "median label: "+str(np.median(Y_R))
samples_features_and_labels={}
for key in sample_dicts.keys():
    samples_features_and_labels[key]={}
    samples_features_and_labels[key]["X"]=[]
    samples_features_and_labels[key]["Y_R"]=[]
    samples_features_and_labels[key]["Y_C"]=[]
    for i in sample_dicts[key]:
        exprmt_feature_vector=[]
        for k in keys:
            exprmt_feature_vector.append(i[k])
        exprmt_label=i[label]
        samples_features_and_labels[key]["X"].append(exprmt_feature_vector)
        samples_features_and_labels[key]["Y_R"].append(exprmt_label)
        samples_features_and_labels[key]["Y_C"].append(int(float(exprmt_label)<label_cutoff))

num_points = len(Y_C)
train_size = int(num_points*0.8)
test_size = num_points-train_size
print "number of datapoints: " + str(num_points)

Y_R_sorted=sorted(Y_R)
buckets=[0]*9
for i in range(0,9):
    buckets[i]=Y_R_sorted[(i)*len(Y_R_sorted)/9]

Y_R_decile=[0]*len(Y_R)
for i in range(0,len(Y_R)):
    bucket=0
    label=Y_R[i]
    while bucket<9 and Y_R[i]> buckets[bucket]:
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
    


train_X=X[0:train_size]
train_Y_C=Y_C[0:train_size]
train_Y_R=Y_R[0:train_size]
train_Y_R_decile=Y_R_decile[0:train_size]

test_X=X[train_size:train_size+test_size]
test_Y_C=Y_C[train_size:train_size+test_size]
test_Y_R=Y_R[train_size:train_size+test_size]
test_Y_R_decile=Y_R_decile[train_size:train_size+test_size]

'''
print "test_Y true labels\t" + str(test_Y_C)

print "label == 0: " + str(float(Y_C.count(0))/len(Y_C))
print "label == 1: " + str(float(Y_C.count(1))/len(Y_C))
'''


# Regression!
'''
for a in [0.00001,0.0001, 0.001,0.01,0.1,1]:
    clf = linear_model.Lasso(alpha=a,copy_X=True)#,normalize=True)
    clf.fit(train_X,train_Y_R_decile)
    Y_R_predicted=clf.predict(test_X)
    MSE=((np.array(test_Y_R_decile) - np.array(Y_R_predicted)) ** 2).mean()
    print "with alpha =" + str(a)+" MSE="+str(MSE)
    print "params: " + str(clf.get_params())
    Y_R_predicted_print = [ '%.2f' % elem for elem in Y_R_predicted ]
    test_Y_R_print = [ '%.2f' % elem for elem in Y_R_decile ]
    print "first 10 labels predicted: \t"+str(Y_R_predicted_print[0:10])
    print "first 10 labels real:\t\t"+str(list(test_Y_R_print[0:10]))
    scores = cross_val_score(clf, train_X, train_Y_R_decile)
    print "Lasso mean cross validation score: " + str( scores.mean())
    print "\n\n"
    for key in sample_dicts.keys()
        sample_dicts[key]
'''
'''
# Random Forest Regressor
print "testing Regressor"
print "size of training set: "+str(len(train_Y_R_decile))
for j in [20,200]:
    for i in [8,10,13]:
    #   clf = AdaBoostRegressor(n_estimators=j)
        clf = RandomForestRegressor(n_estimators=j,
            max_depth=i, min_samples_split=10, random_state=0)
#        clf=GradientBoostingRegressor(n_estimators=100,learning_rate=i)
        clf.fit(train_X,train_Y_R_decile)
        #clf.fit(train_X,train_Y_R)
        Y_R_predicted=clf.predict(test_X)
        #MSE=((np.array(test_Y_R) - np.array(Y_R_predicted)) ** 2).mean()
        MSE=((np.array(test_Y_R_decile) - np.array(Y_R_predicted)) ** 2).mean()
        print "params: " + str(clf.get_params())
        print "\tmax_depth= "+str(j)
        print "\tlearning_rate= "+str(i)
        print "\tMSE="+str(MSE)
        Y_R_predicted_print = [ '%.2f' % elem for elem in Y_R_predicted ]
        test_Y_R_print = [ '%.2f' % elem for elem in Y_R_decile ]
        #test_Y_R_print = [ '%.2f' % elem for elem in Y_R ]
        Y_C_predicted=np.array(Y_R_predicted)<=np.median(Y_R_decile)
        accuracy=(100*(float(sum(test_Y_C==Y_C_predicted)))/len(test_Y_C))
        p_1 =float(sum(test_Y_C==(np.array([1]*len(test_Y_C)))))/len(test_Y_C)
        p_1_pred = float(sum(Y_C_predicted==1))/len(Y_C_predicted)
        print "\tp 1:" +str(p_1)+ "\n\tp 1 predicted: "+ str(p_1_pred)
        print "\ttest accuracy: "+str(accuracy)
        print "first 10 labels predicted: \t"+str(Y_R_predicted_print[0:10])
        print "first 10 labels real:\t\t"+str(list(test_Y_R_print[0:10]))
#        scores = cross_val_score(clf, train_X, train_Y_R_decile)
#        print "Random Forest Regressio mean cross validation score: " + str( scores.mean())
        print "\n\n"
        '''
for j in [30,50,100]:
    clf = RandomForestClassifier(n_estimators=j,
        max_depth=10, min_samples_split=10, random_state=0)
#    clf = AdaBoostClassifier(n_estimators=j)
    clf.fit(train_X,train_Y_C)
    # print "params: "+str(clf.get_params())
    # print "estimators: "+str(clf.estimators_)
    feature_importances = clf.feature_importances_
    print "feature_importances: "
    for i in range(0,len(keys)):
        print "\t"+keys[i]+":\t"+str(feature_importances[i])
    print "score by experiment:"
    Y_C_predicted=clf.predict(test_X)
    p_1 =float(sum(test_Y_C==(np.array([1]*len(test_Y_C)))))/len(test_Y_C)
    p_1_pred = float(sum(Y_C_predicted==1))/len(Y_C_predicted)
    print "\tp 1:" +str(p_1)+ "\n\tp 1 predicted: "+ str(p_1_pred)
    mean_acc=[] 
    for sample in samples_features_and_labels.keys():
        Y_C_sample=samples_features_and_labels[sample]["Y_C"]
        X_sample=samples_features_and_labels[sample]["X"]
        print "\t" +sample+": "+str(len(X_sample))+" points"
     #   tr_size= int(float(len(X_sample))*0.8)
     #   te_size= len(X_sample)-tr_size
     #   Y_C_sample_tr=Y_C_sample[0:tr_size]
     #   Y_C_sample_te=Y_C_sample[tr_size:tr_size+te_size]
     #   X_sample_tr=X_sample[0:tr_size]
     #   X_sample_te=X_sample[tr_size:tr_size+te_size]
        sample_scores=cross_val_score(clf,X_sample,Y_C_sample)
     #   pred=clf.predict(X_sample_te)
     #   accuracy=(100*(float(sum(Y_C_sample_te==pred)))/len(Y_C_sample_te))
        #mean_acc.append(accuracy*(float(len(X_sample)/float(num_points))))
        mean_acc.append(np.mean(sample_scores)*(float(len(X_sample)/float(num_points))))
        #print "\t"+sample+" test accuracy: "+str(accuracy)
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

    plt.suptitle("Adaboost decision boundaries on best two dimensions.")
    plt.axis("tight")
    plt.show()
