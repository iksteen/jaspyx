import ast
from jaspyx.ast_util import ast_store
from jaspyx.tests.visitor.v8_helper import V8Helper


class TestAugAssign(V8Helper):
    def _aug_assign(self, v_type, v1, op, v2, r):
        assert self.run(
            [
                ast.Assign(
                    [ast_store('test')],
                    v_type(v1),
                ),
                ast.AugAssign(
                    ast_store('test'),
                    op(),
                    v_type(v2),
                )
            ],
            'test',
            type(r)
        ) == r

    def test_add_num(self):
        self._aug_assign(ast.Num, 42, ast.Add, 21, 63)

    def test_sub_num(self):
        self._aug_assign(ast.Num, 63, ast.Sub, 42, 21)

    def test_mult_num(self):
        self._aug_assign(ast.Num, 42, ast.Mult, 21, 42 * 21)

    def test_div_num(self):
        self._aug_assign(ast.Num, 5.0, ast.Div, 2.0, 2.5)

    def test_mod_num(self):
        self._aug_assign(ast.Num, 42, ast.Mod, 21, 0)

    def test_bit_and_num(self):
        self._aug_assign(ast.Num, 126, ast.BitAnd, 63, 62)

    def test_bit_or_num(self):
        self._aug_assign(ast.Num, 128, ast.BitOr, 127, 255)

    def test_bit_xor_num(self):
        self._aug_assign(ast.Num, 255, ast.BitXor, 128, 127)

    def test_bit_lshift_num(self):
        self._aug_assign(ast.Num, 128, ast.LShift, 1, 256)

    def test_bit_rshift_num(self):
        self._aug_assign(ast.Num, 256, ast.RShift, 1, 128)

    def test_bit_pow_num(self):
        self._aug_assign(ast.Num, 2, ast.Pow, 8, 256)

    def test_bit_floordiv_num(self):
        self._aug_assign(ast.Num, 5.0, ast.FloorDiv, 2.0, 2.0)

    def test_add_str(self):
        self._aug_assign(ast.Str, 'te', ast.Add, 'st', 'test')
