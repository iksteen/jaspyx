import _ast
from jaspyx.ast_util import ast_store


class TestAstStoreName:
    def setUp(self):
        self.o = ast_store('foo')

    def test_type(self):
        assert isinstance(self.o, _ast.Name)

    def test_id(self):
        assert self.o.id == 'foo'

    def test_ctx(self):
        assert isinstance(self.o.ctx, _ast.Store)


class TestAstStoreAttr:
    def setUp(self):
        self.o = ast_store('foo', 'bar')

    def test_type(self):
        assert isinstance(self.o, _ast.Attribute)

    def test_attr(self):
        assert self.o.attr == 'bar'

    def test_ctx(self):
        assert isinstance(self.o.ctx, _ast.Store)

    def test_value_type(self):
        assert isinstance(self.o.value, _ast.Name)

    def test_value_id(self):
        assert self.o.value.id == 'foo'

    def test_value_ctx(self):
        assert isinstance(self.o.value.ctx, _ast.Load)


class TestAstStoreAttrWithDot:
    def setUp(self):
        self.o = ast_store('foo.bar')

    def test_type(self):
        assert isinstance(self.o, _ast.Attribute)

    def test_attr(self):
        assert self.o.attr == 'bar'

    def test_ctx(self):
        assert isinstance(self.o.ctx, _ast.Store)

    def test_value_type(self):
        assert isinstance(self.o.value, _ast.Name)

    def test_value_id(self):
        assert self.o.value.id == 'foo'

    def test_value_ctx(self):
        assert isinstance(self.o.value.ctx, _ast.Load)


class TestAstStoreAttrWithDotAndStarArgs:
    def setUp(self):
        self.o = ast_store('foo.bar', 'baz')

    def test_type(self):
        assert isinstance(self.o, _ast.Attribute)

    def test_attr(self):
        assert self.o.attr == 'baz'

    def test_ctx(self):
        assert isinstance(self.o.ctx, _ast.Store)

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
