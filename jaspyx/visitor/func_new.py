from jaspyx.ast_util import ast_call, ast_load
from jaspyx.visitor import BaseVisitor


class FuncNew(BaseVisitor):
    def func_new(self, type_, *args):
        self.output('(new ')
        self.visit(ast_call(type_, ast_load('this'), *args))
        self.output(')')
