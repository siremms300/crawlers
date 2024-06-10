import pickle 
import os 
from bs4 import BeautifulSoup 
import requests 

import nltk
from nltk.corpus import stopwords

# Download NLTK stopwords
nltk.download('stopwords') 
nltk.download('punkt')

def save_tokenized_text(tokenized_text, filename):
    with open(filename, 'wb') as f:
        pickle.dump(tokenized_text, f) 

if not os.path.exists('tokenized_text.pkl'):
    websites = ['https://www.university-directory.eu/USA/Alabama', 
                'https://www.university-directory.eu/USA/Alaska',
                'https://www.university-directory.eu/USA/Arizona' 
                ] 

    text_content = [] 

    for website in websites:
        response = requests.get(website) 
        soup = BeautifulSoup(response.text, 'html.parser') 
        text_content.append(soup.get_text()) 

    # Get NLTK English stopwords
    stop_words = set(stopwords.words('english'))

    tokenized_text = [] 
    for text in text_content:
        words = nltk.word_tokenize(text)
        filtered_words = [word.lower() for word in words if word.isalnum() and word.lower() not in stop_words]
        tokenized_text.append(filtered_words)

    # Save tokenized text
    save_tokenized_text(tokenized_text, 'tokenized_text.pkl')