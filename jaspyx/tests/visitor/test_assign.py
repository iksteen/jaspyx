import ast
from nose.tools import raises
from jaspyx.ast_util import ast_store, ast_load, ast_call
from jaspyx.tests.visitor.v8_helper import V8Helper


class TestAssignSingleTarget(V8Helper):
    def test_single_assign(self):
        assert self.run(
            [
                ast.Assign(
                    [ast_store('test')],
                    ast.Str('test'))
            ],
            'test'
        ) == 'test'

    def test_multi_assign(self):
        assert self.run(
            [
                ast.Assign(
                    [
                        ast_store('test1'),
                        ast_store('test2')
                    ],
                    ast.Str('test')
                )
            ],
            'test1 + "+" + test2'
        ) == 'test+test'

    @raises(Exception)
    def test_assign_multiple_slice(self):
        self.v.visit(
            ast.Assign(
                [
                    ast.Subscript(
                        ast_load('foo'),
                        ast.Slice(),
                        ast.Store()
                    ),
                    ast_store('bar'),
                ],
                ast.Str('test')
            )
        )

    def _slice_assign(self, start, end):
        result = self.run(
            [
                ast.Assign(
                    [ast_store('test')],
                    ast.List([ast.Num(x) for x in range(10)], ast.Load())
                ),
                ast.Assign(
                    [
                        ast.Subscript(
                            ast_load('test'),
                            ast.Slice(start and ast.Num(start), end and ast.Num(end), None),
                            ast.Store()
                        ),
                    ],
                    ast.List([ast.Num(42), ast.Num(43)], ast.Load())
                ),
            ],
            'test',
            list
        )
        return result

    def test_assign_slice_full(self):
        assert self._slice_assign(None, None) == [42, 43]

    def test_assign_slice_start(self):
        assert self._slice_assign(5, None) == [0, 1, 2, 3, 4, 42, 43]

    def test_assign_slice_neg_start(self):
        assert self._slice_assign(-6, None) == [0, 1, 2, 3, 42, 43]

    def test_assign_slice_end(self):
        assert self._slice_assign(None, 5) == [42, 43, 5, 6, 7, 8, 9]

    def test_assign_slice_neg_end(self):
        assert self._slice_assign(None, -1) == [42, 43, 9]

    def test_assign_slice_start_end(self):
        assert self._slice_assign(2, 8) == [0, 1, 42, 43, 8, 9]

    def test_assign_slice_neg_start_end(self):
        assert self._slice_assign(-8, 8) == [0, 1, 42, 43, 8, 9]

    def test_assign_slice_neg_start_neg_end(self):
        assert self._slice_assign(-8, -2) == [0, 1, 42, 43, 8, 9]

    def test_assign_expr_slice(self):
        assert self.run(
            [
                ast.Assign(
                    [ast_store('test')],
                    ast.List([ast.Num(x) for x in range(10)], ast.Load())
                ),
                ast.FunctionDef(
                    'f_test',
                    ast.arguments([], None, None, []),
                    [
                        ast.Return(ast_load('test')),
                    ],
                    []
                ),
                ast.Assign(
                    [
                        ast.Subscript(
                            ast_call(ast_load('f_test')),
                            ast.Slice(ast.Num(2), ast.Num(8), None),
                            ast.Store()
                        ),
                    ],
                    ast.List([ast.Num(42), ast.Num(43)], ast.Load())
                ),
            ],
            'test',
            list
        ) == [0, 1, 42, 43, 8, 9]

    @raises(Exception)
    def test_destructure(self):
        assert self.run(
            [
                ast.Assign(
                    [
                        ast.List(
                            [
                                ast_store('test1'),
                                ast_store('test2'),
                            ],
                            ast.Store()
                        )
                    ],
                    ast.List(
                        [
                            ast.Str('test'),
                            ast.Str('test'),
                        ],
                        ast.Load()
                    )
                )
            ],
            'test1 + "+" + test2'
        ) == 'test+test'
