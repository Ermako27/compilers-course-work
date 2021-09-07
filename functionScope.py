class FunctionScope:
    def __init__(self, name) -> None:
        self.name = name
        self.childrenFunctionScope = dict()
        self.functionCalls = []

    def addFunctionScope(self, scopeName, scope):
        self.childrenFunctionScope[scopeName] = scope
    
    def addFunctionCall(self, functionName):
        self.functionCalls.append(functionName)