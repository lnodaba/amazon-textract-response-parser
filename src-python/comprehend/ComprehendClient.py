import boto3
import json
from comprehend.comprehend_models import *

class ComprehendClient:
  def __init__(self):
    self.__comprehend = boto3.client(service_name='comprehend', region_name='us-west-2')



  def dominant_language(self, text: str):
    response = self.__comprehend.detect_dominant_language(Text = text)

    result = []
    for item in response["Languages"]:
      result.append(Language(item))

    return result

  def detect_entities(self, text: str, language_code: str = "en"):
    response = self.__comprehend.detect_entities(Text=text, LanguageCode=language_code)
    
    result = []
    for item in response["Entities"]:
      result.append(Entity(item))

    return result
  
  def detect_key_phrases(self, text: str, language_code: str = "en"):
    response = self.__comprehend.detect_key_phrases(Text=text, LanguageCode=language_code)
    
    result = []
    for item in response["KeyPhrases"]:
      result.append(KeyPhrase(item))

    return result

