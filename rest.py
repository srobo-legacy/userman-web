
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
