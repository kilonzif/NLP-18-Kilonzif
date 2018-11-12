###
'''Name: Faith Kilonzi
filename: Lab4.py
NLP- LAB 4      12th OCtober 2018
Implementation of Naive Bayes and Logistic Regression Classifiers using libraries'''

####


## Importing Libraries

from sklearn.linear_model import LogisticRegression
from sklearn import naive_bayes
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score
import nltk
import numpy as np
import pandas as pd
import re
from io import StringIO

import sys



class classifier:
    

    '''
    @init_ initializes the Naive Bayes and Logistic Regression classifiers as per the user's specifications
    It also defines normalization attribute, whether true or false for each classifier
    '''
    def __init__(self, normalize=True, classifierType = "logistic", split_ratio=0.3):
        if classifierType == "logistic":
            self.classifierType = LogisticRegression(random_state=0, solver='lbfgs',multi_class='multinomial')
        elif classifierType == "naive":
            self.classifierType = naive_bayes.MultinomialNB()
        self.normalize = normalize
        if self.normalize:
            #normalized mode
            self.vec = TfidfVectorizer(use_idf=True)
        else:
            #unnormalized mode
            self.vec = TfidfVectorizer(use_idf=True, lowercase = True, strip_accents=ascii, stop_words = set(nltk.corpus.stopwords.words('english')))

    
    ''''
    @openAndRead function takes on the given document, opens it using pandas and trains 
    '''    
    def openAndRead(self, documents):
        X,Y = [], []
        #read the document and divide it into two colums, review amd sentiment
        doc = pd.read_csv(documents, sep='\t', names=['review','sentiment'],quoting=3, error_bad_lines=False)
        self.doc = doc
        Y = doc.sentiment
        self.vec.fit(doc.review)
        X = self.preprocessData(doc)
        
        return train_test_split(X,Y)
    
   
    """
    @preprocessData takes the given document and transforms it into a normalized one ie it sets normalization to true
    """
    def preprocessData(self, given_doc):
      
        return self.vec.transform(given_doc.review)
    


    '''
        @train function takes the given document and trains it according to the clasifier specified then
         assigns results 
         and calculates accuracy 
    '''
    def train(self, document):

        #read the given document and store variables
        X_train, X_test, Y_train, Y_test =  self.openAndRead(document)       
                
        #fit the vector object on trained data, Y and X
        self.classifierType.fit(X_train,Y_train)
        
        #claculating accuracy
        accuracy = roc_auc_score(Y_test,self.classifierType.predict_proba(X_test)[:,1])
        
        #printing the accuracy
        print ("Accuracy :", round(accuracy, 3))

   
    '''
        @predict function to make predictions on the given sentence
    '''     
    def predict(self, sentence):
        #read the given document review and predict its sentiment using pandas
        predictData = pd.read_csv(StringIO(sentence), names=['review'],quoting=3, error_bad_lines=False)

        #preprocessDataing
        X = self.preprocessData(predictData)
        #Calculate probability
        Y = self.classifierType.predict_proba(X)
        #return the maximum likelihood of prediction done on the data
        return np.argmax(Y)



    '''
        @outputFile function takes the users parameters,
        writes the results in an output file
    '''
    def outputFile(self, file_name, version, classifierType):
        sentimentLabel = []
        with open(file_name) as f:
            for line in f.readlines():
                sentimentLabel.append(self.predict(line))
                
        resultsFile = 'results-' + classifierType + '-' + version + '.txt'
        
        with open(resultsFile, 'w') as f:
            for i in sentimentLabel:
                f.write(str(i)+"\n")
                
        print ("View Results in:",resultsFile)
                
'''
@main_ The DRiver function
'''
if __name__ == '__main__':

    version, classifierType, outputFile = sys.argv[2], sys.argv[1], sys.argv[3]

    if (classifierType == 'nb'):
        if (version == 'u'):
            print ("Unnormalized data, NaiveBayes Classifier")
            GivenClass = classifier(normalize=False, classifierType='naive')
            GivenClass.train("training.txt")
        elif (version == 'n'):
            print ("Normalized data, NaiveBayes Classifier")
            GivenClass = classifier(normalize=True, classifierType='naive')
            GivenClass.train("training.txt")
    elif (classifierType == 'lr'):
        if (version == 'u'):
            print ("Unnormalized data, Logistic Regression Classifier")
            GivenClass = classifier(normalize=False)
            GivenClass.train("training.txt")
        elif (version == 'n'):
            print ("Normalized data, Logistic Regression Classifiers")
            GivenClass = classifier(normalize=True)
            GivenClass.train("training.txt")



    
    GivenClass.outputFile(outputFile, version, classifierType)