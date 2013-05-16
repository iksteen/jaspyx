import ast
import _ast
from jaspyx.ast_util import ast_call, ast_load
from jaspyx.builtins import BUILTINS
from jaspyx.context.block import BlockContext
from jaspyx.context.function import FunctionContext
from jaspyx.context.inline_function import InlineFunctionContext
from jaspyx.context.module import ModuleContext
from jaspyx.visitor.types import Types


class DefaultVisitor(ast.NodeVisitor, Types):
    def __init__(self):
        self.stack = []
        self.module = None
        self.do_indent = False
        self.inhibit_semicolon = False
        self.inhibit_cr = False


    #
    # Output helpers
    #

    def output(self, s):
        if self.do_indent:
            self.stack[-1].add(' ' * (self.stack[-1].indent + 2))
            self.do_indent = False
        self.stack[-1].add(s)

    def group(self, values, prefix='(', infix=' ', infix_node=None, suffix=')'):
        self.output(prefix)
        first = True
        for value in values:
            if not first:
                if infix:
                    self.output(infix)
                if infix_node is not None:
                    self.visit(infix_node)
                    if infix:
                        self.output(infix)
            else:
                first = False
            self.visit(value)
        self.output(suffix)

    def block(self, nodes, context=None):
        if context is not None:
            self.push(context)

        for node in nodes:
            self.do_indent = True
            self.visit(node)
            if not self.inhibit_semicolon:
                self.output(';')
            else:
                self.inhibit_semicolon = False
            if not self.inhibit_cr:
                self.output('\n')
            else:
                self.inhibit_cr = False

        if context is not None:
            self.pop()

    def push(self, block):
        self.stack.append(block)

    def pop(self):
        self.stack[-2].add(self.stack.pop())

    # Scoped operations:
    def visit_Module(self, node):
        self.module = ModuleContext()
        self.push(self.module)
        self.block(node.body)

    def visit_FunctionDef(self, node):
        self.stack[-1].scope.declare(node.name)

        args = [arg.id for arg in node.args.args]
        if node.args.vararg is not None:
            raise Exception('*args not supported')
        if node.args.kwarg is not None:
            raise Exception('**kwargs not supported')

        func = FunctionContext(self.stack[-1], node.name, args)
        self.push(func)

        def_args = node.args.defaults
        for arg_name, arg_val in zip(args[-len(def_args):], def_args):
            self.block([
                _ast.If(
                    _ast.Compare(
                        ast_call(
                            _ast.Name('type', _ast.Load()),
                            _ast.Name(arg_name, _ast.Load()),
                        ),
                        [_ast.Eq(), ],
                        [_ast.Str('undefined'), ],
                    ),
                    [
                        _ast.Assign(
                            [_ast.Name(arg_name, _ast.Store())],
                            arg_val
                        ),
                    ],
                    [],
                )
            ])

        self.block(node.body)
        self.pop()
        self.inhibit_semicolon = True

    def visit_Lambda(self, node):
        args = [arg.id for arg in node.args.args]

        func = InlineFunctionContext(self.stack[-1], '', args)
        self.block([_ast.Return(node.body)], context=func)

    # Print
    def visit_Print(self, node):
        log = ast_load('window.console.log')
        self.visit(ast_call(log, *node.values))

    # Variable operations:
    def visit_Global(self, node):
        for name in node.names:
            self.stack[-1].scope.declare_global(name)
        self.inhibit_semicolon = self.inhibit_cr = True

    def visit_Name(self, node):
        if self.stack[-1].scope.is_global(node.id):
            name = 'window.%s' % node.id
        else:
            name = BUILTINS.get(node.id, node.id)
            self.stack[-1].scope.reference(name)
        self.output(name)

    def visit_Assign_Slice(self, target, value):
        if target.slice.lower is None:
            lower = _ast.Num(0)
        else:
            lower = target.slice.lower

        if target.slice.upper is None:
            upper = _ast.Attribute(
                target.value,
                'length',
                _ast.Load()
            )
        else:
            upper = target.slice.upper

        length = _ast.BinOp(upper, _ast.Sub(), lower)

        arg_list = _ast.List([lower, length], _ast.Load())
        arg_list = ast_call(_ast.Attribute(arg_list, 'concat', _ast.Load()), value)
        apply = ast_load('Array.prototype.splice.apply')
        call = ast_call(apply, target.value, arg_list)
        self.visit(call)

    def visit_Assign(self, node):
        # Check for slice assignment
        for target in node.targets:
            if isinstance(target, _ast.Subscript) and \
                    isinstance(target.slice, _ast.Slice):
                if len(node.targets) > 1:
                    raise Exception('Slice assignment only supported when assignment has a single target')
                self.visit_Assign_Slice(target, node.value)
                return

        for target in node.targets:
            self.visit(target)
        self.output(' = ')
        self.visit(node.value)

    def visit_Attribute(self, node):
        self.visit(node.value)
        self.output('.%s' % node.attr)

    # Control flow operations:
    def visit_Expr(self, node):
        self.visit(node.value)

    def visit_Pass(self, node):
        self.inhibit_semicolon = self.inhibit_cr = True

    def visit_Return(self, node):
        self.output('return ')
        self.visit(node.value)

    def builtin_JS(self, arg):
        if not isinstance(arg, _ast.Str):
            raise Exception('JS() expects a string argument')
        self.output(arg.s)

    def builtin_type(self, arg):
        self.output('typeof ')
        self.visit(arg)

    def visit_Call(self, node):
        if node.keywords:
            raise Exception('keyword arguments are not supported')
        if node.starargs is not None:
            raise Exception('starargs is not supported')
        if node.kwargs is not None:
            raise Exception('kwargs is not supported')

        if isinstance(node.func, _ast.Name):
            builtin = getattr(self, 'builtin_%s' % node.func.id, None)
            if builtin is not None:
                return builtin(*node.args)

        self.visit(node.func)
        self.group(node.args, infix=', ')

    def visit_If(self, node):
        self.output('if(')
        self.visit(node.test)
        self.output(') ')

        self.block(node.body, context=BlockContext(self.stack[-1]))

        if node.orelse:
            self.do_indent = False
            self.output(' else ')
            self.block(node.orelse, context=BlockContext(self.stack[-1]))

        self.inhibit_semicolon = True

    # Operators:
    operator_map = {
        'Add': '+',
        'Sub': '-',
        'Mult': '*',
        'Div': '/',
        'Mod': '%',
        'BitAnd': '&',
        'BitOr': '|',
        'BitXor': '^',
        'Eq': '==',
        'NotEq': '!=',
        'Lt': '<',
        'LtE': '<=',
        'Gt': '>',
        'GtE': '>=',
        'And': '&&',
        'Or': '||',
        'Is': '===',
        'IsNot': '!==',
        'LShift': '<<',
        'RShift': '>>>',
    }

    def visit__op(self, node):
        self.output(self.operator_map[node.__class__.__name__])

    for op in operator_map.keys():
        exec ('visit_%s = visit__op' % op)

    def visit_Subscript(self, node):
        self.visit(node.value)
        self.visit(node.slice)

    def visit_Index(self, node):
        self.output('[')
        self.visit(node.value)
        self.output(']')

    def visit_Slice(self, node):
        self.output('.slice(')
        if node.lower is None:
            self.output('0')
        else:
            self.visit(node.lower)
        if node.upper is not None:
            self.output(', ')
            self.visit(node.upper)
        self.output(')')

    # Comparison:
    def visit_Compare(self, node):
        if len(node.ops) > 1:
            self.output('(')
        first = True
        left = node.left
        for op, comparator in zip(node.ops, node.comparators):
            if not first:
                self.output(' && ')
            else:
                first = False
            self.group([left, op, comparator])
            left = comparator
        if len(node.ops) > 1:
            self.output(')')

    # Augmented assign operations:
    def visit_AugAssign(self, node):
        attr = getattr(self, 'visit_AugAssign_%s' % node.op.__class__.__name__, None)
        if attr is None:
            # Rewrite the expression as an assignment using a BinOp
            self.visit(_ast.Assign(
                [node.target],
                _ast.BinOp(
                    _ast.Name(node.target.id, _ast.Load()),
                    node.op,
                    node.value
                )
            ))
        else:
            attr(node.target, node.op, node.value)

    def visit_AugAssign__op(self, target, op, value):
        self.visit(target)
        self.output(' ')
        self.visit(op)
        self.output('= ')
        self.visit(value)

    visit_AugAssign_Add = visit_AugAssign__op
    visit_AugAssign_Sub = visit_AugAssign__op
    visit_AugAssign_Mult = visit_AugAssign__op
    visit_AugAssign_Div = visit_AugAssign__op
    visit_AugAssign_Mod = visit_AugAssign__op
    visit_AugAssign_BitAnd = visit_AugAssign__op
    visit_AugAssign_BitOr = visit_AugAssign__op
    visit_AugAssign_BitXor = visit_AugAssign__op

    # Binary operations:
    def visit_BinOp(self, node):
        attr = getattr(self, 'visit_BinOp_%s' % node.op.__class__.__name__, None)
        if attr is None:
            self.group([node.left, node.op, node.right])
        else:
            attr(node.op, node.left, node.right)

    def visit_BinOp_Pow(self, node, left, right):
        pow = ast_load('Math.pow')
        self.visit(ast_call(pow, left, right))

    def visit_BinOp_FloorDiv(self, node, left, right):
        floor = ast_load('Math.floor')
        self.visit(ast_call(floor, _ast.BinOp(left, _ast.Div(), right)))

    # Boolean operator:
    def visit_BoolOp(self, node):
        self.group(node.values, infix_node=node.op)

    # Error handler:
    def generic_visit(self, node):
        import sys

        print >> sys.stderr, node
        print >> sys.stderr, 'Fields:'
        for field in node._fields:
            print >> sys.stderr, ' - %s: %s' % (field, getattr(node, field))
        raise Exception('Unsupported AST node %s' % node)
