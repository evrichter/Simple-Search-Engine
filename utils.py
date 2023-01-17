"""
This file contains modular snippet of functions that could be reused in various projects. It is coined as utilities

"""





import re
import string
from stemming.porter2 import stem

def removing_empty_tokens( text):
        """
        removes the token if it is an empty string.

        Parameters:
        text (list): list of tokens

        Returns:
        list: list of tokens filtered

        """

        text = [token.strip() for token in text if token.strip() not in [""," ",'',' ']] #filtering tokens
        return text

def tokenize(text):
        """
        it tokenizes the text passes
        Parameters:
        text (str) : text to be tokenized

        Returns:
        list: list of tokens
        """

        return text.split() #tokenizing

def stemming(text):
    """
    stems each word.
    Parameters: 
    text (list): list of tokens
    Returns:
    list: stemmed list of tokens
    """
    text = [stem(word) for word in text] #stemming by iterating over tokens

    
    return text

def cleaning(text):
    """
    removes xml tags.
    Parameters: 
    text (str): text
    Returns:
    str: cleaned text

    """
    text = re.sub('<[^<]+>', "", text) #regex to replace xml tags
    return text

def remove_punctuation(text):
    """
    Removes punctuation from tokens
    Parameter:
    text (list): list of token
    Returns:
    list: list of cleaned tokens

    """
    cleaned_tokens = []
    for token in text: #iterate over list of tokens
        token = token.strip() #strip to remove extra whitespace
        translator = re.compile('[%s]' % re.escape(string.punctuation)) #regex to detect punctuation character
        token = translator.sub('', token) #replaces punctuation with empty string
        cleaned_tokens.append(token)
    return cleaned_tokens


def preprocessing(text):
    """
    Parameter:
    text (list): list of tokens
    """
    new_dict = dict()
    for key, each in text.items():
        doc_id = key
        doc = " ".join([x.strip() for x in each])
        doc = cleaning(doc)
        doc = doc.lower()
        doc = tokenize(doc)
        doc = remove_punctuation(doc)
        doc = stemming(doc)
        doc = removing_empty_tokens(doc)
        new_dict[doc_id] = doc

    return new_dict


def similarity( value1_d, value2, value1_n):
        """
        calculate the cosine similarity between two vector
        Parameters:
        value1_n (list): list of float values representing a document as a vector
        value2 (list): list of float values representing a document as a vector
        value1_d float: cosine similarity score (list): list of float values representing a document as a vector
        Returns:
        float: cosine similarity score

        """

        norm1 = sum([x ** 2 for x in value1_d]) ** 0.5 #norm value for vector 1
        norm2 = sum([x ** 2 for x in value2]) ** 0.5 #norm value for vector 2
        dot_p = sum([x *y for x,y in zip(value1_n, value2)]) # dot product of two vector

        return dot_p/(norm1*norm2)

