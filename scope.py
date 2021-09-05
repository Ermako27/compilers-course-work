import uuid

class Scope:
    def __init__(self, name, type) -> None:
        self.name = name
        self.type = type
        self.childScopes = []
        self.variables = []
        self.uid = uuid.uuid4().hex

    def addVariable(self, variable):
        self.variables.append(variable)


    def addScope(self, scope):
        self.childScopes.append(scope)


class ScopeVariable:
    def __init__(self, name = '', type = '', value = '') -> None:
        self.name = name
        self.type = type
        self.value = value