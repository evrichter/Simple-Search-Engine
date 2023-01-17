
'''
Introduction to Python Programming (aka Programmierkurs I, aka Python I)
Software Assignment
'''

import sys
import argparse
import tfidf
import utils
from collections import defaultdict

class SearchEngine:

    def __init__(self, collectionName, create):
        '''
        This function calls the tfodf class to read index or create it and then loads the tfidf vector for each document. The tfidf vector is loaded here\
                so that the search function will be faster. Instead of loading tfidf vector for each document over each iteration of query, doing it once\
                is more efficient.
        Parameters:
        collectionName (str): name of the collection
        create (bool): whether to create the index or load it.

        Returns:
        None

        Initialize the search engine, i.e. create or read in index. If
        create=True, the search index should be created and written to
        files. If create=False, the search index should be read from
        the files. The collectionName points to the filename of the
        document collection (without the .xml at the end). Hence, you
        can read the documents from <collectionName>.xml, and should
        write / read the idf index to / from <collectionName>.idf, and
        the tf index to / from <collectionName>.tf respectively. All
        of these files must reside in the same folder as THIS file. If
        your program does not adhere to this "interface
        specification", we will subtract some points as it will be
        impossible for us to test your program automatically!
        '''
        self.tf_obj = tfidf.TfIdf(collectionName) #calls tfidf class
        if create == "True":
            self.tf_obj.create() #creates index by reading xml file for collection
        
        else:
            self.tf_obj.load() #loads the index files


    
    
    def executeQuery(self, queryTerms):
        '''
        This functions process the query and searches for similar document and prints those with similarity score.
        Parameters:
        queryTerms (list of string): query tokens to be searched

        Returns:
        None

        Input to this function: List of query terms

        Returns the 10 highest ranked documents together with their
        tf.idf-sum scores, sorted score. For instance,

        [('NYT_ENG_19950101.0001', 0.07237004260325626),
         ('NYT_ENG_19950101.0022', 0.013039249597972629), ...]

        May be less than 10 documents if there aren't as many documents
        that contain the terms.
        '''

        inference_doc = {"inference":queryTerms} #creating a dictionary for queries in format of document
        inference_doc = utils.preprocessing(inference_doc) #preprocessinf the query passes
        inference_tfidf = []
        queryTerms = inference_doc["inference"]

        for token in set(queryTerms):
            
            tf = self.tf_obj.term_freq("inference",queryTerms, token) # getting the term frequency for the query document
            inference_tfidf.append(tf * self.tf_obj.idf.get(token,0))

        if all(x == 0 for x in inference_tfidf): # check if terms are not available in the corpus
            print("Sorry, I didn’t find any documents for this term.")
            return False

        doc_sim = defaultdict()
        for docid in self.tf_obj.docids: #iterating through each corpus document
            doc_tfidf_n = [ self.tf_obj.tf.get((docid, token), 0)*self.tf_obj.idf.get(token,0) for token in set(queryTerms)] #tfidf vector of document based on unique query tokens only
            doc_tfidf_d = [ self.tf_obj.tf.get((docid, token), 0)*self.tf_obj.idf.get(token,0) for token in self.tf_obj.unique_words] #tfidf vector of document based on all unique tokens only
            
            assert len(doc_tfidf_n) == len(inference_tfidf) #check if dimension is same for dot product
            if all(x == 0 for x in doc_tfidf_n): #check if queries are not at all related to document
                doc_sim[docid] = 0
            else:
                sim = utils.similarity(doc_tfidf_d, inference_tfidf, doc_tfidf_n) # calculating similarity between each document and query
                doc_sim[docid] = sim

        t = sorted(doc_sim.items(), key=lambda x:-x[1])[:10] #sorting the documents based on similarity
        print("I found the following documents:")
        for k,v in t: #printing the documents with largest similarity score
            if v != 0:
                print(k, "("+ str(v) + ")")


        
    def executeQueryConsole(self):
        '''
        This function is a console that asks for user's query in loop unless they click ENTER

        Returns:
        None

        When calling this, the interactive console should be started,
        ask for queries and display the search results, until the user
        simply hits enter.
        '''
        data = str(input("Please enter query, terms separated by whitespace:"))
        if data != "":
            return data.split(" ")
        else:
            return False

    
if __name__ == '__main__':
    '''
    write your code here:
    * load index / start search engine
    * start the loop asking for query terms
    * program should quit if users enters no term and simply hits enter
    '''
    # Example for how we might test your program:
    # Should also work with nyt199501 !


    parser = argparse.ArgumentParser(description='Simple search engine')
    parser.add_argument('-create',default="True", type=str,
                    help='option whether to create index file or read it from available one')
    parser.add_argument('-collectionname',default="nytsmall", type=str,
                    help='name of the xml file')
    args = parser.parse_args()
    searchEngine = SearchEngine(args.collectionname, create=args.create)
    while True:
        query = searchEngine.executeQueryConsole()
        if query:
            searchEngine.executeQuery(query)
        else:
            sys.exit()

