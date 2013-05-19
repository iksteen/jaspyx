import _ast
from jaspyx.visitor import BaseVisitor


class UnaryOp(BaseVisitor):
    def visit_UnaryOp(self, node):
        attr = getattr(self, 'UnaryOp_%s' % node.op.__class__.__name__)
        attr(node.operand)

    def UnaryOp_UAdd(self, operand):
        self.group(['+', operand], infix='')

    def UnaryOp_USub(self, operand):
        self.group(['-', operand], infix='')

    def UnaryOp_Not(self, operand):
        self.group(['!', operand], infix='')

    def UnaryOp_Invert(self, operand):
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
