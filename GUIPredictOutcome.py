"""
File: GUIPredictOutcome.py
Project: Predicting Outcomes of Adverse Drug Reactions
Author: Kathy Chowaniec
File Description:
This script accepts the input entered by the user in GUI.py and determines
the predicted outcome(s) using Logistic Regression for each possible outcome.
"""
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.cross_validation import train_test_split
from sklearn.linear_model import LogisticRegression

#read the outcome file and separate the information from the outcome
def loadData(fname):
    info=[]
    outcome=[]
    f=open(fname)
    for line in f: 
        case,result=line.strip().split('\t') #split the line by tab delimeter
        info.append(case.lower()) #store the information
        outcome.append(int(result)) #store the outcomes
    f.close()
    return info, outcome

#function to build logistic regression model to predict outcome on unclassified data
def trainModel(test_data):
    predictions = dict()
    outcome_list=('DE', 'LT', 'HO', 'DS', 'CA', 'RI', 'OT')
    for o in outcome_list:
        info,outcome=loadData('Outcomes' + '/' + o +'.txt')
        #split data into training dataset      
        train, test, labels_train, labels_test = train_test_split(info, outcome, test_size=0.33)
        counter = CountVectorizer()
        counter.fit(train)
        
        #count the number of times each term appears in a document and transform each doc into a count vector
        counts_train = counter.transform(train)#transform the training data
        counts_test = counter.transform(test_data)#transform the new data

        #build a classifier on the training data        
        LR = LogisticRegression()     
        LR.fit(counts_train,labels_train)        
        #use the classifier to predict on new data
        predicted=LR.predict(counts_test)
        
        #determine prediction results
        if 1 in predicted:
            flag = 'yes'
        else:
            flag = 'no'
        predictions[o] = flag #store result of each outcome
    return predictions

#method called in GUI.py to pass in user-entered data
def getPrediction(new_data):
    test = ' '.join(str(v) for v in new_data) #convert list into string
    test = test.lower() #convert text to lowercase
    test_list = test.split() #turn string back into list
    results = trainModel(test_list) #train model and get results
    return results #return prediction