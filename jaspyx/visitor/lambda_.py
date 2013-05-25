import ast
from jaspyx.visitor import BaseVisitor


class Lambda(BaseVisitor):
    def visit_Lambda(self, node):
        self.visit(ast.FunctionDef(
            '',
            node.args,
            [ast.Return(node.body)],
            []
        ))
