#utils for cleint and server
import json

class Formatter:
    

    @staticmethod    
    def EncodeJson(data):
        #returns a string json format
        return json.dumps(data)

    @staticmethod
    def DecodeJson(data):
        #returns the object according to the json format
        return json.loads(data)        


    '''
    JSON	Python
    object	dict
    array	list
    string	unicode
    number (int)	int, long
    number (real)	float
    true	True
    false	False
    null	None
    '''