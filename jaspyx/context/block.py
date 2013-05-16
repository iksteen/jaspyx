from jaspyx.scope import Scope


class BlockContext(object):
    def __init__(self, parent):
        if parent:
            self.indent = parent.indent + 2
            self.scope = parent.scope
        else:
            self.indent = 0
            self.scope = Scope()
        self.body = []

    def add(self, part):
        self.body.append(part)

    def __str__(self):
        return '{\n%s%s}' % (
            ''.join([str(s) for s in self.body]),
            ' ' * self.indent
        )
