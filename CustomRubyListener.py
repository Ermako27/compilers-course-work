from RubyListener import RubyListener
from RubyParser import RubyParser
from parseTreeProperty import ParseTreeProperty;
from hashtable import HashTable
from io import BytesIO
from llist import sllist, sllistnode

class CustomRubyListener(RubyListener):     
    def __init__(self) -> None:
        super().__init__()
        self.intValues = ParseTreeProperty()
        self.floatValues = ParseTreeProperty()
        self.stringValues = ParseTreeProperty()
        self.whichValues = ParseTreeProperty()

        self.stackOutputStreams = []
        self.functionDefinitionStreams = HashTable(5000)
        self.mainStream = BytesIO()
        self.funcStream = BytesIO()
        self.errorStream = BytesIO()

        self.semanticErrorNum = 0
        self.numStr = 1
        self.numReg = 0
        self.numRegInt = 0
        self.numLabel = 0
        self.stackLoopLabels = []
        self.mainDefinitions = sllist()
        self.functionCalls = []
        self.stackDefinitions = []

    

    def isDefined(self, defenitions, variable):
        for value in defenitions.itervalues():
            if value == variable:
                return True
        return False

    def repeat(self, string, times):
        if times <= 1:
            return ""
        else:
            return string + self.repeat(string, times - 1)

    # --------------------------- PROG ---------------------------

    # Enter a parse tree produced by RubyParser#prog.
    def enterProg(self, ctx:RubyParser.ProgContext):
        print("enterProg!")

        out = self.mainStream
        out.write(b".sub main")

        self.stackDefinitions.append(self.mainDefinitions)
        self.stackOutputStreams.append(out)

    # Exit a parse tree produced by RubyParser#prog.
    def exitProg(self, ctx:RubyParser.ProgContext):
        print("exitProg!")

        out = self.mainStream
        out.write(b".include \"stdlib/stdlib.pir\"")

        print(out.getvalue())
        for funCallName in self.functionCalls:
            fstream = self.functionDefinitionStreams[funCallName]
            if fstream != False: # getvalue
                out.write(fstream.getvalue())

        self.stackDefinitions.pop()
        self.stackOutputStreams.append(out)