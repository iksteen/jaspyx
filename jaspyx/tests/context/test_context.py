from jaspyx.context import Context
from jaspyx.scope import Scope


class TestContext:
    def setUp(self):
        self.c = Context(None)

    def test_indent(self):
        assert self.c.indent == 0

    def test_scope(self):
        assert isinstance(self.c.scope, Scope)

    def test_str(self):
        assert str(self.c) == ''

    def test_add(self):
        self.c.add('foo')
        assert str(self.c) == 'foo'

        self.c.add('bar')
        assert str(self.c) == 'foobar'


class TestContextWithParent:
    def setUp(self):
        self.c1 = Context(None)
        self.c1.indent = 2
        self.c2 = Context(self.c1)

    def test_indent(self):
        assert self.c2.indent == 2

    def test_scope(self):
        assert isinstance(self.c2.scope, Scope)
        assert self.c1.scope is self.c2.scope
