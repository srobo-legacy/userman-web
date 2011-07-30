#!/usr/bin/env python

import json
import cgi
import cgitb
cgitb.enable()

print "Content-Type: text/html"
print

def handleRequest(form):
    if "_uid" not in form:
        return dict(_status = 401, _description = 'No user information provided')

    user = form["_uid"].value
    return dict(user=user)


if __name__ == '__main__':
    data = handleRequest(cgi.FieldStorage())
    print json.dumps(data)

