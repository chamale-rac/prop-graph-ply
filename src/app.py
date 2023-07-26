# -----------------------------------------------------------------------------
# app.py
# -----------------------------------------------------------------------------

from ply.lex import lex
from ply.yacc import yacc

import matplotlib.pyplot as plt
import networkx as nx

# --- PROJECT ---
DEBUG = False
SHOW = True
GRAPH = True

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
t_LETTER = r'[a-np-zA-Z]|[0-9]'  # letters except 'o' used for disjunction


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
    if DEBUG:
        print('Recognized letter:', p[1])


def p_expression_negation(p):
    'expression : NEGATION expression'
    p[0] = ('negation', p[2])
    if DEBUG:
        print('Recognized negation:', p[2])


def p_expression_conjunction(p):
    'expression : expression CONJUNCTION expression'
    p[0] = ('conjunction', p[1], p[3])
    if DEBUG:
        print('Recognized conjunction:', p[1], p[3])


def p_expression_disjunction(p):
    'expression : expression DISJUNCTION expression'
    p[0] = ('disjunction', p[1], p[3])
    if DEBUG:
        print('Recognized disjunction:', p[1], p[3])


def p_expression_implication(p):
    'expression : expression IMPLICATION expression'
    p[0] = ('implication', p[1], p[3])
    if DEBUG:
        print('Recognized implication:', p[1], p[3])


def p_expression_biconditional(p):
    'expression : expression BICONDITIONAL expression'
    p[0] = ('biconditional', p[1], p[3])
    if DEBUG:
        print('Recognized biconditional:', p[1], p[3])


def p_expression_parenthesis(p):
    'expression : LEFT_PARENTHESIS expression RIGHT_PARENTHESIS'
    p[0] = p[2]
    if DEBUG:
        print('Recognized parenthesis:', p[2])


def p_error(p):
    print(f'Syntax error at {p.value!r}')


parser = yacc()

# Parse an expression
original = '(p=>q)^p'
ast = parser.parse(original)
if SHOW:
    print('TEXT TREE REPRESENTATION:', ast)

# --- GRAPH ---


def node_label(node):
    if node[0] == 'letter':
        return node[1]
    elif node[0] == 'negation':
        return '~'
    elif node[0] == 'conjunction':
        return '^'
    elif node[0] == 'disjunction':
        return 'o'
    elif node[0] == 'implication':
        return '=>'
    elif node[0] == 'biconditional':
        return '<=>'
    else:
        return 'error'


def graph_ast(ast, original_ast=''):
    # create a new directed graph
    G = nx.DiGraph()

    # add the root node to the graph
    root = str(id(ast))
    G.add_node(root, label=node_label(ast))

    def custom_add_node(node, parent, first=False):
        # recursively add the child nodes to the graph
        if len(node) == 3:
            node_id = str(id(node))
            if first is False:
                G.add_node(node_id, label=node_label(node))
                G.add_edge(parent, node_id)
            custom_add_node(node[1], node_id)
            custom_add_node(node[2], node_id)
        else:
            node_id = str(id(node))
            G.add_node(node_id, label=node_label(node))
            G.add_edge(parent, node_id)

    custom_add_node(ast, root, True)

    # set the node labels and positions
    labels = nx.get_node_attributes(G, 'label')
    # pos = nx.spring_layout(G)

    # # draw the graph
    # nx.draw_networkx_nodes(G, pos, node_size=1000,
    #                        node_color='white', edgecolors='black')
    # nx.draw_networkx_edges(G, pos, arrowsize=20, edge_color='black')
    # nx.draw_networkx_labels(G, pos, labels, font_size=12)

    # # show the graph
    # plt.axis('off')
    # plt.show()

    # for layer, nodes in enumerate(reversed(tuple(nx.topological_generations(G)))):
    #     # `multipartite_layout` expects the layer as a node attribute, so add the
    #     # numeric layer value as a node attribute
    #     for node in nodes:
    #         G.nodes[node]["layer"] = layer

    # # Compute the multipartite_layout using the "layer" node attribute
    # pos = nx.multipartite_layout(G, subset_key="layer", align='horizontal')

    # fig, ax = plt.subplots()
    # nx.draw_networkx_nodes(G, pos, node_size=1000,
    #                        node_color='white', edgecolors='black')
    # nx.draw_networkx_edges(G, pos, arrowsize=20, edge_color='black')
    # nx.draw_networkx_labels(G, pos, labels, font_size=12)
    # ax.set_title('Grafo dirigido' + '\n' + original_ast, fontsize=20)
    # fig.tight_layout()
    # plt.axis('off')
    # plt.show()
    pos = nx.spring_layout(G)

    # draw the graph
    nx.draw_networkx_nodes(G, pos, node_size=1000,
                           node_color='white', edgecolors='black')
    nx.draw_networkx_edges(G, pos, arrowsize=20, edge_color='black')
    nx.draw_networkx_labels(G, pos, labels, font_size=12)

    # show the graph
    plt.axis('off')
    plt.show()


if GRAPH:
    graph_ast(ast, original)

# TODO show the text representation of the tree to the professor


'''
REFERENCES:
https://stackoverflow.com/questions/29586520/can-one-get-hierarchical-graphs-from-networkx-with-python-3/76215030#76215030
https://github.com/dabeaz/ply

'''
