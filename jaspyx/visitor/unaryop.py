import _ast
from jaspyx.visitor import BaseVisitor


class UnaryOp(BaseVisitor):
    def visit_UnaryOp(self, node):
        attr = getattr(self, 'visit_UnaryOp_%s' % node.op.__class__.__name__, None)
        if attr is None:
            self.group([node.op, node.operand], infix='')
        else:
            attr(node.op, node.operand)

    def visit_UnaryOp_Invert(self, op, operand):
        self.visit(
            _ast.UnaryOp(
                _ast.USub(),
                _ast.BinOp(
                    operand,
                    _ast.Add(),
                    _ast.Num(1)
                ),
            )
        )
