from jaspyx.visitor import BaseVisitor


class Return(BaseVisitor):
    def visit_Return(self, node):
        self.indent()
        self.output('return ')
        self.visit(node.value)
        self.finish()
