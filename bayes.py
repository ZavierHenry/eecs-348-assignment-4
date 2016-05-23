# Name: 
# Date:
# Description:
#
#
neutral_threshold = 0.1;
import math, os, pickle, re
import string
import random
import itertools

def chunkify(lst,n):
    return [ lst[i::n] for i in xrange(n) ]

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

        if ('negative_counts_2.dat' and 'positive_counts_2.dat') in lFileList: #If a dictionary already exist load from that dictionaly
            self.positive = self.load('positive_counts_2.dat') #Load in the positive dictionary
            self.negative = self.load('negative_counts_2.dat') #Load in the negative dictionary
            self.posCounts = self.positive['total_counts'] #load in the number of words in the positive dictionary
            self.negCounts = self.negative['total_counts'] #load in the number of words in the negative dictionary
            self.posOccurences = float(self.positive['occurences!']) #load in the number or positive reviews that exist
            self.negOccurences = float(self.negative['occurences!']) #Load in the number of negative reviews that exist
            self.totOccurences = self.posOccurences + self.negOccurences #The total number of reviews that exist in the set
        else:
            self.train() #Call train which instantiates the positive and negative dictionary.



    def train(self, training=[]):
        """Trains the Naive Bayes Sentiment Classifier."""

        if not training: #If no input list is provided it will train with all the movies in the directory
           for fFileObj in os.walk("movies_reviews/"): #Walk through directory and load in all movie files
               training = fFileObj[2]
               break



        positive = {'total_counts': 0, 'occurences!':0} #Instatiate symbols for the amount of words in the positive reviews and the number of positive reviews.
        negative = {'total_counts': 0, 'occurences!' : 0} #Instantiates symbols for the amount of words in the negative reviews and the number of negative reviews.

        for filename in training: #Steps through eavh file that is going to be used for traing

            if re.match("movies-5-", filename): #regular expression matching for a positive review
                edit_dict = positive #switch the edit dictionary pointer to the positive dictionary
            elif re.match("movies-1-", filename): #regular expression matching for a negative review
                edit_dict = negative #swith the edit dictionary pointer to the negative dictionary
            else:
                continue


            dat = self.loadFile("movies_reviews/" + filename)
            dat = self.tokenize(dat)


            edit_dict['occurences!'] += 1 #Increments the number of positive/negative reviews

            for token_index in range(len(dat)): #Iterate through all the tokens in the given review.
                token = dat[token_index].lower() #Cast to lower_case
                edit_dict['total_counts'] += 1 #Increment the counter for every token that appears. This is counting the total number of features found across a given class type.

                # if token in string.punctuation:
                #     continue
                if token not in edit_dict: #If the token has not been visited before instantiate it in the dictionary with a count of 1
                    edit_dict[token] = 1
                else: #if the token has been visited before increment the counter +1
                    edit_dict[token] += 1




        self.save(positive, 'positive_counts_2.dat') #Save the resulting positive dictionary to memory
        self.save(negative, 'negative_counts_2.dat') #Save the resulting negative dictionary to memory

        #Set up class variables
        self.positive = positive #Bind the positive dictionary to class
        self.negative = negative #Bind the negative dictionary to class
        self.posCounts = self.positive['total_counts'] #Bind the total number of positive features to class
        self.negCounts = self.negative['total_counts'] #Bind the total number of negative features to class
        self.posOccurences = float(self.positive['occurences!']) #Bind the total number of positive reviews to class
        self.negOccurences = float(self.negative['occurences!']) #Bind the total number of negative revies to class
        self.totOccurences = self.posOccurences + self.negOccurences #Bind the total number of reviews to class

    def classify(self, sText):
        """Given a target string sText, this function returns the most likely document
        class to which the target string belongs (i.e., positive, negative or neutral).
        """

        dat = self.tokenize(sText)
        logPositive = math.log(self.posOccurences/self.totOccurences)
        logNegative = math.log(self.negOccurences/self.totOccurences)
        for token_index in range(len(dat)):

            token = dat[token_index].lower()

            #if token not in string.punctuation:
            if token in self.positive or self.negative: #Checks to see if the token exist in at least one of the dictionaries
                if token in self.positive:
                    logPositive += math.log((self.positive[token] + 1.0) / self.posCounts) #Calculates conditional probability of token for positive
                else:
                    logPositive += math.log(1.0 / self.posCounts) #Smoothing

                if token in self.negative:
                    logNegative += math.log((self.negative[token] + 1.0) / self.negCounts) #Calculates conditional probability of token for negative
                else:
                    logNegative += math.log(1.0 / self.negCounts) #Smoothing


        if (logPositive > logNegative):
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
    def crossFold(self):
        '''

        :return: Returns results of 10 fold cross validation
        '''
        lFileList = []
        for fFileObj in os.walk("movies_reviews/"): #Steps through all files in the directory
            lFileList = fFileObj[2]
            break
        random.shuffle(lFileList)
        subsec = chunkify(lFileList, 10) #Splits the data into 10 equal parts



        # train 90 percent of the data
        # classify the remaining 10 percent self.classify(10 percent of data) record results

        #Constants for precision, accuracy, and f values

        correct = 0.0
        total = 0.0
        posClassif = 0.0
        negClassif = 0.0
        posCorrect = 0.0
        negCorrect = 0.0
        totPosPrec = 0.0
        totNegprec = 0.0

        negRecall = 0.0
        negRecallCorrect = 0.0
        posRecall = 0.0
        posRecallCorrect = 0.0
        totPosRecall = 0.0
        totNegRecall = 0.0

        print "Crossfolding...."
        for i in range(10):
            print "Crossfold " + str(i + 1) + " results: "
            self.train([name for index, names in enumerate(subsec) for name in names if index != i]) #(lFileList[:i * step] + lFileList[(i + 1) * step:])
            for filename in subsec[i]: #lFileList[i * step:(i + 1) * step]:
                ret = self.classify(self.loadFile("movies_reviews/" + filename))
                if ret == 'Positive': #Checks to see if the movie was clasified as positive
                    posClassif += 1
                    if re.match("movies-5-", filename): #checks to see if it was correctly classified as positive
                        posCorrect += 1
                        correct += 1
                else:
                    negClassif += 1
                    if re.match("movies-1-", filename): #Checks to see if it was correctly classified as negative
                        negCorrect += 1
                        correct += 1
                if re.match("movies-5-", filename): #Checks to see if the movie should be positive
                    posRecall += 1
                    if ret == "Positive": #Checks to see if it was recalled correctly
                        posRecallCorrect += 1
                else:
                    negRecall += 1
                    if ret == "Negative": #Checks to see if the negative document was recalled correctly
                        negRecallCorrect += 1

                total += 1
            if posClassif == 0: #Smoothing
                posprecision = 1
            else:
                posprecision = posCorrect / posClassif #Calculates positive precision
            if negClassif == 0: #Smoothing
                negprecision = 1
            else:
                negprecision = negCorrect / negClassif #Calculates negative precision

            totPosPrec += posprecision #Aggregates iterations
            totNegprec += negprecision #Aggregates iterations
            totPosRecall += posRecallCorrect/posRecall
            totNegRecall += negRecallCorrect/negRecall


            print "Correct classification(Percent correct): ", correct / total, "Positive Precision: ", posprecision, "Negative Precision: ", negprecision, "Positive recall: ", posRecallCorrect/posRecall, "Negative recall: ", negRecallCorrect/negRecall


        F1POS = ((2 * totPosPrec * totPosRecall)/(totPosPrec + totPosRecall)) / 10
        F2POS = ((2 * totNegprec * totNegRecall)/(totNegprec + totNegRecall)) / 10

        print "Final Aggregate Results"
        print "Classification Accuracy:", correct / total
        print "Total Positive Precision: ", totPosPrec/10
        print "Positive recall: ", totPosRecall/10
        print "Positive F1 measure: ", F1POS
        print "\n"
        print "Total Negative Precision: ", totNegprec/10
        print "Negative recall: ", totNegRecall/10
        print "Negative F1 measure: ", F2POS

classif = Bayes_Classifier()

classif.crossFold()

