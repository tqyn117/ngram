from nltk import word_tokenize
from nltk.util import ngrams
import pathlib
import pickle


def ngram_generator(filepath):
    # Access the file to read from the given filepath
    input_file = open(pathlib.Path.cwd().joinpath(filepath), encoding='utf-8', mode='r')
    # Remove newlines and tokenize the text
    raw_text = input_file.read()
    raw_text = raw_text.replace('\n', '')
    tokens = word_tokenize(raw_text)
    # Create list of unigrams and bigrams
    unigrams = ngrams(tokens, 1)
    bigrams = ngrams(tokens, 2)
    # Create dictionary of unigrams and bigrams
    unigram_dict = {}
    for uni in set(unigrams):
        unigram_dict[uni[0]] = raw_text.count(uni[0])
    bigram_dict = {}
    for bigram in set(bigrams):
        if bigram not in bigram_dict:
            bi = bigram[0] + " " + bigram[1]
            bigram_dict[bi] = raw_text.count(bi)

    return unigram_dict, bigram_dict


if __name__ == '__main__':
    # Hard coded to call the ngram function once for each language
    # Then pickle the unigram and bigram dictionaries from the function
    uni_dict, bi_dict = ngram_generator('ngram_files/LangId.train.English')
    pickle.dump(uni_dict, open('pickles/English_Uni_Dict.p', 'wb'))
    pickle.dump(bi_dict, open('pickles/English_Bi_Dict.p', 'wb'))

    uni_dict, bi_dict = ngram_generator('ngram_files/LangId.train.French')
    pickle.dump(uni_dict, open('pickles/French_Uni_Dict.p', 'wb'))
    pickle.dump(bi_dict, open('pickles/French_Bi_Dict.p', 'wb'))

    uni_dict, bi_dict = ngram_generator('ngram_files/LangId.train.Italian')
    pickle.dump(uni_dict, open('pickles/Italian_Uni_Dict.p', 'wb'))
    pickle.dump(bi_dict, open('pickles/Italian_Bi_Dict.p', 'wb'))