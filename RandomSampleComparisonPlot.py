"""
File: RandomSampleComparisonPlot.py
Project: Predicting Outcomes of Adverse Drug Reactions
Author: Kathy Chowaniec
File Description:
This script compares the accuracies of 4 different classifiers: 
KNN, Logistic Regression,Naive-Bayes and Voting on a random sample of 20,000
records from the FAERS dataset. The results from this comparison are plotted 
for each outcome. 
"""
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.ensemble import VotingClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.cross_validation import train_test_split
import pylab as pl
import random

#read the outcome file and separate document information from the outcome
def loadData(fname):
    info=[]
    outcome=[]
    lines = list()
    f=open(fname)
    for line in f:
        lines.append(line)
    f.close()
    f = random.sample(lines, 20000) #take a random sample of 20,000 records
    for line in f: 
        case,result=line.strip().split('\t') #split line based on tab delimeter
        info.append(case.lower()) #store information
        outcome.append(int(result)) #store outcome
    return info, outcome

outcome_list=('DE', 'LT', 'HO', 'DS', 'CA', 'RI', 'OT')
outcomes = dict()

#for each outcome file, split data into training and test datasets
for o in outcome_list:
    info,outcome=loadData('Outcomes' + '/' + o +'.txt')    
    train, test, labels_train, labels_test = train_test_split(info, outcome, test_size=0.33)
    
    #Build a counter based on the training dataset
    counter = CountVectorizer()
    counter.fit(train)
    
    #count the number of times each term appears in a document and transform each doc into a count vector
    counts_train = counter.transform(train)#transform the training data
    counts_test = counter.transform(test)#transform the testing data
    
    #KNN with k = 5
    KNN= KNeighborsClassifier(5)
    KNN.fit(counts_train,labels_train)    
    predicted=KNN.predict(counts_test)
    accuracy = accuracy_score(predicted,labels_test)
    #print the accuracy
    print 'Accuracy of', o, 'prediction using KNN: ', accuracy
    #store accuracy for plotting
    outcomes.setdefault(o, []).append(accuracy)
    
    #LR
    LR= LogisticRegression()
    LR.fit(counts_train,labels_train)    
    predicted=LR.predict(counts_test)
    accuracy = accuracy_score(predicted,labels_test)
    #print the accuracy
    print 'Accuracy of', o, 'prediction using Logistic Regression: ', accuracy
    #store accuracy for plotting    
    outcomes.setdefault(o, []).append(accuracy)
    
    #NB
    NB = MultinomialNB() 
    NB.fit(counts_train,labels_train)    
    predicted=NB.predict(counts_test)    
    accuracy = accuracy_score(predicted,labels_test)
    #print the accuracy
    print 'Accuracy of', o, 'prediction using Naive-Bayes: ', accuracy
    #store outcome for plotting    
    outcomes.setdefault(o, []).append(accuracy)
   
   #Voting 
    #pick 3 classifiers
    clf1 = LogisticRegression()
    clf2 = KNeighborsClassifier(5)
    clf3 = MultinomialNB()

    #build a voting classifer using soft weights
    eclf = VotingClassifier(estimators=[('lr', clf1), ('knn', clf2), ('mnb', clf3)], voting='soft', weights = [2,1,1])

    #train all classifier on the same datasets
    eclf.fit(counts_train,labels_train)

    #predict the outcome
    predicted=eclf.predict(counts_test)
    accuracy = accuracy_score(predicted,labels_test)
    #print the accuracy
    print 'Accuracy of', o, 'prediction using voting: ', accuracy
    #store the accuracy for plotting    
    outcomes.setdefault(o, []).append(accuracy)

# Make x, y arrays for each graph
count = 1
x = [1,2,3,4,5,6,7]
y1 = []
y2 = []
y3 = []
y4 = []
labels = ['CA', 'DE', 'DS', 'LT', 'HO', 'OT', 'RI']

for outcome in outcomes: #get accuracies for each classifier for each outcome 
    y1.append(outcomes[outcome][0]) #knn accuracy
    y2.append(outcomes[outcome][1]) #lr accuracy
    y3.append(outcomes[outcome][2]) #nb accuracy
    y4.append(outcomes[outcome][3]) #voting accuracy

# use pylab to plot graphs
plot1 = pl.plot(x, y1, 'r')
plot2 = pl.plot(x, y2, 'g')
plot3 = pl.plot(x, y3, 'b')
plot4 = pl.plot(x, y4, 'k')

pl.xticks(x, labels, rotation='horizontal')

# give plot a title
pl.title('Random Sample Accuracy Comparisons')

# make axis labels
pl.xlabel('Outcome')
pl.ylabel('Accuracy')
pl.legend( ['KNN','LR', 'NB', 'Voting'])

# show the plot
pl.show()