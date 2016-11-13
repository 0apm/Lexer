#coding=utf8
import sys
import ply.lex as lex
_FFlag = 0
if sys.argv[1] == '-filter':
    _FFlag = 1;

# List of token names.   This is always required

reserved = {
    'skip' : 'SKIP',
    'read': 'READ',
    'write' :'WRITE',
    'while' : 'WHILE',
    'do': 'DO',
    'if' : 'IF',
    'then' : 'THEN',
    'else' : 'ELSE'
}

tokens = [
    'COMMENT',
    'LINECOMMENT',
    'COLON',
    'VAR',
    'ASSIGNMENT',
    'OP',
    'NUMBER',
    'PARENTHESIS',
    'DIV',
    'MULT'
] + list(reserved.values())
t_NUMBER = r'([1-9][0-9]*)|(0)'
t_PARENTHESIS = r'(\(|\))'
t_COLON = r'\;'
t_ASSIGNMENT = r':='

def t_LINECOMMENT(t):
    r'(//[^\n]*(\n|$))'
    t.lexer.lineno += 1
    if _FFlag == 1:
        pass
    else:
        return t

def t_COMMENT(t):
    r'[(][*]((([^*])*([^)])*)|((([^*])*([^)])*[*][^)]+[)]([^*])*([^)])*))*)[*][)]'
    for i in t.value:
        if i == '\n':
            t.lexer.lineno += 1
    t.type = 'COMMENT'
    if _FFlag == 1:
        pass
    else:
        return t

def t_DIV(t):
    r'/'
    t.type = 'OP'
    return t

def t_OP(t):
    r'([+|\-|%|<|>])|([=|\!]=)|([>|<]=)|(&&)|(\|\|)|[\*][\*]'
    return t

def t_MULT(t):
    r'\*'
    t.type = 'OP'
    return t

def t_VAR(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value,'VAR')
    return t

# Define a rule so we can track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# A string containing ignored characters (spaces and tabs)
t_ignore = ' \t\r'

# Error handling rule
def t_error(t):
    print("Illegal character '%s'" % t.value[0]*20)
    t.lexer.skip(1)

# Build the lexer
lexer = lex.lex()