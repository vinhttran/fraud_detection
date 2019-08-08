import pandas as pd
pd.set_option('display.max_colwidth', -1)
import re
from string import digits
import nltk
from html.parser import HTMLParser

'''you must have nltk packages installed to run this file. To do so run the following commands:

import ntlk 
nltk.download()

A new window should open, showing the NLTK Downloader. Click on the File menu and select Change Download Directory. 
For central installation, set this to C:\nltk_data (Windows), /usr/local/share/nltk_data (Mac)'''

class MLStripper(HTMLParser):
    '''This class parses HTML from the description column
    input: string
    output: string'''
    def __init__(self):
        self.reset()
        self.strict = False
        self.convert_charrefs= True
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)

def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()

def clean_desc(df):

    '''cleans the data. see below for documentation. adds three new columns:
    df['description_clean'] is the new cleaned description data
    df['description_html'] are the descriptions written in html
    df['description_none'] are the descriptions with no text
    '''
    
    #creates a new column for all events using HTML invites
    df['description_html'] = df['description'].apply(lambda x: True if ('</span>' or '</div>') in x else False)

    #strips HTML documentation
    df['description_clean'] = df['description'].apply(lambda x: strip_tags(x))

    #replaces artifacts from HTML tht didn't get cleaned up through the strip_tags script
    df['description_clean'] = df['description_clean'].apply(lambda x: x.replace('\r',''))
    df['description_clean'] = df['description_clean'].apply(lambda x: x.replace('\n',''))
    df['description_clean'] = df['description_clean'].apply(lambda x: x.replace('</li>',''))
    df['description_clean'] = df['description_clean'].apply(lambda x: x.replace('<li>',' '))
    
    #remove websites
    df['description_clean'] = df['description_clean'].apply(lambda x: re.sub(r'www\.\S+\.com', '', x, flags=re.MULTILINE))

    #remove websites
    df['description_clean'] = df['description_clean'].apply(lambda x: re.sub(r'^https?:\/\/.*[\r\n]*', '', x, flags=re.MULTILINE))
    
    #remove email addresses
    df['description_clean'] = df['description_clean'].apply(lambda x: re.sub('\S*@\S*\s?','', x))

    #remove special characters
    df['description_clean'] = df['description_clean'].apply(lambda x: re.sub('\W+',' ', x )) 
    
    # remove numbers from string
    df['description_clean'] = df['description_clean'].apply(lambda x: re.sub(r'\d+', '', x))
    
    # lower case everything
    df['description_clean'] = df['description_clean'].apply(lambda x: x.lower())

    #removes non-english words
    words = set(nltk.corpus.words.words())
    df['description_clean'] = df['description_clean'].apply(lambda x: " ".join(w for w in nltk.wordpunct_tokenize(x) if w.lower() in words or not w.isalpha())) 

    df['description_none']= df['description_clean']==''

    return df