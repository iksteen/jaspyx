from jaspyx.context.module import ModuleContext


class TestModuleContext:
    def setUp(self):
        self.c = ModuleContext()

    def test_arg_names_attr(self):
        assert self.c.arg_names == ['__module__']

    def test_scope_prefix(self):
        assert self.c.scope.prefix == ['__module__']

    def test_str(self):
        assert str(self.c) == '''(function(__module__) {
})'''

    def test_str_with_vars_and_body(self):
        self.c.scope.declare('a', True)
        self.c.scope.declare('b', True)
        self.c.scope.declare('c', False)
        self.c.add('  foo\n')
        # Note: No 'var a,b;' because prefix is __module__.
        assert str(self.c) == '''(function(__module__) {
  foo
})'''
