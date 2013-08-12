import ast
from jaspyx.ast_util import ast_call, ast_store, ast_load
from jaspyx.visitor import BaseVisitor


class ListComp(BaseVisitor):
    def visit_ListComp(self, node):
        body = [
            ast.Expr(
                ast_call(
                    ast_load('$$.push'),
                    node.elt
                )
            )
        ]

        for i, generator in reversed(zip(range(len(node.generators)), node.generators)):
            if not isinstance(generator.target, ast.Name):
                raise TypeError('dereferencing assignment not supported')

            if generator.ifs:
                if len(generator.ifs) > 1:
                    cond = ast.BoolOp(ast.And(), generator.ifs)
                else:
                    cond = generator.ifs[0]
                body = [
                    ast.If(
                        cond,
                        body,
                        []
                    )
                ]

            body = [
                ast.Assign(
                    [ast_store('$$' + generator.target.id)],
                    generator.iter
                ),
                ast.For(
                    ast_store('$' + generator.target.id),
                    ast_call(
                        ast_load('range'),
                        ast.Num(0),
                        ast.Attribute(
                            ast_load('$$' + generator.target.id),
                            'length',
                            ast.Load()
                        )
                    ),
                    [
                        ast.Assign(
                            [generator.target],
                            ast.Subscript(
                                ast_load('$$' + generator.target.id),
                                ast.Index(ast_load('$' + generator.target.id)),
                                ast.Load()
                            )
                        ),
                    ] + body,
                    []
                )
            ]

        self.visit(
            ast_call(
                ast.FunctionDef(
                    '',
                    ast.arguments(
                        [
                        ], None, None, []
                    ),
                    [
                        ast.Assign(
                            [
                                ast_store('$$')
                            ],
                            ast.List(
                                [],
                                ast.Load()
                            )
                        ),
                    ] + body + [
                        ast.Return(ast_load('$$')),
                    ],
                    []
                ),
            )
        )
