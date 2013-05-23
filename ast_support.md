AST grammar
===========

This document contains an enumeration of supported and unsupported AST nodes as described in the python documentation of the [ast module](http://docs.python.org/2/library/ast.html).


Supported statements
--------------------

- `ast.FunctionDef`

    **notes**:
    - `**kwargs` is not supported.
    - `*args` and argument defaults are supported.

    Example:

        def my_function(a, b, c=5):
            pass

- `ast.ClassDef`

    ***notes***:

    - Multiple inheritance is not supported.
    - Inheritance is only supported from other jaspyx classes.
    - The `__init__` method is called upon instantiation, if it is defined.
    - `__class__` is set to the constructor, by the constructor.
    - `__mro__` is an array of super-types in order of inheritance.
    - `__base__` is set to the super-type of the class.
    - No other special methods or attributes are implemented.

    Example:

        class MyClass:
            answer = 42
            def __init__(self):
                print 'This is A.__init__'

            def question(self):
                print self.answer

        class MySubClass(MyClass):
            def __init__(self):
                print 'This is B.__init__'
                MyClass.prototype.__init__(self)

- `ast.Return`

	Example:

        def my_function():
            return 42

- `ast.Delete`

    Example:

        a = {1: 2}
        del a[1]
        del a

- `ast.Assign`

	**notes**:
    - For details about indexed and slice assignment, see description of `ast.Subscript`.

    Example:

        a = 'Hello, world!'

- `ast.AugAssign`

    **notes**:
    - Augmented assignment is supported for each operator for which Python supports it. In cases where JavaScript does not support an equivalent augmented assignment, the statement is rewritten using regular assignment and an `ast.BinOp`.
    - For examples, see the *operators* section.

- `ast.Print`

    **notes**:
    - Does not support specifying a different output file.
    - This functionality depends on the _console_ facility of your browser.
    - Trailing comma mode (`print a,`) is not supported.

    Example:

        print 'Hello, world!'

- `ast.For`

    **notes**:
    - This is always implemented using the JavaScript `for(i in iterable)` construct.
    - The `else` clause of the python `for` statement is not supported.
    - Iterating an array using `for` will probably have unintended results.

    Example:

        obj = {'a': 'b'}
        for i in obj:
            print i, obj[i]

- `ast.While`

    Example:

        while False:
            pass

- `ast.If`

    Example:

        if False:
            pass
        elif False:
            pass
        else:
            pass

- `ast.Raise`

    **notes**:
    - Only the single clause raise statement is supported.

    Example:

        raise 'Something went wrong!'

- `ast.Import`

    **notes**:
    - Relative imports are not supported. This is a design decision, not a technical limitation.
    - Module have the file extension .jpx.
    - When importing module x.y.z, x/y/z/\_\_init\_\_.jpx is first checked. If that does not exist, x/y/z.jpx will be checked.

    Example:

        import module.submodule
        import module.another as another

- `ast.Global`

    Example:

        global status # Access window.status
        status = 'Hello, world!'

- `ast.Expr`

    Used when an expression is used as a statement.

- `ast.Pass`

- `ast.Break`

    Example:
   
        for i in a:
            if i == 'a':
                break

- `ast.Continue`

    Example:

        for i in a:
            if not a[i]:
                continue


Expressions
-----------

- `ast.BoolOp`

    **notes**:
    - Compatible with all boolean operators (see below).

    Example:

        a and b

- `ast.BinOp`

    **notes**:
    - Compatible with all operators (see below).

    Example:

        a + b

- `ast.UnaryOp`

    **notes**:
    - Compatible unary operators (see below)
    
    Example:

        -a

- `ast.Lambda`

    **notes**:
    - Same notes apply as for `ast.FunctionDef`

    Example:

        a = lambda a, b, *args: a + b + ''.join(args)

- `ast.IfExp`

    **notes**:
    - Implemented using JavaScript's ternary operator.

    Example:

        'True' if b else 'False'

- `ast.Dict`

    **notes**:
    - Implemented as a JavaScript object (`{}`).
    - Only literals are supported as keys.

    Example:

        d = {
          'a': 'b',
          'c': 'd',
         }

- `ast.Compare`

    **notes**:
    - Compatible with all comparison operators (see below).

    Example:

        a < 5

- `ast.Call`

    **notes**:
    - Keyword arguments, `*args` and `**kwargs` are not supported.

    Example:

        result = my_function(1, 2)

- `ast.Num`

    Example:

        42

- `ast.Str`

    Example:

        a = "Hello, world!"

- `ast.Attribute`

    Example:
    
        window.status = '...'

- `ast.Subscript`

    **notes**:
    - JavaScript does not support indexed assignment within strings.
    - JavaScript does not support negative indexes (negative values in slices are supported though)
    - Slice stepping, multi-dimensional slices and ellipsis are not supported.

    Example:

        a = [1, 2, 3, 4, 5]
        print a[0]      # 1
        print a[:]      # [1, 2, 3, 4, 5]
        print a[2:]     # [3, 4, 5]
        print a[:2]     # [1, 2]
        print a[1:2]    # [2]
        print a[-1:]    # [5]
        print a[:-1]    # [1, 2, 3, 4]
        print a[-4:-1]  # [2, 3, 4]

        b = 'hello'
        print b[0]      # h
        print b[:]      # hello
        print b[2:]     # llo
        print b[:2]     # he
        print b[1:2]    # e
        print b[-1:]    # o
        print b[:-1]    # hell
        print b[-4:-1]  # ell

        a = [1, 2, 3, 4, 5]
        a[0] = 6                 # [6, 2, 3, 4, 5]
        a[:] = [7, 8, 9, 10, 11] # [7, 8, 9, 10, 11]
        a[2:] = [12, 13]         # [7, 8, 12, 13]
        a[:2] = [14, 15]         # [14, 15, 12, 13]
        a[1:2] = [16, 17]        # [14, 16, 17, 12, 13]
        a[-1:] = [18]            # [14, 16, 17, 12, 18]
        a[:-1] = [19]            # [19, 18]
        a[-2:-1] = [20, 21]      # [20, 21, 18]

- `ast.Name`

    Example:

        a = b

- `ast.List`

    Example:

        a = [1, 2, 3, 4, 5]

- `ast.Tuple`

    **notes**:
    - Maps to JavaScript Array, same as list.

    Example:

        a = (1, 2, 3, 4, 5)


Boolean operators
-----------------

- `ast.And`

    Example:

        a and b and c

- `ast.Or`

    Example:

        a or b or c


Operators
---------

- `ast.Add`

    Example:

        a + b
        a += b

- `ast.Sub`

    Example:

        a - b
        a -= b

- `ast.Mult`

    Example:

        a * b
        a *= b

- `ast.Div`

    Example:

        a / b
        a /= b

- `ast.Mod`

    Example:

        a % b
        a %= b

- `ast.Pow`

    **notes**:
    - Implemented as `Math.pow(a, b)`.

    Example:

        a ** b
        a **= b

- `ast.LShift`

    Example:

        a << b
        a <<= b

- `ast.RShift`

    Example:

        a >> b
        a >>= b

- `ast.BitOr`

    Example:

        a | b
        a |= b

- `ast.BitXor`

    Example:

        a ^ b
        a ^= b

- `ast.BitAnd`

    Example:

        a & b
        a &= b

- `ast.FloorDiv`

    **notes**:
    - Implemented as Math.floor(a / b).

    Example:

        a // b
        a //= b


Unary operators
---------------

- `ast.Invert`

    **note**: This translates to (-(x+1)).

    Example:

        a = ~a

- `ast.Not`

    Example:

        a = !a

- `ast.UAdd`

    Example:

        a = +a

- `ast.USub`

    Example:

        -a


Comparison operators
--------------------

- Eq

    Example:

        a == b

- NotEq

    Example:

        a != b

- Lt

    Example:

        a < b

- LtE

    Example:

        a <= b

- Gt

    Example:

        a > b

- GtE

    Example:

        a >= b

- Is

    Example:

        a === undefined

- IsNot

    Example:

        a !== undefined

- In

    **notes**:
    - Checks if comparator is an array by calling `Array.isArray`.
    - If comparator is an array, `indexOf` is used to check presence of left-hand side.
    - If comparator is not an array, `in` is used to check presence of left-hand side.

    Example:

        'foo' in ['foo', 'bar', 'baz']
        'foo' in {'foo': 1, 'bar': 2, 'baz': 3}

- NotIn

    **notes**:
    - Implemented as `(!(left in comparator))`

    Example:
    
        'foo' not in ['bar', 'baz', 'quux']
        'foo' not in {'bar': 1, 'baz': 2, 'quux': 3}


Unsupported grammar
-------------------

- `ast.Interactive`
- `ast.Expression`
- `ast.Suite`
- `ast.With`
- `ast.TryExcept`
- `ast.TryFinally`
- `ast.Assert`
- `ast.ImportFrom`
- `ast.Exec`
- `ast.Set`
- `ast.ListComp`
- `ast.SetComp`
- `ast.DictComp`
- `ast.GeneratorExp`
- `ast.Yield`
- `ast.Repr`
- `ast.Ellipsis`
- `ast.ExtSlice`
