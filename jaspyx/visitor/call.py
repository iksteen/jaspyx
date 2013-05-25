import _ast
import ast
from jaspyx.ast_util import ast_load, ast_call
from jaspyx.visitor import BaseVisitor


class Call(BaseVisitor):
    def visit_Call(self, node):
        if node.keywords:
            raise Exception('keyword arguments are not supported')
        if node.kwargs is not None:
            raise Exception('kwargs is not supported')

        if isinstance(node.func, _ast.Name):
            func = getattr(self, 'func_%s' % node.func.id, None)
            if func is not None:
                # noinspection PyCallingNonCallable
                return func(*node.args)

        if not node.starargs:
            self.visit(node.func)
            self.group(node.args, infix=', ')
        else:
            # Rewrite the call without starargs using apply.
            if isinstance(node.func, _ast.Attribute):
                this = node.func.value
            else:
                this = ast_load('this')
            if not node.args:
                args = node.starargs
            else:
                args = ast_call(
                    ast.Attribute(
                        ast.List(node.args, ast.Load()),
                        'concat',
                        ast.Load()
                    ),
                    node.starargs
                )
            self.visit(
                ast_call(
                    ast.Attribute(
                        node.func,
                        'apply',
                        ast.Load()
                    ),
                    this,
                    args,
                )
            )
