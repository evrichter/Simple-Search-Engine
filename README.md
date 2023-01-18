## Simple Search Engine

In this final project for the **Introduction to Python** course held in the **WS 2020/21** at **Saarland University** the task was to implement a simple **search engine** using a **vector space retrieval model**. <br />

The searche engine is based on the tfidf weighting scheme which was developed specifically for document search and information retrieval. The idea is to find out how relevant a word is in a collection of documents by multiplying the number of times a word appears in a document (term frequency) by the inverse document frequency of the word across a number of documents. The tfidf score increases proportionally to the number of occurrences of a word in a document, but at the same time is balanced by the number of documents containing the word. Accordingly, words that occur in every document receive a low score, even if they occur very frequently, because they have no particular significance for the respective document. More information on this as well as the mathematical background can be found in the pdf file on **vector space models**, which contains the second part of the project, namely an essay on the essential aspects of vector space models. <br />

Furthermore, a pdf containing the documentation of the practical part of the project can be found along with the other files.
