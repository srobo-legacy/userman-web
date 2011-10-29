
import json

def token_encode(data):
    """
    Converts a dictionary into an encoded string.
    @param data (dict): The data to encode.
    @returns: An encoded token string.
    """
    return json.dumps(data)

def token_decode(token):
    """
    Converts an encoded string into a dictionary.
    @param token (token): The token to decode.
    @returns: A dictionary of the data that was encoded.
    """
    return json.loads(token)

if __name__ == '__main__':
    orig_data = dict(foo="bar", jam=2)
    print orig_data
    token = token_encode(orig_data)
    print token
    data = token_decode(token)
    print data
    assert orig_data == data
