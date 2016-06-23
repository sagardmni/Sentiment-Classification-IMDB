import os
import math

#parse file word-by-word and store in wordlist
def parseFiles(mypath):
  filelist = os.listdir(mypath) 
  wordlist = []
  for file in filelist:
    with open(mypath + "/" + file,"r") as f:
      for line in f:
        for word in line.split():
          wordlist.append(word)
  return wordlist

#For entire directory, weed out stopwords and non-alphanumeric, and count the number of occurences, store in wordDict
def parseWeedCount(mypath, stopwordList):
  filelist = os.listdir(mypath) 
  wordDict = {}
  for file in filelist:
    with open(mypath + "/" + file,"r") as f:
      for line in f:
        for word in line.split():
          if word.isalnum() and word not in stopwordList:
            if word not in wordDict:
              wordDict[word] = 1
            else:
              wordDict[word] += 1
  return wordDict

#For single document, weed out stopwords and non-alphanumeric, and count the number of occurences, store in wordDict
def parseWeedCountSingle(file, stopwordList):
  wordDict = {}
  with open(file) as f:
    for line in f:
      for word in line.split():
        if word.isalnum() and word not in stopwordList:
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
    #print(word)
    #if it has not occurred before, do not use
    if word not in posDict and word not in negDict:
      continue
    #check no. of times it has occurred
    if word in posDict and word in negDict:
      wordCount = posDict[word] + negDict[word]
    elif word in posDict:
      wordCount = posDict[word]
    else: wordCount = negDict[word]
    #calaculate probability of word occuring in any document
    pword = float(wordCount)/totalWordCount
    #calculate probabily of word in occuring in pos/neg
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
    #raw_input("press enter to continue")
  if logpDocPos > logpDocNeg:
    return 1
  else: return 0

def naiveBayes(posDict, negDict, stopwordList):
  listOfPos = os.listdir(os.getcwd() + "/test/pos")
  listOfNeg = os.listdir(os.getcwd() + "/test/neg")
  count = 0
  poscount = 0
  for posReview in listOfPos:
    docWordDict = parseWeedCountSingle(os.getcwd() + "/test/pos/" + posReview, stopwordList)
    poscount += classifyMe(docWordDict, posDict, negDict)
    count+=1
    #break
  posAccuracy = (float(poscount)/count)*100
  print("Accuracy of classifying positive reviews as positive = " + str(posAccuracy) +"%")

  count = 0
  negcount = 0
  for negReview in listOfNeg:
    docWordDict = parseWeedCountSingle(os.getcwd() + "/test/neg/" + negReview, stopwordList)
    negcount += (not classifyMe(docWordDict, posDict, negDict))
    count+=1
    #break
  negAccuracy = (float(negcount)/count)*100
  print("Accuracy of classifying negative reviews as negative = " + str(negAccuracy) +"%")

#main
os.chdir(os.getcwd() + "/txt_sentoken")

stopwordList = parseFiles(os.getcwd() + '/stopwords')
posDict = parseWeedCount(os.getcwd() + "/train/pos", stopwordList)
negDict = parseWeedCount(os.getcwd() + "/train/neg", stopwordList)

#write to csv file
with open("myfile.csv","w") as myfile:
  for key in posDict:
    myfile.write(key + "," + str(posDict[key]))
    if key in negDict:
      myfile.write("," + str(negDict[key]))
    myfile.write("\n")

naiveBayes(posDict,negDict, stopwordList)