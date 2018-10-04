import re


def word_count(phrase):
    phrase = phrase.lower()
    pattern = re.compile(r'[a-zA-Z0-9]+\'[a-zA-Z0-9]+|[a-zA-Z0-9]+', re.I)
    match = pattern.findall(phrase)
    return {i: match.count(i) for i in match}
