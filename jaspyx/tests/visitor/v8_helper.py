import ast
import PyV8
from jaspyx.ast_util import ast_call, ast_load
from jaspyx.context import Context
from jaspyx.visitor import DefaultVisitor


class V8Helper:
    def setUp(self):
        self.v = DefaultVisitor('test.jpx', {}, 0)
        self.v.push(Context(None))

    def run(self, body, expression=None, converter=str):
        self.v.block(body)

        if not expression is None:
            self.v.visit(
                ast.Expr(
                    ast_call(ast_load('JS'), ast.Str(expression))
                )
            )

        ctx = PyV8.JSContext()
        with ctx:
            js_body = str(self.v.stack[-1])
            return converter(ctx.eval(js_body))
