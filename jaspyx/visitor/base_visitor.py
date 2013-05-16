import ast


class BaseVisitor(ast.NodeVisitor):
    def __init__(self):
        self.stack = []
        self.module = None
        self.do_indent = False
        self.inhibit_semicolon = False
        self.inhibit_cr = False

    def push(self, context):
        """
        Push a new context on the stack.

        :param context: An instance of one of the available context from
        the jaspyx.context package.
        """
        self.stack.append(context)

    def pop(self):
        """
        Pop the current context from the stack and append it to the previous
        context as content.
        """
        self.stack[-2].add(self.stack.pop())

    def output(self, s):
        """
        Append literal output to the current context.

        This will also automatically prepend indention.
        """
        if self.do_indent:
            self.stack[-1].add(' ' * (self.stack[-1].indent + 2))
            self.do_indent = False
        self.stack[-1].add(s)

    def group(self, values, prefix='(', infix=' ', infix_node=None, suffix=')'):
        """
        Append a group of values with a configurable prefix, suffix and infix
        to the output buffer. This is used to render a list of AST nodes with
        fixed surroundings.

        :param values: A list of AST nodes.
        :param prefix: Text to prepend before the output.
        :param infix: Text to put between the rendered AST nodes. If
                      infix_node is also specified, infix_node will be
                      surrounded by infix.
        :param infix_node: An AST node to render in between the values.
        :param suffix: Text to append after the output.
        """
        self.output(prefix)
        first = True
        for value in values:
            if not first:
                if infix:
                    self.output(infix)
                if infix_node is not None:
                    self.visit(infix_node)
                    if infix:
                        self.output(infix)
            else:
                first = False
            self.visit(value)
        self.output(suffix)

    def block(self, nodes, context=None):
        """
        Process a block of AST nodes and treat all of them as statements. It
        will also control automatic indention and appending semicolons and
        carriage returns to the output. Can optionally push a context on the
        stack before processing and pop it after it's done.

        :param nodes: A list of AST nodes to render.
        :param context: An optional context to push / pop.
        """
        if context is not None:
            self.push(context)

        for node in nodes:
            self.do_indent = True
            self.visit(node)
            if not self.inhibit_semicolon:
                self.output(';')
            else:
                self.inhibit_semicolon = False
            if not self.inhibit_cr:
                self.output('\n')
            else:
                self.inhibit_cr = False

        if context is not None:
            self.pop()

    def generic_visit(self, node):
        """
        Generic AST node handlers. Prints fields to stderr and raises
        an exception. This is called by ast.NodeVisitor when no
        suitable visit_<name> method is found.

        :param node: The current AST node being visited.
        """
        import sys

        print >> sys.stderr, node
        print >> sys.stderr, 'Fields:'
        for field in node._fields:
            print >> sys.stderr, ' - %s: %s' % (field, getattr(node, field))
        raise Exception('Unsupported AST node %s' % node)
