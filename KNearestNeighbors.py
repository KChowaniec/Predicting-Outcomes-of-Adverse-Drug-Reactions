"""
File: KNearestNeighbors.py
Project: Predicting Outcomes of Adverse Drug Reactions
Author: Kathy Chowaniec
File Description:
This script uses KNN to predict the outcome using a 20,000 document random sampling 
of the FAERS dataset. GridSearchCV is used to determine the best value of k for
each of the different outcome files. The accuracies of the prediction using
the optimal K is printed as the output.
"""
#KNN method

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import accuracy_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn.cross_validation import train_test_split
from sklearn.grid_search import GridSearchCV
import random

#read the outcome files and split by document and outcome
def loadData(fname):
    info=[]
    outcome=[]
    f=open(fname)
    count = 0
    lines= list()
    for line in f:
        lines.append(line)
    f.close()
    f = random.sample(lines, 20000) #take a random sample of 20,000 documents for KNN
    for line in f: 
            case,result=line.strip().split('\t') #split based on information and outcome
            info.append(case.lower())
            outcome.append(int(result))
            count+=1
    return info, outcome

outcome_list=('DE', 'LT', 'HO', 'DS', 'CA', 'RI', 'OT')

#for each outcome file, split data into test and training and build model
for o in outcome_list:
    info,outcome=loadData('Outcomes' + '/' + o +'.txt')    
    
    #split into training and test data  
    train, test, labels_train, labels_test = train_test_split(info, outcome, test_size=0.33)

    counter = CountVectorizer()
    counter.fit(train)

    #count the number of times each term appears in a document and transform each document into a count vector
    counts_train = counter.transform(train)#transform the training data
    counts_test = counter.transform(test)#transform the testing data
    

    #build the parameter grid using k = 5,10,20
    param_grid = [
    {'n_neighbors': [5,10,20],'weights':['uniform','distance']}
    ]

    #build a grid search to find the best parameters
    clf = GridSearchCV(KNeighborsClassifier(), param_grid, cv=10)

    #run the grid search
    clf.fit(counts_train,labels_train)

    #print the score for each parameter setting
    for params, mean_score, scores in clf.grid_scores_:
        print params, mean_score

    #print the best parameter setting
    print "\nBest parameters",clf.best_params_

    #use best parameters to run on knn
    KNN=KNeighborsClassifier(n_neighbors=clf.best_params_['n_neighbors'])
    KNN.fit(counts_train,labels_train)

    #use the classifier to predict
    predicted=KNN.predict(counts_test)

    #print the accuracy
    print 'Accuracy of', o, 'prediction: ', accuracy_score(predicted,labels_test), '\n'
