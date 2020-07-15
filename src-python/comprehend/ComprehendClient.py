import boto3
import json
from comprehend.comprehend_models import *


class ComprehendClient:
  """
  A wrapper around boto3. All of the functions are parsing the result to an Object located inthe comprehend_models module.
  """
  def __init__(self):
    self.__comprehend = boto3.client(service_name='comprehend', region_name='us-west-2')


  def dominant_language(self, text: str): 
    """Get's the dominant languages for the given text.
    Args:
        text: the text to analyze.
    Returns:
        The list of the languages found as Language objects.
    """
    response = self.__comprehend.detect_dominant_language(Text = text)
    return [Language(item) for item in response["Languages"]]


  def detect_entities(self, text: str, language_code: str = "en"):
    """Detects the entities from the given text.
    Args:
        text: the text to analyze.
    Returns:
        The list entities found as Entity objects.
    """
    response = self.__comprehend.detect_entities(Text=text, LanguageCode=language_code)
    return [Entity(item) for item in response["Entities"]]
  

  def detect_key_phrases(self, text: str, language_code: str = "en"):
    """Detects the key phrases from the given text.
    Args:
        text: the text to analyze.
    Returns:
        The listof the key phrases found as KeyPhrase objects.
    """
    response = self.__comprehend.detect_key_phrases(Text=text, LanguageCode=language_code)
    return [KeyPhrase(item) for item in response["KeyPhrases"]]

  