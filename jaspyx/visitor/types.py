import json


class Types(object):
    def visit_Num(self, node):
        self.output(json.dumps(node.n))

    def visit_Str(self, node):
        self.output(json.dumps(node.s))

    def visit_List(self, node):
        self.group(node.elts, prefix='[', infix=', ', suffix=']')
