from jaspyx.context.block import BlockContext
from jaspyx.scope import Scope


class FunctionContext(BlockContext):
    def __init__(self, parent, name, arg_names=[]):
        super(FunctionContext, self).__init__(parent)
        self.scope = Scope(self.scope)
        self.name = name
        self.arg_names = arg_names
        for arg_name in self.arg_names:
            self.scope.declare(arg_name, False)

    def __str__(self):
        declare_vars = [k for k, v in self.scope.declarations.items() if v]

        if not self.scope.prefix and declare_vars:
            indent = ' ' * (self.indent + 2)
            stmt = '%svar %s;\n' % (indent, ', '.join(declare_vars))
            self.body.insert(0, stmt)

        args = ', '.join(self.arg_names)
        body = super(FunctionContext, self).__str__()
        if self.name:
            return '%s = function(%s) %s' % (
                self.scope.parent.prefixed(self.name),
                args,
                body
            )
        else:
            return 'function(%s) %s' % (
                args,
                body
            )
