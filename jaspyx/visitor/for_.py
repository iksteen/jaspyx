import _ast
import ast
from jaspyx.context.block import BlockContext
from jaspyx.visitor import BaseVisitor


class For(BaseVisitor):
    def visit_For(self, node):
        if node.orelse:
            raise Exception('for-else is not supported.')

        if isinstance(node.iter, _ast.Call) and isinstance(node.iter.func, _ast.Name) and \
                node.iter.func.id == 'range':
            if len(node.iter.args) == 1:
                start = ast.Num(0)
                stop = node.iter.args[0]
                step = ast.Num(1)
                cmp_op = ast.Lt()
            elif len(node.iter.args) == 2:
                start = node.iter.args[0]
                stop = node.iter.args[1]
                step = ast.Num(1)
                cmp_op = ast.Lt()
            elif len(node.iter.args) == 3:
                start = node.iter.args[0]
                stop = node.iter.args[1]
                step = node.iter.args[2]
                if not isinstance(step, _ast.Num):
                    raise Exception('range() only supports literal numeric step')
                if step.n >= 0:
                    cmp_op = ast.Lt()
                else:
                    cmp_op = ast.Gt()
            else:
                raise Exception('range() expects 1, 2 or 3 parameters')

            self.indent()
            self.output('for(')
            self.visit(node.target)
            self.output(' = ')
            self.visit(start)
            self.output('; ')
            self.visit(
                ast.Compare(
                    node.target,
                    [cmp_op],
                    [stop]
                )
            )
            self.output('; ')
            self.visit(node.target)
            self.output(' += ')
            self.visit(step)
            self.output(') ')
        else:
            self.indent()
            self.output('for(')
            self.visit(node.target)
            self.output(' in ')
            self.visit(node.iter)
            self.output(') ')

        self.block(node.body, context=BlockContext(self.stack[-1]))
        self.output('\n')
