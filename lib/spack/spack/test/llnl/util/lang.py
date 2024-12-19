# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os.path
import re
import sys
from datetime import datetime, timedelta
from textwrap import dedent

import pytest

import llnl.util.lang
from llnl.util.lang import dedupe, match_predicate, memoized, pretty_date, stable_args


@pytest.fixture()
def now():
    return datetime.now()


@pytest.fixture()
def module_path(tmpdir):
    m = tmpdir.join("foo.py")
    content = """
import os.path

value = 1
path = os.path.join('/usr', 'bin')
"""
    m.write(content)

    yield str(m)

    # Don't leave garbage in the module system
    if "foo" in sys.modules:
        del sys.modules["foo"]


def test_pretty_date():
    """Make sure pretty_date prints the right dates."""
    now = datetime.now()

    just_now = now - timedelta(seconds=5)
    assert pretty_date(just_now, now) == "just now"

    seconds = now - timedelta(seconds=30)
    assert pretty_date(seconds, now) == "30 seconds ago"

    a_minute = now - timedelta(seconds=60)
    assert pretty_date(a_minute, now) == "a minute ago"

    minutes = now - timedelta(seconds=1800)
    assert pretty_date(minutes, now) == "30 minutes ago"

    an_hour = now - timedelta(hours=1)
    assert pretty_date(an_hour, now) == "an hour ago"

    hours = now - timedelta(hours=2)
    assert pretty_date(hours, now) == "2 hours ago"

    yesterday = now - timedelta(days=1)
    assert pretty_date(yesterday, now) == "yesterday"

    days = now - timedelta(days=3)
    assert pretty_date(days, now) == "3 days ago"

    a_week = now - timedelta(weeks=1)
    assert pretty_date(a_week, now) == "a week ago"

    weeks = now - timedelta(weeks=2)
    assert pretty_date(weeks, now) == "2 weeks ago"

    a_month = now - timedelta(days=30)
    assert pretty_date(a_month, now) == "a month ago"

    months = now - timedelta(days=60)
    assert pretty_date(months, now) == "2 months ago"

    a_year = now - timedelta(days=365)
    assert pretty_date(a_year, now) == "a year ago"

    years = now - timedelta(days=365 * 2)
    assert pretty_date(years, now) == "2 years ago"


@pytest.mark.parametrize(
    "delta,pretty_string",
    [
        (timedelta(days=1), "a day ago"),
        (timedelta(days=1), "yesterday"),
        (timedelta(days=1), "1 day ago"),
        (timedelta(weeks=1), "1 week ago"),
        (timedelta(weeks=3), "3 weeks ago"),
        (timedelta(days=30), "1 month ago"),
        (timedelta(days=730), "2 years  ago"),
    ],
)
def test_pretty_string_to_date_delta(now, delta, pretty_string):
    t1 = now - delta
    t2 = llnl.util.lang.pretty_string_to_date(pretty_string, now)
    assert t1 == t2


@pytest.mark.parametrize(
    "format,pretty_string",
    [
        ("%Y", "2018"),
        ("%Y-%m", "2015-03"),
        ("%Y-%m-%d", "2015-03-28"),
        ("%Y-%m-%d %H:%M", "2015-03-28 11:12"),
        ("%Y-%m-%d %H:%M:%S", "2015-03-28 23:34:45"),
    ],
)
def test_pretty_string_to_date(format, pretty_string):
    t1 = datetime.strptime(pretty_string, format)
    t2 = llnl.util.lang.pretty_string_to_date(pretty_string, now)
    assert t1 == t2


def test_pretty_seconds():
    assert llnl.util.lang.pretty_seconds(2.1) == "2.100s"
    assert llnl.util.lang.pretty_seconds(2.1 / 1000) == "2.100ms"
    assert llnl.util.lang.pretty_seconds(2.1 / 1000 / 1000) == "2.100us"
    assert llnl.util.lang.pretty_seconds(2.1 / 1000 / 1000 / 1000) == "2.100ns"
    assert llnl.util.lang.pretty_seconds(2.1 / 1000 / 1000 / 1000 / 10) == "0.210ns"


def test_match_predicate():
    matcher = match_predicate(lambda x: True)
    assert matcher("foo")
    assert matcher("bar")
    assert matcher("baz")

    matcher = match_predicate(["foo", "bar"])
    assert matcher("foo")
    assert matcher("bar")
    assert not matcher("baz")

    matcher = match_predicate(r"^(foo|bar)$")
    assert matcher("foo")
    assert matcher("bar")
    assert not matcher("baz")

    with pytest.raises(ValueError):
        matcher = match_predicate(object())
        matcher("foo")


def test_load_modules_from_file(module_path):
    # Check prerequisites
    assert "foo" not in sys.modules

    # Check that the module is loaded correctly from file
    foo = llnl.util.lang.load_module_from_file("foo", module_path)
    assert "foo" in sys.modules
    assert foo.value == 1
    assert foo.path == os.path.join("/usr", "bin")

    # Check that the module is not reloaded a second time on subsequent calls
    foo.value = 2
    foo = llnl.util.lang.load_module_from_file("foo", module_path)
    assert "foo" in sys.modules
    assert foo.value == 2
    assert foo.path == os.path.join("/usr", "bin")


def test_uniq():
    assert [1, 2, 3] == llnl.util.lang.uniq([1, 2, 3])
    assert [1, 2, 3] == llnl.util.lang.uniq([1, 1, 1, 1, 2, 2, 2, 3, 3])
    assert [1, 2, 1] == llnl.util.lang.uniq([1, 1, 1, 1, 2, 2, 2, 1, 1])
    assert [] == llnl.util.lang.uniq([])


