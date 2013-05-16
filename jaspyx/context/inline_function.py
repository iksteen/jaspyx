from jaspyx.context.block import BlockContext
from jaspyx.scope import Scope


class InlineFunctionContext(BlockContext):
    def __init__(self, parent, name, arg_names=[]):
        super(InlineFunctionContext, self).__init__(parent)
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
            super(InlineFunctionContext, self).__str__()
        )
