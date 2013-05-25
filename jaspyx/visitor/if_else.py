import _ast
from jaspyx.context.block import BlockContext
from jaspyx.visitor import BaseVisitor


class IfElse(BaseVisitor):
    def visit_If(self, node, skip_indent=False):
        if not skip_indent:
            self.indent()
        self.output('if(')
        self.visit(node.test)
        self.output(') ')

        self.block(node.body, context=BlockContext(self.stack[-1]))

        if node.orelse:
            self.output(' else ')
            if len(node.orelse) == 1 and isinstance(node.orelse[0], _ast.If):
                self.visit_If(node.orelse[0], True)
            else:
                self.block(node.orelse, context=BlockContext(self.stack[-1]))
                self.output('\n')
        else:
            self.output('\n')
