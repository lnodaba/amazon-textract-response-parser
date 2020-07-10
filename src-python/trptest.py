import json
from trp import Document

# import nltk
# nltk.download()

from nltk.tokenize import word_tokenize

def getTextFromDoc(doc):
    result = ''
    for page in doc.pages:
        for line in page.lines:
            result += " " + line.text
            # for word in line.words:
            #     word.text      

        for table in page.tables:
            for row in table.rows:
                for cell in row.cells:
                    result += " " + cell.text

    return result

def run():
    response = {}
    
    filePath = "test-response.json"
    with open(filePath, 'r') as document:
        response = json.loads(document.read())

    doc = Document(response)
    result = getTextFromDoc(doc)
    
    print(word_tokenize(result))

run()