#coding=utf8
import sys
from lexer import *
import lexer as l
from parser import build_tree

with open(sys.argv[-1], 'r') as my_file:
    data = my_file.read()
    l.lexer.input(data)
    while True:
        tok = l.lexer.token() # читаем следующий токен
        if not tok: break      # закончились печеньки
            #print(tok.type, tok.value, tok.lineno, tok.lexpos)
        print(tok)
    l._FFlag = 1;
    l.lexer = lex.lex()
    print(build_tree(data))