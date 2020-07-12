import unittest
import json
from textract_response_parser import Document
from textract_tokenizer import *

class TextractTokenizerTests(unittest.TestCase):
    def setUp(self):
        # arrange
        response = {}
        filePath = "3-response.json"
        with open(filePath, 'r') as document:
            response = json.loads(document.read())
        self.doc = Document(response)


    def test_textract_text_from_doc(self):
       # act
       result = textract_text_from_doc(self.doc)

       # assert
       self.assertTrue(len(result) > 0)
    
    def test_textract_text_from_doc_stemmed(self):
        # act
        result = textract_text_from_doc(self.doc, True)

        # assert
        self.assertFalse("Assessment" in result)
        self.assertTrue("assess" in result)

    def test_textract_sentence_tokenize(self):
          # act
        result = textract_sentence_tokenize(self.doc)

        # assert
        self.assertTrue(len(result) > 0)

    def test_textract_sentence_tokenize_stemmed(self):
          # act
        result = textract_sentence_tokenize(self.doc, True)

        # assert
        self.assertTrue(len(result) > 0)
        self.assertFalse("Assessment" in result[0])
        self.assertTrue("assess" in result[0])

  
    def test_textract_word_tokenize(self):
         # act
        result = textract_word_tokenize(self.doc)

        # assert
        self.assertTrue(len(result) > 0)


    def test_textract_word_tokenize_stemmed(self):
        # act
        result = textract_word_tokenize(self.doc, True)

        # assert
        self.assertTrue(len(result) > 0)
        self.assertFalse("Assessment" in result)
        self.assertTrue("assess" in result)
    
    def test_textract_paragraph_tokenize(self):
        self.assertTrue(False)

    def test_textract_paragraph_tokenize_stemmed(self):
        self.assertTrue(False)

if __name__ == '__main__':
    unittest.main()