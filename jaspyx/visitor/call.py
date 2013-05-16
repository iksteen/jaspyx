import _ast
from jaspyx.visitor import BaseVisitor


class Call(BaseVisitor):
    def visit_Call(self, node):
        if node.keywords:
            raise Exception('keyword arguments are not supported')
        if node.starargs is not None:
            raise Exception('starargs is not supported')
        if node.kwargs is not None:
            raise Exception('kwargs is not supported')

        if isinstance(node.func, _ast.Name):
            func = getattr(self, 'func_%s' % node.func.id, None)
            if func is not None:
                # noinspection PyCallingNonCallable
                return func(*node.args)

        self.visit(node.func)
        self.group(node.args, infix=', ')
