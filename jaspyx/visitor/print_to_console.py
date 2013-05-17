from jaspyx.ast_util import ast_load, ast_call
from jaspyx.visitor import BaseVisitor


class PrintToConsole(BaseVisitor):
    def visit_Print(self, node):
        self.indent()
        log = ast_load('console.log')
        self.visit(ast_call(log, *node.values))
        self.finish()
