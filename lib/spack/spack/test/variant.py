# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import numbers

import pytest

import spack.error
import spack.repo
import spack.spec
import spack.variant
from spack.spec import Spec, VariantMap
from spack.variant import (
    AbstractVariant,
    BoolValuedVariant,
    DuplicateVariantError,
    InconsistentValidationError,
    InvalidVariantValueError,
    MultipleValuesInExclusiveVariantError,
    MultiValuedVariant,
    SingleValuedVariant,
    UnsatisfiableVariantSpecError,
    Variant,
    disjoint_sets,
)


class TestMultiValuedVariant:
    def test_initialization(self):
        # Basic properties
        a = MultiValuedVariant("foo", "bar,baz")
        assert repr(a) == "MultiValuedVariant('foo', 'bar,baz')"
        assert str(a) == "foo=bar,baz"
        assert a.value == ("bar", "baz")
        assert "bar" in a
        assert "baz" in a
        assert eval(repr(a)) == a

        # Spaces are trimmed
        b = MultiValuedVariant("foo", "bar, baz")
        assert repr(b) == "MultiValuedVariant('foo', 'bar, baz')"
        assert str(b) == "foo=bar,baz"
        assert b.value == ("bar", "baz")
        assert "bar" in b
        assert "baz" in b
        assert a == b
        assert hash(a) == hash(b)
        assert eval(repr(b)) == a

        # Order is not important
        c = MultiValuedVariant("foo", "baz, bar")
        assert repr(c) == "MultiValuedVariant('foo', 'baz, bar')"
        assert str(c) == "foo=bar,baz"
        assert c.value == ("bar", "baz")
        assert "bar" in c
        assert "baz" in c
        assert a == c
        assert hash(a) == hash(c)
        assert eval(repr(c)) == a

        # Check the copy
        d = a.copy()
        assert repr(a) == repr(d)
        assert str(a) == str(d)
        assert d.value == ("bar", "baz")
        assert "bar" in d
        assert "baz" in d
        assert a == d
        assert a is not d
        assert hash(a) == hash(d)
        assert eval(repr(d)) == a

    def test_satisfies(self):
        a = MultiValuedVariant("foo", "bar,baz")
        b = MultiValuedVariant("foo", "bar")
        c = MultiValuedVariant("fee", "bar,baz")
        d = MultiValuedVariant("foo", "True")

        # 'foo=bar,baz' satisfies 'foo=bar'
        assert a.satisfies(b)

        # 'foo=bar' does not satisfy 'foo=bar,baz'
        assert not b.satisfies(a)

        # 'foo=bar,baz' does not satisfy 'foo=bar,baz' and vice-versa
        assert not a.satisfies(c)
        assert not c.satisfies(a)

        # Implicit type conversion for variants of other types

        b_sv = SingleValuedVariant("foo", "bar")
        assert b.satisfies(b_sv)
        d_sv = SingleValuedVariant("foo", "True")
        assert d.satisfies(d_sv)
        almost_d_bv = SingleValuedVariant("foo", "true")
        assert not d.satisfies(almost_d_bv)

        d_bv = BoolValuedVariant("foo", "True")
        assert d.satisfies(d_bv)
        # This case is 'peculiar': the two BV instances are
        # equivalent, but if converted to MV they are not
        # as MV is case sensitive with respect to 'True' and 'False'
        almost_d_bv = BoolValuedVariant("foo", "true")
        assert not d.satisfies(almost_d_bv)

    def test_compatible(self):
        a = MultiValuedVariant("foo", "bar,baz")
        b = MultiValuedVariant("foo", "True")
        c = MultiValuedVariant("fee", "bar,baz")
        d = MultiValuedVariant("foo", "bar,barbaz")

        # If the name of two multi-valued variants is the same,
        # they are compatible
        assert a.compatible(b)
        assert not a.compatible(c)
        assert a.compatible(d)

        assert b.compatible(a)
        assert not b.compatible(c)
        assert b.compatible(d)

        assert not c.compatible(a)
        assert not c.compatible(b)
        assert not c.compatible(d)

        assert d.compatible(a)
        assert d.compatible(b)
        assert not d.compatible(c)

        # Implicit type conversion for other types

        b_sv = SingleValuedVariant("foo", "True")
        assert b.compatible(b_sv)
        assert not c.compatible(b_sv)

        b_bv = BoolValuedVariant("foo", "True")
        assert b.compatible(b_bv)
        assert not c.compatible(b_bv)

    def test_constrain(self):
        # Try to constrain on a value with less constraints than self
        a = MultiValuedVariant("foo", "bar,baz")
        b = MultiValuedVariant("foo", "bar")

        changed = a.constrain(b)
        assert not changed
        t = MultiValuedVariant("foo", "bar,baz")
        assert a == t

        # Try to constrain on a value with more constraints than self
        a = MultiValuedVariant("foo", "bar,baz")
        b = MultiValuedVariant("foo", "bar")

        changed = b.constrain(a)
        assert changed
        t = MultiValuedVariant("foo", "bar,baz")
        assert a == t

        # Try to constrain on the same value
        a = MultiValuedVariant("foo", "bar,baz")
        b = a.copy()

        changed = a.constrain(b)
        assert not changed
        t = MultiValuedVariant("foo", "bar,baz")
        assert a == t

        # Try to constrain on a different name
        a = MultiValuedVariant("foo", "bar,baz")
        b = MultiValuedVariant("fee", "bar")

        with pytest.raises(ValueError):
            a.constrain(b)

        # Implicit type conversion for variants of other types

        a = MultiValuedVariant("foo", "bar,baz")
        b_sv = SingleValuedVariant("foo", "bar")
        c_sv = SingleValuedVariant("foo", "barbaz")

        assert not a.constrain(b_sv)
        assert a.constrain(c_sv)

        d_bv = BoolValuedVariant("foo", "True")

        assert a.constrain(d_bv)
        assert not a.constrain(d_bv)

    def test_yaml_entry(self):
        a = MultiValuedVariant("foo", "bar,baz,barbaz")
        b = MultiValuedVariant("foo", "bar, baz,  barbaz")
        expected = ("foo", sorted(["bar", "baz", "barbaz"]))

        assert a.yaml_entry() == expected
        assert b.yaml_entry() == expected

        a = MultiValuedVariant("foo", "bar")
        expected = ("foo", sorted(["bar"]))

        assert a.yaml_entry() == expected


