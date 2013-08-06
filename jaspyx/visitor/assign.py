import _ast
import ast
from jaspyx.ast_util import ast_call, ast_load, ast_store
from jaspyx.visitor import BaseVisitor


class Assign(BaseVisitor):
    def visit_Assign_Slice(self, target, value):
        args = []
        if target.slice.lower or target.slice.upper:
            args.append(target.slice.lower or ast.Num(0))
        if target.slice.upper:
            args.append(target.slice.upper)

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
                                ast_store('e'),
                            ], None, None, []
                        ),
                        [
                            ast.Assign(
                                [ast_store('s')],
                                ast.IfExp(
                                    ast.Compare(
                                        ast_call(
                                            ast_load('type'),
                                            ast_load('s')
                                        ),
                                        [ast.Eq()],
                                        [ast.Str('undefined')],
                                    ),
                                    ast.Num(0),
                                    ast.IfExp(
                                        ast.Compare(
                                            ast_load('s'),
                                            [ast.Lt()],
                                            [ast.Num(0)],
                                        ),
                                        ast.BinOp(
                                            ast_load('s'),
                                            ast.Add(),
                                            ast_load('t.length')
                                        ),
                                        ast_load('s')
                                    )
                                )
                            ),
                            ast.Assign(
                                [ast_store('e')],
                                ast.IfExp(
                                    ast.Compare(
                                        ast_call(
                                            ast_load('type'),
                                            ast_load('e')
                                        ),
                                        [ast.Eq()],
                                        [ast.Str('undefined')],
                                    ),
                                    ast_load('t.length'),
                                    ast.IfExp(
                                        ast.Compare(
                                            ast_load('e'),
                                            [ast.Lt()],
                                            [ast.Num(0)],
                                        ),
                                        ast.BinOp(
                                            ast_load('e'),
                                            ast.Add(),
                                            ast_load('t.length')
                                        ),
                                        ast_load('e')
                                    )
                                )
                            ),
                            ast.Expr(
                                ast_call(
                                    ast_load('Array.prototype.splice.apply'),
                                    ast_load('t'),
                                    ast_call(
                                        ast.Attribute(
                                            ast.List([
                                                ast_load('s'),
                                                ast.BinOp(
                                                    ast_load('e'),
                                                    ast.Sub(),
                                                    ast_load('s')
                                                ),
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
                    *args
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

        for target in node.targets:
            if isinstance(target, _ast.List) or isinstance(target, _ast.Tuple):
                raise Exception('Destructuring assignment not supported.')

        self.indent()
        self.group(node.targets, prefix='', infix=' = ', suffix='')
        self.output(' = ')
        self.visit(node.value)
        self.finish()
