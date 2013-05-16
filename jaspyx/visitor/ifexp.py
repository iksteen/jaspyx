from jaspyx.visitor import BaseVisitor


class IfExp(BaseVisitor):
    def visit_IfExp(self, node):
        self.visit(node.test)
        self.output(' ? ')
        self.visit(node.body)
        self.output(' : ')
        self.visit(node.orelse)
