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
        self.registry[module_name] = v = self.__class__(module_path, self.registry)
        v.import_path = self.import_path
        v.visit(c)

    def init_module(self, pieces):
        module_path = []
        for piece in pieces:
            module_path.append(piece)
            module_name = '.'.join(module_path)

            self.load_module(module_path)

            self.visit(
                ast.If(
                    ast.Compare(
                        ast_call(
                            ast_load('type'),
                            ast.Subscript(
                                ast_load('__modules__'),
                                ast.Index(ast.Str(module_name)),
                                ast.Load(),
                            )
                        ),
                        [ast.Eq()],
                        [ast.Str('undefined')]
                    ),
                    [
                        ast.Assign(
                            [ast.Subscript(
                                ast_load('__modules__'),
                                ast.Index(ast.Str(module_name)),
                                ast.Store(),
                            )],
                            ast.Dict(
                                keys=[
                                    ast.Str('__modules__'),
                                    ast.Str('__registry__'),
                                ],
                                values=[
                                    ast_load('__modules__'),
                                    ast_load('__registry__'),
                                ]
                            )
                        ),
                        ast.Expr(
                            ast_call(
                                ast.Subscript(
                                    ast_load('__registry__'),
                                    ast.Index(ast.Str(module_name)),
                                    ast.Load(),
                                ),
                                ast.Subscript(
                                    ast_load('__modules__'),
                                    ast.Index(ast.Str(module_name)),
                                    ast.Load(),
                                ),
                            )
                        )
                    ] + ([
                        ast.Assign(
                            [
                                ast.Attribute(
                                    ast.Subscript(
                                        ast_load('__modules__'),
                                        ast.Index(ast.Str('.'.join(module_path[:-1]))),
                                        ast.Load()
                                    ),
                                    module_path[-1],
                                    ast.Store()
                                )
                            ],
                            ast.Subscript(
                                ast_load('__modules__'),
                                ast.Index(ast.Str(module_name)),
                                ast.Load()
                            )
                        )
                    ] if len(module_path) > 1 else []),
                    []
                )
            )

    def visit_Import(self, node):
        for name in node.names:
            module_path = name.name.split('.')

            self.init_module(module_path)

            if not name.asname:
                self.visit(
                    ast.Assign(
                        [ast_store(module_path[0])],
                        ast_load('__modules__', module_path[0])
                    )
                )
            else:
                self.visit(
                    ast.Assign(
                        [ast_store(name.asname)],
                        ast_load('__modules__', *module_path)
                    )
                )

    def visit_ImportFrom(self, node):
        if node.level:
            raise NotImplementedError('Relative imports are not supported')

        module_path = node.module.split('.')

        self.init_module(module_path)

        for name in node.names:
            if name.name == '*':
                if self.stack[-1].scope.prefix != ['__module__']:
                    raise NotImplementedError('from x import * only implemented at module level')

                self.visit(ast.For(
                    ast_store('$tmp'),
                    ast_load('__modules__', node.module),
                    [
                        ast.Expr(ast_call(
                            ast_load('eval'),
                            ast.Str('__module__[__module__.$tmp] = __module__.__modules__.%s[__module__.$tmp]' %
                                    node.module),
                        ))
                    ],
                    []
                ))
            else:
                asname = name.asname if name.asname else name.name
                self.visit(
                    ast.Assign(
                        [ast_store(asname)],
                        ast_load('__modules__', node.module, name.name)
                    )
                )
