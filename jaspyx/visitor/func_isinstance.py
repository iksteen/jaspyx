from jaspyx.visitor import BaseVisitor


class FuncIsinstance(BaseVisitor):
    def func_isinstance(self, obj, type_):
        self.output('(')
        self.visit(obj)
        self.output(' instanceof ')
        self.visit(type_)
        self.output(')')
