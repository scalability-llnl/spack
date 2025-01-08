# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""This module contains jsonschema files for all of Spack's YAML formats."""
import copy
import typing
import warnings

import llnl.util.lang

from spack.error import SpecSyntaxError


class DeprecationMessage(typing.NamedTuple):
    message: str
    error: bool


# jsonschema is imported lazily as it is heavy to import
# and increases the start-up time
def _make_validator():
    import jsonschema

    def _validate_spec(validator, is_spec, instance, schema):
        """Check if the attributes on instance are valid specs."""
        import jsonschema

        import spack.spec_parser

        if not validator.is_type(instance, "object"):
            return

        for spec_str in instance:
            try:
                spack.spec_parser.parse(spec_str)
            except SpecSyntaxError as e:
                yield jsonschema.ValidationError(str(e))

    def _deprecated_properties(validator, deprecated, instance, schema):
        if not (validator.is_type(instance, "object") or validator.is_type(instance, "array")):
            return

        if not deprecated:
            return

        deprecations = {
            name: DeprecationMessage(message=x["message"], error=x["error"])
            for x in deprecated
            for name in x["names"]
        }

        # Get a list of the deprecated properties, return if there is none
        issues = [entry for entry in instance if entry in deprecations]
        if not issues:
            return

        # Process issues
        errors = []
        for name in issues:
            msg = deprecations[name].message.format(name=name)
            if deprecations[name].error:
                errors.append(msg)
            else:
                warnings.warn(msg)

        if errors:
            yield jsonschema.ValidationError("\n".join(errors))

    return jsonschema.validators.extend(
        jsonschema.Draft4Validator,
        {"validate_spec": _validate_spec, "deprecatedProperties": _deprecated_properties},
    )


Validator = llnl.util.lang.Singleton(_make_validator)


def _append(string: str) -> bool:
    """Test if a spack YAML string is an append.

    See ``spack_yaml`` for details.  Keys in Spack YAML can end in `+:`,
    and if they do, their values append lower-precedence
    configs.

    str, str : concatenate strings.
    [obj], [obj] : append lists.

    """
    return getattr(string, "append", False)


def _prepend(string: str) -> bool:
    """Test if a spack YAML string is an prepend.

    See ``spack_yaml`` for details.  Keys in Spack YAML can end in `+:`,
    and if they do, their values prepend lower-precedence
    configs.

    str, str : concatenate strings.
    [obj], [obj] : prepend lists. (default behavior)
    """
    return getattr(string, "prepend", False)


def override(string: str) -> bool:
    """Test if a spack YAML string is an override.

    See ``spack_yaml`` for details.  Keys in Spack YAML can end in `::`,
    and if they do, their values completely replace lower-precedence
    configs instead of merging into them.

    """
    return hasattr(string, "override") and string.override


def merge_yaml(dest, source, prepend=False, append=False):
    """Merges source into dest; entries in source take precedence over dest.

    This routine may modify dest and should be assigned to dest, in
    case dest was None to begin with, e.g.:

       dest = merge_yaml(dest, source)

    In the result, elements from lists from ``source`` will appear before
    elements of lists from ``dest``. Likewise, when iterating over keys
    or items in merged ``OrderedDict`` objects, keys from ``source`` will
    appear before keys from ``dest``.

    Config file authors can optionally end any attribute in a dict
    with `::` instead of `:`, and the key will override that of the
    parent instead of merging.

    `+:` will extend the default prepend merge strategy to include string concatenation
    `-:` will change the merge strategy to append, it also includes string concatentation
    """

    def they_are(t):
        return isinstance(dest, t) and isinstance(source, t)

    # If source is None, overwrite with source.
    if source is None:
        return None

    # Source list is prepended (for precedence)
    if they_are(list):
        if append:
            # Make sure to copy ruamel comments
            dest[:] = [x for x in dest if x not in source] + source
        else:
            # Make sure to copy ruamel comments
            dest[:] = source + [x for x in dest if x not in source]
        return dest

    # Source dict is merged into dest.
    elif they_are(dict):
        # save dest keys to reinsert later -- this ensures that  source items
        # come *before* dest in OrderdDicts
        dest_keys = [dk for dk in dest.keys() if dk not in source]

        for sk, sv in source.items():
            # always remove the dest items. Python dicts do not overwrite
            # keys on insert, so this ensures that source keys are copied
            # into dest along with mark provenance (i.e., file/line info).
            merge = sk in dest
            old_dest_value = dest.pop(sk, None)

            if merge and not override(sk):
                dest[sk] = merge_yaml(old_dest_value, sv, _prepend(sk), _append(sk))
            else:
                # if sk ended with ::, or if it's new, completely override
                dest[sk] = copy.deepcopy(sv)

        # reinsert dest keys so they are last in the result
        for dk in dest_keys:
            dest[dk] = dest.pop(dk)

        return dest

    elif they_are(str):
        # Concatenate strings in prepend mode
        if prepend:
            return source + dest
        elif append:
            return dest + source

    # If we reach here source and dest are either different types or are
    # not both lists or dicts: replace with source.
    return copy.copy(source)
