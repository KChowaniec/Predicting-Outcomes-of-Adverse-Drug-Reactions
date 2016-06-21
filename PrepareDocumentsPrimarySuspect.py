"""
File: PrepareDocumentsPrimarySuspect.py
Project: Predicting Outcomes of Adverse Drug Reactions
Author: Kathy Chowaniec
File Description:
This script read in the FAERS text files for Q4 2015 (DEMO15Q4, DRUG15Q4, INDI15Q4,
OUTC15Q4, REAC15Q4) located in the 'FAERS Data' folder. Each file is parsed based using
'$' as a delimeter and text is cleaned to remove duplicate spaces and non-letter/digit
characters. The data is stored in a dictionary object, output, which is eventually
used in generating pseudo-documents for each possible outcome. All the outcomes
are stored in an 'Outcomes' folder. This script generates documents for only those
drugs that are identified as 'Primary Suspects'. Once the documents have been generated,
any of the other scripts can be run, as they use these documents to predict outcomes. 

"""

import re,os

#DEMOGRAPHIC DATA
demo=open('FAERS Data/DEMO15Q4.txt')
output = dict() #dictionary object to store all document information (except outcome)
for line in demo:
    attributes = line.strip().split('$')
    primary_id = attributes[0] #report id
    if re.match('[\d]+', primary_id): #ignore any header lines
        #stores age, age unit, gender, weight, weight unit and country where event occurred
        values = attributes[13], attributes[14],  attributes[16], attributes[18], attributes[19], attributes[24]
        output.setdefault(primary_id, []).extend(values)
demo.close()

#DRUG DATA
drug=open('FAERS Data/DRUG15Q4.txt')
drug_list = dict() #stores drug names
for line in drug:
    values = list()
    line=re.sub('[^A-Za-z\d\()$]',' ', line)#replace chars that are not letters or numbers with a space   
    line=re.sub(' +',' ',line).strip()#remove duplicate spaces
    line=line.upper()
    attributes = line.strip().split('$') #split using $ as delimeter
    primary_id = attributes[0]
    if primary_id in output and attributes[3] == "PS": #store only primary suspect drugs
        #stores drug sequence number, drug role and drug name
        values = attributes[2],  attributes[3], attributes[4].strip()  
        drug_list.setdefault(primary_id, []).append(values)
        output.setdefault(primary_id, []).extend(values)
drug.close()


#INDICATION DATA
indict=open('FAERS Data/INDI15Q4.txt')
for line in indict:
    values= list()
    line=re.sub('[^A-Za-z\d\()$]',' ', line)#replace chars that are not letters or numbers with a space
    line=re.sub(' +',' ',line).strip()#remove duplicate spaces
    line=line.upper()
    attributes = line.strip().split('$') #split line using $ as delimeter
    primary_id = attributes[0]
    if primary_id in output:
        drug_seq = drug_list[primary_id][0] #get drug sequence number
        if attributes[2] == drug_seq[0]: #find indication matching primary suspect drug's sequence number
            #store indication data (why drug was taken)            
            values = attributes[2],attributes[3].strip()
            output.setdefault(primary_id, []).extend(values)
indict.close()

#REACTION DATA
react=open('FAERS Data/REAC15Q4.txt')
for line in react:
    values = list()
    line=re.sub('[^A-Za-z\d\()$]',' ', line)#replace chars that are not letters or numbers with a space
    line=re.sub(' +',' ',line).strip()#remove duplicate spaces
    line=line.upper()
    attributes = line.strip().split('$') #split using $ as delimeter
    primary_id = attributes[0]
    if primary_id in output:
        #store reaction data
        values = attributes[2],  attributes[3].strip()
        output.setdefault(primary_id, []).extend(values)
react.close()

#OUTCOME DATA
outcome=open('FAERS Data/OUTC15Q4.txt')
outcomes = dict()
for line in outcome:
    values = list()
    attributes = line.strip().split('$') #split using $ as delimeter
    primary_id = attributes[0]
    if primary_id in output:
        #store list of outcomes separately
        values = attributes[2].strip()
        outcomes.setdefault(primary_id, []).append(values)
outcome.close()

documents = list()
for o in output:
    if o in outcomes: #only if entry has outcome associated with it
        values = outcomes[o]
        documents.append([output[o], values]) #create list containing all information and outcome

#save documents to outcome files
outcome_list=('DE', 'LT', 'HO', 'DS', 'CA', 'RI', 'OT')
#creates Outcomes folder in current directory if it doesn't exist already
if not os.path.exists('Outcomes'):os.mkdir('Outcomes')
for outcome in outcome_list:
    fw=open('Outcomes' + '/'+ outcome+'.txt', 'w')
    for document in documents:
        if outcome not in document[1]:
            flag = 0
        else:
            flag = 1
        fw.write(str(' '.join(document[0]))+'\t'+str(flag)+'\n') #separate document information and outcome by a tab
    fw.close()
