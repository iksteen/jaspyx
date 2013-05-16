from jaspyx.context.block import BlockContext
from jaspyx.visitor import BaseVisitor


class IfElse(BaseVisitor):
    def visit_If(self, node):
        self.indent()
        self.output('if(')
        self.visit(node.test)
        self.output(') ')

        self.block(node.body, context=BlockContext(self.stack[-1]))

        if node.orelse:
            self.output(' else ')
            self.block(node.orelse, context=BlockContext(self.stack[-1]))

        self.output('\n')
