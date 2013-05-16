import _ast
from jaspyx.ast_util import ast_call
from jaspyx.context.function import FunctionContext
from jaspyx.visitor import BaseVisitor


class Function(BaseVisitor):
    def visit_FunctionDef(self, node):
        self.stack[-1].scope.declare(node.name)

        args = [arg.id for arg in node.args.args]
        if node.args.vararg is not None:
            raise Exception('*args not supported')
        if node.args.kwarg is not None:
            raise Exception('**kwargs not supported')

        self.indent()

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
        self.output('\n')
