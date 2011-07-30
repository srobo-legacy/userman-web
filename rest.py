
from rest_request import restRequest
import rest_user, rest_group

class rest(restRequest):
    _mapping = { 'group' : rest_group.group
                ,'user' : rest_user.user
               }

    _handler = None
    def __init__(self, cmdType):
        if cmdType in self._mapping:
            self._handler = self._mapping[cmdType]()
        else:
            raise Exception("Unknown command type. Must be one of %s." %
                    ', '.join(self._mapping.keys())
                )

    def handle(self, command, kwargs):
        return self._handler.handle(command, kwargs)

    def validate(self, command, user):
        return self._handler.validate(command, user)

if __name__ == '__main__':
    # self test
    from types import ListType

    print 'User Search:'
    r = rest('user')
    users = r.handle('search', {'search': ''})
    assert type(users) is ListType, "Got wrong type back from search: '%s'" % users
    print users

    print 'Group Search:'
    r = rest('group')
    groups = r.handle('search', {'regexp': ''})
    assert type(groups) is ListType, "Got wrong type back from search: '%s'" % groups
    print groups
