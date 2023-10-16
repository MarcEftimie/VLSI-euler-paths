import sympy
import networkx as nx
from sympy import And, Or, Not
from sympy.abc import A, B, C


expr = And(A, B).simplify()

expr_complement = Not(expr).simplify()

expr = And(C, expr).simplify()

expr_complement = And(C, expr_complement).simplify()


print(expr)
print(expr_complement)

expr_complement_nots_removed = (
    expr_complement.subs(Not(A), A).subs(Not(B), B).subs(Not(C), C)
)

print(expr_complement_nots_removed)


# def boolean_complement(expr):
#     complement_expr = ~expr
#     return sympy.simplify_logic(complement_expr)


# a, b = sympy.symbols("a b")
# expr = a & b

# expr = sympy.simplify_logic(expr)

# expr_complement = boolean_complement(expr)


# print(expr.args)

# for term in expr.args:
#     print(term)

# # Create a graph representation of the expression
# G = nx.Graph()
# G.add_nodes_from([str(a)])
# for term in expr.args:
#     if isinstance(term, sympy.Symbol):
#         continue
#     elif isinstance(term, sympy.Not):
#         G.add_edge(str(term.args[0]), str(term))
#     else:
#         G.add_edge(str(term.args[0]), str(term.args[1]))

# print(G.edges())
