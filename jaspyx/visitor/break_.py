from jaspyx.visitor import BaseVisitor


class Break(BaseVisitor):
    def visit_Break(self, node):
        self.indent()
        self.output('break')
        self.finish()
