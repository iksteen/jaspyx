import ast
from nose.tools import raises
from jaspyx.ast_util import ast_load, ast_store
from jaspyx.tests.visitor.v8_helper import V8Helper


class TestCall(V8Helper):
    @raises(Exception)
    def test_keywords(self):
        assert self.run(
            [
                ast.Expr(
                    ast.Call(
                        ast_load('alert'),
                        [],
                        {
                            'a': ast.Num(0)
                        },
                        None,
                        None
                    )
                )
            ],
            None,
            int
        ) == 0

    @raises(Exception)
    def test_kwargs(self):
        assert self.run(
            [
                ast.Assign(
                    [ast_store('a')],
                    ast.Dict(
                        [
                            ast.Str('a'),
                        ],
                        [
                            ast.Num(0),
                        ]
                    )
                ),
                ast.Expr(
                    ast.Call(
                        ast_load('alert'),
                        [],
                        {},
                        None,
                        ast_load('a')
                    )
                )
            ],
            None,
            int
        ) == 0

    def test_call(self):
        assert self.run(
            [
                ast.FunctionDef(
                    'test',
                    ast.arguments(
                        [
                            ast_store('a'),
                            ast_store('b'),
                        ],
                        None,
                        None,
                        []
                    ),
                    [
                        ast.Return(
                            ast.BinOp(
                                ast_load('a'),
                                ast.Mult(),
                                ast_load('b')
                            )
                        )
                    ],
                    []
                ),
                ast.Expr(
                    ast.Call(
                        ast_load('test'),
                        [
                            ast.Num(6),
                            ast.Num(7),
                        ],
                        {},
                        None,
                        None
                    )
                )
            ],
            None,
            int
        ) == 42

    def test_starargs(self):
        assert self.run(
            [
                ast.FunctionDef(
                    'test',
                    ast.arguments(
                        [
                            ast_store('a'),
                            ast_store('b'),
                        ],
                        None,
                        None,
                        []
                    ),
                    [
                        ast.Return(
                            ast.BinOp(
                                ast_load('a'),
                                ast.Mult(),
                                ast_load('b')
                            )
                        )
                    ],
                    []
                ),
                ast.Assign(
                    [ast_store('a')],
                    ast.List(
                        [
                            ast.Num(6),
                            ast.Num(7),
                        ],
                        ast.Load()
                    )
                ),
                ast.Expr(
                    ast.Call(
                        ast_load('test'),
                        [],
                        {},
                        ast_load('a'),
                        None
                    )
                )
            ],
            None,
            int
        ) == 42

    def test_args_starargs(self):
        assert self.run(
            [
                ast.FunctionDef(
                    'test',
                    ast.arguments(
                        [
                            ast_store('a'),
                            ast_store('b'),
                        ],
                        None,
                        None,
                        []
                    ),
                    [
                        ast.Return(
                            ast.BinOp(
                                ast_load('a'),
                                ast.Mult(),
                                ast_load('b')
                            )
                        )
                    ],
                    []
                ),
                ast.Assign(
                    [ast_store('a')],
                    ast.List(
                        [
                            ast.Num(7),
                        ],
                        ast.Load()
                    )
                ),
                ast.Expr(
                    ast.Call(
                        ast_load('test'),
                        [
                            ast.Num(6),
                        ],
                        {},
                        ast_load('a'),
                        None
                    )
                )
            ],
            None,
            int
        ) == 42

    def test_starargs_context(self):
        assert self.run(
            [
                ast.Assign(
                    [ast_store('o')],
                    ast.Dict(
                        [ast.Str('a'), ],
                        [ast.Num(6), ]
                    )
                ),
                ast.Assign(
                    [ast_store('o.f')],
                    ast.FunctionDef(
                        '',
                        ast.arguments(
                            [
                                ast_store('a'),
                            ],
                            None,
                            None,
                            []
                        ),
                        [
                            ast.Return(
                                ast.BinOp(
                                    ast_load('this.a'),
                                    ast.Mult(),
                                    ast_load('a')
                                )
                            )
                        ],
                        []
                    ),
                ),
                ast.Assign(
                    [ast_store('a')],
                    ast.List(
                        [
                            ast.Num(7),
                        ],
                        ast.Load()
                    )
                ),
                ast.Expr(
                    ast.Call(
                        ast_load('o.f'),
                        [],
                        {},
                        ast_load('a'),
                        None
                    )
                )
            ],
            None,
            int
        ) == 42

    def test_starargs_no_context(self):
        assert self.run(
            [
                ast.FunctionDef(
                    'test',
                    ast.arguments(
                        [
                            ast_store('a'),
                        ],
                        None,
                        None,
                        []
                    ),
                    [
                        ast.Return(
                            ast.BinOp(
                                ast_load('this.o'),
                                ast.Mult(),
                                ast_load('a')
                            )
                        )
                    ],
                    []
                ),
                ast.Assign(
                    [ast_store('o')],
                    ast.Num(6)
                ),
                ast.Assign(
                    [ast_store('a')],
                    ast.List(
                        [
                            ast.Num(7),
                        ],
                        ast.Load()
                    )
                ),
                ast.Expr(
                    ast.Call(
                        ast_load('test'),
                        [],
                        {},
                        ast_load('a'),
                        None
                    )
                )
            ],
            None,
            int
        ) == 42
