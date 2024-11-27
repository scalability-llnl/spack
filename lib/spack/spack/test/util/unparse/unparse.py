# Copyright (c) 2014-2021, Simon Percivall and Spack Project Developers.
#
# SPDX-License-Identifier: Python-2.0

import ast
import codecs
import os
import sys
import tokenize

import pytest

import spack.util.unparse

pytestmark = pytest.mark.not_on_windows("Test module unsupported on Windows")


def read_pyfile(filename):
    """Read and return the contents of a Python source file (as a
    string), taking into account the file encoding."""
    with open(filename, "rb") as pyfile:
        encoding = tokenize.detect_encoding(pyfile.readline)[0]
    with codecs.open(filename, "r", encoding=encoding) as pyfile:
        source = pyfile.read()
    return source


code_parseable_in_all_parser_modes = """\
(a + b + c) * (d + e + f)
"""

for_else = """\
def f():
    for x in range(10):
        break
    else:
        y = 2
    z = 3
"""

while_else = """\
def g():
    while True:
        break
    else:
        y = 2
    z = 3
"""

relative_import = """\
from . import fred
from .. import barney
from .australia import shrimp as prawns
"""

import_many = """\
import fred, barney
"""

nonlocal_ex = """\
def f():
    x = 1
    def g():
        nonlocal x
        x = 2
        y = 7
        def h():
            nonlocal x, y
"""

# also acts as test for 'except ... as ...'
raise_from = """\
try:
    1 / 0
except ZeroDivisionError as e:
    raise ArithmeticError from e
"""

async_comprehensions_and_generators = """\
async def async_function():
    my_set = {i async for i in aiter() if i % 2}
    my_list = [i async for i in aiter() if i % 2]
    my_dict = {i: -i async for i in aiter() if i % 2}
    my_gen = (i ** 2 async for i in agen())
    my_other_gen = (i - 1 async for i in agen() if i % 2)
"""

class_decorator = """\
@f1(arg)
@f2
class Foo: pass
"""

elif1 = """\
if cond1:
    suite1
elif cond2:
    suite2
else:
    suite3
"""

elif2 = """\
if cond1:
    suite1
elif cond2:
    suite2
"""

try_except_finally = """\
try:
    suite1
except ex1:
    suite2
except ex2:
    suite3
else:
    suite4
finally:
    suite5
"""

with_simple = """\
with f():
    suite1
"""

with_as = """\
with f() as x:
    suite1
"""

with_two_items = """\
with f() as x, g() as y:
    suite1
"""

a_repr = """\
`{}`
"""

complex_f_string = '''\
f\'\'\'-{f"""*{f"+{f'.{x}.'}+"}*"""}-\'\'\'
'''

async_function_def = """\
async def f():
    suite1
"""

async_for = """\
async def f():
    async for _ in reader:
        suite1
"""

async_with = """\
async def f():
    async with g():
        suite1
"""

async_with_as = """\
async def f():
    async with g() as x:
        suite1
"""


match_literal = """\
match status:
    case 400:
        return "Bad request"
    case 404 | 418:
        return "Not found"
    case _:
        return "Something's wrong with the internet"
"""

match_with_noop = """\
match status:
    case 400:
        return "Bad request"
"""

match_literal_and_variable = """\
match point:
    case (0, 0):
        print("Origin")
    case (0, y):
        print(f"Y={y}")
    case (x, 0):
        print(f"X={x}")
    case (x, y):
        print(f"X={x}, Y={y}")
    case _:
        raise ValueError("Not a point")
"""


match_classes = """\
class Point:
    x: int
    y: int

def location(point):
    match point:
        case Point(x=0, y=0):
            print("Origin is the point's location.")
        case Point(x=0, y=y):
            print(f"Y={y} and the point is on the y-axis.")
        case Point(x=x, y=0):
            print(f"X={x} and the point is on the x-axis.")
        case Point():
            print("The point is located somewhere else on the plane.")
        case _:
            print("Not a point")
"""

