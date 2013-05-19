import _ast
from jaspyx.builtins import BUILTINS
from jaspyx.visitor import BaseVisitor


class Variable(BaseVisitor):
    def visit_Name(self, node):
        scope = self.stack[-1].scope

        if isinstance(node.ctx, _ast.Store):
            if scope.is_global(node.id):
                self.output('__module__.' + node.id)
            else:
                scope.declare(node.id)
                self.output(scope.prefixed(node.id))
        elif isinstance(node.ctx, _ast.Load):
            if scope.is_global(node.id):
                self.output('__module__.' + node.id)
            else:
                var_scope = scope.get_scope(node.id)
                if var_scope is not None:
                    self.output(var_scope.prefixed(node.id))
                else:
                    self.output(BUILTINS.get(node.id, node.id))
        else:
            raise NotImplementedError('name lookup not implemented for context %s' % node.ctx.__class__.__name__)
