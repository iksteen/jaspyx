import _ast
from jaspyx.ast_util import ast_load


class TestAstLoadName:
    def setUp(self):
        self.o = ast_load('foo')

    def test_type(self):
        assert isinstance(self.o, _ast.Name)

    def test_id(self):
        assert self.o.id == 'foo'

    def test_ctx(self):
        assert isinstance(self.o.ctx, _ast.Load)


class TestAstLoadAttr:
    def setUp(self):
        self.o = ast_load('foo', 'bar')

    def test_type(self):
        assert isinstance(self.o, _ast.Attribute)

    def test_attr(self):
        assert self.o.attr == 'bar'

    def test_ctx(self):
        assert isinstance(self.o.ctx, _ast.Load)

    def test_value_type(self):
        assert isinstance(self.o.value, _ast.Name)

    def test_value_id(self):
        assert self.o.value.id == 'foo'

    def test_value_ctx(self):
        assert isinstance(self.o.value.ctx, _ast.Load)


class TestAstLoadAttrWithDot:
    def setUp(self):
        self.o = ast_load('foo.bar')

    def test_type(self):
        assert isinstance(self.o, _ast.Attribute)

    def test_attr(self):
        assert self.o.attr == 'bar'

    def test_ctx(self):
        assert isinstance(self.o.ctx, _ast.Load)

    def test_value_type(self):
        assert isinstance(self.o.value, _ast.Name)

    def test_value_id(self):
        assert self.o.value.id == 'foo'

    def test_value_ctx(self):
        assert isinstance(self.o.value.ctx, _ast.Load)


class TestAstLoadAttrWithDotAndStarArgs:
    def setUp(self):
        self.o = ast_load('foo.bar', 'baz')

    def test_type(self):
        assert isinstance(self.o, _ast.Attribute)

    def test_attr(self):
        assert self.o.attr == 'baz'

    def test_ctx(self):
        assert isinstance(self.o.ctx, _ast.Load)

    def test_value_type(self):
        assert isinstance(self.o.value, _ast.Attribute)

    def test_value_attr(self):
        assert self.o.value.attr == 'bar'

    def test_value_ctx(self):
        assert isinstance(self.o.value.ctx, _ast.Load)

    def test_value_value_type(self):
        assert isinstance(self.o.value.value, _ast.Name)

    def test_value_value_id(self):
        assert self.o.value.value.id == 'foo'

    def test_value_value_ctx(self):
        assert isinstance(self.o.value.value.ctx, _ast.Load)
