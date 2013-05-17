from jaspyx.context.block import BlockContext
from jaspyx.visitor import BaseVisitor


class For(BaseVisitor):
    def visit_For(self, node):
        if node.orelse:
            raise Exception('for-else is not supported.')
        self.indent()
        self.output('for(')
        self.visit(node.target)
        self.output(' in ')
        self.visit(node.iter)
        self.output(') ')

        self.block(node.body, context=BlockContext(self.stack[-1]))

        self.output('\n')
