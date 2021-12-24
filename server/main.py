from flask import Flask, request, Response
from flask_cors import CORS

import pandas as pd

from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer

import string
import random

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def load_data(file_name):
    '''
    Loads the file and transform the number(IDs) to int
    returns it as a dataframe
    '''
    cards = pd.read_json(file_name, orient='records')
    cards = pd.json_normalize(cards['cards'])

    cards['number'] = cards['number'].astype('int')
    return cards


def create_soup(x):
    '''
    Combine text (rows) of wanted columns
    '''
    return ' '.join(x['fortune_telling']) + ' ' + ' '.join(x['keywords']) + ' ' + ' '.join(x['Questions to Ask']) + ' ' + ' '.join(x['meanings.light']) + ' ' + ' '.join(x['meanings.shadow'])


def clean_data(text):
    """
    This function handels the text pre-processing:
    1) Removes digits;
    2) Removes punctuations
    3) splits text for:
        a) lemmatizing
        b) Stemming
        b) Stop words removal
    4) Joins tokens
    5) Double-checks the spaces then returns text in form of a joined string
    """
    stop_words = stopwords.words("english")

    text = "".join([i for i in text if not i.isdigit()])
    text = text.translate(str.maketrans("", "", string.punctuation))
    tokens = text.split()
    text = [WordNetLemmatizer().lemmatize(word) for word in tokens]
    text = [PorterStemmer().stem(word) for word in text]
    text = [word for word in text if word not in stop_words]
    text = " ".join(text)
    while "  " in text:
        text = text.replace("  ", " ")

    return text


def getSimilarity(cards, query):
    """
    Counts the Tf/IDF for each of the cards and the query
    Calculates the Cosine similarity between cards & query matrices
    returns the similarity scores
    """
    vectorizer = TfidfVectorizer(
        lowercase=True,
        # max_features=100,
        max_df=0.8,
        min_df=2,
        ngram_range=(1, 3),
        stop_words="english"
    )

    cards_matrix = vectorizer.fit_transform(cards)

    # Transform documents to document-term matrix.
    query_matrix = vectorizer.transform([query])
    print(cards_matrix.shape)
    print(query_matrix.shape)

    # feature_names = vectorizer.get_feature_names_out()
    # print(feature_names)

    # cosine similarity between the matrices (vectors)
    cosine_sim = cosine_similarity(cards_matrix, query_matrix)
    # print(cosine_sim)
    return cosine_sim


def get_random_words(text):
    '''
    Gets random words from the text
    '''
    tokens = text.split()
    # print random string
    randomWords = random.choice(tokens)
    return randomWords


# initalizing app with cors rules
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*",
     "allow_headers": "*", "expose_headers": "*"}})


@ app.route('/cards', methods=["GET"])
def cards():
    """
    Function for handeling the Route's HTTP get requests
    returns following responses to client:
        a) List of random words if query after cleaning is empty
        b) List of matching cards if query has matches
        c) List of random words if query has no matches
    """

    query_client = request.args.get('query', '')
    cards = load_data('../data/tarot-images.json')
    cards['soup'] = cards.apply(create_soup, axis=1)
    cards['soup'] = cards['soup'].apply(lambda x: clean_data(x))

    # Apply text processing on the query
    cleaned_query = clean_data(query_client)

    # Check if the string after cleaning is not empty otherwise return random words
    if not cleaned_query:
        # Retun a random list of words for the user
        cards["random_words"] = cards['soup'].apply(
            lambda x: get_random_words(x))
        response = cards["random_words"].head(
            5).to_json(orient="records", indent=4)
        return Response(response, status=200, mimetype='application/json')

    # checking similarity (matching scores)
    else:
        # create column with the similarity scores, then sort it in desnding order
        cards['similarity_scores'] = getSimilarity(
            cards['soup'], cleaned_query)
        cards = cards.sort_values(["similarity_scores"], ascending=False)

        # check if there are scors
        for score in cards["similarity_scores"].head(3):
            # Retun the top 3 matching cards for the user
            if score != 0.000000:
                response = cards.head(3).to_json(orient="records", indent=4)
                return Response(response, status=200, mimetype='application/json')
            else:
                # Retun a random list of words for the user
                cards["random_words"] = cards['soup'].apply(
                    lambda x: get_random_words(x))
                response = cards["random_words"].head(
                    5).to_json(orient="records", indent=4)
                return Response(response, status=200, mimetype='application/json')


if __name__ == "__main__":
    app.run(debug=True)