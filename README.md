jaspyx
======

JavaScript expressed in Python.


What is it not?
---------------

Jaspyx is **not** a python-to-javascript compiler. Jaspyx does **not** allow you to re-compile your existing python code to javascript. It does **not** allow you to use the python standard library in a web environment.


What is jaspyx?
---------------

Jaspyx allows you to write JavaScript using a pythonic syntax. It does that by using python's built-in compiler to compile your jaspyx code and transliterating the resulting AST (abstract syntax tree) to JavaScript.

Jaspyx tries to stay close to python syntax and idiom as long as this does not interfere with standard JavaScript behaviour. Because it tries to stay close to the JavaScript idiom, jaspyx allows you to use existing JavaScript libraries.

You can use it stand-alone using the bundled _jaspyxc_ command line tool or you can use it as a library in your own applications.


Example
-------

Create a file name _demo.jpx_ with the following content:

    def main():
        alert('Hello, world!')

    main()

Convert it to JavaScript using the _jaspyxc_:

    $ jaspyxc demo.jpx

It will generate the following output:

    (function() {
      function main() {
        alert("Hello, world!");
      }
      main();
    }).call(this);

Nothing spectacular, but it's something!


Contributing
------------

Fork the project on GitHub, clone it, check out a new branch, make your changes, commit, send pull request.


Contact Information
-------------------

Author: Ingmar Steen

E-mail: iksteen@gmail.com

Homepage: https://github.com/iksteen/jaspyx


License
-------

Jaspyx is distributed under the MIT license. See the LICENSE file for details.


Copyright
---------

Copyright (C) 2013 Ingmar Steen <iksteen@gmail.com>
