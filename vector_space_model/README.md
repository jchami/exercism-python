# Vector Space Model

Vector Space Model implementation for information retrieval purposes. Takes query file and db file and generates:

* File containing non-negative tf-idf weights for each term
* File containing query results (cosine similarity) in decreasing order

## Usage
```python vector_space_model.py db.txt query.txt```

Generates weights.txt and result.txt files.
Requires NLTK python package.