from jaspyx.visitor import BaseVisitor


class BoolOp(BaseVisitor):
    def visit_BoolOp(self, node):
        attr = getattr(self, 'BoolOp_%s' % node.op.__class__.__name__)
        attr(node.values)

    def BoolOp_And(self, values):
        self.group(values, infix=' && ')

    def BoolOp_Or(self, values):
        self.group(values, infix=' || ')