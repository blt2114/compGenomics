# Adapted from sklearn example randomforest code
# http://scikit-learn.org/dev/modules/ensemble.html#random-forests 
# Authors: Jan Hendrik Metzen <jhm@informatik.uni-bremen.de>
# License: BSD 3 clause
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error
from sklearn.cross_validation import cross_val_score
from sklearn.ensemble import RandomForestRegressor
#from sklearn.ensemble import AdaBoostClassifier
#from sklearn import linear_model
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
'''
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
        "H2A.Z_num_reads_five_p",
        "H3K4me2_num_reads_five_p",
        "H3K9ac_num_reads_five_p",
        "H3K27ac_num_reads_five_p",
        "H3K79me2_num_reads_five_p",
        "H4K20me1_num_reads_five_p",
        "DNase_num_reads_five_p",

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

def regression_acc_heat_map(Y_pred,Y_true,n_buckets):
    # assing y's in Y_pred to bucket
    for i in range(0,len(Y_pred)):
        Y_pred[i]-=Y_pred[i]%(0.02)
        if (Y_pred[i])>max(Y_true):
            Y_pred[i]=max(Y_true)
    
    for i in range(0,len(Y_pred)):
        Y_true[i]=int(n_buckets*Y_true[i])
        Y_pred[i]=int(n_buckets*Y_pred[i])
    intersection_mat = [[0]*n_buckets]*n_buckets
    intersection_mat= np.matrix(intersection_mat)
    for true_bucket in range(0,n_buckets):
        true_idxs=[]
        for i in range(0,len(Y_true)):
            if Y_true[i]==true_bucket:
                true_idxs.append(i)
        for pred_bucket in range (0,n_buckets):
            for i in range(0,len(Y_pred)):
                if Y_pred[i]==pred_bucket:
                    if not true_idxs.count(i) == 0:
                        intersection_mat[true_bucket,pred_bucket]+=1
    return np.matrix(intersection_mat)
                


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

Y_R_sorted=sorted(Y_R)
num_buckets = 50
cuttoffs=[0]*(num_buckets-1)
for i in range(0,len(cuttoffs)):
    cuttoffs[i]=Y_R_sorted[(i+1)*len(Y_R_sorted)/num_buckets]

Y_R_decile=[0]*len(Y_R)
for i in range(0,len(Y_R)):
    bucket=1
    cuttoff = 0;
    label=Y_R[i]
    while bucket<num_buckets and Y_R[i]> cuttoff:
        cuttoff = cuttoffs[bucket-1]
        bucket+=1
    Y_R_decile[i]=(float(bucket-1)/num_buckets)

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


num_points = len(Y_C)
print "number of datapoints: " + str(num_points)
train_size=int(float(num_points)*0.8)
test_size=num_points-train_size
train_X=X[0:train_size]
#train_Y_C=Y_C[0:train_size]
#train_Y_R=Y_R[0:train_size]
train_Y_R_decile=Y_R_decile[0:train_size]

test_X=X[train_size:train_size+test_size]
#test_Y_C=Y_C[train_size:train_size+test_size]
#test_Y_R=Y_R[train_size:train_size+test_size]
test_Y_R_decile=Y_R_decile[train_size:train_size+test_size]

# Regression!

print "len Y_C: "+str(len(Y_C)) 
#print "len train_Y_R[0]: "+str(len(train_Y_R[0]) )
print "len X: "+str(len(X)) 
print "len X[0]: "+str(len(X[0]) )

# Random Forest Regressor
print "testing Regressor"
#print "size of training set: "+str(len(train_Y_R_decile))
for j in [10]:
    for i in [12]:
    #   clf = AdaBoostRegressor(n_estimators=j)
        clf = RandomForestRegressor(n_estimators=j,
            max_depth=i, min_samples_split=10, random_state=0)
        print "\tmax_depth= "+str(i)
        print "\tn_estimators= "+str(j)
        scores = cross_val_score(clf, X,Y_R_decile,scoring= lambda clf,X,Y: mean_squared_error(Y,clf.predict(X)))
        print "Random Forest Regressio mean cross validation score: " + str( scores.mean())
        print "\n\n"                                                 
        
#        clf=GradientBoostingRegressor(n_estimators=100,learning_rate=i)
        clf.fit(train_X,train_Y_R_decile)
        #clf.fit(train_X,train_Y_R)
        Y_R_decile_predicted=list(clf.predict(test_X))
        MSE=mean_squared_error(Y_R_decile_predicted,test_Y_R_decile)
        print "\tMSE="+str(MSE)
        heat_matrix=regression_acc_heat_map(Y_R_decile_predicted,test_Y_R_decile,num_buckets)


imgplot=plt.imshow(heat_matrix)
fig = plt.figure(figsize=(6, 5.2)) 
imgplot.set_cmap('spectral')
plt.colorbar()
#ax = fig.add_subplot(111)
#ax.set_title('colorMap')
print str(heat_matrix)
#ax.set_aspect('equal')

#cax = fig.add_axes([0,1,2,3])
imgplot.set_interpolation('nearest')
#cax.get_xaxis().set_visible(False)
#cax.get_yaxis().set_visible(False)
#cax.set_frame_on(False)
#plt.colorbar(orientation='vertical')
plt.show()

'''
fig, ax = plt.subplots()
heatmap = ax.pcolor(heat_matrix, cmap=plt.cm.Blues, alpha=0.8)
# put the major ticks at the middle of each cell
ax.set_xticks(np.arange(heat_matrix.shape[0])+0.5, minor=False)
ax.set_yticks(np.arange(heat_matrix.shape[1])+0.5, minor=False)

# want a more natural, table-like display
ax.invert_yaxis()
ax.axis.tick_top()


# Format

plt.show()



'''










#        MSE=((np.array(test_Y_R_decile) - np.array(Y_R_predicted)) ** 2).mean()
#        print "params: " + str(clf.get_params())
#        Y_R_predicted_print = [ '%.2f' % elem for elem in Y_R_predicted ]
#        test_Y_R_print = [ '%.2f' % elem for elem in Y_R_decile ]
#        #test_Y_R_print = [ '%.2f' % elem for elem in Y_R ]
#        Y_C_predicted=np.array(Y_R_predicted)<=np.median(Y_R_decile)
#        accuracy=(100*(float(sum(test_Y_C==Y_C_predicted)))/len(test_Y_C))
#        p_1 =float(sum(test_Y_C==(np.array([1]*len(test_Y_C)))))/len(test_Y_C)
#        p_1_pred = float(sum(Y_C_predicted==1))/len(Y_C_predicted)   
#        print "\tp 1:" +str(p_1)+ "\n\tp 1 predicted: "+ str(p_1_pred)
#        print "\ttest accuracy: "+str(accuracy)                      
#        print "first 10 labels predicted: \t"+str(Y_R_predicted_print[0:10])       
#        print "first 10 labels real:\t\t"+str(list(test_Y_R_print[0:10]))
'''
        print "score by experiment:"
        mean_acc=[] 
        for sample in samples_features_and_labels.keys():
            Y_C_sample=samples_features_and_labels[sample]["Y_C"]
            X_sample=samples_features_and_labels[sample]["X"]
            print "\t" +sample+": "+str(len(X_sample))+" points"
            sample_scores=cross_val_score(clf,X_sample,Y_R_decile,scorer='mean_squared_error')
            mean_acc.append(np.mean(sample_scores)*(float(len(X_sample)/float(num_points))))
            print "\t"+sample+" test accuracy: "+str(np.mean(sample_scores))
        print "average sample accuracy:"+str(sum(mean_acc))
        '''
