from jaspyx.ast_util import ast_call
from jaspyx.visitor import BaseVisitor


class FuncNew(BaseVisitor):
    def func_new(self, type_, *args):
        self.output('(new ')
        self.visit(ast_call(type_, *args))
        self.output(')')
