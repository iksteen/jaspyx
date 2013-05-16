from jaspyx.visitor import BaseVisitor


class Attribute(BaseVisitor):
    def visit_Attribute(self, node):
        self.visit(node.value)
        self.output('.%s' % node.attr)
