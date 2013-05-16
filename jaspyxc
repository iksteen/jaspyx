#! /usr/bin/env python

import ast
from jaspyx.visitor import DefaultVisitor


if __name__ == '__main__':
    import sys

    if len(sys.argv) < 2:
        print >> sys.stderr, 'Syntax: %s <input>' % sys.argv[0]
        sys.exit(1)
    c = ast.parse(open(sys.argv[1]).read(), sys.argv[1])
    v = DefaultVisitor()
    v.visit(c)
    print str(v.module)