match_nested = """\
match points:
    case []:
        print("No points in the list.")
    case [Point(0, 0)]:
        print("The origin is the only point in the list.")
    case [Point(x, y)]:
        print(f"A single point {x}, {y} is in the list.")
    case [Point(0, y1), Point(0, y2)]:
        print(f"Two points on the Y axis at {y1}, {y2} are in the list.")
    case _:
        print("Something else is found in the list.")
"""


def check_ast_roundtrip(code1, filename="internal", mode="exec"):
    ast1 = compile(str(code1), filename, mode, ast.PyCF_ONLY_AST)
    code2 = spack.util.unparse.unparse(ast1)

    ast2 = compile(code2, filename, mode, ast.PyCF_ONLY_AST)

    error_msg = "Failed to roundtrip {} [mode={}]".format(filename, mode)
    assert ast.dump(ast1) == ast.dump(ast2), error_msg


def test_core_lib_files():
    """Roundtrip source files from the Python core libs."""
    test_directories = [
        os.path.join(
            getattr(sys, "real_prefix", sys.prefix), "lib", "python%s.%s" % sys.version_info[:2]
        )
    ]

    names = []
    for test_dir in test_directories:
        for n in os.listdir(test_dir):
            if n.endswith(".py") and not n.startswith("bad"):
                names.append(os.path.join(test_dir, n))

    for filename in names:
        print("Testing %s" % filename)
        source = read_pyfile(filename)
        check_ast_roundtrip(source)


@pytest.mark.skipif(sys.version_info[:2] < (3, 6), reason="Only for Python 3.6 or greater")
def test_simple_fstring():
    check_ast_roundtrip("f'{x}'")


@pytest.mark.skipif(sys.version_info[:2] < (3, 6), reason="Only for Python 3.6 or greater")
def test_fstrings():
    # See issue 25180
    check_ast_roundtrip(r"""f'{f"{0}"*3}'""")
    check_ast_roundtrip(r"""f'{f"{y}"*3}'""")
    check_ast_roundtrip("""f''""")
    check_ast_roundtrip('''f"""'end' "quote\\""""''')


@pytest.mark.skipif(sys.version_info[:2] < (3, 6), reason="Only for Python 3.6 or greater")
def test_fstrings_complicated():
    # See issue 28002
    check_ast_roundtrip("""f'''{"'"}'''""")
    check_ast_roundtrip('''f\'\'\'-{f"""*{f"+{f'.{x}.'}+"}*"""}-\'\'\'''')
    check_ast_roundtrip('''f\'\'\'-{f"""*{f"+{f'.{x}.'}+"}*"""}-'single quote\\'\'\'\'''')
    check_ast_roundtrip("f\"\"\"{'''\n'''}\"\"\"")
    check_ast_roundtrip("f\"\"\"{g('''\n''')}\"\"\"")
    check_ast_roundtrip('''f"a\\r\\nb"''')
    check_ast_roundtrip('''f"\\u2028{'x'}"''')


def test_parser_modes():
    for mode in ["exec", "single", "eval"]:
        check_ast_roundtrip(code_parseable_in_all_parser_modes, mode=mode)


def test_del_statement():
    check_ast_roundtrip("del x, y, z")


def test_shifts():
    check_ast_roundtrip("45 << 2")
    check_ast_roundtrip("13 >> 7")


def test_for_else():
    check_ast_roundtrip(for_else)


def test_while_else():
    check_ast_roundtrip(while_else)


def test_unary_parens():
    check_ast_roundtrip("(-1)**7")
    check_ast_roundtrip("(-1.)**8")
    check_ast_roundtrip("(-1j)**6")
    check_ast_roundtrip("not True or False")
    check_ast_roundtrip("True or not False")


@pytest.mark.skipif(sys.version_info >= (3, 6), reason="Only works for Python < 3.6")
def test_integer_parens():
    check_ast_roundtrip("3 .__abs__()")


def test_huge_float():
    check_ast_roundtrip("1e1000")
    check_ast_roundtrip("-1e1000")
    check_ast_roundtrip("1e1000j")
    check_ast_roundtrip("-1e1000j")


def test_min_int30():
    check_ast_roundtrip(str(-(2**31)))
    check_ast_roundtrip(str(-(2**63)))


