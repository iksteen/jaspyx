from jaspyx.visitor.base_visitor import BaseVisitor
from jaspyx.visitor.break_ import Break
from jaspyx.visitor.class_ import Class
from jaspyx.visitor.continue_ import Continue
from jaspyx.visitor.delete import Delete
from jaspyx.visitor.dict import Dict
from jaspyx.visitor.for_ import For
from jaspyx.visitor.func_isinstance import FuncIsinstance
from jaspyx.visitor.func_js import FuncJS
from jaspyx.visitor.func_new import FuncNew
from jaspyx.visitor.func_super import FuncSuper
from jaspyx.visitor.func_type import FuncType
from jaspyx.visitor.function import Function
from jaspyx.visitor.call import Call
from jaspyx.visitor.attribute import Attribute
from jaspyx.visitor.compare import Compare
from jaspyx.visitor.if_else import IfElse
from jaspyx.visitor.ifexp import IfExp
from jaspyx.visitor.listcomp import ListComp
from jaspyx.visitor.tryexcept import TryExcept
from jaspyx.visitor.import_ import Import
from jaspyx.visitor.lambda_ import Lambda
from jaspyx.visitor.boolop import BoolOp
from jaspyx.visitor.binop import BinOp
from jaspyx.visitor.print_to_console import PrintToConsole
from jaspyx.visitor.raise_ import Raise
from jaspyx.visitor.register_global import RegisterGlobal
from jaspyx.visitor.return_ import Return
from jaspyx.visitor.types import Types
from jaspyx.visitor.assign import Assign
from jaspyx.visitor.augassign import AugAssign
from jaspyx.visitor.subscript import Subscript
from jaspyx.visitor.unaryop import UnaryOp
from jaspyx.visitor.variable import Variable
from jaspyx.visitor.while_ import While


class DefaultVisitor(Types,
                     Dict,
                     Variable,
                     Attribute,
                     Subscript,
                     Lambda,
                     BoolOp,
                     UnaryOp,
                     BinOp,
                     Compare,
                     Assign,
                     AugAssign,
                     IfElse,
                     While,
                     For,
                     Raise,
                     TryExcept,
                     Import,
                     RegisterGlobal,
                     Function,
                     Class,
                     Return,
                     Delete,
                     Break,
                     Continue,
                     Call,
                     IfExp,
                     ListComp,
                     PrintToConsole,
                     FuncJS,
                     FuncType,
                     FuncIsinstance,
                     FuncNew,
                     FuncSuper):
    pass
