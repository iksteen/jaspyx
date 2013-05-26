import ast
import _ast
from jaspyx.ast_util import ast_call, ast_load, ast_store
from jaspyx.context.block import BlockContext
from jaspyx.visitor import BaseVisitor


class TryExcept(BaseVisitor):
    def visit_TryExcept(self, node):
        if node.orelse:
            raise NotImplementedError('Try-except else handler not implemented')

        self.indent()
        self.output('try')
        self.block(node.body, context=BlockContext(self.stack[-1]))
        self.output(' catch($e) ')
        self.push(BlockContext(self.stack[-1]))

        if_start = None
        if_end = None

        for handler in node.handlers:
            if handler.type is not None:
                if handler.name is not None:
                    body = handler.body[:]
                    body.insert(0, ast.Assign(
                        [handler.name],
                        ast_call(ast_load('JS'), ast.Str('$e'))
                    ))
                else:
                    body = handler.body

                types = [handler.type] if isinstance(handler.type, _ast.Name) else handler.type
                conditions = [
                    ast_call(
                        ast_load('isinstance'),
                        ast_call(ast_load('JS'), ast.Str('$e')),
                        type_,
                    )
                    for type_ in types
                ]

                _if = ast.If(
                    ast.BoolOp(ast.Or(), conditions),
                    body,
                    []
                )
                if if_start is None:
                    if_start = if_end = _if
                else:
                    if_end.orelse, if_end = [_if], _if
            else:
                if handler is not node.handlers[-1]:
                    raise SyntaxError("default 'except:' must be last")
                if if_start is None:
                    self.block(handler.body)
                else:
                    if_end.orelse = handler.body

        if if_start is not None:
            self.visit(if_start)

        self.pop()
        self.output('\n')
