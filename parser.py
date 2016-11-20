# coding=utf8
from lexer import tokens
import ply.yacc as yacc

class Node:
    def parts_str(self):
        st = []
        for part in self.parts:
            st.append( str( part ) )
        return "\n".join(st)

    def __repr__(self):
        return self.type + ":\n    " + self.parts_str().replace("\n", "\n    ")

    def add_parts(self, parts):
        self.parts += parts
        return self

    def __init__(self, type, parts):
        self.type = type
        self.parts = parts

#непосредственно парсер

def p_program_state(p):
    '''program : state '''
    p[0] = Node('P', [p[1]])

def p_state_skip(p):
    '''state : SKIP'''
    p[0] = Node('S', ['skip'])

def p_state_assignment(p):
    '''state : x ASSIGNMENT exp'''
    p[0] = Node('S', [p[1], ':=', p[3]])

def p_state_colon(p):
    '''state : state COLON state'''
    p[0] = Node('S', [p[1], p[3]])

def p_state_write(p):
    '''state : WRITE exp'''
    p[0] = Node('S', ['write', p[2]])

def p_state_read(p):
    '''state : READ x'''
    p[0] = Node('S', ['read',p[2]])
    #p[0] = Node('read', [p[2]])

def p_state_while(p):
    '''state : WHILE exp DO state'''
    p[0] = Node('S', ['while', p[2], 'do', p[4]])

def p_state_if(p):
    '''state : IF exp THEN state ELSE state'''
    p[0] = Node('S', ['if', p[2], 'then', p[4], 'else', p[6]])

def p_exp_var(p):
    '''exp : x'''
    p[0] = Node('EXP', [p[1]])

def p_var_x(p):
    '''x : VAR'''
    p[0] = Node('VAR', [p[1]])

def p_exp_number(p):
    '''exp : NUMBER'''
    p[0] = Node('NUM', [p[1]])


def p_expression_parenthesis(p):
    '''exp : PARENTHESIS exp operation exp PARENTHESIS'''
    p[0] = Node('EXP', ['(', p[2], p[3], p[4],')'])
    #p[0] = Node(p[2])

def p_expression_parenthesisfix(p):
    '''exp : exp operation exp'''
    p[0] = Node('EXP', [p[1], p[2], p[3]])

def p_operation_OP(p):
    '''operation : OP
                | MULT
                | DIV'''
    p[0] = Node('OP ', p[1])


def p_state_UNCOMMENT(p):
    '''state : COMMENT state
            | LINECOMMENT state '''
    pass

def p_error(p):
    print("unexpected token '%s'" % p.value[0])


def build_tree(code):
    parser = yacc.yacc(start='program')
    result = parser.parse(code)
    return result