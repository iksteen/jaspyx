import ast


def ast_load(*args):
    pieces = []
    for arg in args:
        pieces += arg.split('.')
    obj = ast.Name(pieces[0], ast.Load())
    for piece in pieces[1:]:
        obj = ast.Attribute(obj, piece, ast.Load())
    return obj


def ast_store(*args):
    obj = ast_load(*args)
    obj.ctx = ast.Store()
    return obj


def ast_call(func, *args):
    return ast.Call(func, args, None, None, None)
