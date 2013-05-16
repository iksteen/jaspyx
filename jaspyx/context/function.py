from jaspyx.context.inline_function import InlineFunctionContext


class FunctionContext(InlineFunctionContext):
    def __init__(self, parent, name, arg_names=[]):
        super(FunctionContext, self).__init__(parent, name, arg_names)

    def __str__(self):
        return '%s%s' % (
            ' ' * self.indent,
            super(FunctionContext, self).__str__(),
        )
