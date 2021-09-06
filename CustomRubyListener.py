from RubyListener import RubyListener
from RubyParser import RubyParser
from parseTreeProperty import ParseTreeProperty;
from hashtable import HashTable
from io import BytesIO
from llist import sllist, sllistnode

from scope import Scope, ScopeVariable

from graph import Graph

class CustomRubyListener(RubyListener):     
    def __init__(self, codeFileName) -> None:
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
        # ========================================

        self.scopeStack = []
        self.graph = Graph(codeFileName)

    def getFunctionName(self, ctx:RubyParser.Function_definitionContext):
        functionHeaderNode = ctx.getChild(0)
        functionNameNode = functionHeaderNode.getChild(1)
        id = functionNameNode.getChild(0);
        functionName = id.getText()
        return functionName

    def getInitialArrayAssignmentValue(self, ctx:RubyParser.Initial_array_assignmentContext):
        value = ''
        for i in range(2, len(ctx.children)):
            char = ctx.children[i].getText();
            value += char;
        return value
        


    # Enter a parse tree produced by RubyParser#prog.
    def enterProg(self, ctx:RubyParser.ProgContext):
        # создаем глобальный scope
        ruleId = ctx.getRuleIndex()
        ruleName = RubyParser.ruleNames[ruleId]
        newScope = Scope(ruleName, "global")

        self.scopeStack.append(newScope)

        self.graph.addRuleNode(ctx)
        

    # Exit a parse tree produced by RubyParser#prog.
    def exitProg(self, ctx:RubyParser.ProgContext):
        rootScope = self.scopeStack.pop()
        self.graph.renderRuleTree()
        pass


    # Enter a parse tree produced by RubyParser#expression_list.
    def enterExpression_list(self, ctx:RubyParser.Expression_listContext):
        self.graph.addRuleNode(ctx)
        

    # Exit a parse tree produced by RubyParser#expression_list.
    def exitExpression_list(self, ctx:RubyParser.Expression_listContext):
        pass


    # Enter a parse tree produced by RubyParser#expression.
    def enterExpression(self, ctx:RubyParser.ExpressionContext):
        self.graph.addRuleNode(ctx)
        

    # Exit a parse tree produced by RubyParser#expression.
    def exitExpression(self, ctx:RubyParser.ExpressionContext):
        pass


    # Enter a parse tree produced by RubyParser#global_get.
    def enterGlobal_get(self, ctx:RubyParser.Global_getContext):
        self.graph.addRuleNode(ctx)
        

    # Exit a parse tree produced by RubyParser#global_get.
    def exitGlobal_get(self, ctx:RubyParser.Global_getContext):
        pass


    # Enter a parse tree produced by RubyParser#global_set.
    def enterGlobal_set(self, ctx:RubyParser.Global_setContext):
        self.graph.addRuleNode(ctx)
        

    # Exit a parse tree produced by RubyParser#global_set.
    def exitGlobal_set(self, ctx:RubyParser.Global_setContext):
        pass


    # Enter a parse tree produced by RubyParser#global_result.
    def enterGlobal_result(self, ctx:RubyParser.Global_resultContext):
        self.graph.addRuleNode(ctx)
        

    # Exit a parse tree produced by RubyParser#global_result.
    def exitGlobal_result(self, ctx:RubyParser.Global_resultContext):
        pass


    # Enter a parse tree produced by RubyParser#function_inline_call.
    def enterFunction_inline_call(self, ctx:RubyParser.Function_inline_callContext):
        self.graph.addRuleNode(ctx)
        

    # Exit a parse tree produced by RubyParser#function_inline_call.
    def exitFunction_inline_call(self, ctx:RubyParser.Function_inline_callContext):
        pass


    # Enter a parse tree produced by RubyParser#require_block.
    def enterRequire_block(self, ctx:RubyParser.Require_blockContext):
        self.graph.addRuleNode(ctx)
        

    # Exit a parse tree produced by RubyParser#require_block.
    def exitRequire_block(self, ctx:RubyParser.Require_blockContext):
        pass


    # Enter a parse tree produced by RubyParser#pir_inline.
    def enterPir_inline(self, ctx:RubyParser.Pir_inlineContext):
        self.graph.addRuleNode(ctx)
        

    # Exit a parse tree produced by RubyParser#pir_inline.
    def exitPir_inline(self, ctx:RubyParser.Pir_inlineContext):
        pass


    # Enter a parse tree produced by RubyParser#pir_expression_list.
    def enterPir_expression_list(self, ctx:RubyParser.Pir_expression_listContext):
        self.graph.addRuleNode(ctx)
        

    # Exit a parse tree produced by RubyParser#pir_expression_list.
    def exitPir_expression_list(self, ctx:RubyParser.Pir_expression_listContext):
        pass


    # Enter a parse tree produced by RubyParser#function_definition.
    def enterFunction_definition(self, ctx:RubyParser.Function_definitionContext):
        scope = self.scopeStack.pop()

        functionName = self.getFunctionName(ctx)
        ruleId = ctx.getRuleIndex()
        ruleName = RubyParser.ruleNames[ruleId]

        # создаем переменную - функцию
        variable = ScopeVariable(functionName, ruleName)
        # кладем переменную-функцию в текущий scope
        scope.addVariable(variable)

        # создаем новый scope - для новой функции, которая сейчас объявляется
        newScope = Scope(functionName, 'function')
        # добавляем в текущий scope с вершины стека только что созданный новый scope функции
        scope.addScope(newScope)

        # возвращаем в стек текущий scope и кладем на вершину newScope для только что созданной функции
        self.scopeStack.append(scope)
        self.scopeStack.append(newScope)

        self.graph.addRuleNode(ctx)

    # Exit a parse tree produced by RubyParser#function_definition.
    def exitFunction_definition(self, ctx:RubyParser.Function_definitionContext):
        print('[ exit ] uid: {0} | rule: function_definition \n'.format(ctx.uid))

        # как только закончили обходить поддерево функции выкидываем ее scope из стека
        self.scopeStack.pop()
        pass


    # Enter a parse tree produced by RubyParser#function_definition_body.
    def enterFunction_definition_body(self, ctx:RubyParser.Function_definition_bodyContext):
        self.graph.addRuleNode(ctx)
        

    # Exit a parse tree produced by RubyParser#function_definition_body.
    def exitFunction_definition_body(self, ctx:RubyParser.Function_definition_bodyContext):
        pass


    # Enter a parse tree produced by RubyParser#function_definition_header.
    def enterFunction_definition_header(self, ctx:RubyParser.Function_definition_headerContext):
        self.graph.addRuleNode(ctx)
        

    # Exit a parse tree produced by RubyParser#function_definition_header.
    def exitFunction_definition_header(self, ctx:RubyParser.Function_definition_headerContext):
        pass


    # Enter a parse tree produced by RubyParser#function_name.
    def enterFunction_name(self, ctx:RubyParser.Function_nameContext):
        self.graph.addRuleNode(ctx)
        

    # Exit a parse tree produced by RubyParser#function_name.
    def exitFunction_name(self, ctx:RubyParser.Function_nameContext):
        pass


    # Enter a parse tree produced by RubyParser#function_definition_params.
    def enterFunction_definition_params(self, ctx:RubyParser.Function_definition_paramsContext):
        self.graph.addRuleNode(ctx)
        

    # Exit a parse tree produced by RubyParser#function_definition_params.
    def exitFunction_definition_params(self, ctx:RubyParser.Function_definition_paramsContext):
        pass


    # Enter a parse tree produced by RubyParser#function_definition_params_list.
    def enterFunction_definition_params_list(self, ctx:RubyParser.Function_definition_params_listContext):
        self.graph.addRuleNode(ctx)
        

    # Exit a parse tree produced by RubyParser#function_definition_params_list.
    def exitFunction_definition_params_list(self, ctx:RubyParser.Function_definition_params_listContext):
        pass


    # Enter a parse tree produced by RubyParser#function_definition_param_id.
    def enterFunction_definition_param_id(self, ctx:RubyParser.Function_definition_param_idContext):
        # достаем текущий scope
        scope = self.scopeStack.pop()

        # создаем переменную-аргумент
        argName = ctx.getText();
        variable = ScopeVariable(argName, 'argument')
        # кладем эту переменную в scope
        scope.addVariable(variable)

        # возвращаем scope обратно в стек
        self.scopeStack.append(scope)
        self.graph.addRuleNode(ctx)
        

    # Exit a parse tree produced by RubyParser#function_definition_param_id.
    def exitFunction_definition_param_id(self, ctx:RubyParser.Function_definition_param_idContext):
        pass


    # Enter a parse tree produced by RubyParser#return_statement.
    def enterReturn_statement(self, ctx:RubyParser.Return_statementContext):
        self.graph.addRuleNode(ctx)
        

    # Exit a parse tree produced by RubyParser#return_statement.
    def exitReturn_statement(self, ctx:RubyParser.Return_statementContext):
        pass


    # Enter a parse tree produced by RubyParser#function_call.
    def enterFunction_call(self, ctx:RubyParser.Function_callContext):
        self.graph.addRuleNode(ctx)
        

    # Exit a parse tree produced by RubyParser#function_call.
    def exitFunction_call(self, ctx:RubyParser.Function_callContext):
        pass


    # Enter a parse tree produced by RubyParser#function_call_param_list.
    def enterFunction_call_param_list(self, ctx:RubyParser.Function_call_param_listContext):
        self.graph.addRuleNode(ctx)
        

    # Exit a parse tree produced by RubyParser#function_call_param_list.
    def exitFunction_call_param_list(self, ctx:RubyParser.Function_call_param_listContext):
        pass


    # Enter a parse tree produced by RubyParser#function_call_params.
    def enterFunction_call_params(self, ctx:RubyParser.Function_call_paramsContext):
        self.graph.addRuleNode(ctx)
        

    # Exit a parse tree produced by RubyParser#function_call_params.
    def exitFunction_call_params(self, ctx:RubyParser.Function_call_paramsContext):
        pass


    # Enter a parse tree produced by RubyParser#function_param.
    def enterFunction_param(self, ctx:RubyParser.Function_paramContext):
        self.graph.addRuleNode(ctx)
        

    # Exit a parse tree produced by RubyParser#function_param.
    def exitFunction_param(self, ctx:RubyParser.Function_paramContext):
        pass


    # Enter a parse tree produced by RubyParser#function_unnamed_param.
    def enterFunction_unnamed_param(self, ctx:RubyParser.Function_unnamed_paramContext):
        self.graph.addRuleNode(ctx)
        

    # Exit a parse tree produced by RubyParser#function_unnamed_param.
    def exitFunction_unnamed_param(self, ctx:RubyParser.Function_unnamed_paramContext):
        pass


    # Enter a parse tree produced by RubyParser#function_named_param.
    def enterFunction_named_param(self, ctx:RubyParser.Function_named_paramContext):
        self.graph.addRuleNode(ctx)
        

    # Exit a parse tree produced by RubyParser#function_named_param.
    def exitFunction_named_param(self, ctx:RubyParser.Function_named_paramContext):
        pass


    # Enter a parse tree produced by RubyParser#function_call_assignment.
    def enterFunction_call_assignment(self, ctx:RubyParser.Function_call_assignmentContext):
        self.graph.addRuleNode(ctx)
        

    # Exit a parse tree produced by RubyParser#function_call_assignment.
    def exitFunction_call_assignment(self, ctx:RubyParser.Function_call_assignmentContext):
        pass


    # Enter a parse tree produced by RubyParser#all_result.
    def enterAll_result(self, ctx:RubyParser.All_resultContext):
        self.graph.addRuleNode(ctx)
        

    # Exit a parse tree produced by RubyParser#all_result.
    def exitAll_result(self, ctx:RubyParser.All_resultContext):
        pass


    # Enter a parse tree produced by RubyParser#elsif_statement.
    def enterElsif_statement(self, ctx:RubyParser.Elsif_statementContext):
        ifScope = self.scopeStack.pop()
        beforeIfScope = self.scopeStack.pop()

        ruleId = ctx.getRuleIndex()
        ruleName = RubyParser.ruleNames[ruleId]
        newScope = Scope(ruleName, 'block')

        beforeIfScope.addScope(newScope)

        self.scopeStack.append(beforeIfScope)
        self.scopeStack.append(ifScope)
        self.scopeStack.append(newScope)
        
        self.graph.addRuleNode(ctx)
        

    # Exit a parse tree produced by RubyParser#elsif_statement.
    def exitElsif_statement(self, ctx:RubyParser.Elsif_statementContext):
        scope = self.scopeStack.pop()

        # если последний скоуп - else, то значит предпоследний - elseif
        # у else нет своего места где его можно закрыть
        if scope.name == 'else_token':
            self.scopeStack.pop()


    # Enter a parse tree produced by RubyParser#if_elsif_statement.
    def enterIf_elsif_statement(self, ctx:RubyParser.If_elsif_statementContext):
        self.graph.addRuleNode(ctx)
        

    # Exit a parse tree produced by RubyParser#if_elsif_statement.
    def exitIf_elsif_statement(self, ctx:RubyParser.If_elsif_statementContext):
        pass


    # Enter a parse tree produced by RubyParser#if_statement.
    def enterIf_statement(self, ctx:RubyParser.If_statementContext):
        scope = self.scopeStack.pop()

        ruleId = ctx.getRuleIndex()
        ruleName = RubyParser.ruleNames[ruleId]
        newScope = Scope(ruleName, 'block')

        scope.addScope(newScope)

        self.scopeStack.append(scope)
        self.scopeStack.append(newScope)

        self.graph.addRuleNode(ctx)
        

    # Exit a parse tree produced by RubyParser#if_statement.
    def exitIf_statement(self, ctx:RubyParser.If_statementContext):
        scope = self.scopeStack.pop()

        # если последний скоуп - else, то значит предпоследний - if
        # у else нет своего места где его можно закрыть
        if scope.name == 'else_token':
            self.scopeStack.pop()


    # Enter a parse tree produced by RubyParser#unless_statement.
    def enterUnless_statement(self, ctx:RubyParser.Unless_statementContext):
        self.graph.addRuleNode(ctx)
        

    # Exit a parse tree produced by RubyParser#unless_statement.
    def exitUnless_statement(self, ctx:RubyParser.Unless_statementContext):
        pass


    # Enter a parse tree produced by RubyParser#while_statement.
    def enterWhile_statement(self, ctx:RubyParser.While_statementContext):
        scope = self.scopeStack.pop()

        ruleId = ctx.getRuleIndex()
        ruleName = RubyParser.ruleNames[ruleId]
        newScope = Scope(ruleName, 'block')

        scope.addScope(newScope)

        self.scopeStack.append(scope)
        self.scopeStack.append(newScope)
        self.graph.addRuleNode(ctx)
        

    # Exit a parse tree produced by RubyParser#while_statement.
    def exitWhile_statement(self, ctx:RubyParser.While_statementContext):
        self.scopeStack.pop()


    # Enter a parse tree produced by RubyParser#for_statement.
    def enterFor_statement(self, ctx:RubyParser.For_statementContext):
        scope = self.scopeStack.pop()

        ruleId = ctx.getRuleIndex()
        ruleName = RubyParser.ruleNames[ruleId]
        newScope = Scope(ruleName, 'block')

        scope.addScope(newScope)

        self.scopeStack.append(scope)
        self.scopeStack.append(newScope)

        self.graph.addRuleNode(ctx)
        

    # Exit a parse tree produced by RubyParser#for_statement.
    def exitFor_statement(self, ctx:RubyParser.For_statementContext):
        self.scopeStack.pop()
        pass


    # Enter a parse tree produced by RubyParser#init_expression.
    def enterInit_expression(self, ctx:RubyParser.Init_expressionContext):
        self.graph.addRuleNode(ctx)
        

    # Exit a parse tree produced by RubyParser#init_expression.
    def exitInit_expression(self, ctx:RubyParser.Init_expressionContext):
        pass


    # Enter a parse tree produced by RubyParser#all_assignment.
    def enterAll_assignment(self, ctx:RubyParser.All_assignmentContext):
        self.graph.addRuleNode(ctx)
        

    # Exit a parse tree produced by RubyParser#all_assignment.
    def exitAll_assignment(self, ctx:RubyParser.All_assignmentContext):
        pass


    # Enter a parse tree produced by RubyParser#for_init_list.
    def enterFor_init_list(self, ctx:RubyParser.For_init_listContext):
        self.graph.addRuleNode(ctx)
        

    # Exit a parse tree produced by RubyParser#for_init_list.
    def exitFor_init_list(self, ctx:RubyParser.For_init_listContext):
        pass


    # Enter a parse tree produced by RubyParser#cond_expression.
    def enterCond_expression(self, ctx:RubyParser.Cond_expressionContext):
        self.graph.addRuleNode(ctx)
        

    # Exit a parse tree produced by RubyParser#cond_expression.
    def exitCond_expression(self, ctx:RubyParser.Cond_expressionContext):
        pass


    # Enter a parse tree produced by RubyParser#loop_expression.
    def enterLoop_expression(self, ctx:RubyParser.Loop_expressionContext):
        self.graph.addRuleNode(ctx)
        

    # Exit a parse tree produced by RubyParser#loop_expression.
    def exitLoop_expression(self, ctx:RubyParser.Loop_expressionContext):
        pass


    # Enter a parse tree produced by RubyParser#for_loop_list.
    def enterFor_loop_list(self, ctx:RubyParser.For_loop_listContext):
        self.graph.addRuleNode(ctx)
        

    # Exit a parse tree produced by RubyParser#for_loop_list.
    def exitFor_loop_list(self, ctx:RubyParser.For_loop_listContext):
        pass


    # Enter a parse tree produced by RubyParser#statement_body.
    def enterStatement_body(self, ctx:RubyParser.Statement_bodyContext):
        self.graph.addRuleNode(ctx)
        

    # Exit a parse tree produced by RubyParser#statement_body.
    def exitStatement_body(self, ctx:RubyParser.Statement_bodyContext):
        pass


    # Enter a parse tree produced by RubyParser#statement_expression_list.
    def enterStatement_expression_list(self, ctx:RubyParser.Statement_expression_listContext):
        self.graph.addRuleNode(ctx)
        

    # Exit a parse tree produced by RubyParser#statement_expression_list.
    def exitStatement_expression_list(self, ctx:RubyParser.Statement_expression_listContext):
        pass


    # Enter a parse tree produced by RubyParser#assignment.
    def enterAssignment(self, ctx:RubyParser.AssignmentContext):
        self.graph.addRuleNode(ctx)
        

    # Exit a parse tree produced by RubyParser#assignment.
    def exitAssignment(self, ctx:RubyParser.AssignmentContext):
        pass


    # Enter a parse tree produced by RubyParser#dynamic_assignment.
    def enterDynamic_assignment(self, ctx:RubyParser.Dynamic_assignmentContext):
        scope = self.scopeStack.pop()

        lvalue = ctx.getChild(0)
        result = ctx.getChild(2)
        varName = lvalue.getText()
        varValue = result.getText()
        ruleId = ctx.getRuleIndex()
        ruleName = RubyParser.ruleNames[ruleId]
        variable = ScopeVariable(varName, ruleName, varValue)

        scope.addVariable(variable)
        self.scopeStack.append(scope)
        self.graph.addRuleNode(ctx)
        

    # Exit a parse tree produced by RubyParser#dynamic_assignment.
    def exitDynamic_assignment(self, ctx:RubyParser.Dynamic_assignmentContext):
        pass


    # Enter a parse tree produced by RubyParser#int_assignment.
    def enterInt_assignment(self, ctx:RubyParser.Int_assignmentContext):
        scope = self.scopeStack.pop()

        lvalue = ctx.getChild(0)
        result = ctx.getChild(2)
        varName = lvalue.getText()
        varValue = result.getText()
        variable = ScopeVariable(varName, 'int', varValue)

        scope.addVariable(variable)
        self.scopeStack.append(scope)
        self.graph.addRuleNode(ctx)
        

    # Exit a parse tree produced by RubyParser#int_assignment.
    def exitInt_assignment(self, ctx:RubyParser.Int_assignmentContext):
        pass


    # Enter a parse tree produced by RubyParser#float_assignment.
    def enterFloat_assignment(self, ctx:RubyParser.Float_assignmentContext):
        scope = self.scopeStack.pop()

        lvalue = ctx.getChild(0)
        result = ctx.getChild(2)
        varName = lvalue.getText()
        varValue = result.getText()
        variable = ScopeVariable(varName, 'string', varValue)

        scope.addVariable(variable)
        self.scopeStack.append(scope)
        self.graph.addRuleNode(ctx)
        

    # Exit a parse tree produced by RubyParser#float_assignment.
    def exitFloat_assignment(self, ctx:RubyParser.Float_assignmentContext):
        pass


    # Enter a parse tree produced by RubyParser#string_assignment.
    def enterString_assignment(self, ctx:RubyParser.String_assignmentContext):
        scope = self.scopeStack.pop()

        lvalue = ctx.getChild(0)
        result = ctx.getChild(2)
        varName = lvalue.getText()
        varValue = result.getText()
        variable = ScopeVariable(varName, 'string', varValue)

        scope.addVariable(variable)
        self.scopeStack.append(scope)
        self.graph.addRuleNode(ctx)
        

    # Exit a parse tree produced by RubyParser#string_assignment.
    def exitString_assignment(self, ctx:RubyParser.String_assignmentContext):
        pass


    # Enter a parse tree produced by RubyParser#initial_array_assignment.
    def enterInitial_array_assignment(self, ctx:RubyParser.Initial_array_assignmentContext):
        scope = self.scopeStack.pop()

        lvalue = ctx.getChild(0)
        varName = lvalue.getText()
        varValue = self.getInitialArrayAssignmentValue(ctx)
        variable = ScopeVariable(varName, 'array', varValue)

        scope.addVariable(variable)
        self.scopeStack.append(scope)
        self.graph.addRuleNode(ctx)
        

    # Exit a parse tree produced by RubyParser#initial_array_assignment.
    def exitInitial_array_assignment(self, ctx:RubyParser.Initial_array_assignmentContext):
        pass


    # Enter a parse tree produced by RubyParser#array_assignment.
    def enterArray_assignment(self, ctx:RubyParser.Array_assignmentContext):
        self.graph.addRuleNode(ctx)
        

    # Exit a parse tree produced by RubyParser#array_assignment.
    def exitArray_assignment(self, ctx:RubyParser.Array_assignmentContext):
        pass


    # Enter a parse tree produced by RubyParser#array_definition.
    def enterArray_definition(self, ctx:RubyParser.Array_definitionContext):
        self.graph.addRuleNode(ctx)
        

    # Exit a parse tree produced by RubyParser#array_definition.
    def exitArray_definition(self, ctx:RubyParser.Array_definitionContext):
        pass


    # Enter a parse tree produced by RubyParser#array_definition_elements.
    def enterArray_definition_elements(self, ctx:RubyParser.Array_definition_elementsContext):
        self.graph.addRuleNode(ctx)
        

    # Exit a parse tree produced by RubyParser#array_definition_elements.
    def exitArray_definition_elements(self, ctx:RubyParser.Array_definition_elementsContext):
        pass


    # Enter a parse tree produced by RubyParser#array_selector.
    def enterArray_selector(self, ctx:RubyParser.Array_selectorContext):
        self.graph.addRuleNode(ctx)
        

    # Exit a parse tree produced by RubyParser#array_selector.
    def exitArray_selector(self, ctx:RubyParser.Array_selectorContext):
        pass


    # Enter a parse tree produced by RubyParser#dynamic_result.
    def enterDynamic_result(self, ctx:RubyParser.Dynamic_resultContext):
        self.graph.addRuleNode(ctx)
        

    # Exit a parse tree produced by RubyParser#dynamic_result.
    def exitDynamic_result(self, ctx:RubyParser.Dynamic_resultContext):
        pass


    # Enter a parse tree produced by RubyParser#dynamic.
    def enterDynamic(self, ctx:RubyParser.DynamicContext):
        self.graph.addRuleNode(ctx)
        

    # Exit a parse tree produced by RubyParser#dynamic.
    def exitDynamic(self, ctx:RubyParser.DynamicContext):
        pass


    # Enter a parse tree produced by RubyParser#int_result.
    def enterInt_result(self, ctx:RubyParser.Int_resultContext):
        self.graph.addRuleNode(ctx)
        

    # Exit a parse tree produced by RubyParser#int_result.
    def exitInt_result(self, ctx:RubyParser.Int_resultContext):
        pass


    # Enter a parse tree produced by RubyParser#float_result.
    def enterFloat_result(self, ctx:RubyParser.Float_resultContext):
        self.graph.addRuleNode(ctx)
        

    # Exit a parse tree produced by RubyParser#float_result.
    def exitFloat_result(self, ctx:RubyParser.Float_resultContext):
        pass


    # Enter a parse tree produced by RubyParser#string_result.
    def enterString_result(self, ctx:RubyParser.String_resultContext):
        self.graph.addRuleNode(ctx)
        

    # Exit a parse tree produced by RubyParser#string_result.
    def exitString_result(self, ctx:RubyParser.String_resultContext):
        pass


    # Enter a parse tree produced by RubyParser#comparison_list.
    def enterComparison_list(self, ctx:RubyParser.Comparison_listContext):
        self.graph.addRuleNode(ctx)

    # Exit a parse tree produced by RubyParser#comparison_list.
    def exitComparison_list(self, ctx:RubyParser.Comparison_listContext):
        pass


    # Enter a parse tree produced by RubyParser#comparison.
    def enterComparison(self, ctx:RubyParser.ComparisonContext):
        self.graph.addRuleNode(ctx)

    # Exit a parse tree produced by RubyParser#comparison.
    def exitComparison(self, ctx:RubyParser.ComparisonContext):
        pass


    # Enter a parse tree produced by RubyParser#comp_var.
    def enterComp_var(self, ctx:RubyParser.Comp_varContext):
        self.graph.addRuleNode(ctx)

    # Exit a parse tree produced by RubyParser#comp_var.
    def exitComp_var(self, ctx:RubyParser.Comp_varContext):
        pass


    # Enter a parse tree produced by RubyParser#lvalue.
    def enterLvalue(self, ctx:RubyParser.LvalueContext):
        self.graph.addRuleNode(ctx)

    # Exit a parse tree produced by RubyParser#lvalue.
    def exitLvalue(self, ctx:RubyParser.LvalueContext):
        pass


    # Enter a parse tree produced by RubyParser#rvalue.
    def enterRvalue(self, ctx:RubyParser.RvalueContext):
        self.graph.addRuleNode(ctx)

    # Exit a parse tree produced by RubyParser#rvalue.
    def exitRvalue(self, ctx:RubyParser.RvalueContext):
        pass


    # Enter a parse tree produced by RubyParser#break_expression.
    def enterBreak_expression(self, ctx:RubyParser.Break_expressionContext):
        self.graph.addRuleNode(ctx)

    # Exit a parse tree produced by RubyParser#break_expression.
    def exitBreak_expression(self, ctx:RubyParser.Break_expressionContext):
        pass


    # Enter a parse tree produced by RubyParser#literal_t.
    def enterLiteral_t(self, ctx:RubyParser.Literal_tContext):
        self.graph.addRuleNode(ctx)

    # Exit a parse tree produced by RubyParser#literal_t.
    def exitLiteral_t(self, ctx:RubyParser.Literal_tContext):
        pass


    # Enter a parse tree produced by RubyParser#float_t.
    def enterFloat_t(self, ctx:RubyParser.Float_tContext):
        self.graph.addRuleNode(ctx)

    # Exit a parse tree produced by RubyParser#float_t.
    def exitFloat_t(self, ctx:RubyParser.Float_tContext):
        pass


    # Enter a parse tree produced by RubyParser#int_t.
    def enterInt_t(self, ctx:RubyParser.Int_tContext):
        self.graph.addRuleNode(ctx)

    # Exit a parse tree produced by RubyParser#int_t.
    def exitInt_t(self, ctx:RubyParser.Int_tContext):
        pass


    # Enter a parse tree produced by RubyParser#bool_t.
    def enterBool_t(self, ctx:RubyParser.Bool_tContext):
        self.graph.addRuleNode(ctx)

    # Exit a parse tree produced by RubyParser#bool_t.
    def exitBool_t(self, ctx:RubyParser.Bool_tContext):
        pass


    # Enter a parse tree produced by RubyParser#nil_t.
    def enterNil_t(self, ctx:RubyParser.Nil_tContext):
        self.graph.addRuleNode(ctx)

    # Exit a parse tree produced by RubyParser#nil_t.
    def exitNil_t(self, ctx:RubyParser.Nil_tContext):
        pass


    # Enter a parse tree produced by RubyParser#id.
    def enterId(self, ctx:RubyParser.IdContext):
        self.graph.addRuleNode(ctx)

    # Exit a parse tree produced by RubyParser#id.
    def exitId(self, ctx:RubyParser.IdContext):
        pass


    # Enter a parse tree produced by RubyParser#id_global.
    def enterId_global(self, ctx:RubyParser.Id_globalContext):
        self.graph.addRuleNode(ctx)

    # Exit a parse tree produced by RubyParser#id_global.
    def exitId_global(self, ctx:RubyParser.Id_globalContext):
        pass


    # Enter a parse tree produced by RubyParser#id_function.
    def enterId_function(self, ctx:RubyParser.Id_functionContext):
        self.graph.addRuleNode(ctx)

    # Exit a parse tree produced by RubyParser#id_function.
    def exitId_function(self, ctx:RubyParser.Id_functionContext):
        pass


    # Enter a parse tree produced by RubyParser#terminator.
    def enterTerminator(self, ctx:RubyParser.TerminatorContext):
        self.graph.addRuleNode(ctx)

    # Exit a parse tree produced by RubyParser#terminator.
    def exitTerminator(self, ctx:RubyParser.TerminatorContext):
        pass


    # Enter a parse tree produced by RubyParser#else_token.
    def enterElse_token(self, ctx:RubyParser.Else_tokenContext):
        scope = self.scopeStack.pop()

        ruleId = ctx.getRuleIndex()
        ruleName = RubyParser.ruleNames[ruleId]
        newScope = Scope(ruleName, 'block')

        if scope.name == 'elsif_statement':
            ifScope = self.scopeStack.pop()
            beforeIfScope = self.scopeStack.pop()

            beforeIfScope.addScope(newScope)

            self.scopeStack.append(beforeIfScope)
            self.scopeStack.append(ifScope)
            self.scopeStack.append(scope)
            self.scopeStack.append(newScope)
        elif scope.name == 'if_statement':
            beforeIfScope = self.scopeStack.pop()

            beforeIfScope.addScope(newScope)

            self.scopeStack.append(beforeIfScope)
            self.scopeStack.append(scope)
            self.scopeStack.append(newScope)

        self.graph.addRuleNode(ctx)

    # Exit a parse tree produced by RubyParser#else_token.
    def exitElse_token(self, ctx:RubyParser.Else_tokenContext):
        pass


    # Enter a parse tree produced by RubyParser#crlf.
    def enterCrlf(self, ctx:RubyParser.CrlfContext):
        self.graph.addRuleNode(ctx)

    # Exit a parse tree produced by RubyParser#crlf.
    def exitCrlf(self, ctx:RubyParser.CrlfContext):
        pass