class TestSingleValuedVariant:
    def test_initialization(self):
        # Basic properties
        a = SingleValuedVariant("foo", "bar")
        assert repr(a) == "SingleValuedVariant('foo', 'bar')"
        assert str(a) == "foo=bar"
        assert a.value == "bar"
        assert "bar" in a
        assert eval(repr(a)) == a

        # Raise if multiple values are passed
        with pytest.raises(ValueError):
            SingleValuedVariant("foo", "bar, baz")

        # Check the copy
        b = a.copy()
        assert repr(a) == repr(b)
        assert str(a) == str(b)
        assert b.value == "bar"
        assert "bar" in b
        assert a == b
        assert a is not b
        assert hash(a) == hash(b)
        assert eval(repr(b)) == a

    def test_satisfies(self):
        a = SingleValuedVariant("foo", "bar")
        b = SingleValuedVariant("foo", "bar")
        c = SingleValuedVariant("foo", "baz")
        d = SingleValuedVariant("fee", "bar")
        e = SingleValuedVariant("foo", "True")

        # 'foo=bar' can only satisfy 'foo=bar'
        assert a.satisfies(b)
        assert not a.satisfies(c)
        assert not a.satisfies(d)

        assert b.satisfies(a)
        assert not b.satisfies(c)
        assert not b.satisfies(d)

        assert not c.satisfies(a)
        assert not c.satisfies(b)
        assert not c.satisfies(d)

        # Implicit type conversion for variants of other types

        a_mv = MultiValuedVariant("foo", "bar")
        assert a.satisfies(a_mv)
        multiple_values = MultiValuedVariant("foo", "bar,baz")
        assert not a.satisfies(multiple_values)

        e_bv = BoolValuedVariant("foo", "True")
        assert e.satisfies(e_bv)
        almost_e_bv = BoolValuedVariant("foo", "true")
        assert not e.satisfies(almost_e_bv)

    def test_compatible(self):
        a = SingleValuedVariant("foo", "bar")
        b = SingleValuedVariant("fee", "bar")
        c = SingleValuedVariant("foo", "baz")
        d = SingleValuedVariant("foo", "bar")

        # If the name of two multi-valued variants is the same,
        # they are compatible
        assert not a.compatible(b)
        assert not a.compatible(c)
        assert a.compatible(d)

        assert not b.compatible(a)
        assert not b.compatible(c)
        assert not b.compatible(d)

        assert not c.compatible(a)
        assert not c.compatible(b)
        assert not c.compatible(d)

        assert d.compatible(a)
        assert not d.compatible(b)
        assert not d.compatible(c)

        # Implicit type conversion for variants of other types

        a_mv = MultiValuedVariant("foo", "bar")
        b_mv = MultiValuedVariant("fee", "bar")
        c_mv = MultiValuedVariant("foo", "baz")
        d_mv = MultiValuedVariant("foo", "bar")

        assert not a.compatible(b_mv)
        assert not a.compatible(c_mv)
        assert a.compatible(d_mv)

        assert not b.compatible(a_mv)
        assert not b.compatible(c_mv)
        assert not b.compatible(d_mv)

        assert not c.compatible(a_mv)
        assert not c.compatible(b_mv)
        assert not c.compatible(d_mv)

        assert d.compatible(a_mv)
        assert not d.compatible(b_mv)
        assert not d.compatible(c_mv)

        e = SingleValuedVariant("foo", "True")
        e_bv = BoolValuedVariant("foo", "True")
        almost_e_bv = BoolValuedVariant("foo", "true")

        assert e.compatible(e_bv)
        assert not e.compatible(almost_e_bv)

    def test_constrain(self):
        # Try to constrain on a value equal to self
        a = SingleValuedVariant("foo", "bar")
        b = SingleValuedVariant("foo", "bar")

        changed = a.constrain(b)
        assert not changed
        t = SingleValuedVariant("foo", "bar")
        assert a == t

        # Try to constrain on a value with a different value
        a = SingleValuedVariant("foo", "bar")
        b = SingleValuedVariant("foo", "baz")

        with pytest.raises(UnsatisfiableVariantSpecError):
            b.constrain(a)

        # Try to constrain on a value with a different value
        a = SingleValuedVariant("foo", "bar")
        b = SingleValuedVariant("fee", "bar")

        with pytest.raises(ValueError):
            b.constrain(a)

        # Try to constrain on the same value
        a = SingleValuedVariant("foo", "bar")
        b = a.copy()

        changed = a.constrain(b)
        assert not changed
        t = SingleValuedVariant("foo", "bar")
        assert a == t

        # Implicit type conversion for variants of other types
        a = SingleValuedVariant("foo", "True")
        mv = MultiValuedVariant("foo", "True")
        bv = BoolValuedVariant("foo", "True")
        for v in (mv, bv):
            assert not a.constrain(v)

    def test_yaml_entry(self):
        a = SingleValuedVariant("foo", "bar")
        expected = ("foo", "bar")

        assert a.yaml_entry() == expected


