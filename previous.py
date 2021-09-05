    # Enter a parse tree produced by RubyParser#prog.
    # def enterProg(self, ctx:RubyParser.ProgContext):
    #     print("enterProg")

    #     self.graph.addRuleNode(ctx)

    #     method_list = [method for method in dir(ctx) if method.startswith('__') is False]
    #     # print('ctx methods', method_list)
    #     # print(ctx.getRuleIndex());
    #     out = self.mainStream
    #     out.write(b".sub main")

    #     self.mainDefinitions
    #     self.stackDefinitions.append(self.mainDefinitions)
    #     self.stackOutputStreams.append(out)

    # # Exit a parse tree produced by RubyParser#prog.
    # def exitProg(self, ctx:RubyParser.ProgContext):
    #     print("exitProg")

    #     out = self.mainStream
    #     out.write(b".include \"stdlib/stdlib.pir\"")

    #     # print(out.getvalue())
    #     for funCallName in self.functionCalls:
    #         fstream = self.functionDefinitionStreams[funCallName]
    #         if fstream != False:
    #             out.write(fstream.getvalue())

    #     self.stackDefinitions.pop()
    #     self.stackOutputStreams.append(out)

    # # --------------------------- Global ---------------------------

    # def exitGlobal_get(self, ctx:RubyParser.Global_getContext):
    #     print("exitGlobal_set")
    #     out = self.stackOutputStreams.pop()
    #     definitions = self.stackDefinitions.pop()
        
    #     var = ctx.var_name.getText()
    #     globalName = ctx.global_name.getText()

    #     if not self.isDefined(definitions, var):
    #         pass
    #         # out.write("")
    #         # out.write(".local pmc " + var)
    #         # out.write(var + " = new \"Integer\"")

    #     # out.write("get_global " + var + ", \"" + globalName + "\"")

    #     self.stackOutputStreams.append(out)
    #     self.stackDefinitions.append(definitions)
    
    # def exitGlobal_set(self, ctx:RubyParser.Global_setContext):
    #     print("exitGlobal_set")
    #     out = self.stackOutputStreams.pop()
    #     definitions = self.stackDefinitions.pop()

    #     globalName = ctx.global_name.getText()

    #     typeArg = self.whichValues.get(ctx.getChild(2))

    #     if typeArg == "Integer":
    #         resultInt = self.intValues.get(ctx.getChild(2))
    #         # out.write("set_global \"" + globalName + "\", " + resultInt);
    #     elif typeArg == "Float":
    #         resultFloat = self.intValues.get(ctx.getChild(2))
    #         # out.write("set_global \"" + globalName + "\", " + resultFloat);
    #     elif typeArg == "String":
    #         resultString = self.intValues.get(ctx.getChild(2))
    #         # out.write("set_global \"" + globalName + "\", " + resultString);
    #     elif typeArg == "Dynamic":
    #         resultDynamic = self.intValues.get(ctx.getChild(2))
    #         # out.write("set_global \"" + globalName + "\", " + resultDynamic);

    #     self.stackOutputStreams.append(out)
    #     self.stackDefinitions.append(definitions)
    
    # # --------------------------- Integer ---------------------------

    # # Enter a parse tree produced by RubyParser#int_assignment.
    # def enterInt_assignment(self, ctx:RubyParser.Int_assignmentContext):
    #     print(ctx.getRuleIndex());
    #     print("enterInt_assignment")
    #     out = self.stackOutputStreams.pop()
    #     definitions = self.stackDefinitions.pop()

    #     # operationType = ctx.op.type()

    #     if ctx.op.type == RubyParser.ASSIGN:
    #         var = ctx.var_id.getText()
    #         if not self.isDefined(definitions, var):
    #             # out.write(b"")
    #             # out.write(b".local pmc " + ctx.var_id.getText())
    #             # out.write(ctx.var_id.getText() + "= new \"Integer\"")
    #             definitions.append(ctx.var_id.getText())
    #     else:
    #         var = ctx.var_id.getText()
    #         if not self.isDefined(definitions, var):
    #             print("line " + self.numStr + " Error! Undefined variable " + var + "!");
    #             self.semanticErrorNum += 1

    #     self.stackOutputStreams.append(out)
    #     self.stackDefinitions.append(definitions)

    # def exitInt_assignment(self, ctx:RubyParser.Int_assignmentContext):
    #     print('exitInt_assignment')
    #     out = self.stackOutputStreams.pop()
    #     varName = ctx.var_id.getText()
    #     operation = ctx.op.text
    #     child = ctx.getChild(2).getText()

    #     self.stackOutputStreams.append(out)



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