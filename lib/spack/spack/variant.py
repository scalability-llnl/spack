# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""The variant module contains data structures that are needed to manage
variants both in packages and in specs.
"""

import functools
import inspect
import itertools
import re
from six import StringIO
import sys

if sys.version_info >= (3, 5):
    from collections.abc import Sequence  # novm
else:
    from collections import Sequence

import llnl.util.tty.color
import llnl.util.lang as lang

from spack.util.string import comma_or
import spack.directives
import spack.error as error

special_variant_values = [None, 'none', '*']


class Variant(object):
    """Represents a variant in a package, as declared in the
    variant directive.
    """

    def __init__(
            self,
            name,
            default,
            description,
            values=(True, False),
            multi=False,
            validator=None):
        """Initialize a package variant.

        Args:
            name (str): name of the variant
            default (str): default value for the variant in case
                nothing has been specified
            description (str): purpose of the variant
            values (sequence): sequence of allowed values or a callable
                accepting a single value as argument and returning True if the
                value is good, False otherwise
            multi (bool): whether multiple CSV are allowed
            validator (callable): optional callable used to enforce
                additional logic on the set of values being validated
        """
        self.name = name
        self.default = default
        self.description = str(description)

        self.values = None
        if values == '*':
            # wildcard is a special case to make it easy to say any value is ok
            self.single_value_validator = lambda x: True

        elif isinstance(values, type):
            # supplying a type means any value *of that type*
            def isa_type(v):
                try:
                    values(v)
                    return True
                except ValueError:
                    return False
            self.single_value_validator = isa_type

        if callable(values):
            # If 'values' is a callable, assume it is a single value
            # validator and reset the values to be explicit during debug
            self.single_value_validator = values

        else:
            # Otherwise assume values is the set of allowed explicit values
            self.values = values
            self.single_value_validator = lambda x: x in tuple(self.values)

        self.multi = multi
        self.group_validator = validator

    def validate_or_raise(self, vspec, pkg=None):
        """Validate a variant spec against this package variant. Raises an
        exception if any error is found.

        Args:
            vspec (VariantSpec): instance to be validated
            pkg (Package): the package that required the validation,
                if available

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

        # Check the values of the variant spec
        value = vspec.value
        if isinstance(vspec.value, (bool, str)):
            value = (vspec.value,)

        # If the value is exclusive there must be at most one
        if not self.multi and len(value) != 1:
            raise MultipleValuesInExclusiveVariantError(vspec, pkg)

        # Check and record the values that are not allowed
        not_allowed_values = [
            x for x in value
            if x != '*' and self.single_value_validator(x) is False
        ]
        if not_allowed_values:
            raise InvalidVariantValueError(self, not_allowed_values, pkg)

        # Validate the group of values if needed
        if self.group_validator is not None and value != ('*',):
            self.group_validator(pkg.name, self.name, value)

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
            return ', '.join(v)
        # In case we were given a single-value validator
        # print the docstring
        docstring = inspect.getdoc(self.single_value_validator)
        v = docstring if docstring else ''
        return v

    def make_default(self):
        """Factory that creates a variant holding the default value.

        Returns:
            MultiValuedVariant or SingleValuedVariant or BoolValuedVariant:
                instance of the proper variant
        """
        return self.make_variant(self.default)

    def make_variant(self, value):
        """Factory that creates a variant holding the value passed as
        a parameter.

        Args:
            value: value that will be hold by the variant

        Returns:
            MultiValuedVariant or SingleValuedVariant or BoolValuedVariant:
                instance of the proper variant
        """
        return self.variant_cls(self.name, value)

    @property
    def variant_cls(self):
        """Proper variant class to be used for this configuration."""
        if self.multi:
            return MultiValuedVariant
        elif self.values == (True, False):
            return BoolValuedVariant
        return SingleValuedVariant


def implicit_variant_conversion(method):
    """Converts other to type(self) and calls method(self, other)

    Args:
        method: any predicate method that takes another variant as an argument

    Returns: decorated method
    """
    @functools.wraps(method)
    def convert(self, other):
        # We don't care if types are different as long as I can convert
        # other to type(self)
        try:
            other = type(self)(other.name, other._original_value)
        except (error.SpecError, ValueError):
            return False
        return method(self, other)
    return convert


