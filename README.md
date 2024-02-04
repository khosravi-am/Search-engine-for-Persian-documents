# Search-engine-for-Persian-documents
This project is a search engine for retrieving Persian text documents, the user enters her query and the system retrieves related documents.

# Data collection:
The dataset used in this project is a collection of news retrieved from several Persian news websites, which is in a JSON file. Only the content of "content" is processed as the content of the document.
The number of each news is considered as the ID of that document, and at the time of answering the query, it shows the title of the news and the URL related to the retrieved document, so that it is possible to check the correct functioning of the system.

The data set has been reduced to 1000 data to reduce the file size. You can replace your json file and make it much bigger.

# Positional Index
In the first stage of the project, in order to create a simple information retrieval model, a positional index is created for the given data set so that when the request is received, the positional index created can be used to retrieve related documents.

# To preprocess the documents used hazm library
https://github.com/roshan-research/hazm


# Document modeling in vector space:
To model the documents in the vector space, the tf-idf weighting method has been used, and a numerical vector is calculated for each document, and finally, each document is represented as a vector including the weights of all the words in that document. The weight of each word t in a document d is calculated by having the set of all documents D using the following relationship:
TFIDF(t,d,D) = TF(t,d) × IDF(t,D) = (1 + log( F(t,d))) × log(N/n(t))
https://www.geeksforgeeks.org/understanding-tf-idf-term-frequency-inverse-document-frequency/

# Answering queries in a vector space:
Different distance criteria can be considered for this task. In this project, cosine similarity between vectors is considered.
In this way, we first extract the specific vector of the query (the weight of the words in the query) and then, using the cosine similarity criterion, we find the documents that have the most similarity (the least distance) to the input query. Then the results are displayed in order of similarity.
https://www.geeksforgeeks.org/cosine-similarity/

# Increasing the speed of query processing
To increase the speed of query processing, we use the hero list in such a way that after building the positional index for each word, we create a list of documents in which the weight of that word is greater than the constant value r.



# Installation hazm
To install the latest version of Hazm, run the following command in your terminal:

```
pip install hazm
```

# Usage
```
python main.py
```

