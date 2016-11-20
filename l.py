#coding=utf8
from lexer import *
import lexer as l

with open(sys.argv[-1], 'r') as my_file:
    data = my_file.read()
    l.lexer.input(data)
    while True:
        tok = l.lexer.token() # читаем следующий токен
        if not tok: break      # закончились печеньки
        print(tok)