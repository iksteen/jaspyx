import _ast
import ast
from jaspyx.ast_util import ast_call, ast_load, ast_store
from jaspyx.visitor import BaseVisitor


class Assign(BaseVisitor):
    def visit_Assign_Slice(self, target, value):
        lower = target.slice.lower or _ast.Num(0)
        upper = target.slice.upper or _ast.Attribute(target.value, 'length', _ast.Load())
        length = _ast.BinOp(upper, _ast.Sub(), lower)

        self.visit(
            ast.Expr(
                ast_call(
                    ast.FunctionDef(
                        '',
                        ast.arguments(
                            [
                                ast_store('t'),
                                ast_store('v'),
                                ast_store('s'),
                                ast_store('l'),
                            ], None, None, []
                        ),
                        [
                            ast.If(
                                ast.Compare(
                                    ast_load('l'),
                                    [ast.Lt()],
                                    [ast.Num(0)]
                                ),
                                [
                                    ast.AugAssign(
                                        ast_load('l'),
                                        ast.Add(),
                                        ast_load('t.length')
                                    ),
                                ],
                                []
                            ),
                            ast.Expr(
                                ast_call(
                                    ast_load('Array.prototype.splice.apply'),
                                    ast_load('t'),
                                    ast_call(
                                        ast.Attribute(
                                            ast.List([
                                                ast_load('s'),
                                                ast_load('l'),
                                            ], ast.Load()),
                                            'concat',
                                            ast.Load(),
                                        ),
                                        ast_load('v'),
                                    )
                                )
                            )
                        ],
                        []
                    ),
                    target.value,
                    value,
                    lower,
                    length,
                )
            )
        )

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
