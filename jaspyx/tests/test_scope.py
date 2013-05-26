from jaspyx.scope import Scope


class TestScopeWithoutParent:
    def setUp(self):
        self.s = Scope()

    def test_parent(self):
        assert self.s.parent is None

    def test_prefix(self):
        assert self.s.prefix == []

    def test_declarations(self):
        assert self.s.declarations == {}

    def test_globals(self):
        assert self.s.globals == set()

    def test_inherited(self):
        assert self.s.inherited

    def test_prefixed_without_prefix(self):
        assert self.s.prefixed('foo') == 'foo'

    def test_prefixed_with_prefix(self):
        self.s.prefix.append('bar')
        assert self.s.prefixed('foo') == 'bar.foo'

    def test_declare_var(self):
        self.s.declare('foo', True)
        assert self.s.declarations == {'foo': True}

    def test_declare_non_var(self):
        self.s.declare('foo', False)
        assert self.s.declarations == {'foo': False}

    def test_get_scope_undefined(self):
        assert self.s.get_scope('foo') is None

    def test_get_scope_declared(self):
        self.s.declare('foo')
        assert self.s.get_scope('foo') is self.s

    def test_declare_global(self):
        self.s.declare_global('foo')
        assert self.s.globals == set(['foo'])

    def test_is_global_undefined(self):
        assert not self.s.is_global('foo')

    def test_is_global_defined(self):
        self.s.declare_global('foo')
        assert self.s.is_global('foo')

    def get_global_scope(self):
        assert self.s.get_global_scope() is self.s


class TestScopeWithParent:
    def setUp(self):
        self.p = Scope()
        self.s = Scope(self.p)

    def test_parent(self):
        assert self.s.parent is self.p

    def test_get_scope_undeclared(self):
        assert self.s.get_scope('foo') is None

    def test_get_scope_inherited(self):
        self.p.declare('foo')
        assert self.s.get_scope('foo') is self.p

    def test_get_scope_inherited(self):
        self.p.declare('foo')
        assert self.s.get_scope('foo') is self.p

    def test_get_global_scope_inherited(self):
        assert self.s.get_global_scope() is self.p


class TestScopeWithNonInheritingParent:
    def setUp(self):
        self.p1 = Scope()
        self.p2 = Scope(self.p1)
        self.p2.inherited = False
        self.s = Scope(self.p2)

    def test_get_scope_inherited(self):
        self.p1.declare('foo')
        self.p2.declare('foo')
        assert self.s.get_scope('foo') is self.p1
