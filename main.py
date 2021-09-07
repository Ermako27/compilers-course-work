import sys
from antlr4 import *
from RubyLexer import RubyLexer
from RubyParser import RubyParser
from CustomRubyListener import CustomRubyListener
 
def main(argv):
    # codeFileName = argv[1]
    codeFileName = 'quicksort'
    input_stream = FileStream('./tests/{0}.rb'.format(codeFileName))
    lexer = RubyLexer(input_stream)
    stream = CommonTokenStream(lexer)
    # allTokens = lexer.getAllTokens()
    # print(lexer.getAllTokens())
    # print(lexer.nextToken())
    # print(lexer.nextToken())
    # print(lexer.nextToken())
    parser = RubyParser(stream)
    tree = parser.prog()
    printer = CustomRubyListener(codeFileName)
    walker = ParseTreeWalker()
    walker.walk(printer, tree)
 
if __name__ == '__main__':
    main(sys.argv)


# поток токенов, ошибки