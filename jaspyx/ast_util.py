import _ast


def ast_load(*args):
    pieces = []
    for arg in args:
        pieces += arg.split('.')
    obj = _ast.Name(pieces[0], _ast.Load())
    for piece in pieces[1:]:
        obj = _ast.Attribute(obj, piece, _ast.Load())
    return obj


def ast_store(*args):
    obj = ast_load(*args)
    obj.ctx = _ast.Store()
    return obj


def ast_call(func, *args):
    return _ast.Call(func, args, None, None, None)
