import unittest
import json
from textract.textract_response_parser import Document
from textract.textract_tokenizer import *
from comprehend.comprehend_tokenizer import comprehend_word_tokenize
from comprehend.ComprehendClient import ComprehendClient

class ComprehendTokenizerTests(unittest.TestCase):
    def setUp(self):
        # arrange
        response = {}
        filePath = "./textract/test_data/6-response.json"
        with open(filePath, 'r') as document:
            response = json.loads(document.read())
        self.text = textract_text_from_doc(Document(response))
        self.client = ComprehendClient()

    def test_comprehend_dominant_language(self):
        # arrange
        comprehend_result = self.client.dominant_language(self.text)

        # act
        tokenize_result = comprehend_word_tokenize(comprehend_result)

        # assert
        self.assertTrue("en" in tokenize_result)


    def test_comprehend_dominant_language_tokenize_stemmed(self):
       # arrange
       comprehend_result = self.client.dominant_language(self.text)

       # act
       tokenize_result = comprehend_word_tokenize(comprehend_result, True)

       # assert
       self.assertTrue("en" in tokenize_result)

    def test_comprehend_detect_entities_tokenize(self):
        # arrange
        comprehend_result = self.client.detect_entities(self.text)

        # act
        tokenize_result = comprehend_word_tokenize(comprehend_result)

        # assert
        self.assertTrue("thirties" in tokenize_result)
        self.assertTrue("Depression" in tokenize_result)

    def test_comprehend_detect_entities_tokenize_stemmed(self):
        # arrange
        comprehend_result = self.client.detect_entities(self.text)

        # act
        tokenize_result = comprehend_word_tokenize(comprehend_result, True)

        # assert
        self.assertTrue("world" in tokenize_result)
        self.assertTrue("war" in tokenize_result)
        self.assertFalse("thirties" in tokenize_result)
        self.assertFalse("Depression" in tokenize_result)
    
    def test_comprehend_detect_key_phrases_tokenize(self):
        # arrange
        comprehend_result = self.client.detect_key_phrases(self.text)

        # act
        tokenize_result = comprehend_word_tokenize(comprehend_result)

        # assert
        self.assertTrue("thirties" in tokenize_result)
        self.assertTrue("Depression" in tokenize_result)

    def test_comprehend_detect_key_phrases_tokenize_stemmed(self):
        # arrange
        comprehend_result = self.client.detect_key_phrases(self.text)

        # act
        tokenize_result = comprehend_word_tokenize(comprehend_result, True)

        # assert
        self.assertTrue("world" in tokenize_result)
        self.assertTrue("war" in tokenize_result)
        self.assertFalse("thirties" in tokenize_result)
        self.assertFalse("Depression" in tokenize_result)

if __name__ == '__main__':
    unittest.main()

# python .\textract\textract_tokenizer_tests.py