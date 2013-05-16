from jaspyx.visitor import BaseVisitor


class FuncType(BaseVisitor):
    def func_type(self, arg):
        self.output('typeof ')
        self.visit(arg)
