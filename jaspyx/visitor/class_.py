import ast
import _ast
from jaspyx.ast_util import ast_load, ast_call, ast_store
from jaspyx.visitor import BaseVisitor


class Class(BaseVisitor):
    def visit_ClassDef(self, node):
        if len(node.bases) > 1:
            raise Exception('Multiple inheritance not supported')
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
                ast.Assign(
                    [ast_store('this.__class__')],
                    ast_load('arguments.callee')
                ),
                ast.For(
                    ast_store('i'),
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
                            ast_load('this.__init__'),
                        ),
                        [ast.IsNot()],
                        [ast.Str('undefined')],
                    ),
                    [
                        ast.Expr(
                            ast_call(
                                ast_load('this.__init__.apply'),
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

        if not node.bases:
            self.visit(
                ast.Assign(
                    [ast_store(node.name, 'prototype')],
                    ast.Dict(
                        [
                            ast.Str('constructor'),
                            ast.Str('__mro__')
                        ],
                        [
                            ast_load(node.name),
                            ast.List([ast_load(node.name)], ast.Load())
                        ]
                    )
                )
            )
        else:
            base = node.bases[0]
            tmp = self.stack[-1].scope.alloc_temp()
            self.visit(
                ast.Assign(
                    [ast_store(node.name, 'prototype')],
                    ast_call(
                        ast.FunctionDef(
                            '',
                            ast.arguments([], None, None, []),
                            [
                                ast.Assign(
                                    [ast_store(tmp)],
                                    ast.FunctionDef(
                                        '',
                                        ast.arguments([], None, None, []),
                                        [],
                                        []
                                    )
                                ),
                                ast.Assign(
                                    [ast_store(tmp, 'prototype')],
                                    ast_load(base.id, 'prototype'),
                                ),
                                ast.Return(
                                    ast_call(
                                        ast_load('new'),
                                        ast_load(tmp),
                                    )
                                )
                            ],
                            []
                        ),
                    )
                )
            )
            self.visit(
                ast.Assign(
                    [ast_store(node.name, 'prototype.constructor')],
                    ast_load(node.name)
                )
            )
            self.visit(
                ast.Assign(
                    [ast_store(node.name, 'prototype.__base__')],
                    base,
                )
            )
            self.visit(
                ast.Assign(
                    [ast_store(node.name, 'prototype.__mro__')],
                    ast_call(
                        ast_load(node.name, 'prototype.__mro__.concat'),
                        ast_load(node.name),
                    )
                )
            )

        for stmt in node.body:
            if isinstance(stmt, _ast.FunctionDef):
                self.visit(
                    ast.Assign(
                        [ast_store(node.name, 'prototype', stmt.name)],
                        ast.FunctionDef(
                            '',
                            stmt.args,
                            stmt.body,
                            stmt.decorator_list
                        )
                    )
                )
            elif isinstance(stmt, _ast.Assign):
                targets = []
                for target in stmt.targets:
                    if not isinstance(target, _ast.Name):
                        raise Exception('Indirect assignment not supported in class definition')
                    targets.append(ast_store(node.name, 'prototype', target.id))
                self.visit(ast.Assign(
                    targets,
                    stmt.value
                ))
