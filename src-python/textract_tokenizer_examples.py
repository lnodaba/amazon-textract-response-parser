import json
from textract.textract_response_parser import Document
from textract.textract_tokenizer import *

def run():
    

    response = {}
    
    filePath = "./textract/test_data/6-response.json"
    with open(filePath, 'r') as document:
        response = json.loads(document.read())

    doc = Document(response)

    
    print("\n\n\n===================== Text ================================\n\n\n")    
    print(textract_text_from_doc(doc))

    print("\n\n\n===================== Text Stemmed ================================\n\n\n")    
    print(textract_text_from_doc(doc, True))

    print("\n\n\n===================== Sentences ================================\n\n\n")    
    sentences = textract_sentence_tokenize(doc)
    for index, sentence in enumerate(sentences):
        print("[{}] [{}]".format(index, sentence))
        
    print("\n\n\n===================== Sentences Stemmed ================================\n\n\n")    
    sentences = textract_sentence_tokenize(doc, True)
    for index, sentence in enumerate(sentences):
        print("[{}] [{}]".format(index, sentence))


    print("\n\n\n===================== Words ================================\n\n\n")
    print(textract_word_tokenize(doc))

    print("\n\n\n===================== Words Stemmed ================================\n\n\n")
    print(textract_word_tokenize(doc, True))
    
    print("\n\n\n===================== Get Paragraphs ================================\n\n\n")   
    textract_get_paragraphs(doc, True)

    print("\n\n\n===================== Paragraphs ================================\n\n\n")    
    print(textract_paragraph_tokenize(doc, True))

run()