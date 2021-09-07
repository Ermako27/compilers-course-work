class FunctionScope:
    def __init__(self, name) -> None:
        self.name = name
        self.childrenFunctionScope = dict()
        self.functionCalls = []
        self.parentScope = None

    def addFunctionScope(self, scopeName, scope):
        # for key, value in self.childrenFunctionScope.items():
        #     scope.childrenFunctionScope[key] = value
        # scope.childrenFunctionScope[scopeName] = scope

        scope.parentScope = self
        self.childrenFunctionScope[scopeName] = scope
    
    def addFunctionCall(self, functionName):
        self.functionCalls.append(functionName)