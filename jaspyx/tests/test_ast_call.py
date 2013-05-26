import ast
import _ast
from jaspyx.ast_util import ast_call


class TestAstCallWithoutArgs:
    def setUp(self):
        self.c = ast_call(ast.Name('foo', ast.Load()))

    def test_type(self):
        assert isinstance(self.c, _ast.Call)

    def test_func_type(self):
        assert isinstance(self.c.func, _ast.Name)

    def test_func_id(self):
        assert self.c.func.id == 'foo'

    def test_args(self):
        assert self.c.args == ()

    def test_keywords(self):
        assert self.c.keywords is None

    def test_starargs(self):
        assert self.c.starargs is None

    def test_kwargs(self):
        assert self.c.kwargs is None


class TestAstCallWithArgs:
    def setUp(self):
        self.c = ast_call(ast.Name('foo', ast.Load()), 'a', 'b', 'c')

    def test_type(self):
        assert isinstance(self.c, _ast.Call)

    def test_func_type(self):
        assert isinstance(self.c.func, _ast.Name)

    def test_func_id(self):
        assert self.c.func.id == 'foo'

    def test_args(self):
        assert self.c.args == ('a', 'b', 'c')

    def test_keywords(self):
        assert self.c.keywords is None

    def test_starargs(self):
        assert self.c.starargs is None

    def test_kwargs(self):
        assert self.c.kwargs is None
