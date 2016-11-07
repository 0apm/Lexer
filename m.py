#coding=utf8
import sys
import ply.lex as lex
_FFlag = 0
if sys.argv[1] == '-filter':
    _FFlag = 1;

# List of token names.   This is always required
tokens = (
    'Comment',
    'MLneComment',
    'KW_SKIP',
    'KW_WRITE',
    'KW_READ',
    'KW_WHILE',
    'KW_DO',
    'KW_IF',
    'KW_ELSE',
    'KW_THEN',
    'Colon',
    'Var',
    'Assignment',
    'Op',
    'Number',
    'Parenthesis',
    'Div',
    'Multiply'
)

t_KW_SKIP = r'skip'
t_KW_WRITE = r'WRITE'
t_KW_READ = r'read'
t_KW_WHILE = r'while'
t_KW_DO = r'do'
t_KW_IF = r'if'
t_KW_ELSE = r'else'
t_KW_THEN = r'then'
t_Number = r'([1-9][0-9]*)|(0)'
t_Parenthesis = r'(\(|\))'
t_Colon = r'\;'
t_Assignment = r':='
t_Var = r'[a-zA-Z_][a-zA-Z_0-9]*'


def t_Comment(t):
    r'(//[^\n]*(\n|$))'
    t.lexer.lineno += 1
    if _FFlag == 1:
        pass
    else:
        return t

def t_MLineComment(t):
    r'[(][*]((([^*])*([^)])*)|((([^*])*([^)])*[*][^)]+[)]([^*])*([^)])*))*)[*][)]'
    for i in t.value:
        if i == '\n':
            t.lexer.lineno += 1
    t.type = 'Comment'
    if _FFlag == 1:
        pass
    else:
        return t

def t_Div(t):
    r'/'
    t.type = 'Op'
    return t

def t_Op(t):
    r'([+|\-|%|<|>])|([=|\!]=)|([>|<]=)|(&&)|(\|\|)|[\*][\*]'
    return t

def t_Multiply(t):
    r'\*'
    t.type = 'Op'
    return t

# Define a rule so we can track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += 1

# A string containing ignored characters (spaces and tabs)
t_ignore = ' \t\r'

# Error handling rule
def t_error(t):
    print("Illegal character '%s'" % t.value[0]*20)
    t.lexer.skip(1)

# Build the lexer
lexer = lex.lex()

with open(sys.argv[-1], 'r') as my_file:
    data = my_file.read()
    lexer.input(data)
    while True:
        tok = lexer.token() # читаем следующий токен
        if not tok: break      # закончились печеньки
            #print(tok.type, tok.value, tok.lineno, tok.lexpos)
        print(tok)