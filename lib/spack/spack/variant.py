# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""The variant module contains data structures that are needed to manage
variants both in packages and in specs.
"""
import collections.abc
import enum
import functools
import inspect
import itertools
import re
from typing import Any, Callable, Collection, Iterable, List, Optional, Tuple, Type, Union

import llnl.util.lang as lang
import llnl.util.tty.color

import spack.error as error
import spack.parser
import spack.spec

#: These are variant names used by Spack internally; packages can't use them
reserved_names = [
    "arch",
    "architecture",
    "dev_path",
    "namespace",
    "operating_system",
    "os",
    "patches",
    "platform",
    "target",
]

special_variant_values = [None, "none", "*"]


class VariantType(enum.Enum):
    """Enum representing the three concrete variant types."""

    MULTI = "multi"
    BOOL = "bool"
    SINGLE = "single"

    @property
    def variant_class(self) -> Type:
        if self is self.MULTI:
            return MultiValuedVariant
        elif self is self.BOOL:
            return BoolValuedVariant
        else:
            return SingleValuedVariant


class Variant:
    """Represents a variant definition, created by the ``variant()`` directive.

    There can be multiple definitions of the same variant, and they are given precedence
    by order of appearance in the package. Later definitions have higher precedence.
    Similarly, definitions in derived classes have higher precedence than those in their
    superclasses.

    """

    name: str
    default: Any
    description: str
    values: Optional[Collection]  #: if None, valid values are defined only by validators
    multi: bool
    single_value_validator: Callable
    group_validator: Optional[Callable]
    sticky: bool
    precedence: int

    def __init__(
        self,
        name: str,
        *,
        default: Any,
        description: str,
        values: Union[Collection, Callable] = (True, False),
        multi: bool = False,
        validator: Optional[Callable] = None,
        sticky: bool = False,
        precedence: int = 0,
    ):
        """Initialize a package variant.

        Args:
            name: name of the variant
            default: default value for the variant, used when nothing is explicitly specified
            description: purpose of the variant
            values: sequence of allowed values or a callable accepting a single value as argument
                and returning True if the value is good, False otherwise
            multi: whether multiple values are allowed
            validator: optional callable that can be used to perform additional validation
            sticky: if true the variant is set to the default value at concretization time
            precedence: int indicating precedence of this variant definition in the solve
                (definition with highest precedence is used when multiple definitions are possible)
        """
        self.name = name
        self.default = default
        self.description = str(description)

        self.values = None
        if values == "*":
            # wildcard is a special case to make it easy to say any value is ok
            self.single_value_validator = lambda v: True

        elif isinstance(values, type):
            # supplying a type means any value *of that type*
            def isa_type(v):
                try:
                    values(v)
                    return True
                except ValueError:
                    return False

            self.single_value_validator = isa_type

        elif callable(values):
            # If 'values' is a callable, assume it is a single value
            # validator and reset the values to be explicit during debug
            self.single_value_validator = values
        else:
            # Otherwise, assume values is the set of allowed explicit values
            values = _flatten(values)
            self.values = values
            self.single_value_validator = lambda v: v in values

        self.multi = multi
        self.group_validator = validator
        self.sticky = sticky
        self.precedence = precedence

    def validate_or_raise(self, vspec: "AbstractVariant", pkg_name: str):
        """Validate a variant spec against this package variant. Raises an
        exception if any error is found.

        Args:
            vspec: variant spec to be validated
            pkg_name: the name of the package class that required this validation (for errors)

        Raises:
            InconsistentValidationError: if ``vspec.name != self.name``

            MultipleValuesInExclusiveVariantError: if ``vspec`` has
                multiple values but ``self.multi == False``

            InvalidVariantValueError: if ``vspec.value`` contains
                invalid values
        """
        # Check the name of the variant
        if self.name != vspec.name:
            raise InconsistentValidationError(vspec, self)

        # If the value is exclusive there must be at most one
        value = vspec.value_as_tuple
        if not self.multi and len(value) != 1:
            raise MultipleValuesInExclusiveVariantError(vspec, pkg_name)

        # Check and record the values that are not allowed
        invalid_vals = ", ".join(
            f"'{v}'" for v in value if v != "*" and self.single_value_validator(v) is False
        )
        if invalid_vals:
            raise InvalidVariantValueError(
                f"invalid values for variant '{self.name}' in package {pkg_name}: {invalid_vals}\n"
            )

        # Validate the group of values if needed
        if self.group_validator is not None and value != ("*",):
            self.group_validator(pkg_name, self.name, value)

    @property
    def allowed_values(self):
        """Returns a string representation of the allowed values for
        printing purposes

        Returns:
            str: representation of the allowed values
        """
        # Join an explicit set of allowed values
        if self.values is not None:
            v = tuple(str(x) for x in self.values)
            return ", ".join(v)
        # In case we were given a single-value validator
        # print the docstring
        docstring = inspect.getdoc(self.single_value_validator)
        v = docstring if docstring else ""
        return v

    def make_default(self):
        """Factory that creates a variant holding the default value.

        Returns:
            MultiValuedVariant or SingleValuedVariant or BoolValuedVariant:
                instance of the proper variant
        """
        return self.make_variant(self.default)

    def make_variant(self, value) -> "AbstractVariant":
        """Factory that creates a variant holding the value passed as
        a parameter.

        Args:
            value: value that will be hold by the variant

        Returns:
            MultiValuedVariant or SingleValuedVariant or BoolValuedVariant:
                instance of the proper variant
        """
        return self.variant_type.variant_class(self.name, value)

    @property
    def variant_type(self) -> VariantType:
        """String representation of the type of this variant (single/multi/bool)"""
        if self.multi:
            return VariantType.MULTI
        elif self.values == (True, False):
            return VariantType.BOOL
        else:
            return VariantType.SINGLE

    def __str__(self):
        return (
            f"Variant('{self.name}', "
            f"default='{self.default}', "
            f"description='{self.description}', "
            f"values={self.values}, "
            f"multi={self.multi}, "
            f"single_value_validator={self.single_value_validator}, "
            f"group_validator={self.group_validator}, "
            f"sticky={self.sticky}, "
            f"precedence={self.precedence})"
        )


def implicit_variant_conversion(method):
    """Converts other to type(self) and calls method(self, other)

    Args:
        method: any predicate method that takes another variant as an argument

    Returns: decorated method
    """

    @functools.wraps(method)
    def convert(self, other):
        # We don't care if types are different as long as I can convert other to type(self)
        try:
            other = type(self)(other.name, other._original_value)
        except (error.SpecError, ValueError):
            return False
        return method(self, other)

    return convert


def _flatten(values) -> Collection:
    """Flatten instances of _ConditionalVariantValues for internal representation"""
    if isinstance(values, DisjointSetsOfValues):
        return values

    flattened: List = []
    for item in values:
        if isinstance(item, _ConditionalVariantValues):
            flattened.extend(item)
        else:
            flattened.append(item)
    # There are parts of the variant checking mechanism that expect to find tuples
    # here, so it is important to convert the type once we flattened the values.
    return tuple(flattened)


#: Type for value of a variant
ValueType = Union[str, bool, Tuple[Union[str, bool], ...]]

#: Type of variant value when output for JSON, YAML, etc.
SerializedValueType = Union[str, bool, List[Union[str, bool]]]


@lang.lazy_lexicographic_ordering
class AbstractVariant:
    """A variant that has not yet decided who it wants to be. It behaves like
    a multi valued variant which **could** do things.

    This kind of variant is generated during parsing of expressions like
    ``foo=bar`` and differs from multi valued variants because it will
    satisfy any other variant with the same name. This is because it **could**
    do it if it grows up to be a multi valued variant with the right set of
    values.
    """

    name: str
    propagate: bool
    _value: ValueType
    _original_value: Any

    def __init__(self, name: str, value: Any, propagate: bool = False):
        self.name = name
        self.propagate = propagate

        # Invokes property setter
        self.value = value

    @staticmethod
    def from_node_dict(name: str, value: Union[str, List[str]]) -> "AbstractVariant":
        """Reconstruct a variant from a node dict."""
        if isinstance(value, list):
            # read multi-value variants in and be faithful to the YAML
            mvar = MultiValuedVariant(name, ())
            mvar._value = tuple(value)
            mvar._original_value = mvar._value
            return mvar

        elif str(value).upper() == "TRUE" or str(value).upper() == "FALSE":
            return BoolValuedVariant(name, value)

        return SingleValuedVariant(name, value)

    def yaml_entry(self) -> Tuple[str, SerializedValueType]:
        """Returns a key, value tuple suitable to be an entry in a yaml dict.

        Returns:
            tuple: (name, value_representation)
        """
        return self.name, list(self.value_as_tuple)

    @property
    def value_as_tuple(self) -> Tuple[Union[bool, str], ...]:
        """Getter for self.value that always returns a Tuple (even for single valued variants).

        This makes it easy to iterate over possible values.
        """
        if isinstance(self._value, (bool, str)):
            return (self._value,)
        return self._value

    @property
    def value(self) -> ValueType:
        """Returns a tuple of strings containing the values stored in
        the variant.

        Returns:
            tuple: values stored in the variant
        """
        return self._value

    @value.setter
    def value(self, value: ValueType) -> None:
        self._value_setter(value)

    def _value_setter(self, value: ValueType) -> None:
        # Store the original value
        self._original_value = value

        if not isinstance(value, (tuple, list)):
            # Store a tuple of CSV string representations
            # Tuple is necessary here instead of list because the
            # values need to be hashed
            value = tuple(re.split(r"\s*,\s*", str(value)))

        for val in special_variant_values:
            if val in value and len(value) > 1:
                msg = "'%s' cannot be combined with other variant" % val
                msg += " values."
                raise InvalidVariantValueCombinationError(msg)

        # With multi-value variants it is necessary
        # to remove duplicates and give an order
        # to a set
        self._value = tuple(sorted(set(value)))

    def _cmp_iter(self) -> Iterable:
        yield self.name
        yield from (str(v) for v in self.value_as_tuple)

    def copy(self) -> "AbstractVariant":
        """Returns an instance of a variant equivalent to self

        Returns:
            AbstractVariant: a copy of self

        >>> a = MultiValuedVariant('foo', True)
        >>> b = a.copy()
        >>> assert a == b
        >>> assert a is not b
        """
        return type(self)(self.name, self._original_value, self.propagate)

    @implicit_variant_conversion
    def satisfies(self, other: "AbstractVariant") -> bool:
        """Returns true if ``other.name == self.name``, because any value that
        other holds and is not in self yet **could** be added.

        Args:
            other: constraint to be met for the method to return True

        Returns:
            bool: True or False
        """
        # If names are different then `self` does not satisfy `other`
        # (`foo=bar` will never satisfy `baz=bar`)
        return other.name == self.name

    def intersects(self, other: "AbstractVariant") -> bool:
        """Returns True if there are variant matching both self and other, False otherwise."""
        if isinstance(other, (SingleValuedVariant, BoolValuedVariant)):
            return other.intersects(self)
        return other.name == self.name

    def compatible(self, other: "AbstractVariant") -> bool:
        """Returns True if self and other are compatible, False otherwise.

        As there is no semantic check, two VariantSpec are compatible if
        either they contain the same value or they are both multi-valued.

        Args:
            other: instance against which we test compatibility

        Returns:
            bool: True or False
        """
        # If names are different then `self` is not compatible with `other`
        # (`foo=bar` is incompatible with `baz=bar`)
        return self.intersects(other)

    @implicit_variant_conversion
    def constrain(self, other: "AbstractVariant") -> bool:
        """Modify self to match all the constraints for other if both
        instances are multi-valued. Returns True if self changed,
        False otherwise.

        Args:
            other: instance against which we constrain self

        Returns:
            bool: True or False
        """
        if self.name != other.name:
            raise ValueError("variants must have the same name")

        old_value = self.value

        values = list(sorted(set(self.value_as_tuple + other.value_as_tuple)))
        # If we constraint wildcard by another value, just take value
        if "*" in values and len(values) > 1:
            values.remove("*")

        self._value_setter(",".join(str(v) for v in values))
        return old_value != self.value

    def __contains__(self, item: Union[str, bool]) -> bool:
        return item in self.value_as_tuple

    def __repr__(self) -> str:
        return f"{type(self).__name__}({repr(self.name)}, {repr(self._original_value)})"

    def __str__(self) -> str:
        delim = "==" if self.propagate else "="
        values = spack.parser.quote_if_needed(",".join(str(v) for v in self.value_as_tuple))
        return f"{self.name}{delim}{values}"


class MultiValuedVariant(AbstractVariant):
    """A variant that can hold multiple values at once."""

    @implicit_variant_conversion
    def satisfies(self, other: AbstractVariant) -> bool:
        """Returns true if ``other.name == self.name`` and ``other.value`` is
        a strict subset of self. Does not try to validate.

        Args:
            other: constraint to be met for the method to return True

        Returns:
            bool: True or False
        """
        super_sat = super().satisfies(other)

        if not super_sat:
            return False

        if "*" in other or "*" in self:
            return True

        # allow prefix find on patches
        if self.name == "patches":
            return all(
                any(str(w).startswith(str(v)) for w in self.value_as_tuple)
                for v in other.value_as_tuple
            )

        # Otherwise we want all the values in `other` to be also in `self`
        return all(v in self for v in other.value_as_tuple)

    def append(self, value: Union[str, bool]) -> None:
        """Add another value to this multi-valued variant."""
        self._value = tuple(sorted((value,) + self.value_as_tuple))
        self._original_value = ",".join(str(v) for v in self._value)

    def __str__(self) -> str:
        # Special-case patches to not print the full 64 character sha256
        if self.name == "patches":
            values_str = ",".join(str(x)[:7] for x in self.value_as_tuple)
        else:
            values_str = ",".join(str(x) for x in self.value_as_tuple)

        delim = "==" if self.propagate else "="
        return f"{self.name}{delim}{spack.parser.quote_if_needed(values_str)}"


class SingleValuedVariant(AbstractVariant):
    """A variant that can hold multiple values, but one at a time."""

    def _value_setter(self, value: ValueType) -> None:
        # Treat the value as a multi-valued variant
        super()._value_setter(value)

        # Then check if there's only a single value
        values = self.value_as_tuple
        if len(values) != 1:
            raise MultipleValuesInExclusiveVariantError(self)

        self._value = values[0]

    @implicit_variant_conversion
    def satisfies(self, other: "AbstractVariant") -> bool:
        abstract_sat = super().satisfies(other)

        return abstract_sat and (
            self.value == other.value or other.value == "*" or self.value == "*"
        )

    def intersects(self, other: "AbstractVariant") -> bool:
        return self.satisfies(other)

    def compatible(self, other: "AbstractVariant") -> bool:
        return self.satisfies(other)

    @implicit_variant_conversion
    def constrain(self, other: "AbstractVariant") -> bool:
        if self.name != other.name:
            raise ValueError("variants must have the same name")

        if other.value == "*":
            return False

        if self.value == "*":
            self.value = other.value
            return True

        if self.value != other.value:
            raise UnsatisfiableVariantSpecError(other.value, self.value)
        return False

    def __contains__(self, item: ValueType) -> bool:
        return item == self.value

    def yaml_entry(self) -> Tuple[str, SerializedValueType]:
        assert isinstance(self.value, (bool, str))
        return self.name, self.value

    def __str__(self) -> str:
        delim = "==" if self.propagate else "="
        return f"{self.name}{delim}{spack.parser.quote_if_needed(str(self.value))}"


class BoolValuedVariant(SingleValuedVariant):
    """A variant that can hold either True or False.

    BoolValuedVariant can also hold the value '*', for coerced
    comparisons between ``foo=*`` and ``+foo`` or ``~foo``."""

    def _value_setter(self, value: ValueType) -> None:
        # Check the string representation of the value and turn
        # it to a boolean
        if str(value).upper() == "TRUE":
            self._original_value = value
            self._value = True
        elif str(value).upper() == "FALSE":
            self._original_value = value
            self._value = False
        elif str(value) == "*":
            self._original_value = value
            self._value = "*"
        else:
            msg = 'cannot construct a BoolValuedVariant for "{0}" from '
            msg += "a value that does not represent a bool"
            raise ValueError(msg.format(self.name))

    def __contains__(self, item: ValueType) -> bool:
        return item is self.value

    def __str__(self) -> str:
        sigil = "+" if self.value else "~"
        if self.propagate:
            sigil *= 2
        return f"{sigil}{self.name}"


# The class below inherit from Sequence to disguise as a tuple and comply
# with the semantic expected by the 'values' argument of the variant directive
class DisjointSetsOfValues(collections.abc.Sequence):
    """Allows combinations from one of many mutually exclusive sets.

    The value ``('none',)`` is reserved to denote the empty set
    and therefore no other set can contain the item ``'none'``.

    Args:
        *sets (list): mutually exclusive sets of values
    """

    _empty_set = set(("none",))

    def __init__(self, *sets):
        self.sets = [set(_flatten(x)) for x in sets]

        # 'none' is a special value and can appear only in a set of
        # a single element
        if any("none" in s and s != set(("none",)) for s in self.sets):
            raise error.SpecError(
                "The value 'none' represents the empty set,"
                " and must appear alone in a set. Use the "
                "method 'allow_empty_set' to add it."
            )

        # Sets should not intersect with each other
        if any(s1 & s2 for s1, s2 in itertools.combinations(self.sets, 2)):
            raise error.SpecError("sets in input must be disjoint")

        #: Attribute used to track values which correspond to
        #: features which can be enabled or disabled as understood by the
        #: package's build system.
        self.feature_values = tuple(itertools.chain.from_iterable(self.sets))
        self.default = None
        self.multi = True
        self.error_fmt = (
            "this variant accepts combinations of values from "
            "exactly one of the following sets '{values}' "
            "@*r{{[{package}, variant '{variant}']}}"
        )

    def with_default(self, default):
        """Sets the default value and returns self."""
        self.default = default
        return self

    def with_error(self, error_fmt):
        """Sets the error message format and returns self."""
        self.error_fmt = error_fmt
        return self

    def with_non_feature_values(self, *values):
        """Marks a few values as not being tied to a feature."""
        self.feature_values = tuple(x for x in self.feature_values if x not in values)
        return self

    def allow_empty_set(self):
        """Adds the empty set to the current list of disjoint sets."""
        if self._empty_set in self.sets:
            return self

        # Create a new object to be returned
        object_with_empty_set = type(self)(("none",), *self.sets)
        object_with_empty_set.error_fmt = self.error_fmt
        object_with_empty_set.feature_values = self.feature_values + ("none",)
        return object_with_empty_set

    def prohibit_empty_set(self):
        """Removes the empty set from the current list of disjoint sets."""
        if self._empty_set not in self.sets:
            return self

        # Create a new object to be returned
        sets = [s for s in self.sets if s != self._empty_set]
        object_without_empty_set = type(self)(*sets)
        object_without_empty_set.error_fmt = self.error_fmt
        object_without_empty_set.feature_values = tuple(
            x for x in self.feature_values if x != "none"
        )
        return object_without_empty_set

    def __getitem__(self, idx):
        return tuple(itertools.chain.from_iterable(self.sets))[idx]

    def __len__(self):
        return len(itertools.chain.from_iterable(self.sets))

    @property
    def validator(self):
        def _disjoint_set_validator(pkg_name, variant_name, values):
            # If for any of the sets, all the values are in it return True
            if any(all(x in s for x in values) for s in self.sets):
                return

            format_args = {"variant": variant_name, "package": pkg_name, "values": values}
            msg = self.error_fmt + " @*r{{[{package}, variant '{variant}']}}"
            msg = llnl.util.tty.color.colorize(msg.format(**format_args))
            raise error.SpecError(msg)

        return _disjoint_set_validator


def _a_single_value_or_a_combination(single_value, *values):
    error = "the value '" + single_value + "' is mutually exclusive with any of the other values"
    return (
        DisjointSetsOfValues((single_value,), values)
        .with_default(single_value)
        .with_error(error)
        .with_non_feature_values(single_value)
    )


# TODO: The factories below are used by package writers to set values of
# TODO: multi-valued variants. It could be worthwhile to gather them in
# TODO: a common namespace (like 'multi') in the future.


def any_combination_of(*values):
    """Multi-valued variant that allows any combination of the specified
    values, and also allows the user to specify 'none' (as a string) to choose
    none of them.

    It is up to the package implementation to handle the value 'none'
    specially, if at all.

    Args:
        *values: allowed variant values

    Returns:
        a properly initialized instance of DisjointSetsOfValues
    """
    return _a_single_value_or_a_combination("none", *values)


def auto_or_any_combination_of(*values):
    """Multi-valued variant that allows any combination of a set of values
    (but not the empty set) or 'auto'.

    Args:
        *values: allowed variant values

    Returns:
        a properly initialized instance of DisjointSetsOfValues
    """
    return _a_single_value_or_a_combination("auto", *values)


#: Multi-valued variant that allows any combination picking
#: from one of multiple disjoint sets
def disjoint_sets(*sets):
    """Multi-valued variant that allows any combination picking from one
    of multiple disjoint sets of values, and also allows the user to specify
    'none' (as a string) to choose none of them.

    It is up to the package implementation to handle the value 'none'
    specially, if at all.

    Args:
        *sets:

    Returns:
        a properly initialized instance of DisjointSetsOfValues
    """
    return DisjointSetsOfValues(*sets).allow_empty_set().with_default("none")


@functools.total_ordering
class Value:
    """Conditional value that might be used in variants."""

    value: Any
    when: Optional["spack.spec.Spec"]  # optional b/c we need to know about disabled values

    def __init__(self, value: Any, when: Optional["spack.spec.Spec"]):
        self.value = value
        self.when = when

    def __repr__(self):
        return f"Value({self.value}, when={self.when})"

    def __str__(self):
        return str(self.value)

    def __hash__(self):
        # Needed to allow testing the presence of a variant in a set by its value
        return hash(self.value)

    def __eq__(self, other):
        if isinstance(other, (str, bool)):
            return self.value == other
        return self.value == other.value

    def __lt__(self, other):
        if isinstance(other, str):
            return self.value < other
        return self.value < other.value


def prevalidate_variant_value(
    pkg_cls: "Type[spack.package_base.PackageBase]",
    variant: AbstractVariant,
    spec: Optional["spack.spec.Spec"] = None,
    strict: bool = False,
) -> List[Variant]:
    """Do as much validation of a variant value as is possible before concretization.

    This checks that the variant value is valid for *some* definition of the variant, and
    it raises if we know *before* concretization that the value cannot occur. On success
    it returns the variant definitions for which the variant is valid.

    Arguments:
        pkg_cls: package in which variant is (potentially multiply) defined
        variant: variant spec with value to validate
        spec: optionally restrict validation only to variants defined for this spec
        strict: if True, raise an exception if no variant definition is valid for any
            constraint on the spec.

    Return:
        list of variant definitions that will accept the given value. List will be empty
        only if the variant is a reserved variant.
    """
    # don't validate wildcards or variants with reserved names
    if variant.value == ("*",) or variant.name in reserved_names:
        return []

    # raise if there is no definition at all
    if not pkg_cls.has_variant(variant.name):
        raise UnknownVariantError(
            f"No such variant '{variant.name}' in package {pkg_cls.name}", [variant.name]
        )

    # do as much prevalidation as we can -- check only those
    # variants whose when constraint intersects this spec
    errors = []
    possible_definitions = []
    valid_definitions = []

    for when, pkg_variant_def in pkg_cls.variant_definitions(variant.name):
        if spec and not spec.intersects(when):
            continue
        possible_definitions.append(pkg_variant_def)

        try:
            pkg_variant_def.validate_or_raise(variant, pkg_cls.name)
            valid_definitions.append(pkg_variant_def)
        except spack.error.SpecError as e:
            errors.append(e)

    # value is valid for at least one definition -- return them all
    if valid_definitions:
        return valid_definitions

    # no when spec intersected, so no possible definition for the variant in this configuration
    if strict and not possible_definitions:
        when_clause = f" when {spec}" if spec else ""
        raise InvalidVariantValueError(
            f"variant '{variant.name}' does not exist for '{pkg_cls.name}'{when_clause}"
        )

    # There are only no errors if we're not strict and there are no possible_definitions.
    # We are strict for audits but not for specs on the CLI or elsewhere. Being strict
    # in these cases would violate our rule of being able to *talk* about any configuration,
    # regardless of what the package.py currently says.
    if not errors:
        return []

    # if there is just one error, raise the specific error
    if len(errors) == 1:
        raise errors[0]

    # otherwise combine all the errors and raise them together
    raise InvalidVariantValueError(
        "multiple variant issues:", "\n".join(e.message for e in errors)
    )


class _ConditionalVariantValues(lang.TypedMutableSequence):
    """A list, just with a different type"""


def conditional(*values: List[Any], when: Optional["spack.directives.WhenType"] = None):
    """Conditional values that can be used in variant declarations."""
    # _make_when_spec returns None when the condition is statically false.
    when = spack.directives._make_when_spec(when)
    return _ConditionalVariantValues([Value(x, when=when) for x in values])


class DuplicateVariantError(error.SpecError):
    """Raised when the same variant occurs in a spec twice."""


class UnknownVariantError(error.SpecError):
    """Raised when an unknown variant occurs in a spec."""

    def __init__(self, msg: str, unknown_variants: List[str]):
        super().__init__(msg)
        self.unknown_variants = unknown_variants


class InconsistentValidationError(error.SpecError):
    """Raised if the wrong validator is used to validate a variant."""

    def __init__(self, vspec, variant):
        msg = 'trying to validate variant "{0.name}" ' 'with the validator of "{1.name}"'
        super().__init__(msg.format(vspec, variant))


class MultipleValuesInExclusiveVariantError(error.SpecError, ValueError):
    """Raised when multiple values are present in a variant that wants
    only one.
    """

    def __init__(self, variant: AbstractVariant, pkg_name: Optional[str] = None):
        pkg_info = "" if pkg_name is None else f" in package '{pkg_name}'"
        msg = f"multiple values are not allowed for variant '{variant.name}'{pkg_info}"

        super().__init__(msg.format(variant, pkg_info))


class InvalidVariantValueCombinationError(error.SpecError):
    """Raised when a variant has values '*' or 'none' with other values."""


class InvalidVariantValueError(error.SpecError):
    """Raised when variants have invalid values."""


class UnsatisfiableVariantSpecError(error.UnsatisfiableSpecError):
    """Raised when a spec variant conflicts with package constraints."""

    def __init__(self, provided, required):
        super().__init__(provided, required, "variant")
