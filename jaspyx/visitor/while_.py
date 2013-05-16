from jaspyx.context.block import BlockContext
from jaspyx.visitor import BaseVisitor


class While(BaseVisitor):
    def visit_While(self, node):
        self.indent()
        self.output('while(')
        self.visit(node.test)
        self.output(') ')
        self.block(node.body, context=BlockContext(self.stack[-1]))
        self.output('\n')
