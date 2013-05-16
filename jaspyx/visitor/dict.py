import _ast
from jaspyx.context.block import BlockContext
from jaspyx.visitor import BaseVisitor


class Dict(BaseVisitor):
    def visit_Dict(self, node):
        self.push(context=BlockContext(self.stack[-1]))
        first = True
        for key, value in zip(node.keys, node.values):
            if not isinstance(key, _ast.Str) and \
                    not isinstance(key, _ast.Num):
                raise Exception('Dictionary keys can only be variables, strings or numbers')
            if not first:
                self.output(',\n')
            else:
                first = False
            self.indent()
            self.visit(key)
            self.output(': ')
            self.visit(value)
        self.output('\n')
        self.pop()