class TestBoolValuedVariant:
    def test_initialization(self):
        # Basic properties - True value
        for v in (True, "True", "TRUE", "TrUe"):
            a = BoolValuedVariant("foo", v)
            assert repr(a) == "BoolValuedVariant('foo', {0})".format(repr(v))
            assert str(a) == "+foo"
            assert a.value is True
            assert True in a
            assert eval(repr(a)) == a

        # Copy - True value
        b = a.copy()
        assert repr(a) == repr(b)
        assert str(a) == str(b)
        assert b.value is True
        assert True in b
        assert a == b
        assert a is not b
        assert hash(a) == hash(b)
        assert eval(repr(b)) == a

        # Basic properties - False value
        for v in (False, "False", "FALSE", "FaLsE"):
            a = BoolValuedVariant("foo", v)
            assert repr(a) == "BoolValuedVariant('foo', {0})".format(repr(v))
            assert str(a) == "~foo"
            assert a.value is False
            assert False in a
            assert eval(repr(a)) == a

        # Copy - True value
        b = a.copy()
        assert repr(a) == repr(b)
        assert str(a) == str(b)
        assert b.value is False
        assert False in b
        assert a == b
        assert a is not b
        assert eval(repr(b)) == a

        # Invalid values
        for v in ("bar", "bar,baz"):
            with pytest.raises(ValueError):
                BoolValuedVariant("foo", v)

    def test_satisfies(self):
        a = BoolValuedVariant("foo", True)
        b = BoolValuedVariant("foo", False)
        c = BoolValuedVariant("fee", False)
        d = BoolValuedVariant("foo", "True")

        assert not a.satisfies(b)
        assert not a.satisfies(c)
        assert a.satisfies(d)

        assert not b.satisfies(a)
        assert not b.satisfies(c)
        assert not b.satisfies(d)

        assert not c.satisfies(a)
        assert not c.satisfies(b)
        assert not c.satisfies(d)

        assert d.satisfies(a)
        assert not d.satisfies(b)
        assert not d.satisfies(c)

        # BV variants are case insensitive to 'True' or 'False'
        d_mv = MultiValuedVariant("foo", "True")
        assert d.satisfies(d_mv)
        assert not b.satisfies(d_mv)

        d_mv = MultiValuedVariant("foo", "FaLsE")
        assert not d.satisfies(d_mv)
        assert b.satisfies(d_mv)

        d_mv = MultiValuedVariant("foo", "bar")
        assert not d.satisfies(d_mv)
        assert not b.satisfies(d_mv)

        d_sv = SingleValuedVariant("foo", "True")
        assert d.satisfies(d_sv)

    def test_compatible(self):
        a = BoolValuedVariant("foo", True)
        b = BoolValuedVariant("fee", True)
        c = BoolValuedVariant("foo", False)
        d = BoolValuedVariant("foo", "True")

        # If the name of two multi-valued variants is the same,
        # they are compatible
        assert not a.compatible(b)
        assert not a.compatible(c)
        assert a.compatible(d)

        assert not b.compatible(a)
        assert not b.compatible(c)
        assert not b.compatible(d)

        assert not c.compatible(a)
        assert not c.compatible(b)
        assert not c.compatible(d)

        assert d.compatible(a)
        assert not d.compatible(b)
        assert not d.compatible(c)

        for value in ("True", "TrUe", "TRUE"):
            d_mv = MultiValuedVariant("foo", value)
            assert d.compatible(d_mv)
            assert not c.compatible(d_mv)

            d_sv = SingleValuedVariant("foo", value)
            assert d.compatible(d_sv)
            assert not c.compatible(d_sv)

    def test_constrain(self):
        # Try to constrain on a value equal to self
        a = BoolValuedVariant("foo", "True")
        b = BoolValuedVariant("foo", True)

        changed = a.constrain(b)
        assert not changed
        t = BoolValuedVariant("foo", True)
        assert a == t

        # Try to constrain on a value with a different value
        a = BoolValuedVariant("foo", True)
        b = BoolValuedVariant("foo", False)

        with pytest.raises(UnsatisfiableVariantSpecError):
            b.constrain(a)

        # Try to constrain on a value with a different value
        a = BoolValuedVariant("foo", True)
        b = BoolValuedVariant("fee", True)

        with pytest.raises(ValueError):
            b.constrain(a)

        # Try to constrain on the same value
        a = BoolValuedVariant("foo", True)
        b = a.copy()

        changed = a.constrain(b)
        assert not changed
        t = BoolValuedVariant("foo", True)
        assert a == t

        # Try to constrain on other values
        a = BoolValuedVariant("foo", "True")
        sv = SingleValuedVariant("foo", "True")
        mv = MultiValuedVariant("foo", "True")
        for v in (sv, mv):
            assert not a.constrain(v)

    def test_yaml_entry(self):
        a = BoolValuedVariant("foo", "True")
        expected = ("foo", True)
        assert a.yaml_entry() == expected

        a = BoolValuedVariant("foo", "False")
        expected = ("foo", False)
        assert a.yaml_entry() == expected


