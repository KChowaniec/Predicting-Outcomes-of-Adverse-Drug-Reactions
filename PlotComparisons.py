"""
File: PlotComparisons.py
Project: Predicting Outcomes of Adverse Drug Reactions
Author: Kathy Chowaniec
File Description:
This script compares the accuracies of 3 different classifiers: Logistic Regression,
Naive-Bayes and Voting. The results from this comparison are plotted for each 
outcome. 
"""
#Plot accuracy comparisons between different classifiers for each outcome

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.ensemble import VotingClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score
from sklearn.linear_model import LogisticRegression
from sklearn.cross_validation import train_test_split
import pylab as pl

#read each outcome file and separate information from outcome
def loadData(fname):
    info=[]
    outcome=[]
    f=open(fname)
    for line in f: 
        case,result=line.strip().split('\t') #split based on tab delimeter to separate info from outcome
        info.append(case.lower()) #store information
        outcome.append(int(result)) #store outcome
    f.close()
    return info, outcome

outcome_list=('DE', 'LT', 'HO', 'DS', 'CA', 'RI', 'OT')
outcomes = dict()

#for each outcome file, generate training and test data to use with each classifier
for o in outcome_list:
    info,outcome=loadData('Outcomes' + '/' + o +'.txt')    
    train, test, labels_train, labels_test = train_test_split(info, outcome, test_size=0.33)
    
    #Build a counter based on the training dataset
    counter = CountVectorizer()
    
    counter.fit(train)
    
    #count the number of times each term appears in a document and transform each doc into a count vector
    counts_train = counter.transform(train)#transform the training data
    counts_test = counter.transform(test)#transform the testing data
    
    
    #build Logistic Regression classifier
    LR= LogisticRegression()
    LR.fit(counts_train,labels_train)    
    predicted=LR.predict(counts_test)
    accuracy = accuracy_score(predicted,labels_test)

    #print the accuracy
    print 'Accuracy of', o, 'prediction using Logistic Regression: ', accuracy
    
    #store accuracy of each outcome to be used in plot
    outcomes.setdefault(o, []).append(accuracy)
    
    #build Naive-Bayes classifier
    NB = MultinomialNB() 
    NB.fit(counts_train,labels_train)    
    predicted=NB.predict(counts_test)    
    accuracy = accuracy_score(predicted,labels_test)
    
    #print the accuracy
    print 'Accuracy of', o, 'prediction using Naive-Bayes: ', accuracy
    #store accuracy of each outcome to be used in  plot    
    outcomes.setdefault(o, []).append(accuracy)

    #Voting using LR and NB
    clf1 = LogisticRegression()
    clf2 = MultinomialNB()

    #build a voting classifer
    eclf = VotingClassifier(estimators=[('lr', clf1), ('mnb', clf2)], voting='soft', weights = [2,1])

    #train all classifier on the same datasets
    eclf.fit(counts_train,labels_train)

    #use soft voting to predict 
    predicted=eclf.predict(counts_test)
    accuracy = accuracy_score(predicted,labels_test)
    
    #print the accuracy
    print 'Accuracy of', o, 'prediction using voting: ', accuracy
    #store accuracy of each outcome to be used in plot
    outcomes.setdefault(o, []).append(accuracy)

# Make x, y arrays for each graph
count = 1
x = [1,2,3,4,5,6,7]
y1 = []
y2 = []
y3 = []
labels = ['CA', 'DE', 'DS', 'LT', 'HO', 'OT', 'RI']

for outcome in outcomes: #get accuracies for each classifier for each outcome
    y1.append(outcomes[outcome][0]) #lr accuracy
    y2.append(outcomes[outcome][1]) #nb accuracy
    y3.append(outcomes[outcome][2]) #voting accuracy

# use pylab to plot different lines
plot1 = pl.plot(x, y1, 'r')
plot2 = pl.plot(x, y2, 'g')
plot3 = pl.plot(x, y3, 'b')

pl.xticks(x, labels, rotation='horizontal')

# give plot a title
pl.title('Classifier Accuracy Comparisons')

# make axis labels
pl.xlabel('Outcome')
pl.ylabel('Accuracy')
pl.legend( ['LR', 'NB', 'Voting'])

# show the plot
pl.show()