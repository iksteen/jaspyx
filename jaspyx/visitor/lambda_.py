import _ast
from jaspyx.context.function import FunctionContext
from jaspyx.visitor import BaseVisitor


class Lambda(BaseVisitor):
    def visit_Lambda(self, node):
        args = [arg.id for arg in node.args.args]

        func = FunctionContext(self.stack[-1], '', args)
        self.block([_ast.Return(node.body)], context=func)