@lang.lazy_lexicographic_ordering
class AbstractVariant(object):
    """A variant that has not yet decided who it wants to be. It behaves like
    a multi valued variant which **could** do things.

    This kind of variant is generated during parsing of expressions like
    ``foo=bar`` and differs from multi valued variants because it will
    satisfy any other variant with the same name. This is because it **could**
    do it if it grows up to be a multi valued variant with the right set of
    values.
    """

    def __init__(self, name, value):
        self.name = name

        # Stores 'value' after a bit of massaging
        # done by the property setter
        self._value = None
        self._original_value = None

        # Invokes property setter
        self.value = value

    @staticmethod
    def from_node_dict(name, value):
        """Reconstruct a variant from a node dict."""
        if isinstance(value, list):
            # read multi-value variants in and be faithful to the YAML
            mvar = MultiValuedVariant(name, ())
            mvar._value = tuple(value)
            mvar._original_value = mvar._value
            return mvar

        elif str(value).upper() == 'TRUE' or str(value).upper() == 'FALSE':
            return BoolValuedVariant(name, value)

        return SingleValuedVariant(name, value)

    def yaml_entry(self):
        """Returns a key, value tuple suitable to be an entry in a yaml dict.

        Returns:
            tuple: (name, value_representation)
        """
        return self.name, list(self.value)

    @property
    def value(self):
        """Returns a tuple of strings containing the values stored in
        the variant.

        Returns:
            tuple of str: values stored in the variant
        """
        return self._value

    @value.setter
    def value(self, value):
        self._value_setter(value)

    def _value_setter(self, value):
        # Store the original value
        self._original_value = value

        if not isinstance(value, (tuple, list)):
            # Store a tuple of CSV string representations
            # Tuple is necessary here instead of list because the
            # values need to be hashed
            value = re.split(r'\s*,\s*', str(value))

        for val in special_variant_values:
            if val in value and len(value) > 1:
                msg = "'%s' cannot be combined with other variant" % val
                msg += " values."
                raise InvalidVariantValueCombinationError(msg)

        # With multi-value variants it is necessary
        # to remove duplicates and give an order
        # to a set
        self._value = tuple(sorted(set(value)))

    def _cmp_iter(self):
        yield self.name

        value = self._value
        if not isinstance(value, tuple):
            value = (value,)
        value = tuple(str(x) for x in value)
        yield value

    def copy(self):
        """Returns an instance of a variant equivalent to self

        Returns:
            any variant type: a copy of self

        >>> a = MultiValuedVariant('foo', True)
        >>> b = a.copy()
        >>> assert a == b
        >>> assert a is not b
        """
        return type(self)(self.name, self._original_value)

    @implicit_variant_conversion
    def satisfies(self, other):
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

    @implicit_variant_conversion
    def compatible(self, other):
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
        return other.name == self.name

    @implicit_variant_conversion
    def constrain(self, other):
        """Modify self to match all the constraints for other if both
        instances are multi-valued. Returns True if self changed,
        False otherwise.

        Args:
            other: instance against which we constrain self

        Returns:
            bool: True or False
        """
        if self.name != other.name:
            raise ValueError('variants must have the same name')

        old_value = self.value

        values = list(sorted(set(self.value + other.value)))
        # If we constraint wildcard by another value, just take value
        if '*' in values and len(values) > 1:
            values.remove('*')

        self.value = ','.join(values)
        return old_value != self.value

    def __contains__(self, item):
        return item in self._value

    def __repr__(self):
        cls = type(self)
        return '{0.__name__}({1}, {2})'.format(
            cls, repr(self.name), repr(self._original_value)
        )

    def __str__(self):
        return '{0}={1}'.format(
            self.name, ','.join(str(x) for x in self.value)
        )


class MultiValuedVariant(AbstractVariant):
    """A variant that can hold multiple values at once."""
    @implicit_variant_conversion
    def satisfies(self, other):
        """Returns true if ``other.name == self.name`` and ``other.value`` is
        a strict subset of self. Does not try to validate.

        Args:
            other: constraint to be met for the method to return True

        Returns:
            bool: True or False
        """
        super_sat = super(MultiValuedVariant, self).satisfies(other)

        # Otherwise we want all the values in `other` to be also in `self`
        return super_sat and (all(v in self.value for v in other.value) or
                              '*' in other or '*' in self)

    def append(self, value):
        """Add another value to this multi-valued variant."""
        self._value = tuple(sorted((value,) + self._value))
        self._original_value = ",".join(self._value)


