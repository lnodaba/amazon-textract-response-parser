
r"""
Tokenizers for Amazon Comprehend. 
The default Stemmer used in each function is the popular PorterStemmer from the NLTK library.
"""
import nltk
import inspect
import functools

from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.stem import PorterStemmer 
from types import FunctionType
from typing import List
from statistics import mean, median_grouped


def comprehend_get_text(data):
    """Extracts the text from a comprehend result.
    Args:
        data: the result obtained with ComprehendClient.
    Returns:
        All the text returned.
    """
    return " ".join([item.get_tokens() for item in data])

def comprehend_print_result(data):
    """A friendly print for the data received from ComprehendClient, good for debuging purposes.
    Args:
        data: the result obtained with ComprehendClient.
    """
    for item in data:
        print(item)

def comprehend_word_tokenize(data, stemmed: bool = False):
    """Tokenizes the content of the data received from ComprehendCLient, it is using the NLTK's word_tokenize.
    And it is working with all of the result types unless they are havinh a get_tokens() method.
    Args:
        data: the result obtained with ComprehendClient.
        stemmed: boolean, if true generates a stemmed result with the NLTK's PorterStemmer
    Returns: 
        The list of the tokens.
    """
    text = comprehend_get_text(data)
    if stemmed:
        ps = PorterStemmer() 
        return [ps.stem(word) for word in word_tokenize(text)]
    else:                 
        return word_tokenize(text)


def comprehend_sentence_tokenize(data, stemmed: bool = False):
    """Tokenizes the content of the data received from ComprehendCLient.
    It threats each item in the collection as a sentence. 
    currently it is recommended to be used only with key phrase extraction as for the other comprehend endpoints the result is just a word. 
    
    Args:
        data: the result obtained with ComprehendClient.
        stemmed: boolean, if true generates a stemmed result with the NLTK's PorterStemmer
    Returns: 
        The list of the sentences.
    """
    
    if stemmed:
        ps = PorterStemmer()
        result = []
        for item in data:
            for sentence in item.get_tokens():
                sentence_stemmed = " ".join([ps.stem(word) for word in word_tokenize(sentence)])
                result.append(sentence_stemmed)

        return result
    else:
        return [item.get_tokens() for item in data]



