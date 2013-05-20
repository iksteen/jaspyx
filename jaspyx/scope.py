class Scope(object):
    def __init__(self, parent=None):
        self.parent = parent
        self.prefix = []
        self.declarations = {}
        self.globals = set()
        self.inherited = True

    def prefixed(self, name):
        return '.'.join(self.prefix + [name])

    def declare(self, name, var=True):
        self.declarations[name] = var

    def get_scope(self, name, inherit=False):
        if name in self.declarations and (not inherit or self.inherited):
            return self
        elif self.parent is not None:
            return self.parent.get_scope(name, True)
        else:
            return None

    def declare_global(self, name):
        self.globals.add(name)

    def is_global(self, name):
        return name in self.globals

    def get_global_scope(self):
        if self.parent:
            return self.parent.get_global_scope()
        else:
            return self
