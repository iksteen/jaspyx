import _ast
from jaspyx.visitor import BaseVisitor


class AugAssign(BaseVisitor):
    def visit_AugAssign(self, node):
        attr = getattr(self, 'visit_AugAssign_%s' % node.op.__class__.__name__, None)
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
            attr(node.target, node.op, node.value)

    def visit_AugAssign__op(self, target, op, value):
        self.visit(target)
        self.output(' ')
        self.visit(op)
        self.output('= ')
        self.visit(value)

    visit_AugAssign_Add = visit_AugAssign__op
    visit_AugAssign_Sub = visit_AugAssign__op
    visit_AugAssign_Mult = visit_AugAssign__op
    visit_AugAssign_Div = visit_AugAssign__op
    visit_AugAssign_Mod = visit_AugAssign__op
    visit_AugAssign_BitAnd = visit_AugAssign__op
    visit_AugAssign_BitOr = visit_AugAssign__op
    visit_AugAssign_BitXor = visit_AugAssign__op
