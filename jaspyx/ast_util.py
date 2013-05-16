import _ast


def ast_load(path):
    pieces = path.split('.')
    obj = _ast.Name(pieces[0], _ast.Load())
    for piece in pieces[1:]:
        obj = _ast.Attribute(obj, piece, _ast.Load())
    return obj


def ast_call(func, *args):
    return _ast.Call(func, args, None, None, None)
