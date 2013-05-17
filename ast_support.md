AST grammar
===========

Supported grammar
-----------------

- Module

    Used when compiling a module.

- FunctionDef

    **note**: \*\*kwargs is not supported. \*args and argument defaults are.

        def my_function(a, b, c=5):
            pass

- ClassDef

    ***notes***: Class model is currently very primitive.

    - Only direct attributes and methods without decorators are supported.
    - Multiple inheritance is not supported.
    - Inheritance is only supported from objects using the same convention as jaspyx.
    - \_\_init\_\_ is called upon instantiation, if it is defined.
    - Special methods other than \_\_init\_\_ are not supported.

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

- Return

        def my_function():
            return 42

- Assign

	**note**: JavaScript does not support indexed assignment on strings.

    Direct assignment:

        a = [1, 2, 3, 4]

    Indexed and slice assignment:
        
        a = [1, 2, 3, 4, 5]
        a[0] = 6                 # [6, 2, 3, 4, 5]
        a[:] = [7, 8, 9, 10, 11] # [7, 8, 9, 10, 11]
        a[2:] = [12, 13]         # [7, 8, 12, 13]
        a[:2] = [14, 15]         # [14, 15, 12, 13]
        a[1:2] = [16, 17]        # [14, 16, 17, 12, 13]
        a[-1:] = [18]            # [14, 16, 17, 12, 18]
        a[:-1] = [19]            # [19, 18]
        a[-2:-1] = [20, 21]      # [20, 21, 18]

- AugAssign

    For more examples, see the individual operators.

        a += 1

- Print

    **note**: This functionality depends on the 'console' facility of your browser. Trailing comma mode (`print a,`) is not supported.

        print 'Hello, world!'

- While

        while False:
            pass

- For

    **notes**:
    - This is always implemented using the JavaScript `for(i in iterable)` construct.
    - The else clause of a for statement is not supported.

            obj = {'a': 'b'}
            for i in obj:
                print i, obj[i]

- If

        if False:
            pass
        elif False:
            pass
        else:
            pass

- Global

        global status # Access window.status
        status = 'Hello, world!'

- Expr
- Pass
- BoolOp

        a and b

- BinOp

        a + b

- UnaryOp

        a = -a

- Lambda

    **note**: \*\*kwargs is not supported. \*args and argument defaults are.

        my_f = lambda: 42

- IfExp

        r = 'a' if True else False

- Dict (only literal string / number keys are supported)

        d = {'a': 1, 'b': 2}

- Compare

        a < 42
        1 < a < 4

- Call

    **note**: keyword arguments, *args and **kwargs are not supported.

        def my_function(a, b, c):
            return a * b * c
            
        my_function(1, 2, 3)


- Num

        42

- Str

        "Hello, world!"

- Attribute

        window.status = window.location

- Subscript

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

- Name

        print a

- List

        [1, 2, 3, 4, 5]

- Tuple

         (1, 2, 3, 4, 5)

- Slice

    See Assign and Subscript for examples

- Index

   See Assign and Subscript for examples

- And

        a and b

- Or

        a or b

- Add

        a + b
        a += b

- Sub

        a - b
        a -= b

- Mult

        a * b
        a *= b

- Div

        a / b
        a /= b

- Mod

        a % b
        a %= b

- Pow

        a ** b
        a **= b

- LShift

        a << b
        a <<= b

- RShift
		
    **note**: This uses the JavaScript >>> operator.

        a >> b
        a >>= b

- BitOr

        a | b
        a |= b

- BitXor

        a ^ b
        a ^= b

- BitAnd

        a & b
        a &= b

- FloorDiv

        a // b
        a //= b

- Invert

    **note**: This translates to (-(x+1)).

        ~a

- UAdd

        +a

- USub

        -a

- Not

        !a

- Eq

        a == b

- NotEq

        a != b

- Lt

        a < b

- LtE

        a <= b

- Gt

        a > b

- GtE

        a >= b

- Is

        a === undefined

- IsNot

        a !== undefined

Unsupported grammar
-------------------

- Interactive
- Suite
- Delete
- With
- Raise
- TryExcept
- TryFinally
- Assert
- Import
- ImportFrom
- Exec
- Set
- ListComp
- SetComp
- DictComp
- GeneratorExp
- Yield
- Repr
- Ellipsis
- ExtSlice
- In
- NotIn