def test_from_node_dict():
    a = MultiValuedVariant.from_node_dict("foo", ["bar"])
    assert type(a) is MultiValuedVariant

    a = MultiValuedVariant.from_node_dict("foo", "bar")
    assert type(a) is SingleValuedVariant

    a = MultiValuedVariant.from_node_dict("foo", "true")
    assert type(a) is BoolValuedVariant


class TestVariant:
    def test_validation(self):
        a = Variant(
            "foo", default="", description="", values=("bar", "baz", "foobar"), multi=False
        )
        # Valid vspec, shouldn't raise
        vspec = a.make_variant("bar")
        a.validate_or_raise(vspec, "test-package")

        # Multiple values are not allowed
        with pytest.raises(MultipleValuesInExclusiveVariantError):
            vspec.value = "bar,baz"

        # Inconsistent vspec
        vspec.name = "FOO"
        with pytest.raises(InconsistentValidationError):
            a.validate_or_raise(vspec, "test-package")

        # Valid multi-value vspec
        a.multi = True
        vspec = a.make_variant("bar,baz")
        a.validate_or_raise(vspec, "test-package")
        # Add an invalid value
        vspec.value = "bar,baz,barbaz"
        with pytest.raises(InvalidVariantValueError):
            a.validate_or_raise(vspec, "test-package")

    def test_callable_validator(self):
        def validator(x):
            try:
                return isinstance(int(x), numbers.Integral)
            except ValueError:
                return False

        a = Variant("foo", default=1024, description="", values=validator, multi=False)
        vspec = a.make_default()
        a.validate_or_raise(vspec, "test-package")
        vspec.value = 2056
        a.validate_or_raise(vspec, "test-package")
        vspec.value = "foo"
        with pytest.raises(InvalidVariantValueError):
            a.validate_or_raise(vspec, "test-package")

    def test_representation(self):
        a = Variant(
            "foo", default="", description="", values=("bar", "baz", "foobar"), multi=False
        )
        assert a.allowed_values == "bar, baz, foobar"

    def test_str(self):
        string = str(
            Variant(
                "foo", default="", description="", values=("bar", "baz", "foobar"), multi=False
            )
        )
        assert "'foo'" in string
        assert "default=''" in string
        assert "description=''" in string
        assert "values=('foo', 'bar', 'baz') in string"


