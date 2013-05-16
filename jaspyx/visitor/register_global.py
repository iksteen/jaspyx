from jaspyx.visitor import BaseVisitor


class RegisterGlobal(BaseVisitor):
    def visit_Global(self, node):
        for name in node.names:
            self.stack[-1].scope.declare_global(name)
