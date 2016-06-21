"""
File: Voting.py
Project: Predicting Outcomes of Adverse Drug Reactions
Author: Kathy Chowaniec
File Description:
This script uses the Voting classifer method to predict the outcome of test data
from the FAERS dataset for each outcome file based on the majority vote by the
Logistic Regression and Naive-Bayes methods. Soft weights are used to give Logistic
Regression more of a vote than Naive-Bayes.The accuracies of each prediction is
printed as the output.
"""

#voting

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import accuracy_score
from sklearn.cross_validation import train_test_split
from sklearn.ensemble import VotingClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression

#read the outcome files and split the information from the outcome
def loadData(fname):
    info=[]
    outcome=[]
    f=open(fname)
    for line in f: 
        case,result=line.strip().split('\t') #split on tab delimeter to separate info from outcome
        info.append(case.lower()) #store information
        outcome.append(int(result)) #store outcome
    f.close()
    return info, outcome

outcome_list=('DE', 'LT', 'HO', 'DS', 'CA', 'RI', 'OT')

#for each outcome file, get training and test data to build a model and predict outcomes
for o in outcome_list:
    info,outcome=loadData('Outcomes' + '/' + o +'.txt')  
    
    #split data into training and test datasets
    train, test, labels_train, labels_test = train_test_split(info, outcome, test_size=0.33)

    counter = CountVectorizer()
    counter.fit(train)

    #count the number of times each term appears in a document and transform each doc into a count vector
    counts_train = counter.transform(train)#transform the training data
    counts_test = counter.transform(test)#transform the testing data
    
    #build a classifier on the training data using LR and NB
    clf1 = LogisticRegression()
    clf2 = MultinomialNB()

    #build a voting classifer - give logistic regression twice as much weight
    eclf = VotingClassifier(estimators=[('lr', clf1), ('mnb', clf2)], voting='soft', weights = [2,1])

    #train all classifier on the same datasets
    eclf.fit(counts_train,labels_train)

    #use hard voting to predict (majority voting)
    predicted=eclf.predict(counts_test)
 
    #print the accuracy
    print 'Accuracy of', o, 'prediction: ', accuracy_score(predicted,labels_test)