class TestVariantMapTest:
    def test_invalid_values(self) -> None:
        # Value with invalid type
        a = VariantMap(Spec())
        with pytest.raises(TypeError):
            a["foo"] = 2

        # Duplicate variant
        a["foo"] = MultiValuedVariant("foo", "bar,baz")
        with pytest.raises(DuplicateVariantError):
            a["foo"] = MultiValuedVariant("foo", "bar")

        with pytest.raises(DuplicateVariantError):
            a["foo"] = SingleValuedVariant("foo", "bar")

        with pytest.raises(DuplicateVariantError):
            a["foo"] = BoolValuedVariant("foo", True)

        # Non matching names between key and vspec.name
        with pytest.raises(KeyError):
            a["bar"] = MultiValuedVariant("foo", "bar")

    def test_set_item(self) -> None:
        # Check that all the three types of variants are accepted
        a = VariantMap(Spec())

        a["foo"] = BoolValuedVariant("foo", True)
        a["bar"] = SingleValuedVariant("bar", "baz")
        a["foobar"] = MultiValuedVariant("foobar", "a, b, c, d, e")

    def test_substitute(self) -> None:
        # Check substitution of a key that exists
        a = VariantMap(Spec())
        a["foo"] = BoolValuedVariant("foo", True)
        a.substitute(SingleValuedVariant("foo", "bar"))

        # Trying to substitute something that is not
        # in the map will raise a KeyError
        with pytest.raises(KeyError):
            a.substitute(BoolValuedVariant("bar", True))

    def test_satisfies_and_constrain(self) -> None:
        # foo=bar foobar=fee feebar=foo
        a = VariantMap(Spec())
        a["foo"] = MultiValuedVariant("foo", "bar")
        a["foobar"] = SingleValuedVariant("foobar", "fee")
        a["feebar"] = SingleValuedVariant("feebar", "foo")

        # foo=bar,baz foobar=fee shared=True
        b = VariantMap(Spec())
        b["foo"] = MultiValuedVariant("foo", "bar, baz")
        b["foobar"] = SingleValuedVariant("foobar", "fee")
        b["shared"] = BoolValuedVariant("shared", True)

        assert a.intersects(b)
        assert b.intersects(a)

        assert not a.satisfies(b)
        assert not b.satisfies(a)

        # foo=bar,baz foobar=fee feebar=foo shared=True
        c = VariantMap(Spec())
        c["foo"] = MultiValuedVariant("foo", "bar, baz")
        c["foobar"] = SingleValuedVariant("foobar", "fee")
        c["feebar"] = SingleValuedVariant("feebar", "foo")
        c["shared"] = BoolValuedVariant("shared", True)

        assert a.constrain(b)
        assert a == c

    def test_copy(self) -> None:
        a = VariantMap(Spec())
        a["foo"] = BoolValuedVariant("foo", True)
        a["bar"] = SingleValuedVariant("bar", "baz")
        a["foobar"] = MultiValuedVariant("foobar", "a, b, c, d, e")

        c = a.copy()
        assert a == c

    def test_str(self) -> None:
        c = VariantMap(Spec())
        c["foo"] = MultiValuedVariant("foo", "bar, baz")
        c["foobar"] = SingleValuedVariant("foobar", "fee")
        c["feebar"] = SingleValuedVariant("feebar", "foo")
        c["shared"] = BoolValuedVariant("shared", True)
        assert str(c) == "+shared feebar=foo foo=bar,baz foobar=fee"

    def test_concrete(self, mock_packages, config) -> None:
        spec = Spec("pkg-a")
        vm = VariantMap(spec)
        assert not vm.concrete

        # concrete if associated spec is concrete
        spec.concretize()
        assert vm.concrete

        # concrete if all variants are present (even if spec not concrete)
        spec._mark_concrete(False)
        assert spec.variants.concrete

        # remove a variant to test the condition
        del spec.variants["foo"]
        assert not spec.variants.concrete