def test_imaginary_literals():
    check_ast_roundtrip("7j")
    check_ast_roundtrip("-7j")
    check_ast_roundtrip("0j")
    check_ast_roundtrip("-0j")


def test_negative_zero():
    check_ast_roundtrip("-0")
    check_ast_roundtrip("-(0)")
    check_ast_roundtrip("-0b0")
    check_ast_roundtrip("-(0b0)")
    check_ast_roundtrip("-0o0")
    check_ast_roundtrip("-(0o0)")
    check_ast_roundtrip("-0x0")
    check_ast_roundtrip("-(0x0)")


def test_lambda_parentheses():
    check_ast_roundtrip("(lambda: int)()")


def test_chained_comparisons():
    check_ast_roundtrip("1 < 4 <= 5")
    check_ast_roundtrip("a is b is c is not d")


def test_function_arguments():
    check_ast_roundtrip("def f(): pass")
    check_ast_roundtrip("def f(a): pass")
    check_ast_roundtrip("def f(b = 2): pass")
    check_ast_roundtrip("def f(a, b): pass")
    check_ast_roundtrip("def f(a, b = 2): pass")
    check_ast_roundtrip("def f(a = 5, b = 2): pass")
    check_ast_roundtrip("def f(*args, **kwargs): pass")
    check_ast_roundtrip("def f(*, a = 1, b = 2): pass")
    check_ast_roundtrip("def f(*, a = 1, b): pass")
    check_ast_roundtrip("def f(*, a, b = 2): pass")
    check_ast_roundtrip("def f(a, b = None, *, c, **kwds): pass")
    check_ast_roundtrip("def f(a=2, *args, c=5, d, **kwds): pass")


def test_relative_import():
    check_ast_roundtrip(relative_import)


def test_import_many():
    check_ast_roundtrip(import_many)


def test_nonlocal():
    check_ast_roundtrip(nonlocal_ex)


def test_raise_from():
    check_ast_roundtrip(raise_from)


def test_bytes():
    check_ast_roundtrip("b'123'")


@pytest.mark.skipif(sys.version_info < (3, 6), reason="Not supported < 3.6")
def test_formatted_value():
    check_ast_roundtrip('f"{value}"')
    check_ast_roundtrip('f"{value!s}"')
    check_ast_roundtrip('f"{value:4}"')
    check_ast_roundtrip('f"{value!s:4}"')


@pytest.mark.skipif(sys.version_info < (3, 6), reason="Not supported < 3.6")
def test_joined_str():
    check_ast_roundtrip('f"{key}={value!s}"')
    check_ast_roundtrip('f"{key}={value!r}"')
    check_ast_roundtrip('f"{key}={value!a}"')


@pytest.mark.skipif(sys.version_info != (3, 6, 0), reason="Only supported on 3.6.0")
def test_joined_str_361():
    check_ast_roundtrip('f"{key:4}={value!s}"')
    check_ast_roundtrip('f"{key:02}={value!r}"')
    check_ast_roundtrip('f"{key:6}={value!a}"')
    check_ast_roundtrip('f"{key:4}={value:#06x}"')
    check_ast_roundtrip('f"{key:02}={value:#06x}"')
    check_ast_roundtrip('f"{key:6}={value:#06x}"')
    check_ast_roundtrip('f"{key:4}={value!s:#06x}"')
    check_ast_roundtrip('f"{key:4}={value!r:#06x}"')
    check_ast_roundtrip('f"{key:4}={value!a:#06x}"')


@pytest.mark.skipif(sys.version_info[:2] < (3, 6), reason="Only for Python 3.6 or greater")
def test_complex_f_string():
    check_ast_roundtrip(complex_f_string)


def test_annotations():
    check_ast_roundtrip("def f(a : int): pass")
    check_ast_roundtrip("def f(a: int = 5): pass")
    check_ast_roundtrip("def f(*args: [int]): pass")
    check_ast_roundtrip("def f(**kwargs: dict): pass")
    check_ast_roundtrip("def f() -> None: pass")


