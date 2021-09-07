import uuid
import graphviz

from RubyParser import RubyParser


class Graph():
    def __init__(self,codeFileName) -> None:
        self.ruleTree = graphviz.Digraph(comment='The Round Table')
        self.callTree = graphviz.Digraph(comment='The Round Table')
        self.codeFileName = codeFileName

    def isLeaf(self, ctx):
        if hasattr(ctx, 'children') and ctx.children != None:
            # Если ctx - это лист, то ребенок у него будет None
            child = ctx.getChild(0)
            return child == None
        return True
    
    def addRuleNode(self, ctx):

        if hasattr(ctx, 'uid'):
            uid = ctx.uid
        else:
            uid = uuid.uuid4().hex
            ctx.uid = uid 

        # try:
        #     uid = ctx.uid
        # except:
        #     uid = uuid.uuid4().hex
        #     ctx.uid = uid

        ruleId = ctx.getRuleIndex()
        ruleName = RubyParser.ruleNames[ruleId]
        self.ruleTree.node(ctx.uid, ruleName)

        # print('[ enter ] uid: {0} | rule: {1} \n'.format(ctx.uid, ruleName))

        if ctx.parentCtx != None:
            self.ruleTree.edge(ctx.parentCtx.uid, ctx.uid)

        if ctx.children != None:
            for child in ctx.children: # пройдемся по всем детям ноды в поисках листов
                if self.isLeaf(child):
                    leafUid = uuid.uuid4().hex
                    leafValue = child.getText()
                    self.ruleTree.node(leafUid, str(leafValue))
                    self.ruleTree.edge(ctx.uid, leafUid)

    def renderRuleTree(self):
        self.ruleTree.render('ruleTree_{0}'.format(self.codeFileName), './img')

    def renderCallTree(self, rootNode):
        self.callTree.node(rootNode.name, rootNode.name)
        self.createCallTree(rootNode)
        self.callTree.render('callTree_{0}'.format(self.codeFileName), './img')

    def findFunctionScope(self, scope, scopeName):
        if scopeName in scope.childrenFunctionScope:
            return scope.childrenFunctionScope[scopeName]
        else:
            return self.findFunctionScope(scope.parentScope, scopeName)

    def createCallTree(self, node):
        for functionCall in node.functionCalls:
            self.callTree.node(functionCall, functionCall)
            self.callTree.edge(node.name, functionCall)

            childFunctionScope = self.findFunctionScope(node, functionCall)
            if childFunctionScope.name != node.name:
                self.createCallTree(childFunctionScope)
