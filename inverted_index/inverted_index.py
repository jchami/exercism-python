import sys
import nltk


# For stem extraction and stopword list
nltk.download('rslp')
nltk.download('stopwords')


# Global variables
DB_FILE = sys.argv[1]
OUT_FILE = 'index.txt'
STOPWORDS = nltk.corpus.stopwords.words('portuguese')


# Lists filenames contained in db file (one per line)
def extract_files(db_file):
    filenames = []
    with open(db_file) as f:
        return f.read().splitlines()


# Reads file, extracts words (lowercase), remove stopwords and punctuation and extracts stems
def extract_stems(filename):
    tokenizer = nltk.RegexpTokenizer(r'\w+')
    stemmer = nltk.stem.RSLPStemmer()
    
    with open(filename) as f:
        words = tokenizer.tokenize(f.read()) 
        words = [w.lower() for w in words]
        words = [w for w in words if w not in STOPWORDS]
        
        return [stemmer.stem(w) for w in words]


# Generates inverted index from list of stems
def inverted_index(stems, i):
    index = {}
    for stem in stems:
        index.update({stem: '{},{}'.format(i, stems.count(stem))})
    return index


# Joins multiple inverted indices (concatenates values of repeated keys)
def join_indices(index_list):
    seen = {}
    uniq = {}

    for index in index_list:
        for stem, quant in index.items():
            if stem in seen:
                seen.update({stem: '{} {}'.format(seen[stem], quant)})
            elif stem in uniq:
                seen.update({stem: '{} {}'.format(uniq[stem], quant)})
                uniq.pop(stem, None)
            else:
                uniq.update({stem: quant})

    return {**seen, **uniq}


# Writes index to index.txt
def write_index(index):
    with open('index.txt', 'w') as f:
        for stem, quant in index.items():
            f.write('{}: {}\n'.format(stem, quant))


# Executes when file is executed
if __name__ == '__main__':
    db = extract_files(DB_FILE)
    
    index_list = []
    for i in range(len(db)):
        stems = extract_stems(db[i])

        index_list.append(inverted_index(stems, i+1))


    index = join_indices(index_list)
    write_index(index)
