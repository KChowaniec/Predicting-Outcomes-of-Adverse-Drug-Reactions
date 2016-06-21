"""
File: LogisticRegression.py
Project: Predicting Outcomes of Adverse Drug Reactions
Author: Kathy Chowaniec
File Description:
This script uses Logistic Regression to predict the outcome of test data from 
the FAERS dataset for each outcome file. The accuracies of each prediction is
printed as the output.
"""
#Logistic Regression method

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import accuracy_score
from sklearn.cross_validation import train_test_split
from sklearn.linear_model import LogisticRegression

#read each outcome file and split document by information and outcome
def loadData(fname):
    info=[]
    outcome=[]
    f=open(fname)
    for line in f: 
        case,result=line.strip().split('\t') #split based on tab to separate info from outcome
        info.append(case.lower()) #store information
        outcome.append(int(result)) #store outcome
    f.close()
    return info, outcome

outcome_list=('DE', 'LT', 'HO', 'DS', 'CA', 'RI', 'OT')

#for each outcome file, get training and test dataset and build classifier to predict on test data
for o in outcome_list:
    info,outcome=loadData('Outcomes' + '/' + o +'.txt')  
    
    #split data into training and test datasets     
    train, test, labels_train, labels_test = train_test_split(info, outcome, test_size=0.33)

    counter = CountVectorizer()
    counter.fit(train)

    #count the number of times each term appears in a document and transform each doc into a count vector
    counts_train = counter.transform(train)#transform the training data
    counts_test = counter.transform(test)#transform the testing data
    
    #Logistic Regression classifier
    LR = LogisticRegression() 
    
    #build a classifier on the training data
    LR.fit(counts_train,labels_train)
    
    #use the classifier to predict
    predicted=LR.predict(counts_test)

    #print the accuracy
    print 'Accuracy of', o, 'prediction: ', accuracy_score(predicted,labels_test)
