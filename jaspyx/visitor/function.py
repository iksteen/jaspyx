import _ast
from jaspyx.ast_util import ast_call, ast_load
from jaspyx.context.function import FunctionContext
from jaspyx.visitor import BaseVisitor


class Function(BaseVisitor):
    def visit_FunctionDef(self, node):
        self.stack[-1].scope.declare(node.name)

        args = [arg.id for arg in node.args.args]
        if node.args.kwarg is not None:
            raise Exception('**kwargs not supported')

        # Name is empty when a lambda function is generated
        if node.name:
            self.indent()
        else:
            self.output('(')

        func = FunctionContext(self.stack[-1], node.name, args)
        self.push(func)

        # Emit vararg
        if node.args.vararg is not None:
            self.visit(
                _ast.Assign(
                    [_ast.Name(node.args.vararg, _ast.Store())],
                    ast_call(
                        ast_load('Array.prototype.slice.call'),
                        _ast.Name('arguments', _ast.Load()),
                        _ast.Num(len(args)),
                    )
                )
            )

        # Emit default arguments
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

        # Emit function body
        self.block(node.body)

        self.pop()

        if node.name:
            self.output('\n')
        else:
            self.output(')')
