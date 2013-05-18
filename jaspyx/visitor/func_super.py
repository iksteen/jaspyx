import ast
from jaspyx.ast_util import ast_call, ast_load
from jaspyx.visitor import BaseVisitor


class FuncSuper(BaseVisitor):
    def func_super(self, type_):
        self.visit(
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
            )

        )
