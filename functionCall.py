class FunctionCall:
    def __init__(self, name) -> None:
        self.name = name
        self.children = []

    def addFuncionCall(self, functionCall):
        self.children.append(functionCall)