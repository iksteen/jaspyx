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
            comp_op = getattr(self, 'CmpOp_%s' % op.__class__.__name__)
            comp_op(left, comparator)
            left = comparator
        if len(node.ops) > 1:
            self.output(')')

    for key, value in {
        'Eq': '==',
        'NotEq': '!=',
        'Lt': '<',
        'LtE': '<=',
        'Gt': '>',
        'GtE': '>=',
        'Is': '===',
        'IsNot': '!==',
    }.items():
        def gen_op(op):
            def f_op(self, left, comparator):
                self.group([left, op, comparator])
            return f_op
        exec 'CmpOp_%s = gen_op("%s")' % (key, value)
