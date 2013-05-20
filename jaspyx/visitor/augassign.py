import _ast
from jaspyx.visitor import BaseVisitor


class AugAssign(BaseVisitor):
    def visit_AugAssign(self, node):
        attr = getattr(self, 'AugAssign_%s' % node.op.__class__.__name__, None)
        if attr is None:
            # Rewrite the expression as an assignment using a BinOp
            self.visit(_ast.Assign(
                [node.target],
                _ast.BinOp(
                    _ast.Name(node.target.id, _ast.Load()),
                    node.op,
                    node.value
                )
            ))
        else:
            attr(node.target, node.value)

    for key, value in {
        'Add': ' += ',
        'Sub': ' -= ',
        'Mult': ' *= ',
        'Div': ' /= ',
        'Mod': ' %= ',
        'BitAnd': ' &= ',
        'BitOr': ' |= ',
        'BitXor': ' ^= ',
    }.items():
        def gen_op(op):
            def f_op(self, target, value):
                self.indent()
                self.group(
                    [target, value],
                    prefix='',
                    infix=op,
                    suffix='',
                )
                self.finish()
            return f_op
        exec 'AugAssign_%s = gen_op("%s")' % (key, value)
