from jaspyx.context import Context


class BlockContext(Context):
    def __init__(self, parent):
        super(BlockContext, self).__init__(parent)
        if parent:
            self.indent += 2

    def __str__(self):
        return '{\n%s%s}' % (
            ''.join([str(s) for s in self.body]),
            ' ' * self.indent
        )
