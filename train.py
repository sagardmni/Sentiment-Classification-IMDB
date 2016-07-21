import sys
import os
import pickle
import re
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

def parseFile(filename):
  wordlist = []
  with open(filename,"r") as f:
    for line in f:
      for word in line.split():
        wordlist.append(word)
  return wordlist

#For entire directory, weed out stopwords and non-alphanumeric, and count the number of occurences, store in wordDict
def parseReviews(mypath):
  filelist = os.listdir(mypath) 
  wordDict = {}
  negationList = ["no","not","never","can't","won't","cannot","didn't","couldn't"]
  negationFlag = False
  stopwordList = set(stopwords.words("english"))
  for file in filelist:
    with open(mypath + "/" + file,"r") as f:
      word_list = word_tokenize(f.read())
    for word in word_list:
      if word in negationList:
        negationFlag = True
        continue
      if word.isalnum() and word not in stopwordList:
        if negationFlag:
          word = "!" + word
          negationFlag = False
        if word not in wordDict:
          wordDict[word] = 1
        else:
          wordDict[word] += 1
  return wordDict

curDir = os.getcwd()
os.chdir(sys.argv[1])
posDict = parseReviews(os.getcwd() + "/pos")
negDict = parseReviews(os.getcwd() + "/neg")
os.chdir(curDir)
with open('pos.pickle', 'wb') as handle:
  pickle.dump(posDict, handle)
with open('neg.pickle', 'wb') as handle:
  pickle.dump(negDict, handle)
