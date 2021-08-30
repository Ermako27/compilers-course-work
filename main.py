import sys
from antlr4 import *
from RubyLexer import RubyLexer
from RubyParser import RubyParser
from CustomRubyListener import CustomRubyListener
 
def main():
    input_stream = FileStream('./main.rb')
    lexer = RubyLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = RubyParser(stream)
    tree = parser.prog()
    printer = CustomRubyListener()
    walker = ParseTreeWalker()
    walker.walk(printer, tree)
 
if __name__ == '__main__':
    main()