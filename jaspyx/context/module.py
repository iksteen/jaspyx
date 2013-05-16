from jaspyx.builtins import BUILTINS
from jaspyx.context.inline_function import InlineFunctionContext


class ModuleContext(InlineFunctionContext):
    def __init__(self):
        super(ModuleContext, self).__init__(None, '')
        for builtin in BUILTINS.values():
            self.scope.declare(builtin)

    def __str__(self):
        return '(%s).call(this);' % super(ModuleContext, self).__str__()
