from jaspyx.visitor import BaseVisitor


class Subscript(BaseVisitor):
    def visit_Subscript(self, node):
        self.visit(node.value)
        self.visit(node.slice)

    def visit_Index(self, node):
        self.output('[')
        self.visit(node.value)
        self.output(']')

    def visit_Slice(self, node):
        self.output('.slice(')
        if node.lower is None:
            self.output('0')
        else:
            self.visit(node.lower)
        if node.upper is not None:
            self.output(', ')
            self.visit(node.upper)
        self.output(')')
