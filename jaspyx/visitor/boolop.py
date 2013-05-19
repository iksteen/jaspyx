from jaspyx.visitor import BaseVisitor


class BoolOp(BaseVisitor):
    def visit_BoolOp(self, node):
        attr = getattr(self, 'BinOp_%s' % node.op.__class__.__name__, None)
        attr(node.left, node.right)

    def BoolOp_And(self, values):
        self.group(values, infix=' && ')

    def BoolOp_Or(self, values):
        self.group(values, infix=' || ')