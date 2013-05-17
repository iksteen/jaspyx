import ast
import _ast
from jaspyx.ast_util import ast_load, ast_call
from jaspyx.visitor import BaseVisitor


class Class(BaseVisitor):
    def visit_ClassDef(self, node):
        if node.bases:
            raise Exception('Inheritance not supported')
        if node.decorator_list:
            raise Exception('Decorators not supported')

        self.visit(ast.FunctionDef(
            node.name,
            ast.arguments([], None, None, []),
            [
                ast.If(
                    ast.UnaryOp(
                        ast.Not(),
                        ast_call(
                            ast_load('isinstance'),
                            ast_load('this'),
                            ast_load('arguments.callee'),
                        )
                    ),
                    [
                        ast.Return(
                            ast_call(
                                ast_load('new'),
                                ast_load('arguments.callee'),
                                ast_load('this'),
                                ast_load('arguments'),
                            )
                        )
                    ],
                    []
                ),
                ast.For(
                    ast.Name('i', ast.Store()),
                    ast_load('this'),
                    [
                        ast.If(
                            ast.Compare(
                                ast_call(
                                    ast_load('type'),
                                    ast.Subscript(
                                        ast_load('this'),
                                        ast.Index(ast_load('i')),
                                        ast.Load(),
                                    )
                                ),
                                [ast.Is()],
                                [ast.Str('function')]
                            ),
                            [
                                ast.Assign(
                                    [ast.Subscript(
                                        ast_load('this'),
                                        ast.Index(ast_load('i')),
                                        ast.Store(),
                                    )],
                                    ast_call(
                                        ast.Attribute(
                                            ast.Subscript(
                                                ast_load('this'),
                                                ast.Index(ast_load('i')),
                                                ast.Load(),
                                            ),
                                            'bind',
                                            ast.Load(),
                                        ),
                                        ast_load('this'),
                                        ast_load('this'),
                                    )
                                ),
                            ],
                            []
                        )
                    ],
                    []
                ),
                ast.If(
                    ast.Compare(
                        ast_call(
                            ast_load('type'),
                            ast.Attribute(
                                ast_load('this'),
                                '__init__',
                                ast.Load(),
                            )
                        ),
                        [ast.IsNot()],
                        [ast.Str('undefined')],
                    ),
                    [
                        ast.Expr(
                            ast_call(
                                ast.Attribute(
                                    ast.Attribute(
                                        ast_load('this'),
                                        '__init__',
                                        ast.Load()
                                    ),
                                    'apply',
                                    ast.Load(),
                                ),
                                ast_load('this'),
                                ast_load('arguments'),
                            )
                        ),
                    ],
                    []
                )
            ],
            []
        ))

        for stmt in node.body:
            if isinstance(stmt, _ast.FunctionDef):
                self.indent()
                self.visit(
                    _ast.Attribute(
                        _ast.Attribute(
                            ast_load(node.name),
                            'prototype',
                            ast.Load(),
                        ),
                        stmt.name,
                        ast.Store()
                    )
                )
                self.output(' = ')
                self.visit(
                    ast.FunctionDef(
                        '',
                        stmt.args,
                        stmt.body,
                        stmt.decorator_list
                    )
                )
                self.output(';\n')
            elif isinstance(stmt, _ast.Assign):
                self.indent()
                for target in stmt.targets:
                    if not isinstance(target, _ast.Name):
                        raise Exception('Indirect assignment not supported in class definition')
                    self.visit(
                        _ast.Attribute(
                            _ast.Attribute(
                                ast_load(node.name),
                                'prototype',
                                ast.Load()
                            ),
                            target.id,
                            ast.Store()
                        )
                    )
                    self.output(' = ')
                self.visit(stmt.value)
                self.output(';\n')
