import ast
from jaspyx.ast_util import ast_call, ast_load, ast_store
from jaspyx.visitor import BaseVisitor


class FuncSuper(BaseVisitor):
    def func_super(self, type_, inst):
        self.visit(
            ast_call(
                ast.FunctionDef(
                    '',
                    ast.arguments([ast_store('p'), ast_store('i')], None, None, []),
                    [
                        ast.FunctionDef(
                            'tmp',
                            ast.arguments([], None, None, []),
                            [
                                ast.Expr(
                                    ast_call(
                                        ast_load('this.__bind__'),
                                        ast_load('i')
                                    )
                                ),
                            ],
                            []
                        ),
                        ast.Assign(
                            [ast_load('tmp.prototype')],
                            ast_load('p')
                        ),
                        ast.Return(
                            ast_call(
                                ast_load('new'),
                                ast_load('tmp'),
                            )
                        )
                    ],
                    []
                ),
                ast.Attribute(
                    ast.Subscript(
                        ast_load('self.__mro__'),
                        ast.Index(
                            ast.BinOp(
                                ast_call(
                                    ast_load('self.__mro__.indexOf'),
                                    type_,
                                ),
                                ast.Sub(),
                                ast.Num(1)
                            )
                        ),
                        ast.Load()
                    ),
                    'prototype',
                    ast.Load()
                ),
                inst,
            )
        )
