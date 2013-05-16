#! /usr/bin/env python

import ast
import _ast
import json


BUILTINS = {
  'undefined': 'undefined',
  'None': 'null',
  'window': 'window',
  'True': 'true',
  'False': 'false',
  'alert': 'alert',
  'Object': 'Object',
  'Number': 'Number',
  'Boolean': 'Boolean',
  'String': 'String',
  'Array': 'Array',
  'Date': 'Date',
  'Math': 'Math',
  'RegExp': 'RegExp',
}


class Scope(object):
  def __init__(self, parent=None):
    self.parent = parent
    self.declarations = set()
    self.references = set()
    self.globals = set()

  def declare(self, name):
    self.declarations.add(name)

  def is_declared(self, name):
    if name in self.declarations:
      return True
    elif self.parent is not None:
      return self.parent.is_declared(name)
    else:
      return False

  def reference(self, name):
    self.references.add(name)

  def declare_global(self, name):
    self.globals.add(name)

  def is_global(self, name):
    return name in self.globals


class Block(object):
  def __init__(self, parent):
    if parent:
      self.indent = parent.indent + 2
      self.scope = parent.scope
    else:
      self.indent = 0
      self.scope = Scope()
    self.body = []

  def add(self, part):
    self.body.append(part)

  def __str__(self):
    return '{\n%s%s}' % (
      ''.join([str(s) for s in self.body]),
      ' ' * self.indent
    )


class InlineFunction(Block):
  def __init__(self, parent, name, arg_names=[]):
    super(InlineFunction, self).__init__(parent)
    self.scope = Scope(self.scope)
    self.name = name
    self.arg_names = arg_names
    for arg_name in self.arg_names:
      self.scope.declare(arg_name)

  def __str__(self):
    declare_vars = []
    for reference in self.scope.references:
      if not self.scope.is_declared(reference):
        self.scope.declare(reference)
        declare_vars.append(reference)

    if declare_vars:
      indent = ' ' * (self.indent + 2)
      stmt = '%svar %s;\n' % (indent, ', '.join(declare_vars))
      self.body.insert(0, stmt)

    return 'function%s(%s) %s' % (
      self.name and ' %s' % self.name or '',
      ', '.join(self.arg_names),
      super(InlineFunction, self).__str__()
    )


class Function(InlineFunction):
  def __init__(self, parent, name, arg_names=[]):
    super(Function, self).__init__(parent, name, arg_names)

  def __str__(self):
    return '%s%s' % (
      ' ' * self.indent,
      super(Function, self).__str__(),
    )


class Module(InlineFunction):
  def __init__(self):
    super(Module, self).__init__(None, '')
    for builtin in BUILTINS.values():
      self.scope.declare(builtin)

  def __str__(self):
    return '(%s).call(this);' % super(Module, self).__str__()


class JaspyxVisitor(ast.NodeVisitor):
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


  #
  # AST helper functions
  #

  def load(self, path):
    pieces = path.split('.')
    obj = _ast.Name(pieces[0], _ast.Load())
    for piece in pieces[1:]:
      obj = _ast.Attribute(obj, piece, _ast.Load())
    return obj

  def call(self, func, *args):
    return _ast.Call(func, args, None, None, None)

  # Scoped operations:
  def visit_Module(self, node):
    self.module = Module()
    self.push(self.module)
    self.block(node.body)

  def visit_FunctionDef(self, node):
    self.stack[-1].scope.declare(node.name)

    args = [arg.id for arg in node.args.args]
    if node.args.vararg is not None:
      raise Exception('*args not supported')
    if node.args.kwarg is not None:
      raise Exception('**kwargs not supported')

    func = Function(self.stack[-1], node.name, args)
    self.push(func)

    def_args = node.args.defaults
    for arg_name, arg_val in zip(args[-len(def_args):], def_args):
      self.block([
        _ast.If(
          _ast.Compare(
            self.call(
              _ast.Name('type', _ast.Load()),
              _ast.Name(arg_name, _ast.Load()),
            ),
            [_ast.Eq(),],
            [_ast.Str('undefined'),],
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

    func = InlineFunction(self.stack[-1], '', args)
    self.block([_ast.Return(node.body)], context=func)

  # Print
  def visit_Print(self, node):
    log = self.load('window.console.log')
    self.visit(self.call(log, *node.values))

  # Literal operations
  def visit_Num(self, node):
    self.output(json.dumps(node.n))

  def visit_Str(self, node):
    self.output(json.dumps(node.s))

  def visit_List(self, node):
    self.group(node.elts, prefix='[', infix=', ', suffix=']')

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
    arg_list = self.call(_ast.Attribute(arg_list, 'concat', _ast.Load()), value)
    apply = self.load('Array.prototype.splice.apply')
    call = self.call(apply, target.value, arg_list)
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

    self.block(node.body, context=Block(self.stack[-1]))

    if node.orelse:
      self.do_indent = False
      self.output(' else ')
      self.block(node.orelse, context = Block(self.stack[-1]))

    self.inhibit_semicolon = True

  # Operators:
  def visit_Add(self, node):
    self.output('+')

  def visit_Sub(self, node):
    self.output('-')

  def visit_Mult(self, node):
    self.output('*')

  def visit_Div(self, node):
    self.output('/')

  def visit_Mod(self, node):
    self.output('%')

  def visit_BitAnd(self, node):
    self.output('&')

  def visit_BitOr(self, node):
    self.output('|')

  def visit_BitXor(self, node):
    self.output('^')

  def visit_Eq(self, node):
    self.output('==')
  
  def visit_NotEq(self, node):
    self.output('!=')
  
  def visit_Lt(self, node):
    self.output('<')

  def visit_LtE(self, node):
    self.output('<=')
  
  def visit_Gt(self, node):
    self.output('>')

  def visit_GtE(self, node):
    self.output('>=')

  def visit_And(self, node):
    self.output('&&')

  def visit_Or(self, node):
    self.output('||')

  def visit_Is(self, node):
    self.output('===')

  def visit_IsNot(self, node):
    self.output('!==')

  def visit_LShift(self, node):
    self.output('<<')

  def visit_RShift(self, node):
    self.output('>>>')

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
    pow = self.load('Math.pow')
    self.visit(self.call(pow, left, right))

  def visit_BinOp_FloorDiv(self, node, left, right):
    floor = self.load('Math.floor')
    self.visit(self.call(floor, _ast.BinOp(left, _ast.Div(), right)))

  # Boolean operator:
  def visit_BoolOp(self, node):
    self.group(node.values, infix_node=node.op)

  # Error handler:
  def generic_visit(self, node):
    import sys
    print >>sys.stderr, node
    print >>sys.stderr, 'Fields:'
    for field in node._fields:
      print >>sys.stderr, ' - %s: %s' % (field, getattr(node, field))
    raise Exception('Unsupported AST node %s' % node)


if __name__ == '__main__':
  import sys
  if len(sys.argv) < 2:
    print >>sys.stderr, 'Syntax: %s <input>' % sys.argv[0]
    sys.exit(1)
  c = ast.parse(open(sys.argv[1]).read(), sys.argv[1])
  v = JaspyxVisitor()
  v.visit(c)
  print str(v.module)
