# Name: 
# Date:
# Description:
#
#

import math, os, pickle, re
import string
class Bayes_Classifier:

   def __init__(self):
      """This method initializes and trains the Naive Bayes Sentiment Classifier.  If a 
      cache of a trained classifier has been stored, it loads this cache.  Otherwise, 
      the system will proceed through training.  After running this method, the classifier 
      is ready to classify input text."""

      lFileList = []
      for fFileObj in os.walk(os.getcwd()): #Checks to see what files are in the current working directory
         lFileList = fFileObj[2]
         break
      

      if ('negative_counts.dat_2' and 'positive_counts_2.dat') in lFileList:
         self.positive = self.load('positive_counts_2.dat')
         self.negative = self.load('negative_counts_2.dat')
         self.posCounts = self.positive['total_counts']
         self.negCounts = self.negative['total_counts']
         self.posOccurences = float(self.positive['occurences!'])
         self.negOccurences = float(self.negative['occurences!'])
         self.totOccurences = self.posOccurences + self.negOccurences
         print self.posCounts, self.negCounts
      else:
         self.positive, self.negative = self.train()
         self.posCounts = self.positive['total_counts']
         self.negCounts = self.negative['total_counts']
         self.posOccurences = self.positive['occurences!']
         self.negOccurences = self.negative['occurences!']
         self.totOccurences = self.posOccurences + self.negOccurences

         # ret = self.train()
         # self.positive = ret[0]
         # self.negative = ret[1]

   def train(self):   
      """Trains the Naive Bayes Sentiment Classifier."""
      
      lFileList = []
      for fFileObj in os.walk("movies_reviews/"):
         lFileList = fFileObj[2]
         break
      

      positive = {'total_counts': 0, 'occurences!':0}
      negative = {'total_counts': 0, 'occurences!' : 0}
      
      for filename in lFileList:
         dat = self.loadFile("movies_reviews/" + filename)
         dat = self.tokenize(dat)
         
         if re.match("movies-5-", filename):
            edit_dict = positive
            edit_dict['occurences!'] += 1
         else:
            edit_dict = negative
            edit_dict['occurences!'] += 1

         for token in dat:
            token = token.lower()
            if token in string.punctuation:
               continue
            elif token not in edit_dict:
               edit_dict[token] = 1
               edit_dict['total_counts'] += 1
            else:
               edit_dict[token] += 1
               edit_dict['total_counts'] += 1
               
      self.save(positive, 'positive_counts_2.dat')
      self.save(negative, 'negative_counts_2.dat')
      
      return positive, negative
               
      
      
      
#       for i in range(0, len(lFileList)):
#          filename = lFileList[i].split('-')
#          if len(filename) == 3:
#             if filename[1] == '1':
#                dat = self.loadFile("movies_reviews/" + lFileList[i])
#                dat = "".join(l for l in dat if l not in string.punctuation) #Removes punctuation from the string 
#                dat = dat.split(' ')
#                for each in dat:
#                  each = each.lower()
#                  if each not in negative.keys():
#                      negative[each] = 1
#                   else:
#                      negative[each] = negative[each] + 1
#             elif filename[1] == '5':
#                dat = self.loadFile("movies_reviews/" + lFileList[i])
#                dat = "".join(l for l in dat if l not in string.punctuation) #Removes punctuation from the string 
#                dat = dat.split(' ')
#                for each in dat:
#                   each = each.lower()
#                   if each not in positive.keys():
#                      positive[each] = 1
#                   else:
#                      positive[each] = positive[each] + 1
# 
#       self.save(positive, 'positive_counts.dat')
#       self.save(negative, 'negative_counts.dat')
# 
#       return(positive, negative)

    
   def classify(self, sText):
      """Given a target string sText, this function returns the most likely document
      class to which the target string belongs (i.e., positive, negative or neutral).
      """
      dat = self.tokenize(sText)
      logPositive = 0
      logNegative = 0
      for token in dat:
         if token not in string.punctuation:
            if token in self.positive:
               logPositive += math.log((self.positive[token] + 1.0) / self.posCounts)

            if token in self.negative:
               logNegative += math.log((self.negative[token] + 1.0) / self.negCounts)
      print logPositive, logNegative
      print self.posOccurences/self.totOccurences, self.negOccurences/self.totOccurences
      if ((math.log(self.posOccurences/self.totOccurences)) + logPositive) > (math.log(self.negOccurences/self.totOccurences) * logNegative):
         return 'Positive'
      else:
         return 'Negative'

   def loadFile(self, sFilename):
      """Given a file name, return the contents of the file as a string."""

      f = open(sFilename, "r")
      sTxt = f.read()
      f.close()
      return sTxt
   
   def save(self, dObj, sFilename):
      """Given an object and a file name, write the object to the file using pickle."""

      f = open(sFilename, "w")
      p = pickle.Pickler(f)
      p.dump(dObj)
      f.close()
   
   def load(self, sFilename):
      """Given a file name, load and return the object stored in the file."""

      f = open(sFilename, "r")
      u = pickle.Unpickler(f)
      dObj = u.load()
      f.close()
      return dObj

   def tokenize(self, sText): 
      """Given a string of text sText, returns a list of the individual tokens that 
      occur in that string (in order)."""

      lTokens = []
      sToken = ""
      for c in sText:
         if re.match("[a-zA-Z0-9]", str(c)) != None or c == "\"" or c == "_" or c == "-":
            sToken += c
         else:
            if sToken != "":
               lTokens.append(sToken)
               sToken = ""
            if c.strip() != "":
               lTokens.append(str(c.strip()))
               
      if sToken != "":
         lTokens.append(sToken)

      return lTokens

classif = Bayes_Classifier()
print classif.classify("lovely"), classif.positive["lovely"], classif.negative["lovely"]


