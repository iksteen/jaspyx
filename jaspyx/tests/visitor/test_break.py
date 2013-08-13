import ast
from jaspyx.ast_util import ast_store, ast_load
from jaspyx.tests.visitor.v8_helper import V8Helper


class TestBreak(V8Helper):
    def test_break(self):
        assert self.run(
            [
                ast.Assign(
                    [ast_store('i')],
                    ast.Num(0),
                ),
                ast.While(
                    ast.Compare(
                        ast_load('i'),
                        [ast.Lt()],
                        [ast.Num(10)]
                    ),
                    [
                        ast.Break(),
                    ],
                    []
                )
            ],
            'i',
            int
        ) == 0
