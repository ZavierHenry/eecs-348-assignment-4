# Name: 
# Date:
# Description:
#
#

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


        if ('negative_counts.dat_2' and 'positive_counts_2.dat') in lFileList:
            self.positive = self.load('positive_counts_2.dat')
            self.negative = self.load('negative_counts_2.dat')
            self.posCounts = self.positive['total_counts']
            self.negCounts = self.negative['total_counts']
            self.posOccurences = float(self.positive['occurences!'])
            self.negOccurences = float(self.negative['occurences!'])
            self.totOccurences = self.posOccurences + self.negOccurences
        else:
            self.train()

    def crossFold(self):
        lFileList = []
        for fFileObj in os.walk("movies_reviews/"):
            lFileList = fFileObj[2]
            break
        random.shuffle(lFileList)
        subsec = chunkify(lFileList, 10)

        step = int(round(len(lFileList) / 10.0, 0))



        # train 90 percent of the data self.positive , self.negative = self.train(90 percent of data)
        # classify the remaining 10 percent self.classify(10 percent of dats) record results

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

        for i in range(10):
            self.positive, self.negative = self.train(list(itertools.chain(*(subsec[:i] + subsec[i+1:])))) #(lFileList[:i * step] + lFileList[(i + 1) * step:])
            self.posCounts = self.positive['total_counts']
            self.negCounts = self.negative['total_counts']
            self.posOccurences = float(self.positive['occurences!'])
            self.negOccurences = float(self.negative['occurences!'])
            self.totOccurences = self.posOccurences + self.negOccurences
            for filename in subsec[i]: #lFileList[i * step:(i + 1) * step]:
                ret = self.classify(self.loadFile("movies_reviews/" + filename))
                if ret == 'Positive':
                    posClassif += 1
                    if re.match("movies-5-", filename):
                        posCorrect += 1
                        correct += 1
                else:
                    negClassif += 1
                    if re.match("movies-1-", filename):
                        negCorrect += 1
                        correct += 1
                if re.match("movies-5-", filename):
                    posRecall += 1
                    if ret == "Positive":
                        posRecallCorrect += 1
                else:
                    negRecall += 1
                    if ret == "Negative":
                        negRecallCorrect += 1

                total += 1
            if posClassif == 0:
                posprecision = 1
            else:
                posprecision = posCorrect / posClassif
            if negClassif == 0:
                negprecision = 1
            else:
                negprecision = negCorrect / negClassif

            totPosPrec += posprecision
            totNegprec += negprecision
            totPosRecall += posRecallCorrect/posRecall
            totNegRecall += negRecallCorrect/negRecall


            print correct / total, "Positive Precision: ", posprecision, "Negative Precision: ", negprecision, "Positive recall: ", posRecallCorrect/posRecall, "Negative recall: ", negRecallCorrect/negRecall
        F1POS = (2 * totPosPrec * totPosRecall)/(totPosPrec + totPosRecall)
        F2POS = (2 * totNegprec * totNegRecall)/(totNegprec + totNegRecall)
        print correct / total, "Total Positive Precision: ", totPosPrec/10 , "Total Negative Precision: ", totNegprec/10, "average Positive recall: ", totPosRecall/10, "Negative recall: ", totNegRecall/10
        print "Positive F1 measure: ", F1POS, "negative F1 measure: ", F2POS
        #         if re.match("movies-5-", filename):
        #             posClassif += 1
        #             if ret == "Positive":
        #                 posCorrect += 1
        #                 correct += 1
        #         else:
        #             negClassif += 1
        #             if ret == "Negative":
        #                 negCorrect += 1
        #                 correct += 1
        #         total += 1
        #     print correct / total, "Positive Precision: ", posCorrect / posClassif, "Negative Precision: ", negCorrect / negClassif
        #
        # print correct / total, "Total Positive Precision: ", posCorrect / posClassif, "Total Negative Precision: ", negCorrect / negClassif, posCorrect, negCorrect

    def train(self, training=[]):
        """Trains the Naive Bayes Sentiment Classifier."""

        if not training:
           for fFileObj in os.walk("movies_reviews/"):
               training = fFileObj[2]
               break


        positive = {'total_counts': 0, 'occurences!':0}
        negative = {'total_counts': 0, 'occurences!' : 0}

        for filename in training:
            dat = self.loadFile("movies_reviews/" + filename)
            dat = self.tokenize(dat)

            if re.match("movies-5-", filename):
                edit_dict = positive
            else:
                edit_dict = negative

            edit_dict['occurences!'] += 1

            for token_index in range(len(dat)):
                token = dat[token_index].lower()
                edit_dict['total_counts'] += 1
                
                # if token in string.punctuation:
                #     continue
                if token_index not in edit_dict:
                    edit_dict[token] = 1
                else:
                    edit_dict[token] += 1
                    
                    
                if token_index != 0:
                    edit_dict['total_counts'] += 1
                    bigram = (dat[token_index-1].lower(), token)
                    
                    if bigram not in edit_dict:
                        edit_dict[bigram] = 1
                    else:
                        edit_dict[bigram] += 1
                
                

        self.save(positive, 'positive_counts_2.dat')
        self.save(negative, 'negative_counts_2.dat')

        self.positive = positive
        self.negative = negative
        self.posCounts = self.positive['total_counts']
        self.negCounts = self.negative['total_counts']
        self.posOccurences = float(self.positive['occurences!'])
        self.negOccurences = float(self.negative['occurences!'])
        self.totOccurences = self.posOccurences + self.negOccurences

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
            if token in self.positive or self.negative:
                if token in self.positive:
                    logPositive += math.log((self.positive[token] + 1.0) / self.posCounts)
                else:
                    logPositive += math.log(1.0 / self.posCounts)

                if token in self.negative:
                    logNegative += math.log((self.negative[token] + 1.0) / self.negCounts)
                else:
                    logNegative += math.log(1.0 / self.negCounts)
                    
            if token_index != 0:
                bigram = (dat[token_index-1].lower(), token)
                if bigram in self.positive:
                    logPositive += math.log((self.positive[bigram] + 1.0) / self.posCounts)
                else:
                    logPositive += math.log(1.0 / self.posCounts)

                if bigram in self.negative:
                    logNegative += math.log((self.negative[bigram] + 1.0) / self.negCounts)
                else:
                    logNegative += math.log(1.0 / self.negCounts)
                    
        #test comment


        if (logPositive > logNegative):
            return 'Positive'
        else:
            return 'Negative'

    def evaluate(self, testset):
        true_positives = 0.0
        true_negatives = 0.0
        false_positives = 0.0
        false_negatives = 0.0

        for filename in testset:
            string = self.loadFile("movies_reviews/" + filename)
            result = self.classify(string)

            if (result == "Positive"):
                if re.match("movies-5-", filename): #if we classified as positive and the file was positive increment true positives
                    true_positives += 1
                elif re.match("movies-1-", filename):
                    false_positives += 1
            elif (result == "Negative"):
                if re.match("movies-1-", filename):
                    true_negatives += 1
                elif re.match("movies-5-", filename):
                    false_negatives += 1

        print true_positives , true_negatives, false_positives, false_negatives
        pos_precision = true_positives / (true_positives + false_positives)
        neg_precision = true_negatives / (true_negatives + false_negatives)

        pos_recall = true_positives / (true_positives + false_negatives)
        neg_recall = true_negatives / (true_negatives + false_positives)

        pos_fmeasure = (2 * pos_precision * pos_recall) / (pos_precision + pos_recall)
        neg_fmeasure = (2 * neg_precision * neg_recall) / (neg_precision + neg_recall)

        return {'posrecall':pos_recall,'posprecision':pos_precision, 'posf':pos_fmeasure, 'negrecall':neg_recall,'negprecision':neg_precision, 'negf':neg_fmeasure}

    def tenFold(self):
        pos_recalls = []
        pos_precisions = []
        pos_fmeasures = []
        neg_recalls = []
        neg_precisions = []
        neg_fmeasures = []
        lFileList = []
        for fFileObj in os.walk("movies_reviews/"):
            lFileList = fFileObj[2]
            break

        random.seed(1)
        random.shuffle(lFileList)

        step = int(round(len(lFileList) / 10.0, 0))

        # train 90 percent of the data self.positive , self.negative = self.train(90 percent of data)
        # classify the remaining 10 percent self.classify(10 percent of dats) record results


        for i in range(10):
            self.train(lFileList[:i * step] + lFileList[(i + 1) * step:])

            results = self.evaluate(lFileList[i * step:][:step])

            pos_recalls.append(results['posrecall'])
            pos_precisions.append(results['posprecision'])
            pos_fmeasures.append(results['posf'])
            neg_recalls.append(results['negrecall'])
            neg_precisions.append(results['negprecision'])
            neg_fmeasures.append(results['negf'])
        print "negative recall", neg_recalls
        print "postivie recall", pos_recalls
        print "negative precision", neg_precisions
        print "positive precision", pos_precisions

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
# print classif.classify("Awful, awful, awful. Nick Cage's worst movie and this is the guy who made Con Air. Magnetic boots that hold prisoners in place? What am I six years old?")
classif.tenFold()

