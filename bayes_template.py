# Name: 
# Date:
# Description:
#
#

import math, os, pickle, re





class Bayes_Classifier:

   def __init__(self):
      """This method initializes and trains the Naive Bayes Sentiment Classifier.  If a 
      cache of a trained classifier has been stored, it loads this cache.  Otherwise, 
      the system will proceed through training.  After running this method, the classifier 
      is ready to classify input text."""
      
      
      
      
      pass
   
   
   
   
   def review_is_positive(self, filename):
      return re.match("^.*movies-5-.*$", name)
   
      
      
      
      
      
      

   def train(self):   
      """Trains the Naive Bayes Sentiment Classifier."""
      
      positive_freq = {}
      negative_freq = {}
      
      
      
      for _, _, files in os.walk("movies_reviews/"):
         for name in files:
            if re.match("^movies-5-.*$", name):
               edit_dict = positive
            else:
               edit_dict = negative
             
             
             
               
            contents = self.loadFile(name)
            contents = self.tokenize(contents)
            
            
         
         
      
      
      
      
      
    
   def classify(self, sText):
      """Given a target string sText, this function returns the most likely document
      class to which the target string belongs (i.e., positive, negative or neutral).
      """
      

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
