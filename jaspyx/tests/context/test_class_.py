from jaspyx.context import Context
from jaspyx.context.class_ import ClassContext


class TestClassContext:
    def setUp(self):
        p = Context(None)
        self.c = ClassContext(p, 'foo')

    def test_indent(self):
        assert self.c.indent == 0

    def test_str(self):
        assert str(self.c) == ''

    def test_scope(self):
        assert self.c.scope.prefix == ['foo', 'prototype']

    def test_inherited(self):
        assert not self.c.scope.inherited


class TestClassContextWithParent:
    def setUp(self):
        p = Context(None)
        p.scope.prefix.extend(['foo', 'prototype'])
        self.c = ClassContext(p, 'bar')

    def test_indent(self):
        assert self.c.indent == 0

    def test_scope(self):
        assert self.c.scope.prefix == ['foo', 'prototype', 'bar', 'prototype']
