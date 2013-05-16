from jaspyx.builtins import BUILTINS
from jaspyx.context.function import FunctionContext


class ModuleContext(FunctionContext):
    def __init__(self):
        super(ModuleContext, self).__init__(None, '')
        for builtin in BUILTINS.values():
            self.scope.declare(builtin)

    def __str__(self):
        return '(%s).call(this);' % super(ModuleContext, self).__str__()
