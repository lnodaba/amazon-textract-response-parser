from textract.textract_response_parser import Document
from textract.textract_tokenizer import *
from comprehend.ComprehendClient import ComprehendClient
from comprehend.comprehend_models import *
import json

def run():
    response = {}
    
    filePath = "./textract/test_data/6-response.json"
    with open(filePath, 'r') as document:
        response = json.loads(document.read())

    doc = Document(response)
    text = textract_text_from_doc(doc)
    client = ComprehendClient()
    
    print("\n\n\n===================== Amazon Comprehend Client Examples and tokenizers ================================\n")    

    print("\n\n\n===================== Text input ================================\n")    
    print(text)

    print("\n\n\n===================== Dominant language result ================================\n")    
    languages = client.dominant_language(text)
    print (languages)

    print("\n\n\n===================== Entities ================================\n")    
    entities = client.detect_entities(text)
    print (entities)

    print("\n\n\n===================== Key Phrases ================================\n")    
    key_phrases = client.detect_key_phrases(text)
    print (key_phrases)


run()