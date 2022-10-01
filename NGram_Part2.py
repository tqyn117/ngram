import pickle
from typing import List, Any

from nltk import word_tokenize
from nltk.util import ngrams


def probability(testData, uniDict, biDict, size):
    # Probability = (b + 1) / (u + v)
    # b = bigrams
    # u = unigrams
    # v = vocab size
    prob = 1
    for bigram in testData:
        if bigram in biDict:
            b = biDict[bigram]
        else:
            b = 0
        if bigram[0] in uniDict:
            u = uniDict[bigram[0]]
        else:
            u = 0
        prob = prob * ((b + 1) / (u + size))

    return prob


if __name__ == '__main__':
    # Create objects from previously created pickles
    englishBi = pickle.load(open('pickles/English_Bi_Dict.p', 'rb'))
    englishUni = pickle.load(open('pickles/English_Uni_Dict.p', 'rb'))
    frenchBi = pickle.load(open('pickles/French_Bi_Dict.p', 'rb'))
    frenchUni = pickle.load(open('pickles/French_Uni_Dict.p', 'rb'))
    italianBi = pickle.load(open('pickles/Italian_Bi_Dict.p', 'rb'))
    italianUni = pickle.load(open('pickles/Italian_Uni_Dict.p', 'rb'))

    # Size of the text is equal to all unigrams
    size = len(englishUni) + len(frenchUni) + len(italianUni)

    testFile = open('ngram_files/LangId.test', 'r').readlines()
    sol = open('ngram_files/LangId.sol', 'r').readlines()
    results = open('ngram_files/LangId.result', 'w')

    lineNum = 1
    wrong = 0
    for line in testFile:

        # Find unigrams and bigrams of test data
        unigrams = word_tokenize(line)
        bigrams = list(ngrams(unigrams, 2))

        # Find probabilities
        englishProb = probability(bigrams, englishUni, englishBi, size)
        print(englishProb)
        frenchProb = probability(bigrams, frenchUni, frenchBi, size)
        print(frenchProb)
        italianProb = probability(bigrams, italianUni, italianBi, size)
        print(italianProb)

        # Find most probabilistic language
        if englishProb < min(frenchProb, italianProb):
            lang = "English"
        elif frenchProb < min(englishProb, italianProb):
            lang = "French"
        elif italianProb < min(frenchProb, englishProb):
            lang = "Italian"
        else:
            lang = "Unknown"

        results.write(str(lineNum) + " " + lang + "\n")

        # Check if prediction was correct
        if sol[lineNum - 1] != str(str(lineNum) + " " + lang + "\n"):
            wrong += 1

        lineNum += 1

    # Print accuracy
    accuracy = ((300 - wrong) / 300) * 100
    print("Accuracy: " + str(accuracy) + '%')
    print("Incorrect: " + str(wrong))





