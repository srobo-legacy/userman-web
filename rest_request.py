
class restRequestBase:
    def handle(self, command, kwargs):
        return None

    def validate(self, command, user):
        return False

class restRequest(restRequestBase):
    _mapping = {}

    def handle(self, command, kwargs):
        if command not in self._mapping:
            raise Exception("Unknown command. Must be one of %s." %
                    ', '.join(self._mapping.keys())
                )
        return self._mapping[command](**kwargs)
