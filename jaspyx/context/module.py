from jaspyx.builtins import BUILTINS
from jaspyx.context.function import FunctionContext


class ModuleContext(FunctionContext):
    def __init__(self):
        super(ModuleContext, self).__init__(None, '', arg_names=['__module__'])
        self.scope.declare('__module__', False)
        self.scope.prefix.append('__module__')

    def __str__(self):
        return '(%s)({});' % super(ModuleContext, self).__str__()
