from jaspyx.visitor.base_visitor import BaseVisitor
from jaspyx.visitor.func_js import FuncJS
from jaspyx.visitor.func_type import FuncType
from jaspyx.visitor.function import Function
from jaspyx.visitor.call import Call
from jaspyx.visitor.attribute import Attribute
from jaspyx.visitor.compare import Compare
from jaspyx.visitor.if_else import IfElse
from jaspyx.visitor.lambda_ import Lambda
from jaspyx.visitor.operators import Operators
from jaspyx.visitor.boolop import BoolOp
from jaspyx.visitor.binop import BinOp
from jaspyx.visitor.print_to_console import PrintToConsole
from jaspyx.visitor.register_global import RegisterGlobal
from jaspyx.visitor.return_ import Return
from jaspyx.visitor.types import Types
from jaspyx.visitor.assign import Assign
from jaspyx.visitor.augassign import AugAssign
from jaspyx.visitor.subscript import Subscript
from jaspyx.visitor.variable import Variable


class DefaultVisitor(Types,
                     Variable,
                     Attribute,
                     Subscript,
                     Lambda,
                     Operators,
                     BoolOp,
                     BinOp,
                     Compare,
                     Assign,
                     AugAssign,
                     IfElse,
                     RegisterGlobal,
                     Function,
                     Return,
                     Call,
                     PrintToConsole,
                     FuncJS,
                     FuncType):
    pass
