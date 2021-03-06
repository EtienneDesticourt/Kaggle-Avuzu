import numpy as np
from sklearn.feature_extraction import FeatureHasher
from sklearn.linear_model import SGDClassifier
from avazuScorer import llfun
from datetime import datetime
import scipy

class Model:
    def __init__(self,numFeatures, learningRate, numEpochs, ppenalty="l1", mustShuffle=True):
        #Init scikit models
        self.FH = FeatureHasher(n_features=numFeatures, input_type='string')
        self.Classifier = SGDClassifier(penalty=ppenalty, loss='log', alpha=learningRate, n_iter = numEpochs, shuffle=mustShuffle)
    def train(self, gen,  v=False):

        i = 0
        for x, y in gen: #For each batch
            xHash = self.FH.transform(x) #hash trick
            y = np.array(y)            
##            for epoch in range(numEpochs):
            self.Classifier.partial_fit(xHash, y, [0,1])
            i += len(x)
            if v : print(str(datetime.now())[:-7] , "example:", i)
            
    def test(self, gen,  v=False):

        #init target and prediction arrays
        ytot = np.array([])
        ptot = np.array([])
        #Get prediction for each batch
        i = 0
        for x,y in gen:
            xHash = self.FH.transform(x) #hash trick
            p = self.Classifier.predict_proba(xHash)
            p = p.T[1].T #Keep column corresponding to probability of class 1
            #Stack target and prediction for later analysis
            ytot = np.hstack((ytot, y)) 
            ptot = np.hstack((ptot, p))
            i += y.shape[0]
            if v : print(str(datetime.now())[:-7] , "example:", i)
        if v: print("Score:", self.score(ytot, ptot))
        
        return (ytot, ptot)
    def predictBatch(self, batch):
        hashedBatch = self.FH.transform(batch)
        prediction = self.Classifier.predict_proba(hashedBatch)
        return prediction
    def generatePrediction(self, generator):
        for xBatch, idBatch in generator:
            prediction = self.predictBatch(xBatch)
            yield prediction, idBatch
    def score(self, target, prediction):
        return llfun(target, prediction)
                
