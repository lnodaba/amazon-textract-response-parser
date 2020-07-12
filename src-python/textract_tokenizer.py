
r"""
Tokenizers for Amazon Textract. 
The default Stemmer used in each function is the popular PorterStemmer from the NLTK library.
"""
import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.stem import PorterStemmer 
from textract_response_parser import Document
from types import FunctionType
import inspect
import functools
from typing import List


def check_types(func):
    msg = "Expected type {etype} for {para} got {got}"
    para = inspect.signature(func).parameters
    keys = tuple(para.keys())

    @functools.wraps(func)
    def wrapper(*args,**kwargs):
        def do_check(anno,value,para):
            if not isinstance(value, anno):
                raise TypeError(msg.format(etype=anno,
                    para=para,
                    got=type(value)))

        for i,value in  enumerate(args):
            anno = para[keys[i]].annotation
            do_check(anno, value, keys[i])

        for arg_name,value in  kwargs.items():
            anno = para[arg_name].annotation
            do_check(anno, value, arg_name)

        ret = func(*args,**kwargs)
        if "return" in func.__annotations__:
            anno = func.__annotations__["return"]
            do_check(anno, ret, "return")
        return ret
    return wrapper

@check_types
def textract_text_from_doc(doc: Document, stemmed: bool = False)-> str: 
    """
    Gathers all the text from the given Textract result. 

    @param doc: Document type defined in the trp module
    @param stemmed: boolean, if true generates a stemmed result with the NLTK's PorterStemmer
    @return: text result
    """

    result = ''
    for page in doc.pages:
        for line in page.lines:
            result += " " + line.text

        for table in page.tables:
            for row in table.rows:
                for cell in row.cells:
                    result += " " + cell.text
    if stemmed:
        ps = PorterStemmer() 
        return " ".join([ps.stem(word) for word in word_tokenize(result)])
    else:                 
        return result

@check_types
def textract_print_document(doc: Document):
    """
    Prints the content of the document:
    Per page it prints the lines, words, tables and the key value pairs of the form. 

    @param doc: Document type defined in the trp module
    """

    for page in doc.pages:
        print("\n\n\n\n\n\n\n\nPAGE\n====================")
        for line in page.lines:
            print("Line: {}--{}".format(line.text, line.confidence))
            for word in line.words:
                print("Word: {}--{}".format(word.text, word.confidence))
        for table in page.tables:
            print("\n\n\n\n\n\n\nTABLE\n====================")
            for r, row in enumerate(table.rows):
                for c, cell in enumerate(row.cells):
                    print("Table[{}][{}] = {}-{}".format(r, c, cell.text, cell.confidence))
        print("\n\n\n\n\n\nForm (key/values)\n====================")
        for field in page.form.fields:
            k = ""
            v = ""
            if(field.key):
                k = field.key.text
            if(field.value):
                v = field.value.text
            print("Field: Key: {}, Value: {}".format(k,v))

@check_types
def textract_sentence_tokenize(doc: Document, stemmed: bool = False)-> List: 
    """
    Tokenizes the content of the document to sentences, it is using the NLTK's sent_tokenizer.

    @param doc: Document type defined in the trp module
    @param stemmed: boolean, if true generates a stemmed result with the NLTK's PorterStemmer
    """
    content = textract_text_from_doc(doc)
    if stemmed:
        ps = PorterStemmer()
        result = []
        for sentence in sent_tokenize(content):
            sentence_stemmed = " ".join([ps.stem(word) for word in word_tokenize(sentence)])
            result.append(sentence_stemmed)
        return result
    else:                 
        return sent_tokenize(content)
    

@check_types
def textract_paragraph_tokenize(doc: Document, stemmed: bool = False): 
    print("Paragraph not supported!")
    print("https://github.com/aws-samples/amazon-textract-response-parser/issues/2")


@check_types
def textract_word_tokenize(doc: Document, stemmed: bool = False)-> List: 
    """
    Tokenizes the content of the document to words, it is using the NLTK's word_tokenize.

    @param doc: Document type defined in the trp module
    @param stemmed: boolean, if true generates a stemmed result with the NLTK's PorterStemmer
    """
    content = textract_text_from_doc(doc)
    if stemmed:
        ps = PorterStemmer() 
        return [ps.stem(word) for word in word_tokenize(content)]
    else:                 
        return word_tokenize(content)

