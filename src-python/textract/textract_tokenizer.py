
r"""
Tokenizers for Amazon Textract. 
The default Stemmer used in each function is the popular PorterStemmer from the NLTK library.
"""
import nltk
import inspect
import functools

from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.stem import PorterStemmer 
from textract.textract_response_parser import Document
from types import FunctionType
from typing import List
from statistics import mean, median_grouped

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
            print("Line: [{}] =>  {}--{}".format(line.geometry.boundingBox , line.text, line.confidence))
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

  

@check_types
def textract_paragraph_tokenize(doc: Document, stemmed: bool = False): 
    """
    Tokenizes the content of the document to paragraphs, it is using a customly written paragraph tokenizer.

    @param doc: Document type defined in the trp module
    @param stemmed: boolean, if true generates a stemmed result with the NLTK's PorterStemmer
    """
    content = textract_get_paragraphs(doc)
    if stemmed:
        ps = PorterStemmer()
        result = []
        for paragrapgh in content:
            paragrapgh_stemmed = " ".join([ps.stem(word) for word in word_tokenize(paragrapgh)])
            result.append(paragrapgh_stemmed)
        return result
    else:                 
        return content
    

class TextractLine:
    def __init__(self, line: str, text_indent: float, row_space: float, page_start: bool):
        self.line = line
        self.text_indent = text_indent
        self.row_space = row_space
        self.__row_space_start = False
        self.__text_indent_start = False
        self.__page_start = page_start
    
    @property
    def page_start(self):
        return self.__page_start

    @page_start.setter
    def page_start(self, page_start: bool):
        self.__page_start = page_start

    @property
    def row_space_start(self):
        return self.__row_space_start

    @row_space_start.setter
    def row_space_start(self, row_space_start: bool):
        self.__row_space_start = row_space_start
    
    @property
    def text_indent_start(self):
        return self.__text_indent_start

    @text_indent_start.setter
    def text_indent_start(self, text_indent_start: bool):
        self.__text_indent_start = text_indent_start

    @property
    def paragraph_start(self):
        return self.page_start or self.row_space_start or self.text_indent_start

    def __repr__(self):
        return '[paragraph_start: {self.paragraph_start} page_start: {self.page_start} row_space_start: {self.row_space_start} text_indent_start: {self.text_indent_start} text_indent: {self.text_indent} row_space: {self.row_space}] {self.line}'.format(self = self)

@check_types
def textract_get_paragraphs(doc: Document, debug: bool = False):
    """
    A self written paragraph tokenizer based on the bounding boxes. It is taking into the consideration the row spacing and the text indention.

    @param doc: Document type defined in the trp module
    @param debug: prints the whole result. 
    """
    
    # calculate row space and text_indention differences between lines
    last_line = None
    lines = []
    for page in doc.pages:
        page_start = True
        for line in page.lines:
            row_space = line.geometry.boundingBox.top - (last_line.geometry.boundingBox.top if last_line else 0)
            text_indent = line.geometry.boundingBox.left - (last_line.geometry.boundingBox.left if last_line else 0)
            lines.append(TextractLine(line.text, text_indent, row_space, page_start))
            page_start = False
            last_line = line

    # set up hyper parameters parameters    
    average_row_space = mean([line.row_space for line in lines])
    text_indents = [line.text_indent for line in lines]
    median_text_indent = mean(text_indents)
    
    hyperparameter = 0.01
    average_row_hyperparameter = abs(average_row_space) + hyperparameter
    text_indent_hyperparameter = abs(median_text_indent) + hyperparameter

    # based on the hyperparameters mark the start lines 
    for line in lines:
        if line.row_space > average_row_hyperparameter:
            line.row_space_start = True
        if line.text_indent > text_indent_hyperparameter:
            line.text_indent_start = True
    
    # create the result list
    result = []
    paragraph = ""
    for line in lines:
        if line.paragraph_start:
            if len(paragraph) > 0:
                result.append(paragraph)
            paragraph = line.line
        else:
            paragraph += " " + line.line
            
    if len(paragraph) > 0:
        result.append(paragraph)

    # print in case of debug
    if debug:
        print("average_row_hyperparameter : {}".format(average_row_hyperparameter))
        print("text_indent_hyperparameter : {}".format(text_indent_hyperparameter))
        for line in lines:
            print(line)
        for text in result:
            print("\n")
            print(text)
    
    return result



    
