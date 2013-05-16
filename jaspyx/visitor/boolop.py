from jaspyx.visitor import BaseVisitor


class BoolOp(BaseVisitor):
    def visit_BoolOp(self, node):
        self.group(node.values, infix_node=node.op)
