from jaspyx.ast_util import ast_load, ast_call
from jaspyx.visitor import BaseVisitor


class PrintToConsole(BaseVisitor):
    def visit_Print(self, node):
        self.indent()
        self.visit(
            ast_call(
                ast_load('console.log'),
                *node.values
            )
        )
        self.finish()
