import math
import xmlParser as xP
import utils
import collections


class TfIdf:
    """
       This is the class for tfidf where the approach has been presented as object oriented concept.

    Attributes

    collectionName
    unique_words
    self.tf
    self.idf
    


    """

    def __init__(self, collectionName):
        """
        Parameters (str) : name of collection
        """
        
        self.collectionName = collectionName
        self.unique_words = set()
        self.docids = set()
        self.tf = dict()
        self.idf = dict()



    def read_data(self):
        """
        reads the xml data and returns the dictionary containing document id, text and headline

        Returns:
        dict: {"docid":[headline, text]}
        """
        
        return xP.get_data(self.collectionName)



    def create_idf(self):
        """
        writes invert document frequency in a tab separated file
        """
        with open(self.collectionName + ".idf", "w") as f:
            for key, value in self.idf.items():
                f.write(key + "\t" + str(value) + "\n")


    def doc_freq(self, preprocessed):
        """
        calculate the document frequency for each term. Document frequency is the count of documents the particular token is in.
        Parameter:
        preprocessed (dict): keys are document id and values are list of tokens which were preprocessed.

        Returns:
        dictionary: keys are tokens and values are the document frequency of that token.

        """

        DF = collections.defaultdict(set)
        for docid, tokens in preprocessed.items(): #iterate over documents
            for w in tokens:
                DF[w].add(docid) # adding docid to the dictionary

        return DF



    def term_freq(self, docid, tokens, token):
        """
        creates the term frequency per document per token

        Parameter:
        docid (str): document id
        tokens(list of string): list of tokens in a document
        token (string): a single token whose term frequency to be calculated

        Returns:
        dictionary: keys are tuple of document and token. Values are the term frequency.
        """

        occurence_count = collections.Counter(tokens) #counts the frequency of tokens
        maxOccurence = occurence_count.most_common(1)[0][1] #get the max occurence value
        return occurence_count[token]/maxOccurence #calculate term frequency



    def create(self):
        """
        the main create function that calculates document frequency, inverse document frequency, term frequency and send it to write in a file.


        """
        print("Creating the index file")         
        data = self.read_data()
        preprocessed =  utils.preprocessing(data) #preprocessing tokens
        doc_freq= self.doc_freq(preprocessed) #get document frequency for each token
        num_doc = len(preprocessed)
        self.idf = {key: math.log(num_doc/len(value)) for key,value in doc_freq.items()} #calculate inverse document frequency for each token
        self.idf = dict( sorted(self.idf.items(), key=lambda x: x[0].lower()) ) #sorting alphabetically
        self.create_idf() #write idf to an index file
        

        self.unique_words = list(self.idf.keys()) #getting unique_words
        
        preprocessed = dict(sorted(preprocessed.items(), key=lambda x: x[0]))
        self.docids = preprocessed.keys()

        f  = open(self.collectionName + ".tf", "w")

        self.tf = collections.defaultdict()
        for docid, tokens in preprocessed.items():
            for word in set(tokens):
                tf = self.term_freq(docid, tokens, word) #calculating term frequency
                self.tf[(docid,word)] = tf
                f.write(docid + "\t"+word +"\t" + str(tf) + "\n")
        print("Done")
        f.close()


    def load(self):
        """
        Reads the term frequencies and inverse document frequencies and write it into the attribute self.tf and self.idf.
        """

        print("Reading index from file...")
        self.tf = collections.defaultdict()
        self.idf = collections.defaultdict()
        with open(self.collectionName +".idf", "r") as f:
            data = f.readlines()
            for line in data: #each line of idf
                line = line.strip().split("\t") #split by tab
                self.idf[line[0]] = float(line[1]) #convert string value to float

        self.unique_words = list(self.idf.keys()) #updating unique words
        with open(self.collectionName +".tf", "r") as f:
            data = f.readlines()
            for line in data:
                line = line.strip().split("\t")
                self.tf[(line[0], line[1])] = float(line[2]) #convert string value to float
                self.docids.add(line[0])
        print("Done")







