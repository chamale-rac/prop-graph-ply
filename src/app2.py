# -----------------------------------------------------------------------------
# app2.py
# author: Grupo 3
# date: 2023-08-25 18:00:00
# -----------------------------------------------------------------------------


from ply.lex import lex
from ply.yacc import yacc


import matplotlib.pyplot as plt
import networkx as nx
# from networkx.drawing.nx_agraph import graphviz_layout


# --------- project ---------
# description: args received from command line


import os


def create_directory_if_not_exists(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)


# --------- tokenizer ---------
# description: lexical analysis of the input string


# tokens = ('NEGATION',
#           'CONJUNCTION',
#           'DISJUNCTION',
#           'IMPLICATION',
#           'BICONDITIONAL',
#           'LPAREN',
#           'RPAREN',
#           'VARIABLE')  # already in precedence order

tokens = ('NEGATION',
          'IMPLICATION',
          'BICONDITIONAL',
          'CONJUNCTION',
          'DISJUNCTION',
          'LPAREN',
          'RPAREN',
          'VARIABLE',
          'CONSTANT')
# TODO ask about the precedence order

# negacion
# implicacion
# doble implicacion
# y:conjuncion o disjuncion

t_ignore = ' \t'

t_NEGATION = r'\~'
t_CONJUNCTION = r'\^'
t_DISJUNCTION = r'o'
t_IMPLICATION = r'=>'
t_BICONDITIONAL = r'<=>'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_VARIABLE = r'[pqrstuvwxyz]'  # letters except 'o' used for disjunction
t_CONSTANT = r'[01]'
# TODO ask about including t_COMMA


def t_ignore_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


def t_error(t):  # error handling or unknown characters
    print(f'Illegal character {t.value[0]}')
    t.lexer.skip(1)


lexer = lex()


# --------- node ---------
# description: node of a tree


class Node:
    _id_counter = 0

    def __init__(self, value):
        self.id = Node._id_counter
        Node._id_counter += 1
        self.value = value
        self.children = []

    def add_child(self, child):
        self.children.append(child)

    def __str__(self):
        return self._str_helper(0)

    def _str_helper(self, depth):
        indent = '---' * depth
        s = f'{indent}{self.id}: {self.value}\n'
        for child in self.children:
            s += child._str_helper(depth + 1)
        return s


# --------- parser ---------
# description: syntactic analysis of the input string


def p_expression_variable(p):
    'expression : VARIABLE'
    p[0] = Node(p[1])


def p_expression_constant(p):
    'expression : CONSTANT'
    p[0] = Node(p[1])


def p_expression_negation(p):
    'expression : NEGATION expression'
    node = Node(p[1])
    node.add_child(p[2])
    p[0] = node


def p_expression_paren(p):
    'expression : LPAREN expression RPAREN'
    p[0] = p[2]


def p_expression(p):
    '''expression : expression CONJUNCTION expression
                  | expression DISJUNCTION expression
                  | expression IMPLICATION expression
                  | expression BICONDITIONAL expression'''

    node = Node(p[2])
    node.add_child(p[3])
    node.add_child(p[1])
    # ask about the order of the children, cause it will affect the diagram
    p[0] = node


def p_error(p):
    print(f'Syntax error at {p.value!r}')


parser = yacc()

chains = [
    '(p=>q)^p',
    'p',
    '~~~q',
    '(p^q)',
    '(0=>(ros))',
    '~(p^q)',
    '(p<=>~p)',
    '((p=>q)^p)',
    '(~(p^(qor))os)',

]

results = []

for chain in chains:
    result = parser.parse(chain)
    results.append(result)
    print(f'Chain: {chain}')
    print(f'Result:\n{result}')
    print()


# --------- tree ---------
def graph_tree(tree):
    G = nx.DiGraph()
    G.add_node(tree.id, label=tree.value)
    for child in tree.children:
        child_G = graph_tree(child)
        G = nx.compose(G, child_G)
        G.add_edge(tree.id, child.id)
    return G


for i, result in enumerate(results):
    G = graph_tree(result)
    labels = nx.get_node_attributes(G, 'label')

    # this is the part that I don't understand, I just copied it from the stackoverflow answer
    for layer, nodes in enumerate(reversed(tuple(nx.topological_generations(G)))):
        # `multipartite_layout` expects the layer as a node attribute, so add the
        # numeric layer value as a node attribute
        for node in nodes:
            G.nodes[node]["layer"] = layer

    pos = nx.multipartite_layout(G, subset_key="layer", align='horizontal')

    fig, ax = plt.subplots()
    nx.draw_networkx_nodes(G, pos, node_size=1000,
                           node_color='white', edgecolors='black')
    nx.draw_networkx_edges(G, pos, arrowsize=20, edge_color='black')
    nx.draw_networkx_labels(G, pos, labels, font_size=12)
    ax.set_title('Grafo dirigido ' + chains[i], fontsize=20)
    fig.tight_layout()
    plt.axis('off')

    dir = '../img/'
    create_directory_if_not_exists(dir)
    plt.savefig(f'{dir}graph{i}.png')
    plt.close()

    # TODO check operations order while graphing


'''
REFERENCES:
https://stackoverflow.com/questions/29586520/can-one-get-hierarchical-graphs-from-networkx-with-python-3/76215030#76215030
https://github.com/dabeaz/ply
'''
