import json
from jaspyx.visitor import BaseVisitor


class Types(BaseVisitor):
    def visit_Num(self, node):
        self.output(json.dumps(node.n))

    def visit_Str(self, node):
        self.output(json.dumps(node.s))

    def visit_List(self, node):
        self.group(node.elts, prefix='[', infix=', ', suffix=']')

    visit_Tuple = visit_List