def test_key_ordering():
    """Ensure that key ordering works correctly."""

    with pytest.raises(TypeError):

        @llnl.util.lang.key_ordering
        class ClassThatHasNoCmpKeyMethod:
            # this will raise b/c it does not define _cmp_key
            pass

    @llnl.util.lang.key_ordering
    class KeyComparable:
        def __init__(self, t):
            self.t = t

        def _cmp_key(self):
            return self.t

    a = KeyComparable((1, 2, 3))
    a2 = KeyComparable((1, 2, 3))
    b = KeyComparable((2, 3, 4))
    b2 = KeyComparable((2, 3, 4))

    assert a == a
    assert a == a2
    assert a2 == a

    assert b == b
    assert b == b2
    assert b2 == b

    assert a != b

    assert a < b
    assert b > a

    assert a <= b
    assert b >= a

    assert a <= a
    assert a <= a2
    assert b >= b
    assert b >= b2

    assert hash(a) != hash(b)
    assert hash(a) == hash(a)
    assert hash(a) == hash(a2)
    assert hash(b) == hash(b)
    assert hash(b) == hash(b2)


@pytest.mark.parametrize(
    "args1,kwargs1,args2,kwargs2",
    [
        # Ensure tuples passed in args are disambiguated from equivalent kwarg items.
        (("a", 3), {}, (), {"a": 3})
    ],
)
def test_unequal_args(args1, kwargs1, args2, kwargs2):
    assert stable_args(*args1, **kwargs1) != stable_args(*args2, **kwargs2)


@pytest.mark.parametrize(
    "args1,kwargs1,args2,kwargs2",
    [
        # Ensure that kwargs are stably sorted.
        ((), {"a": 3, "b": 4}, (), {"b": 4, "a": 3})
    ],
)
def test_equal_args(args1, kwargs1, args2, kwargs2):
    assert stable_args(*args1, **kwargs1) == stable_args(*args2, **kwargs2)


@pytest.mark.parametrize("args, kwargs", [((1,), {}), ((), {"a": 3}), ((1,), {"a": 3})])
def test_memoized(args, kwargs):
    @memoized
    def f(*args, **kwargs):
        return "return-value"

    assert f(*args, **kwargs) == "return-value"
    key = stable_args(*args, **kwargs)
    assert list(f.cache.keys()) == [key]
    assert f.cache[key] == "return-value"


@pytest.mark.parametrize("args, kwargs", [(([1],), {}), ((), {"a": [1]})])
def test_memoized_unhashable(args, kwargs):
    """Check that an exception is raised clearly"""

    @memoized
    def f(*args, **kwargs):
        return None

    with pytest.raises(llnl.util.lang.UnhashableArguments) as exc_info:
        f(*args, **kwargs)
    exc_msg = str(exc_info.value)
    key = stable_args(*args, **kwargs)
    assert str(key) in exc_msg
    assert "function 'f'" in exc_msg


def test_dedupe():
    assert [x for x in dedupe([1, 2, 1, 3, 2])] == [1, 2, 3]
    assert [x for x in dedupe([1, -2, 1, 3, 2], key=abs)] == [1, -2, 3]


def test_grouped_exception():
    h = llnl.util.lang.GroupedExceptionHandler()

    def inner():
        raise ValueError("wow!")

    with h.forward("inner method"):
        inner()

    with h.forward("top-level"):
        raise TypeError("ok")

    assert h.grouped_message(with_tracebacks=False) == dedent(
        """\
    due to the following failures:
    inner method raised ValueError: wow!
    top-level raised TypeError: ok"""
    )


def test_grouped_exception_base_type():
    h = llnl.util.lang.GroupedExceptionHandler()

    with h.forward("catch-runtime-error", RuntimeError):
        raise NotImplementedError()

    with pytest.raises(NotImplementedError):
        with h.forward("catch-value-error", ValueError):
            raise NotImplementedError()

    message = h.grouped_message(with_tracebacks=False)
    assert "catch-runtime-error" in message
    assert "catch-value-error" not in message


def test_class_level_constant_value():
    """Tests that the Const descriptor does not allow overwriting the value from an instance"""

    class _SomeClass:
        CONST_VALUE = llnl.util.lang.Const(10)

    with pytest.raises(TypeError, match="not support assignment"):
        _SomeClass().CONST_VALUE = 11


def test_deprecated_property():
    """Tests the behavior of the DeprecatedProperty descriptor, which is can be used when
    deprecating an attribute.
    """

    class _Deprecated(llnl.util.lang.DeprecatedProperty):
        def factory(self, instance, owner):
            return 46

    class _SomeClass:
        deprecated = _Deprecated("deprecated")

    # Default behavior is to just return the deprecated value
    s = _SomeClass()
    assert s.deprecated == 46

    # When setting error_level to 1 the attribute warns
    _SomeClass.deprecated.error_lvl = 1
    with pytest.warns(UserWarning):
        assert s.deprecated == 46

    # When setting error_level to 2 an exception is raised
    _SomeClass.deprecated.error_lvl = 2
    with pytest.raises(AttributeError):
        _ = s.deprecated


def test_fnmatch_multiple():
    named_patterns = {"a": "libf*o.so", "b": "libb*r.so"}
    regex = re.compile(llnl.util.lang.fnmatch_translate_multiple(named_patterns))

    a = regex.match("libfoo.so")
    assert a and a.group("a") == "libfoo.so"

    b = regex.match("libbar.so")
    assert b and b.group("b") == "libbar.so"

    assert not regex.match("libfoo.so.1")
    assert not regex.match("libbar.so.1")
    assert not regex.match("libfoo.solibbar.so")
    assert not regex.match("libbaz.so")
