from jaspyx.visitor import BaseVisitor


class Continue(BaseVisitor):
    def visit_Continue(self, node):
        self.indent()
        self.output('continue')
        self.finish()