class SingleValuedVariant(AbstractVariant):
    """A variant that can hold multiple values, but one at a time."""

    def _value_setter(self, value):
        # Treat the value as a multi-valued variant
        super(SingleValuedVariant, self)._value_setter(value)

        # Then check if there's only a single value
        if len(self._value) != 1:
            raise MultipleValuesInExclusiveVariantError(self, None)
        self._value = str(self._value[0])

    def __str__(self):
        return '{0}={1}'.format(self.name, self.value)

    @implicit_variant_conversion
    def satisfies(self, other):
        abstract_sat = super(SingleValuedVariant, self).satisfies(other)

        return abstract_sat and (self.value == other.value or
                                 other.value == '*' or self.value == '*')

    def compatible(self, other):
        return self.satisfies(other)

    @implicit_variant_conversion
    def constrain(self, other):
        if self.name != other.name:
            raise ValueError('variants must have the same name')

        if other.value == '*':
            return False

        if self.value == '*':
            self.value = other.value
            return True

        if self.value != other.value:
            raise UnsatisfiableVariantSpecError(other.value, self.value)
        return False

    def __contains__(self, item):
        return item == self.value

    def yaml_entry(self):
        return self.name, self.value


class BoolValuedVariant(SingleValuedVariant):
    """A variant that can hold either True or False.

    BoolValuedVariant can also hold the value '*', for coerced
    comparisons between ``foo=*`` and ``+foo`` or ``~foo``."""

    def _value_setter(self, value):
        # Check the string representation of the value and turn
        # it to a boolean
        if str(value).upper() == 'TRUE':
            self._original_value = value
            self._value = True
        elif str(value).upper() == 'FALSE':
            self._original_value = value
            self._value = False
        elif str(value) == '*':
            self._original_value = value
            self._value = '*'
        else:
            msg = 'cannot construct a BoolValuedVariant for "{0}" from '
            msg += 'a value that does not represent a bool'
            raise ValueError(msg.format(self.name))

    def __contains__(self, item):
        return item is self.value

    def __str__(self):
        return '{0}{1}'.format('+' if self.value else '~', self.name)


