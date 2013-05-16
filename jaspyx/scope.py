class Scope(object):
    tmp_index = 0

    def __init__(self, parent=None):
        self.parent = parent
        self.declarations = set()
        self.references = set()
        self.globals = set()

    def declare(self, name):
        self.declarations.add(name)

    def is_declared(self, name):
        if name in self.declarations:
            return True
        elif self.parent is not None:
            return self.parent.is_declared(name)
        else:
            return False

    def reference(self, name):
        self.references.add(name)

    def declare_global(self, name):
        self.globals.add(name)

    def is_global(self, name):
        return name in self.globals

    @classmethod
    def alloc_temp(cls):
        cls.tmp_index += 1
        return '__jpx_tmp_%i' % cls.tmp_index
