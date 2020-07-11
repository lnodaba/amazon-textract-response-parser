
import nltk

from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.stem import PorterStemmer 

def textract_text_from_doc(doc, stemmed = False):
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

def textract_sentence_tokenize(doc,stemmed = False):
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
    


def textract_paragraph_tokenize(doc,stemmed = False):
    print("Paragraph Tokenize")


def textract_word_tokenize(doc,stemmed = False):
    content = textract_text_from_doc(doc)
    if stemmed:
        ps = PorterStemmer() 
        return [ps.stem(word) for word in word_tokenize(content)]
    else:                 
        return word_tokenize(content)
