import numpy as np
import csv
import time
#DATA GENERATION


def baseGenerator(path, numBatches, lengthBatch, holdout=[], featCreators=[], sep=","):
    trainFile = open(path, "r")
    trainFile.readline() #discard column names
    
    for batchIndex in range(numBatches):
        xBatch = []
        yBatch = []
        exampleIndex = 0
        while exampleIndex < lengthBatch:
            #READ ROW
            line = trainFile.readline()
            if line == "": break #break at end of file
            line = line[:-1] #discard line break char
            example = line.split(sep)
            #MUST HOLDOUT ?
            holdoutFlag = False
            for i in holdout:
                if exampleIndex % i == 0:
                    exampleIndex += 1
                    holdoutFlag = True
                    break
            if holdoutFlag: continue
            #REMOVE TARGET AND ID
            target = float(example[1]) #get click status
            example.pop(1) #remove target from features            
            example.pop(0) #remove ID
            #CALL FEATURE CREATION ROUTINES
            for f in featCreators:
                f(example)
            #ADD TO BATCH
            xBatch.append(example)
            yBatch.append(target)
            exampleIndex +=  1
        if len(xBatch) != 0: #in case of end of file
            yield xBatch, yBatch
            
    trainFile.close()
    


def testGenerator(testPath, numBatches, featCreators=[], sep=","):
    testFile = open(testPath,"r")
    line = testFile.readline() #discard header row
    perbatch = 5000000/numBatches
    for batchIndex in range(numBatches):
        xBatch = []
        idBatch = []
        exampleIndex = 0
        while exampleIndex < perbatch:
            #READ ROW
            line = testFile.readline()
            if line == "": break
            line = line[:-1]
            example = line.split(sep)
            #REMOVE ID
            ID = example.pop(0)
            #CALL FEATURE CREATION ROUTINES
            for f in featCreators:
                f(example)
            #ADD TO BATCH
            exampleIndex += 1
            xBatch.append(example)
            idBatch.append(ID)
        if len(xBatch) != 0:
            yield xBatch, idBatch
    testFile.close()



        
def rawGenerator(path, sep=","):
    "Yields raw split rows with no feature engineering or target separation."
    file = open(path, "r")
    file.readline() #discard column names
    row = file.readline()
    while row != "":
        row = row[:-1] #discard line break char
        features = row.split(sep) #split into features
        yield features
        row = file.readline()
    file.close()

    
    
