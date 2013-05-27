import ast
from nose.tools import raises
from jaspyx.context.module import ModuleContext
from jaspyx.visitor import BaseVisitor


class TestBaseVisitor:
    def setUp(self):
        self.r = {}
        self.v = BaseVisitor('test.jpx', self.r, 2)

    def test_path(self):
        assert self.v.path == 'test.jpx'

    def test_registry(self):
        assert self.v.registry is self.r

    def test_default_indent(self):
        assert self.v.default_indent == 2

    def test_stack(self):
        assert self.v.stack == []

    def test_module(self):
        assert self.v.module is None

    def test_push(self):
        a = {}
        self.v.push(a)
        assert self.v.stack == [a]


class TestBaseVisitorWithStack:
    class S:
        def __init__(self):
            self.data = []
            self.indent = 2

        def add(self, value):
            self.data.append(value)

    def __init__(self):
        self.v = BaseVisitor('test.jpx', {}, 2)
        self.v.visit_Str = lambda n: self.v.output(n.s)

        self.s = self.S()
        self.v.push(self.s)

    def test_pop(self):
        self.v.push('foo')
        self.v.pop()
        assert self.s.data == ['foo']

    def test_output(self):
        self.v.output('foo')
        assert self.s.data == ['foo']

    def test_indent(self):
        self.v.indent()
        assert self.s.data == ['    ']

    def test_finish(self):
        self.v.finish()
        assert self.s.data == [';\n']

    def test_group_defaults_empty(self):
        self.v.group([])
        assert ''.join(self.s.data) == '()'

    def test_group_defaults_one(self):
        self.v.group(['foo'])
        assert ''.join(self.s.data) == '(foo)'

    def test_group_default_two(self):
        self.v.group(['foo', 'bar'])
        assert ''.join(self.s.data) == '(foo bar)'

    def test_group_default_three(self):
        self.v.group(['foo', 'bar', 'baz'])
        assert ''.join(self.s.data) == '(foo bar baz)'

    def test_group_non_defaults_empty(self):
        self.v.group([], prefix='[', infix='+', infix_node=ast.Str('quux'), suffix=']')
        assert ''.join(self.s.data) == '[]'

    def test_group_non_defaults_one(self):
        self.v.group(['foo'], prefix='[', infix='+', infix_node=ast.Str('quux'), suffix=']')
        assert ''.join(self.s.data) == '[foo]'

    def test_group_non_default_two(self):
        self.v.group(['foo', 'bar'], prefix='[', infix='+', infix_node=ast.Str('quux'), suffix=']')
        assert ''.join(self.s.data) == '[foo+quux+bar]'

    def test_group_non_default_three(self):
        self.v.group(['foo', 'bar', 'baz'], prefix='[', infix='+', infix_node=ast.Str('quux'), suffix=']')
        assert ''.join(self.s.data) == '[foo+quux+bar+quux+baz]'

    def test_group_node_value(self):
        self.v.group([ast.Str('foo')])
        assert ''.join(self.s.data) == '(foo)'

    def test_block(self):
        self.v.block([])
        assert self.s.data == []

    def test_block_with_node(self):
        self.v.block([ast.Str('foo')])
        assert self.s.data == ['foo']

    def test_block_with_context(self):
        s = self.S()
        self.v.block([], s)
        assert self.v.stack[-1].data == [s]


class TestBaseVisitorVisitModule:
    def setUp(self):
        self.v = BaseVisitor('test.jpx', {}, 2)
        self.v.visit_Str = lambda n: self.v.output(n.s)
        self.v.visit_Module(ast.Module([ast.Str('foo')]))

    def test_module_attr(self):
        assert isinstance(self.v.module, ModuleContext)

    def test_indent(self):
        assert self.v.module.indent == self.v.default_indent

    def test_stack(self):
        assert self.v.stack == [self.v.module]

    def test_body(self):
        assert self.v.module.body == ['foo']


class TestBaseVisitorVisitExprAndPass:
    def setUp(self):
        self.v = BaseVisitor('test.jpx', {}, 2)
        self.v.visit_Str = lambda n: self.v.output(n.s)
        self.v.visit_Module(ast.Module([]))

    def test_expr(self):
        self.v.visit(ast.Expr(ast.Str('foo')))
        assert self.v.stack[-1].body == ['    ', 'foo', ';\n']

    def test_pass(self):
        self.v.visit(ast.Pass())
        assert self.v.stack[-1].body == []

    @raises(NotImplementedError)
    def test_generic_visit(self):
        self.v.visit(ast.Print())
