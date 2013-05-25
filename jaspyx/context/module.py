from jaspyx.context.function import FunctionContext


class ModuleContext(FunctionContext):
    def __init__(self):
        super(ModuleContext, self).__init__(None, arg_names=['__module__'])
        self.scope.prefix.append('__module__')
