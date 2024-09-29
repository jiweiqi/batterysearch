import nltk
import contractions
import string
from nltk.tokenize import word_tokenize

nltk.download("punkt", quiet=True)


def expand_contractions(text):
    """
    Expands contractions in the given text.
    """
    return contractions.fix(text)


def remove_punctuation(text):
    """
    Removes punctuation from the given text.
    """
    translator = str.maketrans("", "", string.punctuation)
    return text.translate(translator)


def to_lowercase(text):
    """
    Converts text to lowercase.
    """
    return text.lower()


def tokenize(text):
    """
    Tokenizes the text into individual words.
    """
    return word_tokenize(text)


def preprocess_text(text):
    """
    Applies all preprocessing steps to the text.
    """
    text = expand_contractions(text)
    text = remove_punctuation(text)
    text = to_lowercase(text)
    tokens = tokenize(text)
    return tokens
