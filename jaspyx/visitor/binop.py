import _ast
from jaspyx.ast_util import ast_load, ast_call
from jaspyx.visitor import BaseVisitor


class BinOp(BaseVisitor):
    def visit_BinOp(self, node):
        attr = getattr(self, 'visit_BinOp_%s' % node.op.__class__.__name__, None)
        if attr is None:
            self.group([node.left, node.op, node.right])
        else:
            attr(node.op, node.left, node.right)

    def visit_BinOp_Pow(self, node, left, right):
        pow_func = ast_load('Math.pow')
        self.visit(ast_call(pow_func, left, right))

    def visit_BinOp_FloorDiv(self, node, left, right):
        floor = ast_load('Math.floor')
        self.visit(ast_call(floor, _ast.BinOp(left, _ast.Div(), right)))
