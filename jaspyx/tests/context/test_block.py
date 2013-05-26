from jaspyx.context.block import BlockContext


class TestBlockContext:
    def setUp(self):
        self.c = BlockContext(None)
        self.c2 = BlockContext(self.c)

    def test_indent(self):
        assert self.c.indent == 0
        assert self.c2.indent == 2

    def test_str(self):
        assert str(self.c) == '{\n}'

    def test_add_str(self):
        self.c.add('foo')
        assert str(self.c) == '{\nfoo}'


class TestBlockContextWithParent:
    def setUp(self):
        p = BlockContext(None)
        self.c = BlockContext(p)

    def test_indent(self):
        assert self.c.indent == 2

    def test_add_str(self):
        self.c.add('foo')
        assert str(self.c) == '{\nfoo  }'
