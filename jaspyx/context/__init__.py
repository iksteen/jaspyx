from jaspyx.scope import Scope


class Context(object):
    def __init__(self, parent):
        if parent:
            self.indent = parent.indent
            self.scope = parent.scope
        else:
            self.indent = 0
            self.scope = Scope()
        self.body = []

    def add(self, part):
        self.body.append(part)

    def __str__(self):
        return ''.join([str(s) for s in self.body])