def test_disjoint_set_initialization_errors():
    # Constructing from non-disjoint sets should raise an exception
    with pytest.raises(spack.error.SpecError) as exc_info:
        disjoint_sets(("a", "b"), ("b", "c"))
    assert "sets in input must be disjoint" in str(exc_info.value)

    # A set containing the reserved item 'none' along with other items
    # should raise an exception
    with pytest.raises(spack.error.SpecError) as exc_info:
        disjoint_sets(("a", "b"), ("none", "c"))
    assert "The value 'none' represents the empty set," in str(exc_info.value)


def test_disjoint_set_initialization():
    # Test that no error is thrown when the sets are disjoint
    d = disjoint_sets(("a",), ("b", "c"), ("e", "f"))

    assert d.default == "none"
    assert d.multi is True
    assert set(x for x in d) == set(["none", "a", "b", "c", "e", "f"])


def test_disjoint_set_fluent_methods():
    # Construct an object without the empty set
    d = disjoint_sets(("a",), ("b", "c"), ("e", "f")).prohibit_empty_set()
    assert set(("none",)) not in d.sets

    # Call this 2 times to check that no matter whether
    # the empty set was allowed or not before, the state
    # returned is consistent.
    for _ in range(2):
        d = d.allow_empty_set()
        assert set(("none",)) in d.sets
        assert "none" in d
        assert "none" in [x for x in d]
        assert "none" in d.feature_values

    # Marking a value as 'non-feature' removes it from the
    # list of feature values, but not for the items returned
    # when iterating over the object.
    d = d.with_non_feature_values("none")
    assert "none" in d
    assert "none" in [x for x in d]
    assert "none" not in d.feature_values

    # Call this 2 times to check that no matter whether
    # the empty set was allowed or not before, the state
    # returned is consistent.
    for _ in range(2):
        d = d.prohibit_empty_set()
        assert set(("none",)) not in d.sets
        assert "none" not in d
        assert "none" not in [x for x in d]
        assert "none" not in d.feature_values


