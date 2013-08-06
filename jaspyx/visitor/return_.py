from jaspyx.visitor import BaseVisitor


class Return(BaseVisitor):
    def visit_Return(self, node):
        self.indent()
        if node.value is not None:
            self.output('return ')
            self.visit(node.value)
        else:
            self.output('return')
        self.finish()
