from jaspyx.context.function import FunctionContext


class ModuleContext(FunctionContext):
    def __init__(self):
        super(ModuleContext, self).__init__(None, '', arg_names=['__module__'])
        self.indent = 4
        self.scope.declare('__module__', False)
        self.scope.prefix.append('__module__')

    def __str__(self):
        indent = ' ' * (self.indent + 2)
        stmt = '%sreturn __module__;\n' % indent
        self.body.append(stmt)
        return '(%s)' % super(ModuleContext, self).__str__()
