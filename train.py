import sys
import os
import pickle
import re

def parseFile(filename):
  wordlist = []
  with open(filename,"r") as f:
    for line in f:
      for word in line.split():
        wordlist.append(word)
  return wordlist

#For entire directory, weed out stopwords and non-alphanumeric, and count the number of occurences, store in wordDict
def parseReviews(mypath, stopwordList):
  filelist = os.listdir(mypath) 
  wordDict = {}
  for file in filelist:
    with open(mypath + "/" + file,"r") as f:
      for line in f:
        for word in re.split('\W+',line):
          if word.isalnum() and word not in stopwordList:
            if word not in wordDict:
              wordDict[word] = 1
            else:
              wordDict[word] += 1
  return wordDict

stopwordList = parseFile('stopwords.txt')

curDir = os.getcwd()
# os.chdir(curDir + "/txt_sentoken/train")
os.chdir(sys.argv[1])
posDict = parseReviews(os.getcwd() + "/pos", stopwordList)
negDict = parseReviews(os.getcwd() + "/neg", stopwordList)
os.chdir(curDir)
with open('pos.pickle', 'wb') as handle:
  pickle.dump(posDict, handle)
with open('neg.pickle', 'wb') as handle:
  pickle.dump(negDict, handle)
with open('stopword.pickle', 'wb') as handle:
  pickle.dump(stopwordList, handle)

