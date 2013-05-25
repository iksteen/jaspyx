import ast
from jaspyx.ast_util import ast_call, ast_load
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

    def CmpOp_In(self, left, comparator):
        self.visit(ast_call(
            ast.FunctionDef(
                '',
                ast.arguments([ast_load('l'), ast_load('c')], None, None, []),
                [
                    ast.Return(
                        ast.IfExp(
                            ast_call(
                                ast_load('Array.isArray'),
                                ast_load('c'),
                            ),
                            ast.Compare(
                                ast_call(
                                    ast_load('Array.prototype.indexOf.call'),
                                    ast_load('c'),
                                    ast_load('l'),
                                ),
                                [ast.Gt()],
                                [ast.Num(-1)]
                            ),
                            ast_call(
                                ast_load('JS'),
                                ast.Str("l in c"),
                            )
                        )
                    )
                ],
                []
            ),
            left,
            comparator
        ))

    def CmpOp_NotIn(self, left, comparator):
        self.visit(
            ast.UnaryOp(
                ast.Not(),
                ast.Compare(
                    left,
                    [ast.In()],
                    [comparator]
                )
            )
        )