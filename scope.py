import uuid

class Scope:
    def __init__(self, name, type) -> None:
        self.name = name
        self.type = type
        self.parentScope = None
        self.childScopes = []
        self.variables = []
        self.uid = uuid.uuid4().int

    def isVariableAlreadyExists(self, variable):
        for varInScope in self.variables:
            if varInScope.name == variable.name:
                return True
        return False

    def addVariable(self, variable):
        if not self.isVariableAlreadyExists(variable):
            self.variables.append(variable)


    def addScope(self, scope):
        scope.parentScope = self
        self.childScopes.append(scope)
        
        


class ScopeVariable:
    def __init__(self, name = '', type = '', value = '') -> None:
        self.name = name
        self.type = type
        self.value = value