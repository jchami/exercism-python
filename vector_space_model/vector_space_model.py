import sys
import nltk
from math import log10, sqrt


# Library modules for stopwords
# nltk.download('rslp')
# nltk.download('stopwords')


# Global variables
DB_FILE = sys.argv[1]
QUERY_FILE = sys.argv[2]
WEIGHTS_FILE = 'pesos.txt'
ANSWER_FILE = 'resposta.txt'
STOPWORDS = nltk.corpus.stopwords.words('portuguese')


# Lists filenames contained in main database file
def extract_files(db_file):
    with open(db_file) as f:
        return f.read().splitlines()


# Returns list of stems from file after tokenization and stopword removal
def tokenize_and_stem(file):
    tokenizer = nltk.RegexpTokenizer(r'\w+')
    stemmer = nltk.stem.RSLPStemmer()

    with open(file) as f:
        tokens = tokenizer.tokenize(f.read()) 
        tokens = [t.lower() for t in tokens]
        tokens = [t for t in tokens if t not in STOPWORDS]
        
        return {file: [stemmer.stem(t) for t in tokens]}


# Returns sorted list of all unique stems across all files in database 
def extract_vocabulary(tokenized_files):
    vocabulary = [token for tokens in tokenized_files.values() for token in tokens]
    
    return sorted(list(set(vocabulary)))


# Returns map from file to number of occurrences of each word in said file
# e.g. word_freqs[doc1] = [doc1.count(word1), doc1.count(word2), ...]
def calculate_word_freqs(tokenized_files, vocabulary):
    word_freqs = {}
    for file in tokenized_files.keys():
        word_freqs[file] = [tokenized_files[file].count(token) for token in vocabulary]
    
    return word_freqs


# Returns list with word frequency across documents
# i.e. doc_freqs[i] is the amount of documents in which the i-th word in the vocabulary exists 
def calculate_doc_freqs(vocabulary, word_freqs):
    doc_freqs = [0] * len(vocabulary)
    for i in range(len(vocabulary)):
        for doc in word_freqs:
            doc_freqs[i] += 1 if word_freqs[doc][i] > 0 else 0

    return doc_freqs


# Returns weight list for each word in vocabulary
# i.e. idf[i] is idf weight for i-th word in vocabulary
def calculate_idf(N_docs, doc_freqs):
    idf = []
    for freq in doc_freqs:
        idf.append(log10(N_docs/freq))

    return idf


# Returns map from document to list of term frequency weights for each word
# e.g. tf[doc1] = [Wterm0, Wterm1, Wterm2, ...]
def calculate_tf(word_freqs):
    tf = {}

    for doc, freqs in word_freqs.items():
        tf[doc] = [1 + log10(freq) if freq > 0 else 0 for freq in freqs]

    return tf


# Returns map from document to list of term frequency weights for each word
# e.g. tf[doc1] = [Wterm0, Wterm1, Wterm2, ...]
def calculate_tf_idf(tf, idf):
    tf_idf = {}
    for doc in tf.keys():
        tf_idf[doc] = [tf[doc][i]*idf[i] for i in range(len(idf))]

    return tf_idf


# Writes weights to file, one line per document, for non-negative weights
def write_weights(out_file, tf_idf):
    WEIGHTS_FILE = open(out_file, "w")
    for doc in tf_idf:
        weights = "{}: ".format(doc)
        for i in range(len(tf_idf[doc])):
            if tf_idf[doc][i] > 0:
                weights += "{},{} ".format(i, tf_idf[doc][i])
        weights += "\n"
        WEIGHTS_FILE.write(weights)
    WEIGHTS_FILE.close()


# Returns map to tokenized, stemmed subqueries (separated at every disjunction)
def process_query(query_file):
    tokenizer = nltk.RegexpTokenizer(r'\w+')
    stemmer = nltk.stem.RSLPStemmer()

    with open(query_file) as f:
        query = f.read().replace(' ', '')
    
    subqueries = [[stemmer.stem(token) for token in tokenizer.tokenize(sub)] for sub in query.split('|')]
    subqueries = {i: subqueries[i] for i in range(len(subqueries))}

    return subqueries


# Returns map from document to list of similarities for each subquery
def calculate_similarity(tf_idf, tf_idf_query):
    similarity = {}
    for doc in tf_idf:
        similarity[doc] = []
        for subquery in tf_idf_query.values():
            numerator = sum([tf_idf[doc][i]*subquery[i] for i in range(len(subquery))])
            denominator1 = sqrt(sum([tf_idf[doc][i]**2 for i in range(len(subquery))]))
            denominator2 = sqrt(sum([subquery[i]**2 for i in range(len(subquery))]))
            
            similarity[doc].append(numerator/(denominator1*denominator2))

    return similarity


# Writes number of documents that satisfy query to file, as well as query results in decreasing order of similarity
def write_results(result_file, similarity):
    N_docs = sum([1 if measure > 0.001 else 0 for doc in similarity for measure in similarity[doc]])
    
    ranking = sorted([measure for doc in list(similarity.values()) for measure in doc if measure > 0.001])
    f = open(result_file, 'w')
    f.write("{}\n".format(N_docs))

    for measure in ranking[::-1]:
        for doc in similarity:
            if measure in similarity[doc]:
                f.write('{}: {}\n'.format(doc, measure))
                ranking.pop()

    f.close()


# Main execution block
if __name__ == '__main__':
    file_list = extract_files(DB_FILE)
    # print(file_list)

    N_docs = len(file_list)
    # print(N_docs)

    tokenized_files = {}
    for f in file_list:
        tokenized_files.update(tokenize_and_stem(f))
    # print(tokenized_files)

    vocabulary = extract_vocabulary(tokenized_files)
    # print(vocabulary)
    
    word_freqs = calculate_word_freqs(tokenized_files, vocabulary)
    # print(word_freqs)

    doc_freqs = calculate_doc_freqs(vocabulary, word_freqs)
    # print(doc_freqs)

    idf = calculate_idf(N_docs, doc_freqs)
    # print(idf)

    tf = calculate_tf(word_freqs)
    # print(tf)

    tf_idf = calculate_tf_idf(tf, idf)
    # print(tf_idf)

    write_weights(WEIGHTS_FILE, tf_idf)

    subqueries = process_query(QUERY_FILE)
    # print(subqueries)

    word_freqs_query = calculate_word_freqs(subqueries, vocabulary)
    # print(word_freqs_query)

    tf_query = calculate_tf(word_freqs_query)
    # print(tf_query)

    tf_idf_query = calculate_tf_idf(tf_query, idf)
    # print(tf_idf_query)

    similarity = calculate_similarity(tf_idf, tf_idf_query)
    # print(similarity)

    write_results(ANSWER_FILE, similarity)