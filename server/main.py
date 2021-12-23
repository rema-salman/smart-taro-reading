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

    # cards['number'] = cards['number'].astype('int')
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
        a) Stemming
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

    feature_names = vectorizer.get_feature_names_out()

    # print(feature_names)

    # cosine similarity between the matrices (vectors)
    cosine_sim = cosine_similarity(cards_matrix, query_matrix)
    # print(cosine_sim)
    return cosine_sim


def get_random_words(text):
    tokens = text.split()

    # print random string
    randomWords = random.choice(tokens)


if __name__ == "__main__":

    cards = load_data('../data/tarot-images.json')
    print(cards.info())
    cards['soup'] = cards.apply(create_soup, axis=1)

    print("-------soup--------------")
    print(cards['soup'][8])

    cards['soup'] = cards['soup'].apply(lambda x: clean_data(x))
    print("-------cleaned_soup--------------")
    print(cards['soup'][8])

    # Apply text processing on the query
    query = "mysterious woman secrets 32 necessary tomorrow"
    cleaned_query = clean_data(query)
    print("-------cleaned_query--------------")
    print(cleaned_query)

    # create column with the similarity scores
    cards['similarity_scores'] = getSimilarity(cards['soup'], cleaned_query)
    print(cards['similarity_scores'])

    # Sort the cards in desnding order
    cards = cards.sort_values(["similarity_scores"], ascending=False)
    print(cards.head(10))

    # check if there are scors
    for score in cards["similarity_scores"].head(3):
        # Retun the top 3 matching cards for the user
        if score != 0.000000:
            response = cards.head(3).to_json(orient="records", indent=4)
            print(response)
        else:
            # Retun a random list of words for the user
            response = get_random_words()
