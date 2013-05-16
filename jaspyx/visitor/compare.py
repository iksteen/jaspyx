from jaspyx.visitor import BaseVisitor


class Compare(BaseVisitor):
    def visit_Compare(self, node):
        if len(node.ops) > 1:
            self.output('(')
        first = True
        left = node.left
        for op, comparator in zip(node.ops, node.comparators):
            if not first:
                self.output(' && ')
            else:
                first = False
            self.group([left, op, comparator])
            left = comparator
        if len(node.ops) > 1:
            self.output(')')
