

import re
import string
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

sastrawi = StopWordRemoverFactory()
stopword_list = ' '.join(stopwords.words('indonesian') + sastrawi.get_stop_words())
stopword_list = word_tokenize(stopword_list)
stopword_list.remove('tidak') # remove 'tidak' from stopword since it may be related to negative sentiment
stopword_list.remove('tidak')
stemmer = StemmerFactory()
stemmer = stemmer.create_stemmer()

# removing emojis (source: https://gist.github.com/slowkow/remove-emoji.py)
def remove_emoji(string):
    emoji_pattern = re.compile("["
                               u"\U0001F600-\U0001F64F"  # emoticons
                               u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                               u"\U0001F680-\U0001F6FF"  # transport & map symbols
                               u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                               u"\U00002500-\U00002BEF"  # chinese char
                               u"\U00002702-\U000027B0"
                               u"\U00002702-\U000027B0"
                               u"\U000024C2-\U0001F251"
                               u"\U0001f926-\U0001f937"
                               u"\U00010000-\U0010ffff"
                               u"\u2640-\u2642"
                               u"\u2600-\u2B55"
                               u"\u200d"
                               u"\u23cf"
                               u"\u23e9"
                               u"\u231a"
                               u"\ufe0f"  # dingbats
                               u"\u3030"
                               "]+", flags=re.UNICODE)
    return emoji_pattern.sub(r'', string)

def clean_text(text):
    text = re.sub(r'[0-9]+', '', text) # remove numbers
    text = text.replace('\n', ' ') # change enter to space
    text = text.replace(r'[^\w\d\s]', ' ')
    text = text.replace(r'\s+', ' ')
    text = text.replace(r'^\s+|\s+?$', ' ')
    text = remove_emoji(text)
    
    # "barang" is removed, since it will always be included in both sentiment
    text = text.replace(r'barang', '')
    text = text.replace(r'nya', '')
    text = text.translate(str.maketrans(' ', ' ', string.punctuation)) #remove punctuation
    text = text.strip(' ') # remove space char from both left and right text
    return text

def lower_text(text):
    return text.lower()

def tokenize_text(text):
    return word_tokenize(text)
    
def filter_text(text):
    filtered = list()
    for txt in text:
        if txt not in stopword_list:
            filtered.append(txt)
    text = filtered
    return text

def stem_text(text):
    text = [stemmer.stem(word) for word in text]
    return text

def to_sentence(word_list):
    sentence = ' '.join(word for word in word_list)
    return sentence

def preprocess_text(text):
    text = lower_text(text)
    cleaned_ = clean_text(text)
    tokenized_ = tokenize_text(cleaned_)
    filtered_ = filter_text(tokenized_)
    stemmed_ = stem_text(filtered_)
    sentence_ = to_sentence(stemmed_)
    return cleaned_, stemmed_, sentence_