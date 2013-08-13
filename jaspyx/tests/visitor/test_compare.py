import ast
from jaspyx.tests.visitor.v8_helper import V8Helper


class TestCompare(V8Helper):
    def test_single_op(self):
        assert self.run(
            [
                ast.Compare(
                    ast.Num(1),
                    [ast.Lt()],
                    [ast.Num(2)]
                ),
            ],
            None,
            bool
        ) is True

    def test_multi_op(self):
        assert self.run(
            [
                ast.Compare(
                    ast.Num(1),
                    [ast.Lt(), ast.Gt()],
                    [ast.Num(3), ast.Num(2)]
                ),
            ],
            None,
            bool
        ) is True

    def test_multi_in_array(self):
        assert self.run(
            [
                ast.Compare(
                    ast.Num(1),
                    [ast.In()],
                    [ast.List([
                        ast.Num(1),
                        ast.Num(2),
                        ast.Num(3),
                    ], ast.Load())]
                ),
            ],
            None,
            bool
        ) is True

    def test_multi_not_in_array(self):
        assert self.run(
            [
                ast.Compare(
                    ast.Num(4),
                    [ast.NotIn()],
                    [ast.List([
                        ast.Num(1),
                        ast.Num(2),
                        ast.Num(3),
                    ], ast.Load())]
                ),
            ],
            None,
            bool
        ) is True

    def test_multi_in_dict(self):
        assert self.run(
            [
                ast.Compare(
                    ast.Str('a'),
                    [ast.In()],
                    [ast.Dict(
                        [
                            ast.Str('a'),
                            ast.Str('b'),
                            ast.Str('c'),
                        ],
                        [
                            ast.Num(1),
                            ast.Num(2),
                            ast.Num(3),
                        ]
                    )]
                ),
            ],
            None,
            bool
        ) is True

    def test_multi_not_in_dict(self):
        assert self.run(
            [
                ast.Compare(
                    ast.Str('d'),
                    [ast.NotIn()],
                    [ast.Dict(
                        [
                            ast.Str('a'),
                            ast.Str('b'),
                            ast.Str('c'),
                        ],
                        [
                            ast.Num(1),
                            ast.Num(2),
                            ast.Num(3),
                        ]
                    )]
                ),
            ],
            None,
            bool
        ) is True