@pytest.mark.skipif(sys.version_info < (2, 7), reason="Not supported < 2.7")
def test_set_literal():
    check_ast_roundtrip("{'a', 'b', 'c'}")


@pytest.mark.skipif(sys.version_info < (2, 7), reason="Not supported < 2.7")
def test_set_comprehension():
    check_ast_roundtrip("{x for x in range(5)}")


@pytest.mark.skipif(sys.version_info < (2, 7), reason="Not supported < 2.7")
def test_dict_comprehension():
    check_ast_roundtrip("{x: x*x for x in range(10)}")


@pytest.mark.skipif(sys.version_info < (3, 6), reason="Not supported < 3.6")
def test_dict_with_unpacking():
    check_ast_roundtrip("{**x}")
    check_ast_roundtrip("{a: b, **x}")


@pytest.mark.skipif(sys.version_info < (3, 6), reason="Not supported < 3.6")
def test_async_comp_and_gen_in_async_function():
    check_ast_roundtrip(async_comprehensions_and_generators)


@pytest.mark.skipif(sys.version_info < (3, 7), reason="Not supported < 3.7")
def test_async_comprehension():
    check_ast_roundtrip("{i async for i in aiter() if i % 2}")
    check_ast_roundtrip("[i async for i in aiter() if i % 2]")
    check_ast_roundtrip("{i: -i async for i in aiter() if i % 2}")


@pytest.mark.skipif(sys.version_info < (3, 7), reason="Not supported < 3.7")
def test_async_generator_expression():
    check_ast_roundtrip("(i ** 2 async for i in agen())")
    check_ast_roundtrip("(i - 1 async for i in agen() if i % 2)")


def test_class_decorators():
    check_ast_roundtrip(class_decorator)


def test_class_definition():
    check_ast_roundtrip("class A(metaclass=type, *[], **{}): pass")


def test_elifs():
    check_ast_roundtrip(elif1)
    check_ast_roundtrip(elif2)


def test_try_except_finally():
    check_ast_roundtrip(try_except_finally)


def test_starred_assignment():
    check_ast_roundtrip("a, *b, c = seq")
    check_ast_roundtrip("a, (*b, c) = seq")
    check_ast_roundtrip("a, *b[0], c = seq")
    check_ast_roundtrip("a, *(b, c) = seq")


@pytest.mark.skipif(sys.version_info < (3, 6), reason="Not supported < 3.6")
def test_variable_annotation():
    check_ast_roundtrip("a: int")
    check_ast_roundtrip("a: int = 0")
    check_ast_roundtrip("a: int = None")
    check_ast_roundtrip("some_list: List[int]")
    check_ast_roundtrip("some_list: List[int] = []")
    check_ast_roundtrip("t: Tuple[int, ...] = (1, 2, 3)")
    check_ast_roundtrip("(a): int")
    check_ast_roundtrip("(a): int = 0")
    check_ast_roundtrip("(a): int = None")


def test_with_simple():
    check_ast_roundtrip(with_simple)


def test_with_as():
    check_ast_roundtrip(with_as)


@pytest.mark.skipif(sys.version_info < (2, 7), reason="Not supported < 2.7")
def test_with_two_items():
    check_ast_roundtrip(with_two_items)


@pytest.mark.skipif(sys.version_info < (3, 5), reason="Not supported < 3.5")
def test_async_function_def():
    check_ast_roundtrip(async_function_def)


@pytest.mark.skipif(sys.version_info < (3, 5), reason="Not supported < 3.5")
def test_async_for():
    check_ast_roundtrip(async_for)


@pytest.mark.skipif(sys.version_info < (3, 5), reason="Not supported < 3.5")
def test_async_with():
    check_ast_roundtrip(async_with)


@pytest.mark.skipif(sys.version_info < (3, 5), reason="Not supported < 3.5")
def test_async_with_as():
    check_ast_roundtrip(async_with_as)


@pytest.mark.skipif(sys.version_info < (3, 10), reason="Not supported < 3.10")
@pytest.mark.parametrize(
    "literal",
    [match_literal, match_with_noop, match_literal_and_variable, match_classes, match_nested],
)
def test_match_literal(literal):
    check_ast_roundtrip(literal)
