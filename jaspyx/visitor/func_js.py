import _ast
from jaspyx.visitor import BaseVisitor


class FuncJS(BaseVisitor):
    def func_JS(self, arg):
        if not isinstance(arg, _ast.Str):
            raise Exception('JS() expects a string argument')
        self.output(arg.s)
