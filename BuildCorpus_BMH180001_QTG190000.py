from bs4 import BeautifulSoup
import requests
import urllib.request
import pickle
from os import listdir
from os.path import isfile, join
import re
from nltk import sent_tokenize
from nltk import word_tokenize
from nltk.corpus import stopwords
from nltk.probability import FreqDist

STOPWORDS = set(stopwords.words('english'))


def crawler(starter_url):
    # Crawl through using FIFO queue and each url will add 3 URL to the queue until we have 20 valid URLs
    visited = 0
    maxpages = 20
    queue = [starter_url]
    crawled = []
    # Filter applied to URLs to avoid social media websites and accept matching URLs
    ignore_keys = ['comment', 'share', 'rank', 'index', 'click', 'Query', 'submit', 'direct',
                   'tweet', 'create', 'save', 'send', 'archive', 'automation', 'book', 'tv', 'plus']
    accept_keys = ['Horror', 'horror']
    # Loop through the queue to visit valid unique URLs
    while visited < maxpages and queue:
        url = queue.pop(0)

        r = requests.get(url)

        data = r.text
        soup = BeautifulSoup(data, "html.parser")

        crawled.append(url)
        visited += 1
        count = 0
        # Append 3 links from a single URL into list with additional filters
        for link in soup.find_all('a'):
            link_str = str(link.get('href'))
            if any(ignore in link_str for ignore in ignore_keys):
                continue
            if any(accept in link_str for accept in accept_keys):
                if link_str.startswith('/url?q='):
                    link_str = link_str[7:]
                if '&' in link_str:
                    i = link_str.find('&')
                    link_str = link_str[:i]
                if link_str.startswith('http'):
                    # Check if the URL is unique
                    if link_str not in crawled and link_str not in queue:
                        # Check if the URL is valid in case of HTTP Error
                        try:
                            urllib.request.urlopen(link_str)
                        except urllib.error.URLError:
                            continue
                        queue.append(link_str)
                        count += 1
                        if count >= 3:
                            break
    return crawled


def scraper(queue):
    for url in queue:
        html = urllib.request.urlopen(url, timeout=2).read()
        soup = BeautifulSoup(html, "html.parser")

        # Remove all scripts and styles
        for script in soup(['script', 'style']):
            script.extract()    # Remove script and style

        # Extract text
        text = soup.get_text()
        # Write the scraped text into a file using pickle
        pickle.dump(text, open('scraped/text{}.txt'.format(queue.index(url)), 'wb'))


def process():
    # Get a list of files from scraped directory to process
    files = [f for f in listdir('scraped') if isfile(join('scraped', f))]
    for file in files:
        # Open the scraped text file from pickle
        raw_text = pickle.load(open('scraped/{}'.format(file), 'rb'))
        # Removal of undesired character
        raw_text = raw_text.replace('\t', '').replace('\n', '').replace(u'\xa0', '').strip()
        sent_tokens = sent_tokenize(raw_text)
        # Write the processed scraped text into a file using pickle
        pickle.dump(sent_tokens, open('processed_scraped/{}'.format(file), 'wb'))


def extractFrequent():
    # Extract important words from the processed text
    files = [f for f in listdir('processed_scraped') if isfile(join('processed_scraped', f))]
    for file in files:
        tokens = []
        raw_text = pickle.load(open('processed_scraped/{}'.format(file), 'rb'))
        for sentence in raw_text:
            sent = re.sub(r'[^\w\s]', '', sentence)
            tokens += word_tokenize(sent)
        no_stop = [w for w in tokens if not w.lower() in STOPWORDS]
        freq = FreqDist(no_stop)
        frequent = freq.most_common(25)
        print(frequent)
        # Write the important terms into a file using pickle
        pickle.dump(frequent, open('important_terms/{}'.format(file), 'wb'))


def buildKnowledgeBase():
    knowledge_base = {
        'films': 'Motion pictures date all the way back to the 1890s when the first moving picture cameras were invented.',
        'horror': '\'Horror\' comes from a Latin verb meaning \"to bristle\" or \"to shudder.\"',
        'smile': 'Smiling can actually help us live longer.',
        'trailer': 'The first trailer was released in 1913.',
        'scream': 'Screaming is exhibited by many animals, but no species uses this extreme vocalization in as many different contexts as humans.',
        'hours': 'There is slightly less than 24 hours in a day',
        'family': 'A family is complete with or without children, as long as there is an association of two or more persons.',
        'dark': 'The fear of the darkness is called Nyctophobia.',
        'blumhouse': 'Blumhouse Pictures produced the box office hit Tooth Fairy, starring Dwayne \"The Rock\" Johnson.',
        'think': 'The average person has around 70 thousand thoughts per day.'
    }
    pickle.dump(knowledge_base, open('knowledge_base', 'wb'))

if __name__ == '__main__':
    # Topic is Horror film
    url_list = crawler("https://en.wikipedia.org/wiki/Horror_film")
    scraper(url_list)
    process()
    extractFrequent()
    top10 = ['films', 'horror', 'smile', 'trailer', 'scream', 'hours', 'family', 'dark', 'blumhouse', 'think']
    buildKnowledgeBase()
