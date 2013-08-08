import ast
import os
from jaspyx.ast_util import ast_load, ast_store, ast_call
from jaspyx.visitor import BaseVisitor


class Import(BaseVisitor):
    import_path = ['.']

    def load_module(self, pieces):
        module_name = '.'.join(pieces)
        if module_name in self.registry:
            return

        if len(pieces) > 1:
            parent = self.registry['.'.join(pieces[:-1])]
            import_path = [os.path.split(parent.path)[0]]
        else:
            import_path = self.import_path

        for path in import_path:
            module_path = os.path.join(path, pieces[-1], '__init__.jpx')
            if os.path.exists(module_path):
                break
            module_path = os.path.join(path, pieces[-1]) + '.jpx'
            if os.path.isfile(module_path):
                break
        else:
            raise ImportError('module %s not found' % module_name)

        c = ast.parse(open(module_path).read(), module_path)
        self.registry[module_name] = v = self.__class__(module_path, self.registry, indent=self.default_indent)
        v.import_path = self.import_path
        v.visit(c)

    def init_module(self, module_path):
        for i in range(len(module_path)):
            self.load_module(module_path[:i + 1])

        return ast_call(
            ast_call(ast_load('JS'), ast.Str('__import__')),
            ast_call(ast_load('JS'), ast.Str('__module__')),
            ast.Str('.'.join(module_path))
        )

    def visit_Import(self, node):
        for name in node.names:
            module_path = name.name.split('.')

            import_module = self.init_module(module_path)

            if not name.asname:
                self.visit(ast.Expr(import_module))
                self.visit(
                    ast.Assign(
                        [ast_store(module_path[0])],
                        self.init_module(module_path[:1])
                    )
                )
            else:
                self.visit(
                    ast.Assign(
                        [ast_store(name.asname)],
                        import_module
                    )
                )

    def visit_ImportFrom(self, node):
        if node.level:
            raise NotImplementedError('Relative imports are not supported')

        module_path = node.module.split('.')

        import_module = self.init_module(module_path)

        if len(node.names) > 1 or node.names[0].name == '*':
            self.visit(ast.Assign(
                [ast_store('$t1')],
                import_module
            ))
            import_from = ast_load('$t1')
        else:
            import_from = import_module

        if node.names[0].name == '*':
            name = node.names[0]
            if name.name == '*':
                if self.stack[-1].scope.prefix != ['__module__']:
                    raise NotImplementedError('from x import * only implemented at module level')

                self.visit(ast.For(
                    ast_store('$t2'),
                    import_from,
                    [
                        ast.Assign(
                            [
                                ast.Subscript(
                                    ast_call(ast_load('JS'), ast.Str('__module__')),
                                    ast.Index(ast_load('$t2')),
                                    ast.Load()
                                )
                            ],
                            ast.Subscript(
                                import_from,
                                ast.Index(ast_load('$t2')),
                                ast.Load(),
                            )
                        ),
                    ],
                    []
                ))
        else:
            for name in node.names:
                asname = name.asname if name.asname else name.name
                self.visit(
                    ast.Assign(
                        [ast_store(asname)],
                        ast.Attribute(
                            import_from,
                            name.name,
                            ast.Load()
                        )
                    )
                )
