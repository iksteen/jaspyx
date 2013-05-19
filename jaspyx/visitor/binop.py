import _ast
from jaspyx.ast_util import ast_load, ast_call
from jaspyx.visitor import BaseVisitor


class BinOp(BaseVisitor):
    def visit_BinOp(self, node):
        attr = getattr(self, 'BinOp_%s' % node.op.__class__.__name__, None)
        attr(node.left, node.right)

    for key, value in {
        'Add': '+',
        'Sub': '-',
        'Mult': '*',
        'Div': '/',
        'Mod': '%',
        'BitAnd': '&',
        'BitOr': '|',
        'BitXor': '^',
        'LShift': '<<',
        'RShift': '>>>',
    }.items():
        def gen_op(op):
            def f_op(self, left, right):
                self.group([left, op, right])
            return f_op
        exec 'BinOp_%s = gen_op("%s")' % (key, value)

    def BinOp_Pow(self, left, right):
        pow_func = ast_load('Math.pow')
        self.visit(ast_call(pow_func, left, right))

    def BinOp_FloorDiv(self, left, right):
        floor = ast_load('Math.floor')
        self.visit(ast_call(floor, _ast.BinOp(left, _ast.Div(), right)))
