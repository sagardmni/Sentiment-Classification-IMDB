import sys
import pickle
import os
import math
import re

#For the given document, weed out stopwords and non-alphanumeric, count the number of occurences of each word, and store in wordDict
def parseReview(file, stopwordList):
  wordDict = {}
  negationList = ["no","not","never","can't","won't","cannot","didn't","couldn't"]
  negationFlag = False
  with open(file) as f:
    for line in f:
      for word in re.split('\W+',line):
        if word in negationList:
            negationFlag = True
            continue
        if word.isalnum() and word not in stopwordList:
          if negationFlag:
            word = "!"+word
            negationFlag = False
          if word not in wordDict:
            wordDict[word] = 1
          else:
            wordDict[word] += 1
  return wordDict

def classifyMe(docWordDict, posDict, negDict):
  posDictCount = sum(posDict.values())
  negDictCount = sum(negDict.values())
  logpDocPos = 0
  logpDocNeg = 0
  totalWordCount = posDictCount + negDictCount
  for word in docWordDict:
    #if word has not occurred before, skip
    if word not in posDict and word not in negDict:
      continue

    #check no. of times it has occurred
    if word in posDict and word in negDict:
      wordCount = posDict[word] + negDict[word]
    elif word in posDict:
      wordCount = posDict[word]
    else: wordCount = negDict[word]

    #calculate probability of word occuring in any document
    pword = float(wordCount)/totalWordCount

    #calculate probabily of word in occuring in pos/neg document
    if word in posDict:
      pwordpos = float(posDict[word])/posDictCount
    else: pwordpos = 0
    if word in negDict:
      pwordneg = float(negDict[word])/negDictCount
    else: pwordneg = 0

    #Use naive bayes
    pwordpos = float(pwordpos)/pword
    pwordneg = float(pwordneg)/pword
    if pwordpos != 0:
      logpDocPos += math.log(pwordpos)
    if pwordneg !=0:
      logpDocNeg += math.log(pwordneg)

  #classifiy: 1=positive, 0=negative
  if logpDocPos > logpDocNeg:
    return 1
  return 0

#load the data that was obtained during training
with open('pos.pickle', 'rb') as handle:
  posDict = pickle.load(handle)
with open('neg.pickle', 'rb') as handle:
  negDict = pickle.load(handle)
with open('stopword.pickle', 'rb') as handle:
  stopwordList = pickle.load(handle)

# os.chdir(os.getcwd() + "/txt_sentoken/test")
os.chdir(sys.argv[1])
posList = os.listdir(os.getcwd() + "/pos")
negList = os.listdir(os.getcwd() + "/neg")

posCount = 0
for review in posList:
  docWordDict = parseReview(os.getcwd() + "/pos/" + review, stopwordList)
  posCount += classifyMe(docWordDict, posDict, negDict)

posAccuracy = (float(posCount)/len(posList))*100
print("Accuracy of classifying positive reviews as positive = " + str(posAccuracy) +"%")

negcount = 0
for review in negList:
  docWordDict = parseReview(os.getcwd() + "/neg/" + review, stopwordList)
  negcount += (not classifyMe(docWordDict, posDict, negDict))

negAccuracy = (float(negcount)/len(negList))*100
print("Accuracy of classifying negative reviews as negative = " + str(negAccuracy) +"%")