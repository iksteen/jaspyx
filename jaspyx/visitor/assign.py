import _ast
from jaspyx.ast_util import ast_call, ast_load
from jaspyx.visitor import BaseVisitor


class Assign(BaseVisitor):
    def visit_Assign_Slice(self, target, value):
        lower = target.slice.lower or _ast.Num(0)
        upper = target.slice.upper or _ast.Attribute(target.value, 'length', _ast.Load())
        length = _ast.BinOp(upper, _ast.Sub(), lower)

        tmp = self.stack[-1].scope.alloc_temp()
        self.visit(
            _ast.Assign(
                [_ast.Name(tmp, _ast.Store())],
                length
            )
        )

        self.visit(
            _ast.If(
                _ast.Compare(
                    ast_load(tmp),
                    [_ast.Lt()],
                    [_ast.Num(0)]
                ),
                [
                    _ast.AugAssign(
                        _ast.Name(tmp, _ast.Store()),
                        _ast.Add(),
                        _ast.Attribute(target.value, 'length', _ast.Load()),
                    ),
                ],
                []
            )
        )

        arg_list = _ast.List([lower, ast_load(tmp)], _ast.Load())
        arg_list = ast_call(_ast.Attribute(arg_list, 'concat', _ast.Load()), value)
        apply_func = ast_load('Array.prototype.splice.apply')
        call = ast_call(apply_func, target.value, arg_list)

        self.indent()
        self.visit(call)
        self.finish()

    def visit_Assign(self, node):
        # Check for slice assignment
        for target in node.targets:
            if isinstance(target, _ast.Subscript) and \
                    isinstance(target.slice, _ast.Slice):
                if len(node.targets) > 1:
                    raise Exception('Slice assignment only supported when assignment has a single target')
                self.visit_Assign_Slice(target, node.value)
                return

        self.indent()
        for target in node.targets:
            self.visit(target)
        self.output(' = ')
        self.visit(node.value)
        self.finish()