@pytest.mark.regression("32694")
@pytest.mark.parametrize("other", [True, False])
def test_conditional_value_comparable_to_bool(other):
    value = spack.variant.Value("98", when="@1.0")
    comparison = value == other
    assert comparison is False


@pytest.mark.regression("40405")
def test_wild_card_valued_variants_equivalent_to_str():
    """
    There was a bug prioro to PR 40406 in that variants with wildcard values "*"
    were being overwritten in the variant constructor.
    The expected/appropriate behavior is for it to behave like value=str and this
    test demonstrates that the two are now equivalent
    """
    str_var = spack.variant.Variant(
        name="str_var",
        default="none",
        values=str,
        description="str variant",
        multi=True,
        validator=None,
    )

    wild_var = spack.variant.Variant(
        name="wild_var",
        default="none",
        values="*",
        description="* variant",
        multi=True,
        validator=None,
    )

    several_arbitrary_values = ("doe", "re", "mi")
    # "*" case
    wild_output = wild_var.make_variant(several_arbitrary_values)
    wild_var.validate_or_raise(wild_output, "test-package")
    # str case
    str_output = str_var.make_variant(several_arbitrary_values)
    str_var.validate_or_raise(str_output, "test-package")
    # equivalence each instance already validated
    assert str_output.value == wild_output.value


def test_variant_definitions(mock_packages):
    pkg = spack.repo.PATH.get_pkg_class("variant-values")

    # two variant names
    assert len(pkg.variant_names()) == 2
    assert "build_system" in pkg.variant_names()
    assert "v" in pkg.variant_names()

    # this name doesn't exist
    assert len(pkg.variant_definitions("no-such-variant")) == 0

    # there are 4 definitions but one is completely shadowed by another
    assert len(pkg.variants) == 4

    # variant_items ignores the shadowed definition
    assert len(list(pkg.variant_items())) == 3

    # variant_definitions also ignores the shadowed definition
    defs = [vdef for _, vdef in pkg.variant_definitions("v")]
    assert len(defs) == 2
    assert defs[0].default == "foo"
    assert defs[0].values == ("foo",)

    assert defs[1].default == "bar"
    assert defs[1].values == ("foo", "bar")


@pytest.mark.parametrize(
    "pkg_name,value,spec,def_ids",
    [
        ("variant-values", "foo", "", [0, 1]),
        ("variant-values", "bar", "", [1]),
        ("variant-values", "foo", "@1.0", [0]),
        ("variant-values", "foo", "@2.0", [1]),
        ("variant-values", "foo", "@3.0", [1]),
        ("variant-values", "foo", "@4.0", []),
        ("variant-values", "bar", "@2.0", [1]),
        ("variant-values", "bar", "@3.0", [1]),
        ("variant-values", "bar", "@4.0", []),
        # now with a global override
        ("variant-values-override", "bar", "", [0]),
        ("variant-values-override", "bar", "@1.0", [0]),
        ("variant-values-override", "bar", "@2.0", [0]),
        ("variant-values-override", "bar", "@3.0", [0]),
        ("variant-values-override", "bar", "@4.0", [0]),
        ("variant-values-override", "baz", "", [0]),
        ("variant-values-override", "baz", "@2.0", [0]),
        ("variant-values-override", "baz", "@3.0", [0]),
        ("variant-values-override", "baz", "@4.0", [0]),
    ],
)
def test_prevalidate_variant_value(mock_packages, pkg_name, value, spec, def_ids):
    pkg = spack.repo.PATH.get_pkg_class(pkg_name)

    all_defs = [vdef for _, vdef in pkg.variant_definitions("v")]

    valid_defs = spack.variant.prevalidate_variant_value(
        pkg, SingleValuedVariant("v", value), spack.spec.Spec(spec)
    )
    assert len(valid_defs) == len(def_ids)

    for vdef, i in zip(valid_defs, def_ids):
        assert vdef is all_defs[i]