class VariantMap(lang.HashableMap):
    """Map containing variant instances. New values can be added only
    if the key is not already present.
    """

    def __init__(self, spec):
        super(VariantMap, self).__init__()
        self.spec = spec

    def __setitem__(self, name, vspec):
        # Raise a TypeError if vspec is not of the right type
        if not isinstance(vspec, AbstractVariant):
            msg = 'VariantMap accepts only values of variant types'
            msg += ' [got {0} instead]'.format(type(vspec).__name__)
            raise TypeError(msg)

        # Raise an error if the variant was already in this map
        if name in self.dict:
            msg = 'Cannot specify variant "{0}" twice'.format(name)
            raise DuplicateVariantError(msg)

        # Raise an error if name and vspec.name don't match
        if name != vspec.name:
            msg = 'Inconsistent key "{0}", must be "{1}" to match VariantSpec'
            raise KeyError(msg.format(name, vspec.name))

        # Set the item
        super(VariantMap, self).__setitem__(name, vspec)

    def substitute(self, vspec):
        """Substitutes the entry under ``vspec.name`` with ``vspec``.

        Args:
            vspec: variant spec to be substituted
        """
        if vspec.name not in self:
            msg = 'cannot substitute a key that does not exist [{0}]'
            raise KeyError(msg.format(vspec.name))

        # Set the item
        super(VariantMap, self).__setitem__(vspec.name, vspec)

    def satisfies(self, other, strict=False):
        """Returns True if this VariantMap is more constrained than other,
        False otherwise.

        Args:
            other (VariantMap): VariantMap instance to satisfy
            strict (bool): if True return False if a key is in other and
                not in self, otherwise discard that key and proceed with
                evaluation

        Returns:
            bool: True or False
        """
        to_be_checked = [k for k in other]

        strict_or_concrete = strict
        if self.spec is not None:
            strict_or_concrete |= self.spec._concrete

        if not strict_or_concrete:
            to_be_checked = filter(lambda x: x in self, to_be_checked)

        return all(k in self and self[k].satisfies(other[k])
                   for k in to_be_checked)

    def constrain(self, other):
        """Add all variants in other that aren't in self to self. Also
        constrain all multi-valued variants that are already present.
        Return True if self changed, False otherwise

        Args:
            other (VariantMap): instance against which we constrain self

        Returns:
            bool: True or False
        """
        if other.spec is not None and other.spec._concrete:
            for k in self:
                if k not in other:
                    raise UnsatisfiableVariantSpecError(self[k], '<absent>')

        changed = False
        for k in other:
            if k in self:
                # If they are not compatible raise an error
                if not self[k].compatible(other[k]):
                    raise UnsatisfiableVariantSpecError(self[k], other[k])
                # If they are compatible merge them
                changed |= self[k].constrain(other[k])
            else:
                # If it is not present copy it straight away
                self[k] = other[k].copy()
                changed = True

        return changed

    @property
    def concrete(self):
        """Returns True if the spec is concrete in terms of variants.

        Returns:
            bool: True or False
        """
        return self.spec._concrete or all(
            v in self for v in self.spec.package_class.variants
        )

    def copy(self):
        """Return an instance of VariantMap equivalent to self.

        Returns:
            VariantMap: a copy of self
        """
        clone = VariantMap(self.spec)
        for name, variant in self.items():
            clone[name] = variant.copy()
        return clone

    def __str__(self):
        # print keys in order
        sorted_keys = sorted(self.keys())

        # Separate boolean variants from key-value pairs as they print
        # differently. All booleans go first to avoid ' ~foo' strings that
        # break spec reuse in zsh.
        bool_keys = []
        kv_keys = []
        for key in sorted_keys:
            bool_keys.append(key) if isinstance(self[key].value, bool) \
                else kv_keys.append(key)

        # add spaces before and after key/value variants.
        string = StringIO()

        for key in bool_keys:
            string.write(str(self[key]))

        for key in kv_keys:
            string.write(' ')
            string.write(str(self[key]))

        return string.getvalue()


def substitute_abstract_variants(spec):
    """Uses the information in `spec.package` to turn any variant that needs
    it into a SingleValuedVariant.

    This method is best effort. All variants that can be substituted will be
    substituted before any error is raised.

    Args:
        spec: spec on which to operate the substitution
    """
    # This method needs to be best effort so that it works in matrix exlusion
    # in $spack/lib/spack/spack/spec_list.py
    failed = []
    for name, v in spec.variants.items():
        if name in spack.directives.reserved_names:
            if name == 'dev_path':
                new_variant = SingleValuedVariant(name, v._original_value)
                spec.variants.substitute(new_variant)
            continue
        pkg_variant = spec.package_class.variants.get(name, None)
        if not pkg_variant:
            failed.append(name)
            continue
        new_variant = pkg_variant.make_variant(v._original_value)
        pkg_variant.validate_or_raise(new_variant, spec.package_class)
        spec.variants.substitute(new_variant)

    # Raise all errors at once
    if failed:
        raise UnknownVariantError(spec, failed)


