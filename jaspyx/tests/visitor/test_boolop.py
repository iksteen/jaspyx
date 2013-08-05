import ast
from jaspyx.ast_util import ast_store, ast_load
from jaspyx.tests.visitor.v8_helper import V8Helper


class TestBoolOp(V8Helper):
    def _bool_op(self, v_type, op, v, r):
        assert self.run(
            [
                ast.Assign(
                    [ast_store('test')],
                    ast.BoolOp(op(), [
                        v_type(i) for i in v
                    ]),
                ),
            ],
            'test',
            type(r)
        ) == r

    def test_true_and_true(self):
        self._bool_op(ast_load, ast.And, ['True', 'True'], True)

    def test_true_and_false(self):
        self._bool_op(ast_load, ast.And, ['True', 'False'], False)

    def test_false_and_true(self):
        self._bool_op(ast_load, ast.And, ['False', 'True'], False)

    def test_false_and_false(self):
        self._bool_op(ast_load, ast.And, ['False', 'False'], False)

    def test_true_and_true_and_true(self):
        self._bool_op(ast_load, ast.And, ['True', 'True', 'True'], True)

    def test_true_and_true_and_false(self):
        self._bool_op(ast_load, ast.And, ['True', 'True', 'False'], False)

    def test_true_or_true(self):
        self._bool_op(ast_load, ast.Or, ['True', 'True'], True)

    def test_true_or_false(self):
        self._bool_op(ast_load, ast.Or, ['True', 'False'], True)

    def test_false_or_true(self):
        self._bool_op(ast_load, ast.Or, ['False', 'True'], True)

    def test_false_or_false(self):
        self._bool_op(ast_load, ast.Or, ['False', 'False'], False)

    def test_true_or_true_or_true(self):
        self._bool_op(ast_load, ast.Or, ['True', 'True', 'True'], True)

    def test_true_or_true_or_false(self):
        self._bool_op(ast_load, ast.Or, ['True', 'True', 'False'], True)

    def test_false_or_false_or_false(self):
        self._bool_op(ast_load, ast.Or, ['False', 'False', 'False'], False)
