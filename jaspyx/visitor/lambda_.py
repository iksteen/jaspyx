import _ast
from jaspyx.visitor import BaseVisitor


class Lambda(BaseVisitor):
    def visit_Lambda(self, node):
        self.visit(_ast.FunctionDef(
            '',
            node.args,
            [_ast.Return(node.body)],
            []
        ))