@pytest.mark.parametrize(
    "pkg_name,value,spec",
    [
        ("variant-values", "baz", ""),
        ("variant-values", "bar", "@1.0"),
        ("variant-values", "bar", "@4.0"),
        ("variant-values", "baz", "@3.0"),
        ("variant-values", "baz", "@4.0"),
        # and with override
        ("variant-values-override", "foo", ""),
        ("variant-values-override", "foo", "@1.0"),
        ("variant-values-override", "foo", "@2.0"),
        ("variant-values-override", "foo", "@3.0"),
        ("variant-values-override", "foo", "@4.0"),
    ],
)
def test_strict_invalid_variant_values(mock_packages, pkg_name, value, spec):
    pkg = spack.repo.PATH.get_pkg_class(pkg_name)

    with pytest.raises(spack.variant.InvalidVariantValueError):
        spack.variant.prevalidate_variant_value(
            pkg, SingleValuedVariant("v", value), spack.spec.Spec(spec), strict=True
        )


@pytest.mark.parametrize(
    "pkg_name,spec,satisfies,def_id",
    [
        ("variant-values", "@1.0", "v=foo", 0),
        ("variant-values", "@2.0", "v=bar", 1),
        ("variant-values", "@3.0", "v=bar", 1),
        ("variant-values-override", "@1.0", "v=baz", 0),
        ("variant-values-override", "@2.0", "v=baz", 0),
        ("variant-values-override", "@3.0", "v=baz", 0),
    ],
)
def test_concretize_variant_default_with_multiple_defs(
    mock_packages, config, pkg_name, spec, satisfies, def_id
):
    pkg = spack.repo.PATH.get_pkg_class(pkg_name)
    pkg_defs = [vdef for _, vdef in pkg.variant_definitions("v")]

    spec = spack.spec.Spec(f"{pkg_name}{spec}").concretized()
    assert spec.satisfies(satisfies)
    assert spec.package.get_variant("v") is pkg_defs[def_id]


@pytest.mark.parametrize(
    "spec,variant_name,after",
    [
        # dev_path is a special case
        ("foo dev_path=/path/to/source", "dev_path", SingleValuedVariant),
        # reserved name: won't be touched
        ("foo patches=2349dc44", "patches", AbstractVariant),
        # simple case -- one definition applies
        ("variant-values@1.0 v=foo", "v", SingleValuedVariant),
        # simple, but with bool valued variant
        ("pkg-a bvv=true", "bvv", BoolValuedVariant),
        # variant doesn't exist at version
        ("variant-values@4.0 v=bar", "v", spack.spec.InvalidVariantForSpecError),
        # multiple definitions, so not yet knowable
        ("variant-values@2.0 v=bar", "v", AbstractVariant),
    ],
)
def test_substitute_abstract_variants(mock_packages, spec, variant_name, after):
    spec = Spec(spec)

    # all variants start out as AbstractVariant
    assert isinstance(spec.variants[variant_name], AbstractVariant)

    if issubclass(after, Exception):
        # if we're checking for an error, use pytest.raises
        with pytest.raises(after):
            spack.spec.substitute_abstract_variants(spec)
    else:
        # ensure that the type of the variant on the spec has been narrowed (or not)
        spack.spec.substitute_abstract_variants(spec)
        assert isinstance(spec.variants[variant_name], after)
