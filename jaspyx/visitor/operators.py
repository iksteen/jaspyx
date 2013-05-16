from jaspyx.visitor import BaseVisitor


class Operators(BaseVisitor):
    # Operators:
    operator_map = {
        'Add': '+',
        'UAdd': '+',
        'Sub': '-',
        'USub': '-',
        'Mult': '*',
        'Div': '/',
        'Mod': '%',
        'BitAnd': '&',
        'BitOr': '|',
        'BitXor': '^',
        'Eq': '==',
        'NotEq': '!=',
        'Lt': '<',
        'LtE': '<=',
        'Gt': '>',
        'GtE': '>=',
        'And': '&&',
        'Or': '||',
        'Is': '===',
        'IsNot': '!==',
        'LShift': '<<',
        'RShift': '>>>',
    }

    def visit__op(self, node):
        self.output(self.operator_map[node.__class__.__name__])

    for op in operator_map.keys():
        exec ('visit_%s = visit__op' % op)