# The class below inherit from Sequence to disguise as a tuple and comply
# with the semantic expected by the 'values' argument of the variant directive
class DisjointSetsOfValues(Sequence):
    """Allows combinations from one of many mutually exclusive sets.

    The value ``('none',)`` is reserved to denote the empty set
    and therefore no other set can contain the item ``'none'``.

    Args:
        *sets (list of tuples): mutually exclusive sets of values
    """

    _empty_set = set(('none',))

    def __init__(self, *sets):
        self.sets = [set(x) for x in sets]

        # 'none' is a special value and can appear only in a set of
        # a single element
        if any('none' in s and s != set(('none',)) for s in self.sets):
            raise error.SpecError("The value 'none' represents the empty set,"
                                  " and must appear alone in a set. Use the "
                                  "method 'allow_empty_set' to add it.")

        # Sets should not intersect with each other
        if any(s1 & s2 for s1, s2 in itertools.combinations(self.sets, 2)):
            raise error.SpecError('sets in input must be disjoint')

        #: Attribute used to track values which correspond to
        #: features which can be enabled or disabled as understood by the
        #: package's build system.
        self.feature_values = tuple(itertools.chain.from_iterable(self.sets))
        self.default = None
        self.multi = True
        self.error_fmt = "this variant accepts combinations of values from " \
                         "exactly one of the following sets '{values}' " \
                         "@*r{{[{package}, variant '{variant}']}}"

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
        self.feature_values = tuple(
            x for x in self.feature_values if x not in values
        )
        return self

    def allow_empty_set(self):
        """Adds the empty set to the current list of disjoint sets."""
        if self._empty_set in self.sets:
            return self

        # Create a new object to be returned
        object_with_empty_set = type(self)(('none',), *self.sets)
        object_with_empty_set.error_fmt = self.error_fmt
        object_with_empty_set.feature_values = self.feature_values + ('none', )
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
            x for x in self.feature_values if x != 'none'
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

            format_args = {
                'variant': variant_name, 'package': pkg_name, 'values': values
            }
            msg = self.error_fmt + \
                " @*r{{[{package}, variant '{variant}']}}"
            msg = llnl.util.tty.color.colorize(msg.format(**format_args))
            raise error.SpecError(msg)
        return _disjoint_set_validator


def _a_single_value_or_a_combination(single_value, *values):
    error = "the value '" + single_value + \
            "' is mutually exclusive with any of the other values"
    return DisjointSetsOfValues(
        (single_value,), values
    ).with_default(single_value).with_error(error).\
        with_non_feature_values(single_value)


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
    return _a_single_value_or_a_combination('none', *values)


def auto_or_any_combination_of(*values):
    """Multi-valued variant that allows any combination of a set of values
    (but not the empty set) or 'auto'.

    Args:
        *values: allowed variant values

    Returns:
        a properly initialized instance of DisjointSetsOfValues
    """
    return _a_single_value_or_a_combination('auto', *values)


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
    return DisjointSetsOfValues(*sets).allow_empty_set().with_default('none')


class DuplicateVariantError(error.SpecError):
    """Raised when the same variant occurs in a spec twice."""


class UnknownVariantError(error.SpecError):
    """Raised when an unknown variant occurs in a spec."""
    def __init__(self, spec, variants):
        self.unknown_variants = variants
        variant_str = 'variant' if len(variants) == 1 else 'variants'
        msg = ('trying to set {0} "{1}" in package "{2}", but the package'
               ' has no such {0} [happened during concretization of {3}]')
        msg = msg.format(variant_str, comma_or(variants), spec.name, spec.root)
        super(UnknownVariantError, self).__init__(msg)


class InconsistentValidationError(error.SpecError):
    """Raised if the wrong validator is used to validate a variant."""
    def __init__(self, vspec, variant):
        msg = ('trying to validate variant "{0.name}" '
               'with the validator of "{1.name}"')
        super(InconsistentValidationError, self).__init__(
            msg.format(vspec, variant)
        )


class MultipleValuesInExclusiveVariantError(error.SpecError, ValueError):
    """Raised when multiple values are present in a variant that wants
    only one.
    """
    def __init__(self, variant, pkg):
        msg = 'multiple values are not allowed for variant "{0.name}"{1}'
        pkg_info = ''
        if pkg is not None:
            pkg_info = ' in package "{0}"'.format(pkg.name)
        super(MultipleValuesInExclusiveVariantError, self).__init__(
            msg.format(variant, pkg_info)
        )


class InvalidVariantValueCombinationError(error.SpecError):
    """Raised when a variant has values '*' or 'none' with other values."""


class InvalidVariantValueError(error.SpecError):
    """Raised when a valid variant has at least an invalid value."""

    def __init__(self, variant, invalid_values, pkg):
        msg = 'invalid values for variant "{0.name}"{2}: {1}\n'
        pkg_info = ''
        if pkg is not None:
            pkg_info = ' in package "{0}"'.format(pkg.name)
        super(InvalidVariantValueError, self).__init__(
            msg.format(variant, invalid_values, pkg_info)
        )


class UnsatisfiableVariantSpecError(error.UnsatisfiableSpecError):
    """Raised when a spec variant conflicts with package constraints."""

    def __init__(self, provided, required):
        super(UnsatisfiableVariantSpecError, self).__init__(
            provided, required, "variant")
