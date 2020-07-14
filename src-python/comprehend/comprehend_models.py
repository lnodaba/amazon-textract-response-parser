
class Language:
    def __init__(self, block):
        self._language = block["LanguageCode"] if block["LanguageCode"] else ""
        self._score = block["Score"] if block["Score"] else "" 

    @property
    def language(self):
        return self._language
    
    @property
    def score(self):
        return self._score

    def get_tokens(self): 
        return self._language

    def __repr__(self):
        return f"[LanguageCode: '{self._language}' Score: {self._score}]"

class Entity:
    def __init__(self, block):
        self._begin_offset = block["BeginOffset"] if block["BeginOffset"] else ""
        self._end_offset = block["EndOffset"] if block["EndOffset"] else "" 
        self._score = block["Score"] if block["Score"] else "" 
        self._text = block["Text"] if block["Text"] else "" 
        self._entity_type = block["Type"] if block["Type"] else "" 

    @property
    def begin_offset(self):
        return self._begin_offset
    
    @property
    def end_offset(self):
        return self._end_offset
    
    @property
    def score(self):
        return self._score

    @property
    def text(self):
        return self._text

    @property
    def entity_type(self):
        return self._entity_type

    def get_tokens(self): 
        return self._text 

    def __repr__(self):
        return f"[ text: '{self._text}' type: '{self._entity_type}' score: {self._score} begin_offset: '{self._begin_offset}' end_offset: {self._end_offset}]"


class KeyPhrase:
    def __init__(self, block):
        self._begin_offset = block["BeginOffset"] if block["BeginOffset"] else ""
        self._end_offset = block["EndOffset"] if block["EndOffset"] else "" 
        self._score = block["Score"] if block["Score"] else "" 
        self._text = block["Text"] if block["Text"] else "" 

    @property
    def begin_offset(self):
        return self._begin_offset
    
    @property
    def end_offset(self):
        return self._end_offset
    
    @property
    def score(self):
        return self._score

    @property
    def text(self):
        return self._text

    def get_tokens(self): 
        return self._text 

    def __repr__(self):
        return f"[ text: '{self._text}' score: {self._score} begin_offset: '{self._begin_offset}' end_offset: {self._end_offset}]"
