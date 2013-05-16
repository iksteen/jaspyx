from jaspyx.builtins import BUILTINS
from jaspyx.visitor import BaseVisitor


class Variable(BaseVisitor):
    def visit_Name(self, node):
        if self.stack[-1].scope.is_global(node.id):
            name = 'window.%s' % node.id
        else:
            name = BUILTINS.get(node.id, node.id)
            self.stack[-1].scope.reference(name)
        self.output(name)
