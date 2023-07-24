# -----------------------------------------------------------------------------
# app.py
# -----------------------------------------------------------------------------

from ply.lex import lex
from ply.yacc import yacc


# --- TOKENIZER ---

# a list of all the token names accepted by the parser
tokens = ('NEGATION',
          'CONJUNCTION',
          'DISJUNCTION',
          'IMPLICATION',
          'BICONDITIONAL',
          'LEFT_PARENTHESIS',
          'RIGHT_PARENTHESIS',
          'LETTER')  # already in precedence order
# TODO ask about the precedence order

t_ignore = ' \t'

t_NEGATION = r'\~'
t_CONJUNCTION = r'\^'
t_DISJUNCTION = r'o'
t_IMPLICATION = r'=>'
t_BICONDITIONAL = r'<=>'
t_LEFT_PARENTHESIS = r'\('
t_RIGHT_PARENTHESIS = r'\)'
# t_COMMA = r',' TODO why to include this, is it even used?
t_LETTER = r'[a-np-zA-Z]'  # letters except 'o' used for disjunction


def t_ignore_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


def t_error(t):  # error handling or unknown characters
    print(f'Illegal character {t.value[0]}')
    t.lexer.skip(1)


# build the lexer obj
lexer = lex()

# --- PARSER ---
# here we define the grammar rules and
# the actions to be taken when a rule is recognized


def p_expression_letter(p):
    'expression : LETTER'
    p[0] = ('letter', p[1])
    print('Recognized letter:', p[1])


def p_expression_negation(p):
    'expression : NEGATION expression'
    p[0] = ('negation', p[2])
    print('Recognized negation:', p[2])


def p_expression_conjunction(p):
    'expression : expression CONJUNCTION expression'
    p[0] = ('conjunction', p[1], p[3])
    print('Recognized conjunction:', p[1], p[3])


def p_expression_disjunction(p):
    'expression : expression DISJUNCTION expression'
    p[0] = ('disjunction', p[1], p[3])
    print('Recognized disjunction:', p[1], p[3])


def p_expression_implication(p):
    'expression : expression IMPLICATION expression'
    p[0] = ('implication', p[1], p[3])
    print('Recognized implication:', p[1], p[3])


def p_expression_biconditional(p):
    'expression : expression BICONDITIONAL expression'
    p[0] = ('biconditional', p[1], p[3])
    print('Recognized biconditional:', p[1], p[3])


def p_expression_parenthesis(p):
    'expression : LEFT_PARENTHESIS expression RIGHT_PARENTHESIS'
    p[0] = p[2]
    print('Recognized parenthesis:', p[2])


def p_error(p):
    print(f'Syntax error at {p.value!r}')


parser = yacc()

# Parse an expression
ast = parser.parse('(p=>q)^p')
print(ast)
# TODO show the text representation of the tree to the professor
