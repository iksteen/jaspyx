from jaspyx.ast_util import ast_load, ast_call
from jaspyx.visitor import BaseVisitor


class PrintToConsole(BaseVisitor):
    def visit_Print(self, node):
        log = ast_load('window.console.log')
        self.visit(ast_call(log, *node.values))
