from jaspyx.context.function import FunctionContext


class TestFunctionContext:
    def setUp(self):
        self.c = FunctionContext(None)

    def test_arg_names_attr(self):
        assert self.c.arg_names == []

    def test_str(self):
        assert str(self.c) == '''(function() {
})'''

    def test_str_with_body_and_vars(self):
        self.c.scope.declare('a', True)
        self.c.scope.declare('b', True)
        self.c.scope.declare('c', False)
        self.c.add('  foo\n')
        assert str(self.c) == '''(function() {
  var a, b;
  foo
})'''


class TestFunctionContextWithArguments:
    def setUp(self):
        self.c = FunctionContext(None, arg_names=['a', 'b', 'c'])

    def test_arg_names_attr(self):
        assert self.c.arg_names == ['a', 'b', 'c']

    def test_str_method(self):
        assert str(self.c) == '''(function(a, b, c) {
})'''


class TestFunctionContextWithParent:
    def setUp(self):
        self.p = FunctionContext(None)
        self.c = FunctionContext(self.p)

    def test_scope_not_parent_scope(self):
        assert not self.p.scope is self.c.scope
