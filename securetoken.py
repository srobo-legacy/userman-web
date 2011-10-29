
import json
from time import time
from datetime import datetime, timedelta

class Token(object):
    _createdKey = '_created'

    def __init__(self, info):
        info = info.copy()
        if not self._createdKey in info:
            info[self._createdKey] = time()

        self.__dict__['_info'] = info

    def __getattr__(self, name):
        return self._info[name]

    def __setattr__(self, n, v):
        raise Exception('Tokens are read only!')

    def age(self):
        """
        Returns a timedelta object that describes the age of the token
        """
        created = datetime.fromtimestamp(float(self._created))
        now = datetime.now()
        return now - created

    def encrypt(self):
        """
        Returns an encrypted string representing the Token
        """
        return json.dumps(self._info)

def load(string):
    """
    Creates a new Token from an encrypted string representation of one
    """
    data = json.loads(string)
    if data is not None:
        return Token(data)

def encode(data):
    """
    Converts a dictionary into an encoded string.
    @param data (dict): The data to encode.
    @returns: An encoded token string.
    """
    tok = Token(data)
    return tok.encrypt()

def decode(token):
    """
    Converts an encoded string into a dictionary.
    @param token (token): The token to decode.
    @returns: A dictionary of the data that was encoded.
    """
    tok = load(token)
    if tok is not None:
        info = tok._info
        del info[Token._createdKey]
        return info

if __name__ == '__main__':
    orig_data = dict(foo="bar", jam=2)
    print orig_data
    token = encode(orig_data)
    print token
    data = decode(token)
    print data
    assert orig_data == data, "\nExpected: %s\n  Actual: %s" % (orig_data, data)
